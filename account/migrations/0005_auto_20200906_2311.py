# Generated by Django 3.1.1 on 2020-09-06 23:11

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20200906_1315'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='school',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=cloudinary.models.CloudinaryField(default='avatar.png', max_length=255, verbose_name='avatar'),
        ),
    ]
