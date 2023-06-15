from django.db import models

class Member(models.Model):
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)
  phone = models.IntegerField(null=True)
  joined_date = models.DateField(null=True)

class Item(models.Model):
  typ = models.CharField(max_length=128)
  mark = models.CharField(max_length=128)
  size = models.CharField(max_length=8)
  color = models.CharField(max_length=128)
  wear = models.CharField(max_length=128)
  SEX_CHOICES = [
    ('Men', 'Men'),
    ('Woman', 'Woman'),
  ]
  sex = models.CharField(max_length=128, choices=SEX_CHOICES, default='Unknown')