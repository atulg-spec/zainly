# Generated by Django 5.0.3 on 2024-08-25 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0031_alter_categories_short_caption'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='short_caption',
            field=models.CharField(default='', max_length=12),
        ),
    ]
