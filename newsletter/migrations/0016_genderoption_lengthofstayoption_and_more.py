# Generated by Django 5.0.2 on 2024-04-04 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0015_alter_user_filter_full_place_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenderOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='LengthOfStayOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.IntegerField(unique=True)),
                ('label', models.CharField(max_length=10)),
            ],
        ),
        migrations.RemoveField(
            model_name='user_filter',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='user_filter',
            name='length_of_stay',
        ),
        migrations.AddField(
            model_name='user_filter',
            name='gender',
            field=models.ManyToManyField(blank=True, to='newsletter.genderoption'),
        ),
        migrations.AddField(
            model_name='user_filter',
            name='length_of_stay',
            field=models.ManyToManyField(blank=True, to='newsletter.lengthofstayoption'),
        ),
    ]
