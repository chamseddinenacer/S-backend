from django.urls import path,include
from .views import  *
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers



router = routers.DefaultRouter()
router.register('leave-requests', LeaveRequestViewSet)


urlpatterns = [
    
    path('api/email/', createmail, name='employee-list-cr'),

    path('api/', include(router.urls)),
    path('api/leave-requests/<int:pk>/status/', LeaveRequestStatusUpdateView.as_view(), name='leaveStatus'),
    # path('api/leave-requests/', LeaveRequestViewSet.as_view(), name='leave'),
    path('api/employees/<int:employee_id>/leave-requests/',leave_requests_by_employee, name='leave-requests-by-employee'),

    path('api/employ/', EmployeeCreateView.as_view(), name='employee-list-create'),

    path('api/employees/', EmployeeListCreateView.as_view(), name='employee-list-create'),
    path('api/employees/<int:pk>/', EmployeeRetrieveUpdateDeleteView.as_view(), name='employee-retrieve-update-delete'),
   
    path('api/departments/', DepartmentListCreateView.as_view(), name='department-list-create'),
    path('api/departments/<int:pk>/', DepartmentRetrieveUpdateDeleteView.as_view(), name='department-retrieve-update-delete'),
   

    path('api/roles/', RoleListCreateView.as_view(), name='role-list-create'),
    path('api/roles/<int:pk>/', RoleRetrieveUpdateDeleteView.as_view(), name='role-retrieve-update-delete'),
   

    path('api/positions/', PositionListCreateView.as_view(), name='position-list-create'),
    path('api/positions/<int:pk>/', PositionRetrieveUpdateDeleteView.as_view(), name='position-retrieve-update-delete'),
    
    
    path('api/attendances/', AttendanceListCreateView.as_view(), name='attendance-list-create'),
    path('api/attendances/<int:pk>/', AttendanceRetrieveUpdateDeleteView.as_view(), name='attendance-retrieve-update-delete'),
    path('api/attendances/<int:employee_id>/att/',delete_Attenad_by_employee, name='Attenad_by_employee'),
    path('api/attendances/<int:employee_id>/empl/',Attenad_by_employee, name='Attenad_by_employee'),




    path('api/bonuses/', BonusListCreateView.as_view(), name='bonus-list-create'),
    path('api/bonuses/<int:pk>/', BonusRetrieveUpdateDeleteView.as_view(), name='bonus-retrieve-update-delete'),
    path('api/employees/history/', EmployeeHistoryView.as_view(), name='employee-history'),
    path('api/attendances/history/', AttendanceHistoryView.as_view(), name='attendance-history'),
    path('api/bonuses/history/', BonusHistoryView.as_view(), name='bonus-history'),
    path('api/employees/signup/', EmployeeSignupView.as_view(), name='employee-signup'),
    path('api/login/', EmployeeLoginView.as_view(), name='employee-login'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),  # If you want to use DRF's built-in obtain_auth_token view




    path('api/smsAddEmploye/',EnvoyerSMS_AddEmploye.as_view(), name='envoyer-sms'),

    path('api/restpassdataSMS/', PasswordResetBySms.as_view(), name='user'),
    path('api/smsRestPassword/',EnvoyerSMS_Rest_Pass.as_view(), name='envoyer-smsRest'),

     path('api/editcode/<str:vpt>/', Updatecode.as_view(), name='update_code'),

    path('api/ListEmployesall/', EmployeeHistoryView.as_view(), name='user'),



    path('api/smstoadminConge/',Send_SMS_To_Admin.as_view(), name='envoyer-sms-admin'),
    path('api/smsToEmployeAccpte/',Send_SMS_Accept_To_Employe.as_view(), name='envoyer-sms-accept'),
    path('api/smsToEmployeReject/',Send_SMS_Rejecte_To_Employe.as_view(), name='envoyer-sms-reject'),




]
