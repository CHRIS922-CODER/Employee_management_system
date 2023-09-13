from Employee.models import *
from .models import *
from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib import messages
from django import forms
from django.contrib.auth.forms import UserCreationForm


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'profile_image','contact', 'department', 'task', 'role', 'salary']

class CreationUserForm(UserCreationForm):
    # Remove existing fields (username, password1, password2) and add them automatically
    # Include additional fields from Employee model
    contact = forms.CharField(label='Contact', max_length=200)
    department = forms.ModelChoiceField(label='Department', queryset=Department.objects.all())
    task = forms.ModelChoiceField(label='Task', queryset=Tasks.objects.all(), required=False)
    role = forms.ModelChoiceField(label='Role', queryset=Roles.objects.all(), required=False)
    salary = forms.DecimalField(label='Salary', max_digits=10, decimal_places=2, required=False)


    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2', 'contact', 'department', 'task', 'role', 'salary']

    def save(self, commit=True):
        user = super().save(commit=False)
        # Save additional fields from the form to the User model
        user.username = self.cleaned_data['username']  # Assuming email is a unique identifier
        user.set_password(self.cleaned_data['password1'])  # Set the password using the built-in method
        user.save()
        return user


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'


class RolesForm(forms.ModelForm):
    class Meta:
        model = Roles
        fields = '__all__'


class TimeRecordForm(forms.ModelForm):
    class Meta:
        model = TimeRecord
        fields = ('user', 'clock_in', 'clock_out','record_date',
                  'is_approved', 'is_clock_in')


class PaymentRecordForm(forms.ModelForm):
    class Meta:
        model = PaymentRecord
        fields = ('user', 'payment_date', 'amount', 'notes')


class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ('user', 'start_date', 'end_date', 'status', 'notes')


class RolesForm(forms.ModelForm):
    class Meta:
        model = Roles
        fields = ['department', 'roles_name']
