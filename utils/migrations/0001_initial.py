# Generated by Django 3.2.7 on 2022-01-02 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dictionary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trad', models.CharField(max_length=100)),
                ('pinyin', models.CharField(max_length=100)),
                ('sim', models.CharField(max_length=100)),
                ('eng', models.CharField(max_length=100)),
                ('ko', models.CharField(max_length=100)),
                ('ind', models.CharField(max_length=100)),
                ('es', models.CharField(max_length=100)),
                ('ur', models.CharField(max_length=100)),
                ('tl', models.CharField(max_length=100)),
                ('de', models.CharField(max_length=100)),
                ('hu', models.CharField(max_length=100)),
                ('vi', models.CharField(max_length=100)),
            ],
        ),
    ]
