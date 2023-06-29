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
    else:
        form = RecordITForm()
    return render(request, 'createIt.html', {'form': form})

def sku_num_inp(request):
    return 1