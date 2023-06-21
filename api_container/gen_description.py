import boto3
from PIL import Image
import os
import openai
import requests
from dotenv import dotenv_values
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import List
from fastapi_healthcheck import HealthCheckFactory, healthCheckRoute


# Load the environment variables from the .env file
env = dotenv_values()

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


  # Z dzisiaj -----------------------------------------
  # IMAGEDIR = "images/"
  #
  # app = FastAPI()
  # templates = Jinja2Templates(directory="templates")
  # app.mount("/images", StaticFiles(directory="images"), name="images")
  #
  # @app.get('/', response_class=HTMLResponse)
  # def home(request: Request):
  #   return templates.TemplateResponse("index.html", {"request": request})
  #
  # @app.post("/upload-files")
  # async def create_upload_files(request: Request, files: List[UploadFile] = File(...)):
  #   for file in files:
  #     contents = await file.read()
  #     # save the file
  #     with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
  #       f.write(contents)
  #
  #   show = [file.filename for file in files]
  #
  #   # return {"Result": "OK", "filenames": [file.filename for file in files]}
  #   return templates.TemplateResponse("index.html", {"request": request, "show": show})
  # Z dzisiaj -----------------------------------------


  payload['messages'].append({"role": "user", "content": f'Create rich description of a cloth that is specified by its properties: {str(image_labels)}. You description should be very general but very long. It should be more like a description of the thing that this garment is than a description of that particular garment. Furthermore you shouldn\'t quote given tags! Type in polish language! This is example description for cloth that is based on properties: Clothing, Jeans, Pants, Smoke Pipe: Spodnie dżinsowe - to jedna z najbardziej uniwersalnych i popularnych części garderoby, które z pewnością przypadną do gustu każdemu, kto ceni sobie komfort, styl i trwałość. Jeżeli jesteś miłośnikiem wygody i modnych rozwiązań, spodnie dżinsowe z pewnością będą idealnym wyborem dla Ciebie. \nNie tylko są praktyczne, ale również niezwykle stylowe. Dżinsowe spodnie to nieodzowny element codziennego ubioru, który doskonale wpisuje się w niemal każdą okazję. Bez względu na to, czy wybierasz się na spotkanie ze znajomymi, do pracy, czy po prostu na relaksujący spacer, spodnie dżinsowe będą idealnym towarzyszem Twojego stylu.\nNasze spodnie dżinsowe charakteryzują się wysoką jakością wykonania oraz trwałością materiału. Dzięki temu, będziesz mógł cieszyć się nimi przez wiele sezonów, niezależnie od zmieniających się trendów mody. Warto zainwestować w produkt, który nie tylko wygląda świetnie, ale również zachowuje swoje właściwości nawet po wielu praniach.\nJeżeli jesteś miłośnikiem klasycznego stylu, spodnie dżinsowe będą dla Ciebie idealnym wyborem. Ich uniwersalność pozwoli Ci stworzyć wiele różnorodnych zestawień, dopasowując je do różnych stylizacji i okazji. Możesz połączyć je z elegancką koszulą i marynarką, aby stworzyć elegancki look, lub z luźnym t-shirtem i trampekami, aby uzyskać bardziej casualowy, ale nadal stylowy wygląd.\nTo pozwoli Ci wybrać model, który najlepiej podkreśli Twoją sylwetkę i pasuje do Twojego indywidualnego stylu.\nNie zapomnij również o dodatkach, które mogą podkreślić Twoją osobowość i dodać charakteru Twoim spodniom dżinsowym. To niewielkie elementy, które sprawią, że Twoje spodnie dżinsowe staną się niepowtarzalne.\nDżinsowe spodnie to nie tylko modny wybór, ale również wyraz osobistego stylu i swobody. W naszej kolekcji znajdziesz różnorodność wzorów, kolorów i detali, które pozwolą Ci w pełni wyrazić siebie poprzez swój ubiór. Nie wahaj się, pozwól swojej kreatywności rozbłysnąć i stwórz unikalne zestawienia z naszymi dżinsowymi spodniami.\nOdkryj świat spodni dżinsowych i dołącz do grona osób, które doceniają wygodę, styl i trwałość w jednym produkcie. Nasza kolekcja spodni dżinsowych czeka na Ciebie - wybierz te, które pasują do Ciebie najlepiej i ciesz się niezrównanym komfortem oraz wyjątkowym wyglądem, który przyciągnie spojrzenia innych.\n'})
  response = requests.post(URL, headers=headers, json=payload, stream=False)
  response_json = response.json()
  message_content = response_json['choices'][0]['message']['content']

  output = '\nGenerated Image Description:\n' + message_content

  return output


# print(image_caption_generator('but.jpg'))
# print('-'*70)

# print(image_caption_generator('spodnie.jpg'))
# print('-'*70)
#
# print(image_caption_generator('bluzka.jpg'))
# print('-'*70)

app = FastAPI()

_healthChecks = HealthCheckFactory()

app.add_api_route('/health', endpoint=healthCheckRoute(factory=_healthChecks))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/desc")
def read_root(tag_color: str, tag_size: str, image: UploadFile):
    file_location = f"files/{image.filename}"
    os.makedirs(os.path.dirname(file_location), exist_ok=True)
    with open(file_location, "wb+") as file_object:
        file_object.write(image.file.read())
    #return {"info": f"file '{image.filename}' saved at '{file_location}'", "tag_color": tag_color, "tag_size": tag_size}
    #return {"Description": 'Opis dziala. Opis dziala. Opis dzila.'}
    return {"Description": image_caption_generator(file_location, tag_color, tag_size)}


@app.get("/test-return-image")  # Enpoint for tetsing purposes
def return_image():
    base_directory = os.path.dirname(os.path.abspath(__file__))
    file_location = os.path.join(base_directory, "tmp/tmp.jpg")
    return FileResponse(file_location, media_type="image/jpeg")

