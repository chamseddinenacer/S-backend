from rest_framework import generics, status , viewsets
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from rest_framework.parsers import MultiPartParser, FormParser
 
from rest_framework.generics import ListAPIView, get_object_or_404

 
from django.contrib.auth import authenticate
from .serializers import UserSerializer, EmployeeSerializer

  

from .models import Employee, Department, Position, Attendance, Bonus, Role

from .serializers import  *
from .utils import send_leave_request_email
from django.http import HttpResponse


def createmail(request):
  
    send_leave_request_email()
    return HttpResponse('Leave request submitted successfully cd')












class EmployeeSignupView(generics.CreateAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        user_data = request.data.get('user')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Create the user using the serializer
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        # Save the employee with the user object
        employee = serializer.save(user=user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)



class EmployeeLoginView(generics.CreateAPIView):
    serializer_class = UserSerializer
    aserializer_class = EmployeeSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Récupérer les données de la requête POST
        username = request.data.get('username')
        password = request.data.get('password')

       
        if not username or not password:
            return Response({'detail': 'Please provide both username and password.'}, status=status.HTTP_400_BAD_REQUEST)

       
        user = authenticate(username=username, password=password)

     
        if user is not None:
            # Vérifier si le compte de l'employé est activé
            if not user.employee.is_active:
                return Response({'detail': 'Your account is not activated yet. Please contact the admin.'}, status=status.HTTP_401_UNAUTHORIZED)

            # Générer un jeton d'authentification pour l'utilisateur
            token, created = Token.objects.get_or_create(user=user)

            # Répondre avec le jeton généré
            return Response({
                'token': token.key,
                'user': self.aserializer_class(user.employee).data,

    
            
            
            
            }, status=status.HTTP_200_OK)
        else:
            # Si l'authentification échoue, renvoyer une réponse d'erreur
            return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)








class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

from rest_framework.views import APIView


class EmployeeCreateView(APIView):
    def post(self, request):
        employee_serializer = EmployeeSerializer(data=request.data)
        if employee_serializer.is_valid():
            employee = employee_serializer.save()

            # Récupérer les objets associés
            role = Role.objects.get(id=request.data['role'])
            department = Department.objects.get(id=request.data['department'])
            position = Position.objects.get(id=request.data['position'])

            # Sérialiser les objets associés
            role_serializer = RoleSerializer(role)
            department_serializer = DepartmentSerializer(department)
            position_serializer = PositionSerializer(position)

            # Ajouter les objets sérialisés à la réponse JSON
            response_data = {
                'employee': employee_serializer.data,
                'role': role_serializer.data,
                'department': department_serializer.data,
                'position': position_serializer.data
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(employee_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.decorators import api_view



@api_view(['GET'])
def leave_requests_by_employee(request, employee_id):
    try:
        leave_requests = LeaveRequest.objects.filter(employee=employee_id)
        serializer = LeaveRequestSerializer(leave_requests, many=True)
        return Response(serializer.data, status=200)
    except LeaveRequest.DoesNotExist:
        return Response({'message': 'No leave requests found for the specified employee ID.'}, status=404)
    except Exception as e:
        return Response({'message': str(e)}, status=500)


# class EmployeeRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
#     parser_classes = [MultiPartParser, FormParser]
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer
#     permission_classes = [AllowAny]

class EmployeeRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    parser_classes = [MultiPartParser, FormParser]
    queryset = Employee.objects.all()
    serializer_class = EmployeeUpSerializer
    permission_classes = [AllowAny]
    






class LeaveRequestViewSet(viewsets.ModelViewSet):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer

    
 
 # Mettez à jour le statut de la demande de congé
class LeaveRequestStatusUpdateView(APIView):
    def post(self, request, pk):
        try:
            leave_request = LeaveRequest.objects.get(pk=pk)
            status = request.data.get('status')

            # Mettez à jour le statut de la demande de congé
            leave_request.status = status
            leave_request.save()
            from rest_framework import status
            return Response({'message': 'Statut mis à jour avec succès.'}, status=status.HTTP_200_OK)
        except LeaveRequest.DoesNotExist:
            return Response({'message': 'La demande de congé spécifiée n\'existe pas.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






class DepartmentListCreateView(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [AllowAny]


class DepartmentRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [AllowAny]

class PositionListCreateView(generics.ListCreateAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [AllowAny]

class PositionRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [AllowAny]

class AttendanceListCreateView(generics.ListCreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [AllowAny]

class AttendanceRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [AllowAny]





@api_view(['GET'])
def delete_Attenad_by_employee(request, employee_id):
    try:
        # Attenad = Attendance.objects.filter(employee=employee_id)
        # serializer = LeaveRequestSerializer(Attenad, many=True)
        Attenad = get_object_or_404(Attendance , employee=employee_id)
        Attenad.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Attendance.DoesNotExist:
        return Response({'message': 'No Attendance requests found for the specified employee ID.'}, status=404)
    except Exception as e:
        return Response({'message': str(e)}, status=500)

 

@api_view(['GET'])
def Attenad_by_employee(request, employee_id):
    try:
        attendance = Attendance.objects.filter(employee=employee_id)
        serializer = AttendanceSerializer(attendance, many=True)
        return Response(serializer.data, status=200)
    except LeaveRequest.DoesNotExist:
        return Response({'message': 'No attendance found for the specified employee ID.'}, status=404)
    except Exception as e:
        return Response({'message': str(e)}, status=500)










class BonusListCreateView(generics.ListCreateAPIView):
    queryset = Bonus.objects.all()
    serializer_class = BonusSerializer
    permission_classes = [AllowAny]

class BonusRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bonus.objects.all()
    serializer_class = BonusSerializer
    permission_classes = [AllowAny]



class EmployeeHistoryView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [AllowAny]

class AttendanceHistoryView(generics.ListAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        employee = self.request.user.employee
        return Attendance.objects.filter(employee=employee).order_by('-date')

class BonusHistoryView(generics.ListAPIView):
    serializer_class = BonusSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        employee = self.request.user.employee
        return Bonus.objects.filter(employee=employee).order_by('-date')


class RoleListCreateView(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [AllowAny]

class RoleRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [AllowAny]