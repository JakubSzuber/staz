# Generated by Django 4.1.4 on 2023-07-03 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0006_remove_item_photo_item_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='image',
            new_name='image_1',
        ),
        migrations.RemoveField(
            model_name='item',
            name='color',
        ),
        migrations.RemoveField(
            model_name='item',
            name='mark',
        ),
        migrations.RemoveField(
            model_name='item',
            name='sex',
        ),
        migrations.RemoveField(
            model_name='item',
            name='size',
        ),
        migrations.RemoveField(
            model_name='item',
            name='typ',
        ),
        migrations.RemoveField(
            model_name='item',
            name='wear',
        ),
        migrations.AddField(
            model_name='item',
            name='Category',
            field=models.CharField(default='', max_length=128),
        ),
        migrations.AddField(
            model_name='item',
            name='Fabric',
            field=models.CharField(default='', max_length=128),
        ),
        migrations.AddField(
            model_name='item',
            name='image_2',
            field=models.ImageField(null=True, upload_to='item_images/'),
        ),
        migrations.AddField(
            model_name='item',
            name='Color',
            field=models.CharField(default='', max_length=128),
        ),
        migrations.AddField(
            model_name='item',
            name='Mark',
            field=models.CharField(default='', max_length=128),
        ),
        migrations.AddField(
            model_name='item',
            name='Size',
            field=models.CharField(default='', max_length=128),
        ),
        migrations.AddField(
            model_name='item',
            name='Wear',
            field=models.CharField(default='', max_length=128),
        ),
    ]
