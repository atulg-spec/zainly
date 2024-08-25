# Generated by Django 5.0.3 on 2024-08-23 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0025_order_expected_delivery_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=15)),
                ('query', models.TextField()),
                ('date_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Contact Us Request',
                'verbose_name_plural': 'Contact Requests',
            },
        ),
    ]
