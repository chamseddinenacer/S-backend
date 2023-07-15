from django.urls import path,include
from .views import  *
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers



router = routers.DefaultRouter()
router.register('leave-requests', LeaveRequestViewSet)


urlpatterns = [
    
    path('api/', include(router.urls)),

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
    path('api/bonuses/', BonusListCreateView.as_view(), name='bonus-list-create'),
    path('api/bonuses/<int:pk>/', BonusRetrieveUpdateDeleteView.as_view(), name='bonus-retrieve-update-delete'),
    path('api/employees/history/', EmployeeHistoryView.as_view(), name='employee-history'),
    path('api/attendances/history/', AttendanceHistoryView.as_view(), name='attendance-history'),
    path('api/bonuses/history/', BonusHistoryView.as_view(), name='bonus-history'),
    path('api/employees/signup/', EmployeeSignupView.as_view(), name='employee-signup'),
    path('api/login/', EmployeeLoginView.as_view(), name='employee-login'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),  # If you want to use DRF's built-in obtain_auth_token view
]
