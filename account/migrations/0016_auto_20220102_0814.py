# Generated by Django 3.2.7 on 2022-01-02 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0023_auto_20220102_0814'),
        ('account', '0015_auto_20211228_2219'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='hashtags',
            field=models.ManyToManyField(blank=True, to='post.HashTag'),
        ),
    ]