# Generated by Django 3.2.7 on 2021-09-18 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_item_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='slug',
            field=models.SlugField(default='Test product'),
            preserve_default=False,
        ),
    ]
