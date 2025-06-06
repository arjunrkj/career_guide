# Generated by Django 5.1.3 on 2025-01-15 06:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_loan'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mentor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=30, null=True)),
                ('qualification', models.CharField(max_length=30, null=True)),
                ('phone', models.CharField(max_length=30, null=True)),
                ('location', models.CharField(max_length=30, null=True)),
                ('clg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.college')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
