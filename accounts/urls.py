from knox import views as knox_views
from .views import LoginAPI, RegisterAPI, UserAPI, ChangePasswordView,ImageListCreateView,ImageDeleteView,UpdateUserView,userdd
from django.urls import path
from .views import get_image
 
urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('api/user/', UserAPI.as_view(), name='user'),
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('api/editUser/<int:user_id>/', UpdateUserView.as_view(), name='update_user'),
 
    path('api/users/<int:pk>/', userdd.as_view(), name='user-detail'),

   


    
    path('images/', ImageListCreateView.as_view(), name='image-list-create'),
    # path('images/<int:idimage>/', ImageDetailView.as_view(), name='image-detail'),
    path('images/<int:idimage>/', get_image, name='get_image'),
    path('delimage/<int:idimage>/', ImageDeleteView.as_view(), name='image-delete'),

]

 
