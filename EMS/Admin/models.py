from django.db import models
# Import Django's built-in User model for Admin
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _


class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.name} "


class Roles(models.Model):
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name='department')
    roles_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.roles_name} "


class Tasks(models.Model):
    task_name = models.CharField(max_length=100)
    task_description = models.TextField()
    progress = models.IntegerField()

    def __str__(self):
        return f"{self.task_name} {self.progress} "


# start of the employee records

class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True,default='default.jpg')  
    contact = models.CharField(max_length=200, null=True)
    department = models.ForeignKey(
        'Department', on_delete=models.CASCADE, related_name='employee')
    task = models.ForeignKey(
        'Tasks', on_delete=models.CASCADE, related_name='employee', null=True)
    role = models.ForeignKey(
        'Roles', on_delete=models.CASCADE, related_name='employee', null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True)


class TimeRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    record_date = models.DateField(null=True)
    clock_in = models.TimeField(null=True, blank=True)
    clock_out = models.TimeField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    # Indicates whether it's a clock-in record
    is_clock_in = models.BooleanField(default=False)
    is_clock_out = models.BooleanField(default=False)
    approved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='approved_time_records'
    )


    def __str__(self):
        return f"{self.user} - {self.record_date} - {'Clock In' if self.is_clock_in else 'Clock Out'}"


class PaymentRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.payment_date}"


class LeaveRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
    ]
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.FileField(upload_to='leave_request_files')
    approving_admin = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='leave_approvals')

    def __str__(self):
        return f"{self.user.first_name} - {self.start_date} to {self.end_date}"


class LeaveApproval(models.Model):  # New model to handle leave approvals
    leave_request = models.ForeignKey(LeaveRequest, on_delete=models.CASCADE)
    approving_admin = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)
    approval_timestamp = models.DateTimeField(auto_now_add=True)
