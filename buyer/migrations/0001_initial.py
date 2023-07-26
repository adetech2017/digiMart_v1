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
            name='Buyer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_type', models.CharField(choices=[('buyer', 'Buyer')], default='buyer', max_length=20)),
                ('gender', models.CharField(blank=True, max_length=10, null=True)),
                ('phone_number', models.CharField(max_length=20)),
                ('last_login', models.DateTimeField(blank=True, default='Null', null=True)),
                ('address', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
