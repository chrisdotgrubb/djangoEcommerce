# Generated by Django 4.0.3 on 2022-05-09 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_remove_order_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_instructions',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='order',
            name='address1',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='order',
            name='address2',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]