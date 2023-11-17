# Generated by Django 4.2.5 on 2023-10-14 06:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('applicant_status', models.CharField(max_length=10)),
                ('date_added', models.DateField(default=django.utils.timezone.now)),
                ('source', models.CharField(max_length=200)),
                ('presentEmployment', models.JSONField(null=True)),
                ('academicRec', models.JSONField(null=True)),
                ('employementRec', models.JSONField(null=True)),
                ('teachingSupervision', models.JSONField(null=True)),
                ('languages', models.JSONField(null=True)),
                ('family', models.JSONField(null=True)),
                ('referees', models.JSONField(null=True)),
                ('documents', models.JSONField(null=True)),
            ],
        ),
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
                ('salaryMin', models.IntegerField()),
                ('salaryMax', models.IntegerField()),
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