# Generated by Django 4.2.4 on 2023-09-12 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_variation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='variation',
            old_name='creted_date',
            new_name='created_date',
        ),
    ]
