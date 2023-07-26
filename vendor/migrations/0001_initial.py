# Generated by Django 4.2.3 on 2023-07-25 23:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_type', models.CharField(choices=[('vendor', 'Vendor')], default='vendor', max_length=20)),
                ('digi_number', models.CharField(blank=True, max_length=100, null=True)),
                ('company_name', models.CharField(max_length=100)),
                ('alt_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('bank_name', models.CharField(blank=True, max_length=100, null=True)),
                ('account_name', models.CharField(blank=True, max_length=100, null=True)),
                ('account_number', models.CharField(blank=True, max_length=100, null=True)),
                ('country', models.CharField(blank=True, max_length=225, null=True)),
                ('state', models.CharField(blank=True, max_length=225, null=True)),
                ('city', models.CharField(blank=True, max_length=225, null=True)),
                ('vendor_photo', models.ImageField(blank=True, default='placeholder.png', null=True, upload_to='')),
                ('vend_logo', models.ImageField(blank=True, default='placeholder.png', null=True, upload_to='')),
                ('website', models.URLField(blank=True, null=True)),
                ('last_login', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('create_vendor', 'Can create vendor'), ('read_vendor', 'Can read vendor details'), ('update', 'Can update vendor details')),
            },
        ),
    ]