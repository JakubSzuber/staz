from django.http import HttpResponse
from django.template import loader
from .models import Member, Item
from django.shortcuts import render, redirect
from .forms import RecordForm, RecordITForm

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

def create_it_record(request):
    if request.method == 'POST':
        form = RecordITForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = RecordITForm()
    return render(request, 'createIt.html', {'form': form})
