from django.urls import path
from .views import *

urlpatterns = [
    path('', admin_dashboard, name='admin_dashboard'),
    path('department_dashboard/', department_dashboard,
         name='department_dashboard'),
    path('attendance_dashboard/', attendance_dashboard,
         name='attendance_dashboard'),
    path('employee_list_dashboard/', employee_list_dashboard,
         name='employee_list_dashboard'),
    path('leave_request_dashboard/', leave_request_dashboard,
         name='leave_request_dashboard'),

    path('employee_list', employee_list, name='employee_list'),
    path('employee_list_record', employee_list_record,
         name='employee_list_record'),
    path('employee/<int:pk>/', employee_detail, name='employee_detail'),
    path('employee_create/', employee_create, name='employee_create'),
    path('employee/<int:pk>/update/', employee_update, name='employee_update'),
    path('employee/<int:pk>/delete/', employee_delete, name='employee_delete'),
    path('create-employee-user/<int:pk>/',
         create_employee_user, name='create_employee_user'),
     path('generate_employee_report', generate_employee_report, name='generate_employee_report'),

    path('attendance/', attendance, name='attendance'),
    path('approve_adjust/<int:pk>/', approve_adjust, name='approve_adjust'),
    path('generate_time_record_report', generate_time_record_report, name='generate_time_record_report'),

    path('department_list', department_list, name='department_list'),
    path('department_list_record', department_list_record,
         name='department_list_record'),
    path('department/<int:pk>/', department_detail, name='department_detail'),
    path('department_create/', department_create, name='department_create'),
    path('department/<int:pk>/update/',
         department_update, name='department_update'),
    path('department/<int:pk>/delete/',
         department_delete, name='department_delete'),
     path('generate_department_report', generate_department_report, name='generate_department_report'),

    path('pay-structure/', pay_structure, name='pay_structure'),
    path('payment-records/<int:employee_id>/',
         payment_records, name='payment_records'),
    path('record-payment/', record_payment, name='record_payment'),

    path('leave-requests/', leave_requests, name='leave_requests'),
    path('approve-deny-leave/<int:request_id>/<str:decision>/',
         approve_deny_leave, name='approve_deny_leave'),
    path('view-leave-requests/', view_leave_requests, name='view_leave_requests'),
    path('download_leave_request_attachment/<int:request_id>/', download_leave_request_attachment, name='download_leave_request_attachment'),
    path('generate_leave_request_report', generate_leave_request_report, name='generate_leave_request_report'),

    path('roles_list/', roles_list, name='roles_list'),
    path('create_role/', create_role, name='create_role'),
    path('edit_role/<int:role_id>/', edit_role, name='edit_role'),
    path('delete_role/<int:role_id>/', delete_role, name='delete_role'),
]
