# Generated by Django 4.2.5 on 2023-10-16 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod', '0008_application_membershipfellowship'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='membershipFellowship',
            field=models.TextField(default='', null=True),
        ),
    ]
