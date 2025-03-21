# Generated by Django 5.1.2 on 2025-01-04 19:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('isbn_no', models.CharField(max_length=13, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=255)),
                ('quantity', models.PositiveIntegerField()),
                ('category', models.CharField(max_length=100)),
                ('image', models.URLField(blank=True, max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Borrowing',
            fields=[
                ('id', models.CharField(primary_key=True, serialize=False, unique=True)),
                ('isbn_no', models.CharField(max_length=13)),
                ('date', models.DateField(auto_now_add=True)),
                ('state', models.CharField(choices=[('approved', 'Approved'), ('unapproved', 'Not Approved')], default='unapproved', max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Returning',
            fields=[
                ('id', models.CharField(primary_key=True, serialize=False, unique=True)),
                ('isbn_no', models.CharField(max_length=13)),
                ('borrow_date', models.DateField()),
                ('return_date', models.DateField()),
                ('state', models.CharField(choices=[('approved', 'Approved'), ('unapproved', 'Not Approved')], default='unapproved', max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
