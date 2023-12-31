# Generated by Django 4.2.4 on 2023-09-29 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_order_payment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='address_line1',
            new_name='address_line_1',
        ),
        migrations.RemoveField(
            model_name='order',
            name='address_line2',
        ),
        migrations.AddField(
            model_name='order',
            name='address_line_2',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='ip',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_note',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
