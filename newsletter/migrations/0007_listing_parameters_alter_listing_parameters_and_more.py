# Generated by Django 5.0.2 on 2024-03-28 05:38

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0006_filter_full_place_alter_filter_gender'),
    ]

    operations = [
        migrations.CreateModel(
            name='Listing_Parameters',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(default=0)),
                ('num_baths', models.IntegerField(default=0)),
                ('num_beds', models.IntegerField(default=0)),
                ('furnished', models.BooleanField(default=False)),
                ('full_place', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name='listing',
            name='parameters',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='newsletter.listing_parameters'),
        ),
        migrations.CreateModel(
            name='User_Filter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_range', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5000)])),
                ('no_price_limit', models.BooleanField(default=False)),
                ('personal_bathroom', models.BooleanField(default=False)),
                ('full_place', models.BooleanField(default=False)),
                ('furnished', models.BooleanField(default=False)),
                ('min_beds', models.IntegerField(default=0)),
                ('min_bathrooms', models.IntegerField(default=0)),
                ('gender', models.IntegerField(choices=[(0, 'male'), (1, 'female'), (2, 'either')], default=2)),
                ('neighbourhoods', models.ManyToManyField(blank=True, to='newsletter.neighbourhood')),
            ],
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='filter',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='newsletter.user_filter'),
        ),
        migrations.DeleteModel(
            name='Filter',
        ),
    ]
