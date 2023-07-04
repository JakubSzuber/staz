from django.http import HttpResponse
from django.template import loader
from .models import Member, Item
from django.shortcuts import render, redirect
from .forms import RecordForm, RecordITForm
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import requests
from dotenv import dotenv_values
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import json


def main(request):
  template = loader.get_template('main.html')
  return HttpResponse(template.render())


def members(request):
    mymembers = Member.objects.all().values()
    template = loader.get_template('all_members.html')
    context = {
        'mymembers': mymembers,
    }
    return HttpResponse(template.render(context, request))


def details(request, id):
    mymember = Member.objects.get(id=id)
    template = loader.get_template('details.html')
    context = {
        'mymember': mymember,
    }
    return HttpResponse(template.render(context, request))


def testing(request):
  template = loader.get_template('template.html')
  context = {
    'fruits': ['Apple', 'Banana', 'Cherry'],
  }
  return HttpResponse(template.render(context, request))


def create(request):
  template = loader.get_template('create.html')
  return HttpResponse(template.render())


def create_record(request):
    if request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/members')
    else:
        form = RecordForm()
    return render(request, 'create.html', {'form': form})


def ItemL(request):
    myItem = Item.objects.all().values()
    template = loader.get_template('itemlist.html')
    context = {
        'myItems': myItem,
    }
    return HttpResponse(template.render(context, request))


def ItemDet(request, id):
    Myitem = Item.objects.get(id=id)
    template = loader.get_template('itemdetail.html')
    context = {
        'MyItem': Myitem,
    }
    return HttpResponse(template.render(context, request))


def createIt(request):
  template = loader.get_template('createIt.html')
  return HttpResponse(template.render())


@csrf_exempt
def create_it_record(request):
    if request.method == 'POST':
        form = RecordITForm(request.POST)
        print('form jest valid.....')
        if form.is_valid():
            form.save()
            image = request.FILES.get('image')
            if image:
                print('JEST IMAGE')

                url_main = f"http://my_tennis_club-api-1/desc?tag_color={form.cleaned_data['color']}&tag_size={form.cleaned_data['size']}"
                data1 = {'tag_color': form.cleaned_data['color'], 'tag_size': form.cleaned_data['size']}
                files = {'image': image}
                print('argumenty do posta', url_main, data1, files)
                response = requests.post(url_main, headers={"access_token": "9d207bf0-10f5-4d8f-a479-22ff5aeff8d1"}, files=files)
                if response.status_code == 200:
                    # Process the FastAPI response or handle any errors
                    response_data = response.json()
                    description = response_data.get('Description')
                    context = {
                        'description': description,
                    }
                    template = loader.get_template('createIt.html')
                    return HttpResponse(template.render(context, request))
                else:
                    print('Error:', response.status_code, response.text)
                    return render(request, 'error.html')
            else:
                print("NIE MA IMAGE")
    elif request.method == 'GET':
        print('REQUEST Z GET ----------------------------------------------------------')
        if 'add_tags' in request.GET:
            sku_value = request.GET.get('sku')
            # # Assuming value1, value2, and value3 are related to the sku
            # value1 = "example value1 related to " + sku_value
            # value2 = "example value2 related to " + sku_value
            # value3 = "example value3 related to " + sku_value
            # form = RecordITForm(initial={'typ': value1, 'mark': value2, 'size': value3})

            #graphql_token = env['GRAPHQL_TOKEN']

            transport = AIOHTTPTransport(url="https://saleor.gammasoft.pl/graphql/")

            # Create a GraphQL client using the defined transport
            client = Client(transport=transport, fetch_schema_from_transport=True)

            query = gql(
                """
                query ($sku: String) {
                  productVariant(sku: $sku, channel:"fashion4you") {
                    product {
                      category {
                        name
                      }
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
            # result = client.execute(query)
            print("Result nizej: -----------------------------")
            print(result)
            print('Typ resoult:', type(result))

            data = result

            category = data['productVariant']['product']['category']['name']
            image1 = data['productVariant']['product']['media'][0]['url']
            image2 = data['productVariant']['product']['media'][1]['url']
            brand = data['productVariant']['product']['attributes'][0]['values'][0]['name']
            color = data['productVariant']['product']['attributes'][1]['values'][0]['name']
            size = data['productVariant']['product']['attributes'][2]['values'][0]['name']
            fabric = data['productVariant']['product']['attributes'][3]['values'][0]['name']
            condition = data['productVariant']['product']['attributes'][4]['values'][0]['name']
            #quality = data['productVariant']['product']['attributes'][5]['values'][0]['name']
            #defects = data['productVariant']['product']['attributes'][6]['values'][0]['name']

            print('Assigned variables: -------------')
            print(image1, image2, brand, color, size, fabric, condition, category)
            #print(image1, image2, brand, color, size, fabric, condition, quality, defects)

            form = RecordITForm(initial={'typ': 'value111', 'mark': brand, 'size': size, 'color': color, 'wear': "value333", 'sex': "value333"})
        else:
            form = RecordITForm(request.GET)
    else:
        form = RecordITForm()
    return render(request, 'createIt.html', {'form': form})


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
