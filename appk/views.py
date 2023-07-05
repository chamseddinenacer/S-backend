from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from rest_framework.parsers import MultiPartParser, FormParser
 

 
from django.contrib.auth import authenticate
from .serializers import UserSerializer, EmployeeSerializer

  

from .models import Employee, Department, Position, Attendance, Bonus
from .serializers import (
    UserSerializer, EmployeeSerializer, DepartmentSerializer,
    PositionSerializer, AttendanceSerializer, BonusSerializer,
)

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











 

# class EmployeeLoginView(generics.CreateAPIView):
#     serializer_class = UserSerializer
#     permission_classes = [AllowAny]

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']

#         if not user.employee.is_active:
#             return Response({'detail': 'Your account is not activated yet. Please contact the admin.'}, status=status.HTTP_401_UNAUTHORIZED)

#         token, created = Token.objects.get_or_create(user=user)
#         return Response({'token': token.key}, status=status.HTTP_200_OK)
 
 
 

class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]



class EmployeeRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    parser_classes = [MultiPartParser, FormParser]
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]


class DepartmentListCreateView(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

class DepartmentRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

class PositionListCreateView(generics.ListCreateAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [IsAuthenticated]

class PositionRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [IsAuthenticated]

class AttendanceListCreateView(generics.ListCreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

class AttendanceRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

class BonusListCreateView(generics.ListCreateAPIView):
    queryset = Bonus.objects.all()
    serializer_class = BonusSerializer
    permission_classes = [IsAuthenticated]

class BonusRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bonus.objects.all()
    serializer_class = BonusSerializer
    permission_classes = [IsAuthenticated]



class EmployeeHistoryView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

class AttendanceHistoryView(generics.ListAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        employee = self.request.user.employee
        return Attendance.objects.filter(employee=employee).order_by('-date')

class BonusHistoryView(generics.ListAPIView):
    serializer_class = BonusSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        employee = self.request.user.employee
        return Bonus.objects.filter(employee=employee).order_by('-date')


