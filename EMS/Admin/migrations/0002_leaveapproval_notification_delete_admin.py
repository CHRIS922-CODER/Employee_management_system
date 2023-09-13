# Generated by Django 4.2.1 on 2023-08-24 12:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Employee', '0002_remove_employee_email_remove_employee_first_name_and_more'),
        ('Admin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeaveApproval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approval_timestamp', models.DateTimeField(auto_now_add=True)),
                ('approving_admin', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('leave_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Employee.leaverequest')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Admin',
        ),
    ]