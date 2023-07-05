 
from django.contrib import admin
from django.urls import path, include
# from appk.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    
    # path('api-auth/', include('rest_framework.urls')),
    # path('', include('accounts.urls')),
    # path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),


    path('', include('appk.urls')),
    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
