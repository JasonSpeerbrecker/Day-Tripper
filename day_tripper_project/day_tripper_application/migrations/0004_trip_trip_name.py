# Generated by Django 2.2.4 on 2021-03-30 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('day_tripper_application', '0003_trail_trip'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='trip_name',
            field=models.CharField(default='name', max_length=255),
            preserve_default=False,
        ),
    ]
