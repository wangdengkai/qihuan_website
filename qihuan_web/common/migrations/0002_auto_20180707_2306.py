# Generated by Django 2.0.7 on 2018-07-07 23:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='common',
            options={'ordering': ['-create_time'], 'verbose_name': '评论详情表'},
        ),
    ]
