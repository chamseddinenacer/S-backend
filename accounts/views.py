from django.contrib.auth import login
from .models import Image
from .serializers import ImageSerializer,UpdateUserSerializer
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, ChangePasswordSerializer
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework.views import APIView
from rest_framework import generics
from .models import Image
from .serializers import ImageSerializer
from django.core.files.base import ContentFile
from django.http import JsonResponse
import base64

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })


class UpdateUserView(APIView):
    def put(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


 
# Login API
# class LoginAPI(KnoxLoginView):
#     permission_classes = (permissions.AllowAny,)

#     def post(self, request, format=None):
#         serializer = AuthTokenSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         login(request, user)
#         return super(LoginAPI, self).post(request, format=None)
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)

        # Récupérer les données de l'utilisateur
        user_serializer = UserSerializer(user)  # Assurez-vous d'importer UserSerializer
        user_data = user_serializer.data

        # Générer le jeton d'authentification
        token = AuthToken.objects.create(user)

        # Construire la réponse avec les données de l'utilisateur et le jeton d'authentification
        response_data = {
            'user': user_data,
            'token': token[1],
        }

        return Response(response_data)


from rest_framework.authtoken.models import Token     

# Get User API
class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

from rest_framework import generics, permissions

from rest_framework import generics
from rest_framework import permissions
from .serializers import UserSerializer
from django.contrib.auth.models import User

# class UserRetrieveAPIView(generics.RetrieveAPIView):
#     permission_classes = [permissions.IsAuthenticated,]
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     lookup_field = 'id'

from rest_framework.generics import ListAPIView, get_object_or_404


class userdd(APIView):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)





# Change Password
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated   

class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class ImageListCreateView(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     idimage = self.request.query_params.get('idimage', None)
    #     if idimage is not None:
    #         queryset = queryset.filter(id=idimage)
    #     return queryset


# class ImageDetailView(generics.RetrieveAPIView):
#     queryset = Image.objects.all()
#     serializer_class = ImageSerializer
#     lookup_field = 'idimage'  # Définir le champ de recherche sur "idimage"
    

def get_image(request, idimage):
        try:
            image = Image.objects.get(idimage=idimage)
            image_data = image.image.read()
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            return JsonResponse({'idimage': idimage, 'image': image_base64})
        except Image.DoesNotExist:
            return JsonResponse({'error': 'Image not found'}, status=404)


class ImageDeleteView(generics.DestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    lookup_field = 'idimage'  # Assuming 'idimage' is the field to use for lookup

    def perform_destroy(self, instance):
        instance.image.delete()  # Delete the associated image file
        instance.delete()  # Delete the Image object

    def get_object(self):
        queryset = self.get_queryset()
        idimage = self.kwargs['idimage']
        try:
            obj = queryset.get(idimage=idimage)
        except Image.DoesNotExist:
            raise NotFound('Image not found')
        self.check_object_permissions(self.request, obj)
        return obj







from twilio.rest import Client
 

class EnvoyerSMS_AddEmployes(APIView):

    def post(self, request):

        # Récupérer les données de la requête
        recipient_list = request.data.get('recipient_list')
        SMS_username = request.data.get('username')
        SMS_pass = request.data.get('password')

        # Vos informations d'identification Twilio
        account_sid = 'AC55c1cbbbce4ff11e72cfebf10e60c873'
        auth_token = '49f351d53a0c12ce5897b5a1aaccd9d7'

        # Initialiser le client Twilio
        client = Client(account_sid, auth_token)

        # Construire le message avec les données de l'employé
        message_body = f"Cher/Chère employé,\n\nVotre compte a été créé avec succès :\n- Nom d'utilisateur : {SMS_username}\n- Mot de passe : {SMS_pass}\n\nConnectez-vous à [Insérer l'URL de connexion] pour accéder à votre compte.\n\nSi vous avez des questions ou avez besoin d'aide, contactez notre équipe de support au [Insérer le numéro de support].\n\nBienvenue et profitez de votre expérience !\n\nCordialement,\n[Votre nom]\n[Votre entreprise]"

        # Envoyer le SMS
        message = client.messages.create(
            body=message_body,
            from_='+12513335440',  # Numéro Twilio autorisé
            to = '+216' + str(recipient_list)  # Numéro de téléphone du destinataire
        )

        return Response({'message': 'SMS envoyé avec succès !'})


# class EnvoyerSMS_AddEmploye(APIView):

#     def post(self, request):

#         recipient_list = request.data.get('recipient_list')
#         SMS_username = request.data.get('username')
#         SMS_pass = request.data.get('password')
#         account_sid = 'ACfa7d8c1c9cc21368bd07e81d2f868e81'
#         auth_token = 'fc6daeebab7777eb8b1c66800efa767c'
#         Number = '+48669993336'

#         client = Client(account_sid, auth_token)

#         nbtt = '+48' + str(recipient_list)
#         print(nbtt)
#         message = client.messages \
#             .create(
#                 body='\nYour secret code for Stagi account  is: \n Username:'+SMS_username + '\n Password:'+SMS_pass,
#                 from_ =  '+12512374137',
#                 to = '+48' + str(recipient_list)

#              )

#         return Response({'message': 'SMS envoyé avec succès !'})