# Generated by Django 4.0.3 on 2022-03-27 18:03

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='country',
            field=django_countries.fields.CountryField(blank=True, max_length=2),
        ),
    ]