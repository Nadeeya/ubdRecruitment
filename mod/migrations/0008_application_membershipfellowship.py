# Generated by Django 4.2.5 on 2023-10-16 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod', '0007_application_documents'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='membershipFellowship',
            field=models.TextField(default=''),
        ),
    ]
