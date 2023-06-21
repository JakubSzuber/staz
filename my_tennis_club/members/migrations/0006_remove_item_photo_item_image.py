# Generated by Django 4.1.4 on 2023-06-19 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0005_item_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='photo',
        ),
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.ImageField(null=True, upload_to='item_images/'),
        ),
    ]
