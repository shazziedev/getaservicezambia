# Generated by Django 4.0.4 on 2022-04-12 19:06

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('acc', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=900)),
                ('script', models.TextField(blank=True, default=None)),
                ('cert0', models.FileField(blank=True, default=None, upload_to='user/skills/')),
                ('cert1', models.FileField(blank=True, default=None, upload_to='user/skills/')),
                ('cert2', models.FileField(blank=True, default=None, upload_to='user/skills/')),
                ('slug', models.SlugField(default=None)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='country',
            field=django_countries.fields.CountryField(blank=True, max_length=2),
        ),
        migrations.AddField(
            model_name='user',
            name='dob',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='user',
            name='location',
            field=models.CharField(blank=True, max_length=50, verbose_name='location'),
        ),
        migrations.AddField(
            model_name='user',
            name='nrc',
            field=models.CharField(blank=True, max_length=300, verbose_name='national registration number'),
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None),
        ),
        migrations.AddField(
            model_name='user',
            name='skill',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='acc.skill'),
        ),
    ]
