from .models import Member, Item
from .forms import RecordForm, RecordITForm
import requests
from dotenv import dotenv_values
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


env = dotenv_values()

def download_image_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return ContentFile(response.content)
    return None


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
    context = ''

    if request.method == 'POST':
        form = RecordITForm(request.POST, request.FILES)
        print('Method POST executed')

        if form.is_valid():
            print('Form is valid')
            form.save()
            image = request.FILES.get('image_1')

            if image:
                print('Image is present')

                url_main = f"http://my_tennis_club-api-1/desc?tag_category={form.cleaned_data['Category']}&tag_mark={form.cleaned_data['Mark']}&tag_color={form.cleaned_data['Color']}&tag_size={form.cleaned_data['Size']}&tag_fabric={form.cleaned_data['Fabric']}&tag_wear={form.cleaned_data['Wear']}"
                data1 = {'tag_category': form.cleaned_data['Category'], 'tag_mark': form.cleaned_data['Mark'], 'tag_color': form.cleaned_data['Color'], 'tag_size': form.cleaned_data['Size'], 'tag_fabric': form.cleaned_data['Fabric'], 'tag_wear': form.cleaned_data['Wear']}
                files = {'image1': image}

                print('Parameters for FastAPI request:', url_main, data1, files)

                response = requests.post(url_main, headers={"access_token": env['FASTAPI_KEY']}, files=files)

                if response.status_code == 200:
                    print('Response from FastAPI returned successfully')
                    response_data = response.json()
                    description = response_data.get('Description')
                    print(f'Generated description: {description}')
                    context = {
                        'description': description,
                    }
                    template = loader.get_template('createIt.html')
                    return HttpResponse(template.render(context, request))
                else:
                    print('Error:', response.status_code, response.text)
                    return render(request, 'error.html')
            else:
                print("Image is not present!")
        else:
            print('Form is not valid:', form.errors)

    elif request.method == 'GET':
        print('Method GET executed')

        if 'add_tags' in request.GET:
            print('Button that adds tags was clicked')

            sku_value = request.GET.get('sku')

            transport = AIOHTTPTransport(url="https://saleor.gammasoft.pl/graphql/")
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
            print(f'GraphQL Query: {query}')
            variables = {
                "sku": sku_value
            }
            result = client.execute(query, variable_values=variables)

            print(f"Result of GraphQL Query: {result}")
            print('Type of the result:', type(result))

            category = result['productVariant']['product']['category']['name']
            image1 = result['productVariant']['product']['media'][0]['url']
            image2 = result['productVariant']['product']['media'][1]['url']
            brand = result['productVariant']['product']['attributes'][0]['values'][0]['name']
            color = result['productVariant']['product']['attributes'][1]['values'][0]['name']
            size = result['productVariant']['product']['attributes'][2]['values'][0]['name']
            fabric = result['productVariant']['product']['attributes'][3]['values'][0]['name']
            condition = result['productVariant']['product']['attributes'][4]['values'][0]['name']

            print('Assigned variables based on the GraphQL query\'s result:')
            print(image1, image2, brand, color, size, fabric, condition, category)

            form = RecordITForm(initial={'Category': category, 'Mark': brand, 'Color': color, 'Size': size, 'Fabric': fabric, 'Wear': condition})
            context = {'form': form, 'image1': image1, 'image2': image2}
        else:
            print('The method is GET even though the button that adds tags was clicked')
            form = RecordITForm(request.GET)
    else:
        form = RecordITForm()
    if context:
        return render(request, 'createIt.html', context)
    else:
        return render(request, 'createIt.html', {'form': form})
