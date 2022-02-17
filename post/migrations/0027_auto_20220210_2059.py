# Generated by Django 3.2.7 on 2022-02-10 14:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0026_auto_20220210_1841'),
    ]

    operations = [
        migrations.AddField(
            model_name='favouritevocabulary',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='vocabulary/'),
        ),
        migrations.AddField(
            model_name='favouritevocabulary',
            name='pinyin',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='favouritevocabulary',
            name='post',
            field=models.ForeignKey(default=1537, on_delete=django.db.models.deletion.CASCADE, to='post.post'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='favouritevocabulary',
            name='meaning',
            field=models.CharField(max_length=2000),
        ),
    ]
