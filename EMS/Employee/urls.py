from django.urls import path
from .views import *

urlpatterns = [
path('', employee_dashboard, name='employee_dashboard'),
   path('leave_request_dashboard/<int:user_id>/', leave_request_dashboard, name='leave_request_dashboard'),
    path('attendance_dashboard/<int:user_id>/', attendance_dashboard, name='attendance_dashboard'),

    path('view_employee_profile/', view_employee_profile, name='view_employee_profile'),
    path('edit_employee_profile/<int:user_id>', edit_employee_profile, name='edit_employee_profile'),
    path('change_password/<int:user_id>', ChangePasswordView.as_view(), name='change_password'), 

    path('view-payroll-info/', view_payroll_info, name='view_payroll_info'),
    path('view-payment-history/', view_payment_history, name='view_payment_history'),

    path('leave_request_list/<int:user_id>/', leave_request_list, name='leave_request_list'),
    path('create_leave_request/', create_leave_request, name='create_leave_request'),
    path('leave_request_detail/<int:user_id>/', leave_request_detail, name='leave_request_detail'),
     path('edit_leave_request/<int:request_id>/', edit_leave_request, name='edit_leave_request'),
    path('delete_leave_request/<int:request_id>/', delete_leave_request, name='delete_leave_request'),

    path('report-time/', report_time, name='report_time'),
    path('time_record_list/<int:user_id>', time_record_list, name='time_record_list'),
    path('clock_out/<int:pk>', clock_out, name='clock_out'),

    path('generate-pdf-report/<int:user_id>', generate_pdf_report, name='generate_pdf_report'),
]  


