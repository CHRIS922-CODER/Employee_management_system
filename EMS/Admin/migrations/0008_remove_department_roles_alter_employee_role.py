# Generated by Django 4.2.4 on 2023-09-06 05:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0007_alter_leaverequest_notes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name='roles',
        ),
        migrations.AlterField(
            model_name='employee',
            name='role',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employee', to='Admin.roles'),
        ),
    ]
