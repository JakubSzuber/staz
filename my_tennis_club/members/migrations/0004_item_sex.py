# Generated by Django 4.1.4 on 2023-06-15 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0003_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='sex',
            field=models.CharField(choices=[('Men', 'Men'), ('Woman', 'Woman')], default='Unknown', max_length=128),
        ),
    ]
