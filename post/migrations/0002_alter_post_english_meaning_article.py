# Generated by Django 3.2.7 on 2021-10-31 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='english_meaning_article',
            field=models.TextField(blank=True, null=True),
        ),
    ]
