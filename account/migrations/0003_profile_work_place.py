# Generated by Django 3.1 on 2020-08-30 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_relationship'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='work_place',
            field=models.CharField(blank=True, max_length=400),
        ),
    ]
