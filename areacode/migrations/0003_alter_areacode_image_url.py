# Generated by Django 5.1.3 on 2024-12-05 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('areacode', '0002_remove_areacode_region_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='areacode',
            name='image_url',
            field=models.URLField(default='/static/404_error.png', max_length=500),
        ),
    ]
