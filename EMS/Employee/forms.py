from .models import *
from Admin.models import *
from django import forms


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'




class PayrollInformationForm(forms.ModelForm):
    class Meta:
        model = PayrollInformation
        fields = ('bank_name', 'account_number', 'routing_number')


class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ('start_date', 'end_date', 'notes')
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


class EmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'profile_image','contact', 'department', 'task', 'role']
