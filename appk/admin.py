from django.contrib import admin
from .models import Employee, Department, Position, Attendance, Bonus,Role

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['title']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email','role', 'department', 'position', 'date_of_birth', 'date_of_hire', 'salary','profile_image', 'is_active']
    list_filter = ['department', 'position', 'is_active','role']
    search_fields = ['first_name', 'last_name', 'email']

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'date', 'is_present']
    list_filter = ['employee', 'date']
    search_fields = ['employee__first_name', 'employee__last_name', 'date']

@admin.register(Bonus)
class BonusAdmin(admin.ModelAdmin):
    list_display = ['employee', 'date', 'amount']
    list_filter = ['employee', 'date']
    search_fields = ['employee__first_name', 'employee__last_name', 'date']
