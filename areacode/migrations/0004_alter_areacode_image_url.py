# Generated by Django 5.1.3 on 2024-12-05 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('areacode', '0003_alter_areacode_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='areacode',
            name='image_url',
            field=models.CharField(default='/static/404_error.png', max_length=255),
        ),
    ]