# Generated by Django 2.1.3 on 2018-11-18 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_transactions_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='dateTime',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
