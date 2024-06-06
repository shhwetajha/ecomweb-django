# Generated by Django 5.0 on 2024-01-05 10:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_variations'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='variations',
            options={'verbose_name': 'variation', 'verbose_name_plural': 'variations'},
        ),
        migrations.CreateModel(
            name='ProductGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(upload_to='photos/products')),
                ('product', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='store.products')),
            ],
        ),
    ]
