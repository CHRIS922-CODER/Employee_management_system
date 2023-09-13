# Generated by Django 4.2.4 on 2023-09-03 06:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employeeprofile',
            name='department',
        ),
        migrations.RemoveField(
            model_name='employeeprofile',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='AdminProfile',
        ),
        migrations.DeleteModel(
            name='EmployeeProfile',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]