# Generated by Django 2.2.6 on 2020-01-13 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generalApp', '0005_users_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='text',
            field=models.CharField(max_length=1000),
        ),
    ]
