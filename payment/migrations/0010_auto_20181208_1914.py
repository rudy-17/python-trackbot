# Generated by Django 2.1.3 on 2018-12-08 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0009_auto_20181208_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='duration',
            field=models.IntegerField(),
        ),
    ]
