# Generated by Django 4.2.3 on 2023-08-19 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0004_vendor_vendor_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='digi_number',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
