from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('members/', views.members, name='members'),
    path('members/details/<int:id>', views.details, name='details'),
    path('create/', views.create_record, name='create_record'),
    path('items/', views.ItemL, name='items'),
    path('items/detailed/<int:id>', views.ItemDet, name='itemdetail'),
    path('items/create-item/', views.create_it_record, name='create_it_record'),
    path('items/sku_num/', views.create_it_record, name='sku_num_inp'),
    path('testing/', views.testing, name='testing'),
]