# Generated by Django 4.0.3 on 2022-04-15 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='delivery_instructions',
            field=models.CharField(blank=True, max_length=255, verbose_name='Delivery instructions'),
        ),
    ]