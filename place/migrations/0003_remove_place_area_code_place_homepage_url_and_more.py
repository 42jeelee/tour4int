# Generated by Django 5.1.3 on 2024-12-05 05:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('areacode', '0003_alter_areacode_image_url'),
        ('place', '0002_alter_place_area_code_alter_place_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='place',
            name='area_code',
        ),
        migrations.AddField(
            model_name='place',
            name='homepage_url',
            field=models.URLField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='place',
            name='is_detail',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='place',
            name='overview',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='place',
            name='sigungu_code',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='areacode.sigungucode'),
        ),
    ]
