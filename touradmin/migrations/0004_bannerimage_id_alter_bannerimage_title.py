# Generated by Django 5.1.3 on 2025-01-10 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('touradmin', '0003_remove_bannerimage_id_alter_bannerimage_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='bannerimage',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bannerimage',
            name='title',
            field=models.CharField(help_text='배너 제목', max_length=100),
        ),
    ]