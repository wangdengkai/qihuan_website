# Generated by Django 2.0.7 on 2018-07-18 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qihuan', '0002_auto_20180718_1734'),
    ]

    operations = [
        migrations.AddField(
            model_name='developproject',
            name='pro_cate',
            field=models.CharField(default='web', max_length=20),
        ),
    ]
