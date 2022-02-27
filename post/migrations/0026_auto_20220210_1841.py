# Generated by Django 3.2.7 on 2022-02-10 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0025_followhashtag_likehashtag'),
    ]

    operations = [
        migrations.AddField(
            model_name='favouritevocabulary',
            name='meaning',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='favouritevocabulary',
            name='word',
            field=models.CharField(max_length=500),
        ),
    ]