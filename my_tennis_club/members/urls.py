from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('members/', views.members, name='members'),
    path('members/details/<int:id>', views.details, name='details'),
    path('create/', views.create_record, name='create_record'),
    path('items/', views.Item, name='items'),
    path('item/details/<int:id>', views.ItemDet, name='itemdetail'),
    path('testing/', views.testing, name='testing'),
]