# Generated by Django 4.2.2 on 2023-06-29 13:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth1', '0004_examinerprofile_alter_profile_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date_of_birth',
            field=models.DateField(default=datetime.datetime(2023, 6, 29, 14, 56, 14, 354391)),
        ),
    ]
