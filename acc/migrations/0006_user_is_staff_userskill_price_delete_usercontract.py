# Generated by Django 4.0.6 on 2022-07-26 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acc', '0005_usercontract_remove_userrating_rating_once_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False, verbose_name='staff'),
        ),
        migrations.AddField(
            model_name='userskill',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8),
        ),
        migrations.DeleteModel(
            name='UserContract',
        ),
    ]