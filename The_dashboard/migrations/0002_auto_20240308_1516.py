# Generated by Django 3.2.24 on 2024-03-08 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('The_dashboard', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='profile',
        ),
        migrations.AddField(
            model_name='message',
            name='profile',
            field=models.IntegerField(default=1),
        ),
    ]
