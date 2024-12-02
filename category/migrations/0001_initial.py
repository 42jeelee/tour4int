# Generated by Django 5.1.3 on 2024-12-02 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('content_type', models.IntegerField()),
                ('name', models.CharField(max_length=20)),
            ],
        ),
    ]
