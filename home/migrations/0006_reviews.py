# Generated by Django 3.2.3 on 2023-12-24 18:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_book_sku'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=30)),
                ('review_title', models.CharField(max_length=50)),
                ('review_body', models.CharField(max_length=500)),
                ('review_image', models.ImageField(upload_to='book_more_info/')),
                ('rating', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
            ],
        ),
    ]
