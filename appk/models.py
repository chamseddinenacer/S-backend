from django.db import models
from django.contrib.auth.models import User
 

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Position(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
        
class Role(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Employee(models.Model):
     

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    cin = models.CharField(max_length=20)
    email = models.EmailField()
    gender = models.CharField(max_length=20)
  
    mobile = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    cnss = models.CharField(max_length=30)
    

    # Poste d'employee
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    salary = models.DecimalField(max_digits=8, decimal_places=2)
    date_of_hire = models.DateField()
    experience = models.CharField(max_length=255)
    type_of_contrat = models.CharField(max_length=20)
    date_of_out = models.DateField()


    def get_department_name(self):
        return self.department.name

    def get_role_name(self):
        return self.role.name

    def get_position_title(self):
        return self.position.title
    



    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class LeaveRequest(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
 
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.CharField(max_length=100)
    leave_type = models.CharField(max_length=100,default='')
    nbjour = models.PositiveIntegerField(blank=True, null=True)
    status = models.CharField(max_length=20, default='Pending')

    # def add_employee_detail(self):
    #     return self.employee.first_name    
    # def get_employee_last_name(self):
    #     return self.employee.last_name  
    # def get_employee_cin(self):
    #     return self.employee.cin  
    # def get_employee_profile_image(self):
    #     return self.employee.profile_image


    
class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])
    is_present = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.employee} - {self.date}"

class Bonus(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.employee} - {self.date}"
