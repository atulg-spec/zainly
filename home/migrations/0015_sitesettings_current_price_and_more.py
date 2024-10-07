# Generated by Django 4.2.7 on 2024-10-07 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_productbycategory_alter_sitesettings_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='current_price',
            field=models.PositiveIntegerField(default=369),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='discount_percentage',
            field=models.PositiveIntegerField(default=40),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='last_price',
            field=models.PositiveIntegerField(default=799),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='main_page_timer',
            field=models.CharField(default='2025/05/01', max_length=30),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='main_page_timer_caption',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='main_page_timer_thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='slider_images/'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='main_page_timer_url',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]
