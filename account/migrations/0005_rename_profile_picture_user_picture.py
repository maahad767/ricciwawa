# Generated by Django 3.2.7 on 2021-11-25 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20211125_1721'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='profile_picture',
            new_name='picture',
        ),
    ]
