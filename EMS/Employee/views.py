from datetime import datetime
from .models import TimeRecord
from .forms import EmployeeProfileForm
from .forms import LeaveRequestForm
from .models import LeaveRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect
from Admin.models import Employee, LeaveRequest, TimeRecord
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import timezone, datetime
from .forms import *
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import Employee
from django.shortcuts import get_object_or_404
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy, reverse
from django.db.models import Q



# employee portal
# View to show the employee dashboard
@login_required(login_url='login')
def employee_dashboard(request):
    user_id = request.user.id

    leave_requests = LeaveRequest.objects.all().filter(user=user_id)
    context = {
        'user_id': user_id,
        'leave_requests': leave_requests,
    }

    return render(request, 'employee/dashboard.html', context)

@login_required(login_url='login')
def leave_request_dashboard(request, user_id):
    user_id = request.user.id
    leave_requests = LeaveRequest.objects.filter(
        user=user_id).order_by('-id')[:5]
    context = {
        'leave_requests': leave_requests,
        'user_id': user_id,
    }
    return render(request, 'employee/leave_request_dashboard.html', context)

@login_required(login_url='login')
def attendance_dashboard(request, user_id):
    user_id = request.user.id
    attendances = TimeRecord.objects.filter(
        user=user_id).order_by('-record_date')
    context = {
        'attendances': attendances,
        'user_id': user_id,
    }
    return render(request, 'employee/attendance_dashboard.html', context)

@login_required(login_url='login')
def leave_request_list(request, user_id):
    user_id = request.user.id
    leave_requests = LeaveRequest.objects.all().filter(user_id=user_id)
    context = {
        'leave_requests': leave_requests,
        'user_id': user_id,
    }
    return render(request, 'employee/leave_request_list.html', context)


@login_required(login_url='login')
def create_leave_request(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST, request.FILES)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.user = request.user  # Associate the user
            leave_request.save()
            return redirect('leave_request_list',user_id=request.user.id)
    else:
        form = LeaveRequestForm()

    context = {
        'form': form,
    }
    return render(request, 'employee/create_leave_request.html', context)

@login_required(login_url='login')
def edit_leave_request(request, request_id):
    leave_request = get_object_or_404(LeaveRequest, id=request_id, user=request.user)

    if request.method == 'POST':
        form = LeaveRequestForm(request.POST, request.FILES, instance=leave_request)
        if form.is_valid():
            leave_request = form.save()
            return redirect('leave_request_list', user_id=request.user.id)

    else:
        form = LeaveRequestForm(instance=leave_request)

    context = {
        'form': form,
        'leave_request': leave_request,
    }
    return render(request, 'employee/edit_leave_request.html', context)

@login_required(login_url='login')
def delete_leave_request(request, request_id):
    leave_request = get_object_or_404(LeaveRequest, id=request_id, user=request.user)

    if request.method == 'POST':
        leave_request.delete()
    
    return redirect('leave_request_list', user_id=request.user.id)
@login_required(login_url='login')
def leave_request_detail(request, user_id):
    leave_request = get_object_or_404(LeaveRequest, user=user_id)
    return render(request, 'leave_request_detail.html', {'leave_request': leave_request})

@login_required(login_url='login')
def view_employee_profile(request):
    user_id = request.user.id
    employee = get_object_or_404(Employee, user=user_id)
    return render(request, 'employee/view_profile.html', {'employee': employee})

@login_required(login_url='login')
def edit_employee_profile(request,user_id):
    employee = get_object_or_404(Employee, user=user_id)
    if request.method == 'POST':
        form = EmployeeProfileForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('view_employee_profile')
    else:
        form = EmployeeProfileForm(instance=employee)
    return render(request, 'employee/edit_profile.html', {'employee': employee, 'form': form})


class ChangePasswordView(PasswordChangeView):
    template_name = 'employee/change_password.html'
    success_url = reverse_lazy('view_employee_profile')

@login_required(login_url='login')
def report_time(request):
    user = request.user
    record_date = datetime.now().date()
    
    # Check if there is an existing record for today
    existing_record = TimeRecord.objects.filter(
        Q(user=user, record_date=record_date),
        ~Q(clock_in=None),
    ).exists()

    if existing_record:
        messages.warning(request, 'You are already clocked in for today wait for approval !')
    else:
            # User is not clocked in, so this is a clock-in event
            TimeRecord.objects.create(
                user=user,
                record_date=record_date,
                clock_in=datetime.now().time(),
                clock_out=None,
                is_clock_in=True,
            )
            messages.success(request, 'You clock in successfully.')

    return redirect(reverse('time_record_list', args=[request.user.id]))

@login_required(login_url='login')
def clock_out(request, pk):
    user=request.user
    record_date = datetime.now().date()

    record = TimeRecord.objects.filter(pk=pk,
    user=user,
    record_date=record_date
    ).first()


    if record and  record.is_clock_out:
        # Check if the record is approved before allowing clock-out
        if record.is_approved:
            record.clock_out = datetime.now().time()
            record.is_clock_in = False
            record.is_clock_out = False
            record.save()
            messages.success(request, 'You clock out successfully.')
        else:
            messages.warning(request, 'You already clock out for the day!!.')
    else:
        messages.warning(request, 'Wait for the Approval.')
    return redirect(reverse('time_record_list', args=[request.user.id]))

@login_required(login_url='login')
def time_record_list(request, user_id):
    time_records = TimeRecord.objects.filter(
        user=user_id).order_by('-record_date')
    context = {
        'time_records': time_records,
        'user_id': user_id
    }
    return render(request, 'employee/time_record_list.html', context)


# generating reports using reportlab

@login_required(login_url='login')
def generate_pdf_report(request, user_id):
    # Retrieve the employee using the provided ID
    employee = get_object_or_404(Employee, user=user_id)

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="employee_report_{employee.employee_id}.pdf"'

    # Create the PDF document
    p = canvas.Canvas(response)

    # Add content to the PDF (employee details)
    p.drawString(100, 760, f'Employee Name: {employee.user.username}')
    p.drawString(100, 740, f'Email: {employee.email}')
    p.drawString(100, 720, f'Contact: {employee.contact}')
    p.drawString(100, 700, f'Department: {employee.department}')
    p.drawString(100, 700, f'Role ID: {employee.role}')
    # Add more details as needed

    # Close the PDF document
    p.showPage()
    p.save()
    return response


# payroll information
# view payment history
def view_payroll_info(request):
    employee = Employee.objects.get(user_id=request.user)
    try:
        payroll_info = PayrollInformation.objects.get(employee=employee)
    except PayrollInformation.DoesNotExist:
        payroll_info = None
    return render(request, 'employee/view_payroll_info.html', {'employee': employee, 'payroll_info': payroll_info})


def view_payment_history(request):
    employee = Employee.objects.get(user=request.user)
    payment_history = PaymentRecord.objects.filter(employee=employee)
    return render(request, 'employee/view_payment_history.html', {'employee': employee, 'payment_history': payment_history})
