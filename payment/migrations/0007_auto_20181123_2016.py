# Generated by Django 2.1.3 on 2018-11-23 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0006_auto_20181118_2214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='dateTime',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
