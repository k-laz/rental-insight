# Generated by Django 5.0.2 on 2024-04-16 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0017_remove_listing_parameters_pub_date_listing_pub_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing_parameters',
            name='gender',
        ),
        migrations.AddField(
            model_name='listing_parameters',
            name='gender',
            field=models.ManyToManyField(blank=True, to='newsletter.genderoption'),
        ),
    ]
