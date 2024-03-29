# Generated by Django 5.0.2 on 2024-03-02 01:54

import datetime
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
            name='Filter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_price', models.IntegerField(default=0)),
                ('own_bathroom', models.BooleanField(default=False)),
                ('min_beds', models.IntegerField(default=0)),
                ('min_bathrooms', models.IntegerField(default=0)),
                ('move_in_date', models.DateField(default=datetime.date.today)),
                ('length_of_stay', models.IntegerField(choices=[(4, '4 months'), (8, '8 months'), (12, '12 months')], default=4)),
                ('gender', models.IntegerField(choices=[(0, 'male'), (1, 'female')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('link', models.CharField(max_length=200, null=True)),
                ('own_bathroom', models.BooleanField(default=False)),
                ('beds', models.IntegerField(default=0)),
                ('bathrooms', models.IntegerField(default=0)),
                ('location', models.CharField(default='UBC campus', max_length=100)),
                ('price', models.IntegerField(default=0)),
                ('potential_spam', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filter', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='newsletter.filter')),
                ('listings', models.ManyToManyField(to='newsletter.listing')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
