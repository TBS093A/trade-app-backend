# Generated by Django 2.2.6 on 2020-01-15 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generalApp', '0006_auto_20200113_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='password',
            field=models.CharField(max_length=200),
        ),
    ]
