# Generated by Django 3.2.7 on 2021-11-07 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_post_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='subscription_thumbnails/'),
        ),
    ]
