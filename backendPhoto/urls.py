from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from rest_framework_simplejwt.views import (
    TokenObtainPairView, #Data for obtein pair tokens 
    TokenRefreshView, #Data for obtein refresh token
)

urlpatterns = [
    #Endpoint for give refresh and access token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #Endpoint for refresh access token 
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
    path('api/', include("myapp.urls"))
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   

