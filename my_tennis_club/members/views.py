from django.http import HttpResponse
from django.template import loader
from .models import Member, Item
from django.shortcuts import render, redirect
from .forms import RecordForm, RecordITForm
from django.shortcuts import render
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import os
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import requests


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

import requests

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
                url = f"http://my_tennis_club-api-1/desc?tag_color={form.cleaned_data['color']}&tag_size={form.cleaned_data['size']}"
                data1 = {'tag_color': form.cleaned_data['color'], 'tag_size': form.cleaned_data['size']}
                files = {'image': image}
                print('argumenty do posta', url, data1, files)
                response = requests.post(url, files=files)
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
    else:
        form = RecordITForm()
    return render(request, 'createIt.html', {'form': form})



# @csrf_exempt
# def create_it_record(request):
#     if request.method == 'POST':
#         print('Metoda to post')
#         form = RecordITForm(request.POST)
#         if form.is_valid():
#             form.save()
#             tag_color = form.cleaned_data['color']
#             tag_size = form.cleaned_data['size']
#             image = request.FILES.get('image')
#
#             # Save the image locally
#             file_location = f"files/{image.name}"
#             os.makedirs(os.path.dirname(file_location), exist_ok=True)
#             with open(file_location, "wb+") as file_object:
#                 for chunk in image.chunks():
#                     file_object.write(chunk)
#
#             # Send the image and parameters to FastAPI
#             api_url = 'http://my_tennis_club-api-1/desc'
#             response = requests.post(
#                 f"{api_url}",
#                 data={
#                     'tag_color': tag_color,
#                     'tag_size': tag_size
#                 },
#                 files={
#                     'image': open(file_location, 'rb')
#                 }
#             )
#
#             print(JsonResponse(response.json()))
#             print(response)
#             print(response.text)
#
#             # Check the response from FastAPI
#             if response.status_code == 200:
#                 print('CHyba powinno byc ok!!!')
#                 data = response.json()
#                 print(JsonResponse(data))
#                 return JsonResponse(data)
#             else:
#                 return JsonResponse({'error': 'An error occurred'}, status=500)
#     else:
#         form = RecordITForm()
#     return render(request, 'createIt.html', {'form': form})
