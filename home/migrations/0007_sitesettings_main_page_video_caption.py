# Generated by Django 5.0.3 on 2024-08-24 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_sitesettings_main_page_video_thumbnail_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='main_page_video_caption',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
