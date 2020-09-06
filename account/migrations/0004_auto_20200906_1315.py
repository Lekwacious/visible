# Generated by Django 3.1.1 on 2020-09-06 13:15

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_profile_work_place'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=cloudinary.models.CloudinaryField(default='avatar.png', max_length=255, verbose_name='avatar/'),
        ),
    ]
