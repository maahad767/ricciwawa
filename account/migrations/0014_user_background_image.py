# Generated by Django 3.2.7 on 2021-12-27 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_alter_blockuser_by_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='background_image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_background_pictures'),
        ),
    ]
