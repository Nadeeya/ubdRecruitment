# Generated by Django 4.2.5 on 2023-10-19 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod', '0009_alter_application_membershipfellowship'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='fullname',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='application',
            name='postApplied',
            field=models.CharField(default='', max_length=20),
        ),
    ]
