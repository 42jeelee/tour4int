# Generated by Django 5.1.3 on 2024-12-05 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('place', '0003_remove_place_area_code_place_homepage_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='homepage_url',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
