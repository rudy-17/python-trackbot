# Generated by Django 2.1.3 on 2018-11-11 07:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('amazon_seller', '0003_auto_20181109_0642'),
        ('orders', '0002_orders_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='user',
        ),
        migrations.AddField(
            model_name='orders',
            name='user_seller',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='amazon_seller.SellerAccount'),
            preserve_default=False,
        ),
    ]
