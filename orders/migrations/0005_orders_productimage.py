# Generated by Django 2.1.3 on 2018-11-18 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_orders_trackingid'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='productImage',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
