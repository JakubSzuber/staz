from django.db import models

class Member(models.Model):
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)
  phone = models.IntegerField(null=True)
  joined_date = models.DateField(null=True)

class Item(models.Model):
  Category = models.CharField(max_length=128, default='')
  Mark = models.CharField(max_length=128, default='')
  Color = models.CharField(max_length=128, default='')
  Size = models.CharField(max_length=128, default='')
  Fabric = models.CharField(max_length=128, default='')
  Wear = models.CharField(max_length=128, default='')
