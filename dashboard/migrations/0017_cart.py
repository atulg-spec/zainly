# Generated by Django 5.0.3 on 2024-07-30 06:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0016_alter_product_discount_percent'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to='dashboard.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Cart Items',
                'verbose_name_plural': 'Cart',
            },
        ),
    ]
