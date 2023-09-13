from django.db import models
# Import Django's built-in User model for Admin
from django.contrib.auth.models import User
from Admin.models import *

class PayrollInformation(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=50)
    routing_number = models.CharField(max_length=50)
    # Add other payroll-related fields as needed

    def __str__(self):
        return f"Payroll Information for {self.employee}"