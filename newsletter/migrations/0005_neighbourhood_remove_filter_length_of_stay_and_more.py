# Generated by Django 5.0.2 on 2024-03-10 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0004_alter_listing_parameters'),
    ]

    operations = [
        migrations.CreateModel(
            name='Neighbourhood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='filter',
            name='length_of_stay',
        ),
        migrations.RemoveField(
            model_name='filter',
            name='move_in_date',
        ),
        migrations.AddField(
            model_name='filter',
            name='furnished',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='listings',
            field=models.ManyToManyField(blank=True, to='newsletter.listing'),
        ),
        migrations.AddField(
            model_name='filter',
            name='neighbourhoods',
            field=models.ManyToManyField(blank=True, to='newsletter.neighbourhood'),
        ),
    ]