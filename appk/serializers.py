from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Employee, Department, Position, Attendance, Bonus,Role,LeaveRequest
 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}


 
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
    class Meta:
        model = Attendance
        fields = '__all__'
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        employee = instance.employee
        employee_serializer = EmployeeSerializer(employee)
        representation['employee'] = employee_serializer.data
        return representation
        
            

class BonusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bonus
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

 



class EmployeeUpSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    # role= RoleSerializer()
    # department= DepartmentSerializer()
    # position= PositionSerializer()
    department_name = serializers.SerializerMethodField()
    role_name = serializers.SerializerMethodField()
    position_title = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = '__all__'   

    def get_department_name(self, obj):
        return obj.get_department_name()

    def get_role_name(self, obj):
        return obj.get_role_name()

    def get_position_title(self, obj):
        return obj.get_position_title()




    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        employee = Employee.objects.create(user=user, **validated_data)
        return employee
  

class UpdateEmplyecodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id','codesms')

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    # role= RoleSerializer()
    # department= DepartmentSerializer()
    # position= PositionSerializer()
    department_name = serializers.SerializerMethodField()
    role_name = serializers.SerializerMethodField()
    position_title = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = '__all__'   

    def get_department_name(self, obj):
        return obj.get_department_name()

    def get_role_name(self, obj):
        return obj.get_role_name()

    def get_position_title(self, obj):
        return obj.get_position_title()




    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        employee = Employee.objects.create(user=user, **validated_data)
        return employee
  
  
class LeaveRequestSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())

    class Meta:
        model = LeaveRequest
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        employee = instance.employee
        employee_serializer = EmployeeSerializer(employee)
        representation['employee'] = employee_serializer.data
        return representation

        

    # def get_employee_first_name(self, obj):
    #     return obj.get_employee_first_name()

    # def get_employee_last_name(self, obj):
    #     return obj.get_employee_last_name()

    # def get_employee_cin(self, obj):
    #     return obj.get_employee_cin()

    # def get_employee_profile_image(self, obj):
    #     return obj.get_employee_profile_image()
   
