# Generated by Django 4.2.3 on 2024-09-27 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile/'),
        ),
    ]
