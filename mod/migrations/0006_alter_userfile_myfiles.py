# Generated by Django 4.2.5 on 2023-10-15 03:15

from django.db import migrations, models
import mod.models


class Migration(migrations.Migration):

    dependencies = [
        ('mod', '0005_alter_userfile_applicant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfile',
            name='myfiles',
            field=models.FileField(default='', max_length=500, upload_to=mod.models.user_directory_path),
        ),
    ]
