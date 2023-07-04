import boto3
from PIL import Image
import os
import openai
import requests
from dotenv import dotenv_values
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, UploadFile, File, Form, Depends, HTTPException, status, Security
from fastapi_healthcheck import HealthCheckFactory, healthCheckRoute
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from starlette.status import HTTP_403_FORBIDDEN


# Load the environment variables from the .env file
env = dotenv_values()

API_KEYS = [
    "9d207bf0-10f5-4d8f-a479-22ff5aeff8d1",
    "f47d4a2c-24cf-4745-937e-620a5963c0b8",
    "b7061546-75e8-444b-a2c4-f19655d07eb8",
]

API_KEY_NAME = "access_token"
COOKIE_DOMAIN = "localtest.me"

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)  # Could be also "x-api-key"
api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)

openai.api_key = env['OPENAI_API']
client = boto3.client('rekognition', region_name='eu-central-1')
URL = "https://api.openai.com/v1/chat/completions"


payload = {
  "model": "gpt-3.5-turbo",
  "messages": [],
  "temperature": 1.0,
  "top_p": 1.0,
  "n": 1,
  "stream": False,
  "presence_penalty": 0,
  "frequency_penalty": 0,
}

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {openai.api_key}"
}

def image_caption_generator(image_path, tag_color, tag_size):
  # create a tmp folder in order to save the resized input image
  if not os.path.exists('tmp'):
    os.makedirs('tmp')

  # Open the original image
  img = Image.open(image_path)

  if img.mode in ('RGBA', 'P'):
      img = img.convert('RGB')

  img.save(image_path, 'JPEG')

  # Set the desired size for the resized image
  new_size = (100, 100)

  # Resize the image
  resized_img = img.resize(new_size)

  # Save the resized image
  resized_img.save('tmp/tmp.jpg')

  with open('tmp/tmp.jpg', 'rb') as image:
    response = client.detect_labels(Image={'Bytes': image.read()})

  image_labels = [tag_color, tag_size]

  print('Image tags:')
  for label in response['Labels']:
    if label['Confidence'] > 97:
      image_labels.append(label['Name'].lower())
      print(f"{label['Name']} with confidance {label['Confidence']}")

  payload['messages'].append({"role": "user", "content": f'Create rich description of a cloth that is specified by its properties: {str(image_labels)}. You description should be very general but very long. It should be more like a description of the thing that this garment is than a description of that particular garment. Furthermore you shouldn\'t quote given tags! Type in polish language! This is example description for cloth that is based on properties: Clothing, Jeans, Pants, Smoke Pipe: Spodnie dżinsowe - to jedna z najbardziej uniwersalnych i popularnych części garderoby, które z pewnością przypadną do gustu każdemu, kto ceni sobie komfort, styl i trwałość. Jeżeli jesteś miłośnikiem wygody i modnych rozwiązań, spodnie dżinsowe z pewnością będą idealnym wyborem dla Ciebie. \nNie tylko są praktyczne, ale również niezwykle stylowe. Dżinsowe spodnie to nieodzowny element codziennego ubioru, który doskonale wpisuje się w niemal każdą okazję. Bez względu na to, czy wybierasz się na spotkanie ze znajomymi, do pracy, czy po prostu na relaksujący spacer, spodnie dżinsowe będą idealnym towarzyszem Twojego stylu.\nNasze spodnie dżinsowe charakteryzują się wysoką jakością wykonania oraz trwałością materiału. Dzięki temu, będziesz mógł cieszyć się nimi przez wiele sezonów, niezależnie od zmieniających się trendów mody. Warto zainwestować w produkt, który nie tylko wygląda świetnie, ale również zachowuje swoje właściwości nawet po wielu praniach.\nJeżeli jesteś miłośnikiem klasycznego stylu, spodnie dżinsowe będą dla Ciebie idealnym wyborem. Ich uniwersalność pozwoli Ci stworzyć wiele różnorodnych zestawień, dopasowując je do różnych stylizacji i okazji. Możesz połączyć je z elegancką koszulą i marynarką, aby stworzyć elegancki look, lub z luźnym t-shirtem i trampekami, aby uzyskać bardziej casualowy, ale nadal stylowy wygląd.\nTo pozwoli Ci wybrać model, który najlepiej podkreśli Twoją sylwetkę i pasuje do Twojego indywidualnego stylu.\nNie zapomnij również o dodatkach, które mogą podkreślić Twoją osobowość i dodać charakteru Twoim spodniom dżinsowym. To niewielkie elementy, które sprawią, że Twoje spodnie dżinsowe staną się niepowtarzalne.\nDżinsowe spodnie to nie tylko modny wybór, ale również wyraz osobistego stylu i swobody. W naszej kolekcji znajdziesz różnorodność wzorów, kolorów i detali, które pozwolą Ci w pełni wyrazić siebie poprzez swój ubiór. Nie wahaj się, pozwól swojej kreatywności rozbłysnąć i stwórz unikalne zestawienia z naszymi dżinsowymi spodniami.\nOdkryj świat spodni dżinsowych i dołącz do grona osób, które doceniają wygodę, styl i trwałość w jednym produkcie. Nasza kolekcja spodni dżinsowych czeka na Ciebie - wybierz te, które pasują do Ciebie najlepiej i ciesz się niezrównanym komfortem oraz wyjątkowym wyglądem, który przyciągnie spojrzenia innych.\n'})
  response = requests.post(URL, headers=headers, json=payload, stream=False)
  response_json = response.json()
  message_content = response_json['choices'][0]['message']['content']

  output = '\nGenerated Image Description:\n' + message_content

  return output


async def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
    api_key_cookie: str = Security(api_key_cookie),
):

    if api_key_query in API_KEYS:
        return api_key_query
    elif api_key_header in API_KEYS:
        return api_key_header
    elif api_key_cookie in API_KEYS:
        return api_key_cookie
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="API key is not valid or expired!"
        )


app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

_healthChecks = HealthCheckFactory()

app.add_api_route('/health', endpoint=healthCheckRoute(factory=_healthChecks))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

def gen_tags(sku_value):
    graphql_token = env['GRAPHQL_TOKEN']

    transport = AIOHTTPTransport(url="https://saleor.gammasoft.pl/graphql/")

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # TODO Provide a GraphQL query (not final)
    query = gql(
        """
        query ($sku: String) {
          productVariant(sku: $sku, channel:"fashion4you") {
            product {
              media {
                url
              }
              attributes {
                attribute {
                  name
                }
                values {
                  name
                }
              }
            }
          }
        }
    """)
    print(query)
    variables = {
        "sku": sku_value
    }
    result = client.execute(query, variable_values=variables)
    #result = client.execute(query)
    print(result)
    return(result)


# TODO below code to parse result:
# import json
#
# OF COURSE IT'S ONLY EXAMPLE WITH JSON AS STRING
# json_string = """
# {
#     "productVariant": {
#         "product": {
#             "media": [
#                 {
#                     "url": "https://example.com/products/photo_1132466587739927487_0bbfa6be.jpg"
#                 },
#                 {
#                     "url": "https://example.com/products/photo_170064535416482196_f1f96473.jpg"
#                 }
#             ],
#             "attributes": [
#                 {
#                     "attribute": {
#                         "name": "Marka odzież męska"
#                     },
#                     "values": [
#                         {
#                             "name": "inna"
#                         }
#                     ]
#                 },
#                 {
#                     "attribute": {
#                         "name": "Kolor"
#                     },
#                     "values": [
#                         {
#                             "name": "granatowy"
#                         }
#                     ]
#                 },
#                 {
#                     "attribute": {
#                         "name": "Rozmiar"
#                     },
#                     "values": [
#                         {
#                             "name": "XL"
#                         }
#                     ]
#                 },
#                 {
#                     "attribute": {
#                         "name": "Materiał"
#                     },
#                     "values": [
#                         {
#                             "name": "bawełna"
#                         }
#                     ]
#                 },
#                 {
#                     "attribute": {
#                         "name": "Stan"
#                     },
#                     "values": [
#                         {
#                             "name": "Używany z defektem"
#                         }
#                     ]
#                 },
#                 {
#                     "attribute": {
#                         "name": "Jakość"
#                     },
#                     "values": [
#                         {
#                             "name": "Shop Mix"
#                         }
#                     ]
#                 },
#                 {
#                     "attribute": {
#                         "name": "Wady"
#                     },
#                     "values": [
#                         {
#                             "name": "zmechacenie"
#                         }
#                     ]
#                 }
#             ]
#         }
#     }
# }
# """
#
# data = json.loads(json_string)
#
# image1 = data['productVariant']['product']['media'][0]['url']
# image2 = data['productVariant']['product']['media'][1]['url']
# brand = data['productVariant']['product']['attributes'][0]['values'][0]['name']
# color = data['productVariant']['product']['attributes'][1]['values'][0]['name']
# size = data['productVariant']['product']['attributes'][2]['values'][0]['name']
# fabric = data['productVariant']['product']['attributes'][3]['values'][0]['name']
# condition = data['productVariant']['product']['attributes'][4]['values'][0]['name']
# quality = data['productVariant']['product']['attributes'][5]['values'][0]['name']
# defects = data['productVariant']['product']['attributes'][6]['values'][0]['name']
#
#
# print(image1, image2, brand, color, size, fabric, condition, quality, defects)



# ---------------------------------------------- Endpoint ----------------------------------------------
@app.post("/desc")
def read_root(
    tag_color: str,
    tag_size: str,
    image: UploadFile,
    api_key: str = Security(get_api_key)
):
    file_location = f"files/{image.filename}"
    os.makedirs(os.path.dirname(file_location), exist_ok=True)
    with open(file_location, "wb+") as file_object:
        file_object.write(image.file.read())
    return {"Description": image_caption_generator(file_location, tag_color, tag_size)}

@app.get("/sku-tags")
def return_tags(sku_number: str, api_key: str = Security(get_api_key)):
    tags_json = gen_tags(sku_number)
    return tags_json

@app.get("/test-return-image")  # Not secure enpoint for tetsing purposes
def return_image():
    base_directory = os.path.dirname(os.path.abspath(__file__))
    file_location = os.path.join(base_directory, "tmp/tmp.jpg")
    return FileResponse(file_location, media_type="image/jpeg")
