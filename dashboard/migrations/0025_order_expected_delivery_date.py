# Generated by Django 5.0.3 on 2024-07-31 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0024_slider_redirect_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='expected_delivery_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
