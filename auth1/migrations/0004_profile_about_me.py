# Generated by Django 4.1.7 on 2023-05-14 08:18

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth1', '0003_profile_profile_pics'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='about_me',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]