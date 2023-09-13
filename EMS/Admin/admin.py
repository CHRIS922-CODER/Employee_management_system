from django.contrib import admin
from .models import Employee, Department, TimeRecord, PaymentRecord, LeaveRequest, LeaveApproval, Tasks, Roles
from django.contrib.auth.models import User

# Register your models here.
admin.site.unregister(User)
admin.site.register(Employee)
admin.site.register(Department)
admin.site.register(TimeRecord)
admin.site.register(PaymentRecord)
admin.site.register(LeaveRequest)
admin.site.register(LeaveApproval)
admin.site.register(Tasks)
admin.site.register(Roles)
admin.site.register(User)

