# Generated by Django 5.1.2 on 2024-12-26 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_alter_shopaddress_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopaddress',
            name='hours',
            field=models.CharField(max_length=11),
        ),
    ]