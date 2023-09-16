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







from twilio.rest import Client
 

class EnvoyerSMS_AddEmploye(APIView):

    def post(self, request):

        # Récupérer les données de la requête
        recipient_list = request.data.get('recipient_list')
        SMS_username = request.data.get('username')
        SMS_pass = request.data.get('password')
        # recipient_list = "29225523"
        # SMS_username = 'chamsaa'
        # SMS_pass = 'chamsa12345'

        # Vos informations d'identification Twilio
        account_sid = 'AC55c1cbbbce4ff11e72cfebf10e60c873'
        auth_token = '49f351d53a0c12ce5897b5a1aaccd9d7'

        # Initialiser le client Twilio
        client = Client(account_sid, auth_token)

        # Construire le message avec les données de l'employé
        message_body = f"\n\nCher/Chère employé,\n\nVotre compte a été prêt :\n- Username : {SMS_username}\n- Password : {SMS_pass}\n\nConnectez-vous à: \n [https://ria-box.netlify.app/] \n pour accéder à votre compte.\n\nSi vous avez des questions ou avez besoin d'aide, contactez notre équipe de support au: \n [+216 29225523].\n\nBienvenue et profitez de votre expérience !\n\nCordialement,\n [CHAMSEDDINE NACER]"

        # Envoyer le SMS
        message = client.messages.create(
            body=message_body,
            from_='+19209455841',  # Numéro Twilio autorisé
            # to = '+216' + str(recipient_list)   
            to = '+216' + str(recipient_list)
        )

        return Response({'message': 'SMS envoyé avec succès !'})



# send sms code for reset password 

class EnvoyerSMS_Rest_Pass(APIView):

    def post(self, request):

        recipient_list = request.data.get('recipient_list')
        SMS_verification = request.data.get('codesms')
        # SMS_verification = str(randint(100000,999999))
        account_sid = 'AC55c1cbbbce4ff11e72cfebf10e60c873'
        auth_token = '49f351d53a0c12ce5897b5a1aaccd9d7'
      

        client = Client(account_sid, auth_token)

        nbtt = '+48' + str(recipient_list)
        print(nbtt)
        message = client.messages \
            .create(
                body='\nYour secret code for Stagi reset Password is: '+SMS_verification,
                from_ =  '+19209455841',
                to = '+216' + str(recipient_list)

                
            )

        return Response({'message': 'SMS envoyé avec succès !'})



# Get data (code sms , new password ) and change & saved it 

class PasswordResetBySms(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        token = request.data.get('token')
        new_password = request.data.get('new_password')

        print('le tokeeennn est ' + token)
        print('le paaasss est ' + new_password)

        if not token or not new_password:
            return Response({'detail': 'Token and new password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        employee = Employee.objects.get(codesms=token)
        user = employee.user
        
         
        print(employee)
        

       
        new_user=''
        if user is not None:

            print("sdddsdsdsdssss")
             
            user.set_password(new_password)
            
            employee.codesms=new_user
            print("t7att l mot jdid")
            user.save()
            employee.save()
            
            print("save mot jdid")
            # employee.delete()



            return Response({'detail': 'Password reset successful.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'user not found.'}, status=status.HTTP_400_BAD_REQUEST)


 
# Update code sms v1 Employé

class Updatecode(APIView):

    def put(self, request, vpt):
        try:
            employe = Employee.objects.get(mobile=vpt)
            print('employe',employe)


        except Employee.DoesNotExist:
            return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

        print('request.data: e jdida',request.data)
        serializer = UpdateEmplyecodeSerializer(employe, data=request.data)
        if serializer.is_valid():
            print('serializer.is_valid')
            serializer.save()
        return Response(serializer.data)


 
# Update code sms v2 User


class Updatecode2(APIView):

    def put(self, request, vpt):
        try:
            user = User.objects.get(last_name=vpt)
            print('user',user)


        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        print('request.data: e jdida',request.data)
        serializer = UpdateUsercodeSerializer(user, data=request.data)
        if serializer.is_valid():
            print('serializer.is_valid')
            serializer.save()
        return Response(serializer.data)





# Send sms to ADMIN when the employe add congé 

class Send_SMS_To_Admin(APIView):

    def post(self, request):

        # Récupérer les données de la requête
        # recipient_list = request.data.get('recipient_list')

        SMS_username = request.data.get('username')
        SMS_last_name = request.data.get('last_name')
        SMS_mobile = request.data.get('mobile')
        # SMS_pass = request.data.get('password')

        num_admin = "29225523"


        # Vos informations d'identification Twilio
        account_sid = 'AC55c1cbbbce4ff11e72cfebf10e60c873'
        auth_token = '49f351d53a0c12ce5897b5a1aaccd9d7'

        # Initialiser le client Twilio
        client = Client(account_sid, auth_token)

        # Construire le message avec les données de l'employé
        message_alerte_conge = f"""
        Demande de congé reçue :

        Nom de l'employé : {SMS_username}
        Prenom de l'employé : {SMS_last_name}
        Numéro de téléphone : {SMS_mobile}

        L'employé {SMS_username} a soumis une demande de congé. Veuillez prendre en considération cette demande.

        Cordialement,
        [ CHAMSEDDINE NACER ]
        """


        # Envoyer le SMS
        message = client.messages.create(
            body=message_alerte_conge,
            from_='+19209455841',  # Numéro Twilio autorisé
            # to = '+216' + str(recipient_list)   
            to = '+216' + str(num_admin)
        )

        return Response({'message': 'SMS envoyé avec succès !'})






# Send sms TO Employe when the admin ACCEPTED congé 

class Send_SMS_Accept_To_Employe(APIView):

    def post(self, request):

        # Récupérer les données de la requête
        recipient_list = request.data.get('recipient_list')
 
        # Vos informations d'identification Twilio
        account_sid = 'AC55c1cbbbce4ff11e72cfebf10e60c873'
        auth_token = '49f351d53a0c12ce5897b5a1aaccd9d7'

        # Initialiser le client Twilio
        client = Client(account_sid, auth_token)

        # Construire le message avec les données de l'employé
        message_acceptation = f"""
        Cher/Chére Employé,

        Nous sommes heureux de vous informer que votre demande de congé a été acceptée.

        Vous pouvez désormais profiter de votre congé aux dates demandées en toute tranquillité.

        Cordialement,
        [ CHAMSEDDINE NACER ]
        """


        # Envoyer le SMS
        message = client.messages.create(
            body=message_acceptation,
            from_='+19209455841',  # Numéro Twilio autorisé
            # to = '+216' + str(recipient_list)   
            to = '+216' + str(recipient_list)
        )

        return Response({'message': 'SMS envoyé avec succès !'})






# Send sms TO Employe when the admin REJECTED congé 

class Send_SMS_Rejecte_To_Employe(APIView):

    def post(self, request):

        # Récupérer les données de la requête
        recipient_list = request.data.get('recipient_list')
 
        # Vos informations d'identification Twilio
        account_sid = 'AC55c1cbbbce4ff11e72cfebf10e60c873'
        auth_token = '49f351d53a0c12ce5897b5a1aaccd9d7'

        # Initialiser le client Twilio
        client = Client(account_sid, auth_token)

        # Construire le message avec les données de l'employé
        message_acceptation = f"""
        Cher/Chére Employé,

        Nous sommes désolés de vous informer que votre demande de congé a été refusée.
        Si vous avez des questions ou des préoccupations, n'hésitez pas à nous contacter a : \n [+216 29225523]..

        Cordialement,
        [ CHAMSEDDINE NACER ]
        """


        # Envoyer le SMS
        message = client.messages.create(
            body=message_acceptation,
            from_='+19209455841',  # Numéro Twilio autorisé
            # to = '+216' + str(recipient_list)   
            to = '+216' + str(recipient_list)
        )

        return Response({'message': 'SMS envoyé avec succès !'})