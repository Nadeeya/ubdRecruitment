# Generated by Django 4.2.5 on 2023-10-14 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('department', models.CharField(max_length=200)),
                ('category', models.CharField(max_length=200)),
                ('type', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=200)),
                ('uploadDate', models.DateField(auto_now_add=True)),
                ('salary', models.IntegerField()),
                ('minReq', models.CharField(max_length=200)),
                ('yearsExp', models.IntegerField()),
                ('description', models.TextField()),
                ('contractDur', models.IntegerField()),
                ('dateClose', models.DateField()),
                ('jobForm', models.CharField(max_length=200)),
                ('btnMsg', models.CharField(max_length=200)),
            ],
        ),
    ]
