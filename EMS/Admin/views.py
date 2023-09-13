from django.http import FileResponse, HttpResponse
from .forms import RolesForm  # Create a form for role creation and update
from .models import Roles
from django.shortcuts import render, redirect, get_object_or_404
import os
from django.shortcuts import get_object_or_404
from .models import LeaveRequest
from django.shortcuts import render
from django.shortcuts import render, redirect
from Employee.models import LeaveRequest,  Employee
from Admin.models import Department
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PaymentRecordForm, DepartmentForm
from .models import *
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from .models import Employee
from .forms import EmployeeForm
from django.db.models import Q
from django.conf import settings
from reportlab.pdfgen import canvas
from django.http import HttpResponse,HttpResponseForbidden,HttpResponseNotFound
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter,landscape
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from io import BytesIO
from reportlab.lib.pagesizes import letter, landscape, inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
from django.utils import timezone

# View to show the admin dashboard
# @login_required(login_url='login')

@login_required(login_url='login')
def admin_dashboard(request):
    attendances = TimeRecord.objects.filter(
        is_approved=False).order_by('-id')[:5]
    context = {
        'attendances': attendances
    }
    return render(request, 'admin/dashboard_test.html', context)

@login_required(login_url='login')
def department_dashboard(request):
    departments = Department.objects.all().order_by('-id')[:5]
    return render(request, 'admin/department_dashboard.html', {'departments': departments})

@login_required(login_url='login')
def attendance_dashboard(request):
    attendances = TimeRecord.objects.all().order_by('-id')[:5]
    return render(request, 'admin/attendance_dashboard.html', {'attendances': attendances})

@login_required(login_url='login')
def employee_list_dashboard(request):
    employees = Employee.objects.order_by('-id')[:5]
    return render(request, 'admin/employee_list_dashboard.html', {'employees': employees})

@login_required(login_url='login')
def leave_request_dashboard(request):
    leave_requests = LeaveRequest.objects.filter(
        status='pending').order_by('-id')[:5]
    return render(request, 'admin/leave_request_dashboard.html', {'leave_requests': leave_requests})

# user management

# create , edit and delete employee profiles
# assign roles and permissions to different users

@login_required(login_url='login')
def employee_list(request):
    search_query = request.GET.get('search')
    employees = Employee.objects.all()
    print(employees)

    if search_query:
        employees = employees.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(contact__icontains=search_query) |
            Q(department__name__icontains=search_query) |  # Use __name to filter on department name
            Q(role__roles_name__icontains=search_query)  # Use __roles_name to filter on role name
        )
    # Initialize the no_results_message as empty
    no_results_message = ""

    # Check if there is no search query or if no matching records are found
    if not search_query or not employees:
        no_results_message = "No records found."
        employees = Employee.objects.all()

    return render(request, 'admin/employee_list.html', {'employees': employees, 'search_query': search_query, 'no_results_message': no_results_message})

@login_required(login_url='login')
def employee_list_record(request):
    employees = Employee.objects.all()
    return render(request, 'admin/employee_list_record.html', {'employees': employees})

@login_required(login_url='login')
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'admin/employee_detail.html', {'employee': employee})

@login_required(login_url='login')
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Employee details Captured successfully')
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'admin/employee_form.html', {'form': form})

@login_required(login_url='login')
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request,'Employee details updated successfully')
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'admin/employee_form.html', {'form': form})

@login_required(login_url='login')
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        messages.success(request,'Employee details deleted successfully')
        return redirect('employee_list')
    return render(request, 'admin/employee_confirm_delete.html', {'employee': employee})

@login_required(login_url='login')
def create_employee_user(request, pk):
    # Retrieve the employee object
    employee = get_object_or_404(Employee, pk=pk)

    # Generate a random password (you can customize this logic)
    default_password = "0000"

    # Create a username based on first letter of first name and last name
    first_letter = employee.first_name[0].upper()
    last_name = employee.last_name.lower()
    base_username = f"{first_letter}{last_name}"

    # Check if a user with the same base username already exists
    username = base_username
    suffix = 1
    while get_user_model().objects.filter(username=username).exists():
        # If the username already exists, add a unique suffix
        suffix += 1
        username = f"{base_username}{suffix}"

    # Create a new user account with the AUTH_USER_MODEL setting
    user = get_user_model().objects.create_user(
        username=username,
        password=default_password,
    )

    # Associate the user account with the employee
    employee.user = user
    employee.save()
    messages.success(request, 'Employee username: '+username + " password:" + default_password)
    
    return redirect('employee_list')
    

@login_required(login_url='login')
def generate_employee_report(request):
    employees = Employee.objects.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="employee_report.pdf"'
 
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))

    # Create the PDF content
    elements = []

    # Add logo and header information
    logo_path = os.path.join(settings.BASE_DIR, 'static/images/logo.png')  # Replace with the actual path to your logo image
    logo = Image(logo_path, width=1.5 * inch, height=1.5 * inch)
    elements.append(logo)

    styles = getSampleStyleSheet()
    header_text = '<h1>Employee Report</h1>'
    header = Paragraph(header_text, styles['Heading1'])
    elements.append(header)

    additional_info = '<strong>Date:</strong> {}<br/><strong>Generated By:</strong> {}' \
                      .format(datetime.now().strftime('%Y-%m-%d'), request.user)
    additional_info_paragraph = Paragraph(additional_info, styles['Normal'])
    elements.append(additional_info_paragraph)

    elements.append(Spacer(1, 0.5 * inch))

    # Create the table for employee records
    data = [["Employee Name", "First Name", "Last Name", "Contact", "Department", "Role"]]

    for employee in employees:
        data.append([
            employee.user.username,
            employee.first_name,
            employee.last_name,
            employee.contact,
            employee.department.name,
            employee.role.roles_name,
        ])

    table = Table(data, colWidths=[100, 100, 100, 100, 100, 100])
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()

    # Set the PDF content in the response
    response.write(pdf)

    return response

# departments management
@login_required(login_url='login')
def department_list(request):
    departments = Department.objects.all().order_by('-id')
    return render(request, 'admin/department_list.html', {'departments': departments})

@login_required(login_url='login')
def department_list_record(request):
    departments = Department.objects.all()
    return render(request, 'admin/department_list_record.html', {'departments': departments})

@login_required(login_url='login')
def department_detail(request, pk):
    department = get_object_or_404(Department, pk=pk)
    return render(request, 'admin/department_detail.html', {'department': department})

@login_required(login_url='login')
def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Department created successfully ')
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'admin/department_form.html', {'form': form})

@login_required(login_url='login')
def department_update(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request,'Department updated successfully ')
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'admin/department_form.html', {'form': form})

@login_required(login_url='login')
def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        department.delete()
        messages.success(request,'Department deleted successfully ')
        return redirect('department_list')
    return render(request, 'admin/department_confirm_delete.html', {'department': department})

@login_required(login_url='login')
def generate_department_report(request):
    departments = Department.objects.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="department_report.pdf"'

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))

    # Create the PDF content
    elements = []

    # Add logo and header information
    logo_path = os.path.join(settings.BASE_DIR, 'static/images/logo.png')  # Replace with the actual path to your logo image
    logo = Image(logo_path, width=1.5 * inch, height=1.5 * inch)
    elements.append(logo)

    styles = getSampleStyleSheet()
    header_text = '<h1>Department Report</h1>'
    header = Paragraph(header_text, styles['Heading1'])
    elements.append(header)

    additional_info = '<strong>Date:</strong> {}<br/><strong>Generated By:</strong> {}' \
                      .format(datetime.now().strftime('%Y-%m-%d'), request.user)
    additional_info_paragraph = Paragraph(additional_info, styles['Normal'])
    elements.append(additional_info_paragraph)

    elements.append(Spacer(1, 0.5 * inch))

    # Create the table for department records
    data = [["Department Name", "Description"]]

    for department in departments:
        data.append([
            department.name,
            department.description,
        ])

    table = Table(data, colWidths=[200, 300])
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()

    # Set the PDF content in the response
    response.write(pdf)

    return response

# Time and attendance
# clock-ins and clock-outs
@login_required(login_url='login')
def attendance(request):
    attendances = TimeRecord.objects.all().order_by
    context = {
        'attendances': attendances
    }
    return render(request, 'admin/attendance.html', context)

@login_required(login_url='login')
def approve_adjust(request, pk):
    admin = request.user
    time_record = get_object_or_404(TimeRecord, pk=pk)
    if time_record.is_clock_in:
        time_record.is_approved = True
        time_record.approved_by = admin
        time_record.is_clock_out = True
        time_record.save()
        messages.success(request, 'Time record approved successfully.')
        return redirect('attendance')
    else:
        messages.warning(request, 'You cannot approve a clock-out record without a corresponding clock-in.')
        return redirect('attendance')



@login_required(login_url='login')
def generate_time_record_report(request):
    time_records = TimeRecord.objects.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="time_record_report.pdf"'

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))

    # Create the PDF content
    elements = []

    # Add logo and header information
    logo_path = os.path.join(settings.BASE_DIR, 'static/images/logo.png')  # Replace with the actual path to your logo image
    logo = Image(logo_path, width=1.5 * inch, height=1.5 * inch)
    elements.append(logo)

    styles = getSampleStyleSheet()
    header_text = '<h1>Time Record Report</h1>'
    header = Paragraph(header_text, styles['Heading1'])
    elements.append(header)

    additional_info = '<strong>Date:</strong> {}<br/><strong>Generated By:</strong> {}' \
                      .format(datetime.now().strftime('%Y-%m-%d'), request.user)
    additional_info_paragraph = Paragraph(additional_info, styles['Normal'])
    elements.append(additional_info_paragraph)

    elements.append(Spacer(1, 0.5 * inch))

    # Create the table for time record records
    data = [["User", "Record Date", "Clock In", "Clock Out", "Approved By"]]

    for time_record in time_records:
        data.append([
            time_record.user.username,
            time_record.record_date.strftime('%Y-%m-%d'),
            time_record.clock_in.strftime('%H:%M:%S') if time_record.clock_in else '',
            time_record.clock_out.strftime('%H:%M:%S') if time_record.clock_out else '',
            time_record.approved_by.username if time_record.approved_by else '',
        ])

    table = Table(data, colWidths=[100, 100, 100, 100, 100])
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()

    # Set the PDF content in the response
    response.write(pdf)

    return response

# approve or adjust time records


# payroll management
# pay structure
# payment records of certain employee
def pay_structure(request):
    employees = Employee.objects.all()
    return render(request, 'admin/pay_structure.html', {'employees': employees})


def payment_records(request, employee_id):
    employee = Employee.objects.get(id=employee_id)
    payment_records = PaymentRecord.objects.filter(employee=employee)
    return render(request, 'admin/payment_records.html', {'employee': employee, 'payment_records': payment_records})


def record_payment(request):
    if request.method == 'POST':
        form = PaymentRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Payment record recorded successfully.')
            return redirect('pay_structure')
    else:
        form = PaymentRecordForm()
    return render(request, 'admin/record_payment.html', {'form': form})


# leave and absence management
# approve and deny leave requests
# track and manage employees time off
@login_required(login_url='login')
def leave_requests(request):
    leave_requests = LeaveRequest.objects.all()
    return render(request, 'admin/leave_requests.html', {'leave_requests': leave_requests})

@login_required(login_url='login')
def approve_deny_leave(request, request_id, decision):
    leave_request = LeaveRequest.objects.get(id=request_id)
    if decision == 'approve':
        leave_request.status = 'approved'
    elif decision == 'deny':
        leave_request.status = 'denied'
    leave_request.save()
    messages.success(request, f'Leave request {decision.capitalize()}d.')
    return redirect('leave_requests')
@login_required(login_url='login')
def view_leave_requests(request):
    # Query all leave requests
    leave_requests = LeaveRequest.objects.all()

    context = {
        'leave_requests': leave_requests,
    }

    return render(request, 'admin_view_leave_requests.html', context)

@login_required(login_url='login')
def download_leave_request_attachment(request, request_id):
    if not request.user.is_staff:
        return HttpResponseForbidden("You don't have permission to download this attachment.")

    leave_request = get_object_or_404(LeaveRequest, id=request_id)

    if leave_request.notes:
        file_path = leave_request.notes.path
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{leave_request.notes.name}"'
            return response

    return HttpResponseNotFound("Attachment not found.")

@login_required(login_url='login')
def generate_leave_request_report(request):
    leave_requests = LeaveRequest.objects.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="leave_request_report.pdf"'

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))

    # Create the PDF content
    elements = []

    # Add logo and header information
    logo_path = os.path.join(settings.BASE_DIR, 'static/images/logo.png')  # Replace with the actual path to your logo image
    logo = Image(logo_path, width=1.5 * inch, height=1.5 * inch)
    elements.append(logo)

    styles = getSampleStyleSheet()
    header_text = '<h1>Leave Request Report</h1>'
    header = Paragraph(header_text, styles['Heading1'])
    elements.append(header)

    additional_info = '<strong>Date:</strong> {}<br/><strong>Generated By:</strong> {}' \
                      .format(datetime.now().strftime('%Y-%m-%d'), request.user)
    additional_info_paragraph = Paragraph(additional_info, styles['Normal'])
    elements.append(additional_info_paragraph)

    elements.append(Spacer(1, 0.5 * inch))

    # Create the table for leave request records
    data = [["User", "Start Date", "End Date", "Status"]]

    for leave_request in leave_requests:
        data.append([
            f'{leave_request.user.username}',
            leave_request.start_date.strftime('%Y-%m-%d'),
            leave_request.end_date.strftime('%Y-%m-%d'),
            leave_request.status,
        ])

    table = Table(data, colWidths=[200, 100, 100, 100, 100])
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()

    # Set the PDF content in the response
    response.write(pdf)

    return response
# Roles

@login_required(login_url='login')
def roles_list(request):
    roles = Roles.objects.all()
    return render(request, 'roles/roles_list.html', {'roles': roles})

@login_required(login_url='login')
def create_role(request):
    if request.method == 'POST':
        form = RolesForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Role created successfully.')
            return redirect('roles_list')
    else:
        form = RolesForm()
    return render(request, 'roles/create_role.html', {'form': form})

@login_required(login_url='login')
def edit_role(request, role_id):
    role = get_object_or_404(Roles, pk=role_id)
    if request.method == 'POST':
        form = RolesForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            messages.success(request, 'Role updated successfully.')
            return redirect('roles_list')
    else:
        form = RolesForm(instance=role)
    return render(request, 'roles/edit_role.html', {'form': form, 'role': role})

@login_required(login_url='login')
def delete_role(request, role_id):
    role = get_object_or_404(Roles, pk=role_id)
    if request.method == 'POST':
        role.delete()
        messages.success(request, 'Role deleted successfully.')
        return redirect('roles_list')
    return render(request, 'roles/delete_role.html', {'role': role})




