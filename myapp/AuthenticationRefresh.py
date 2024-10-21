from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.response import Response
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class AuthenticationRefresh(BasePermission):
    """
    Permitir el acceso solo si el token de acceso es válido o se puede refrescar.
    """

    def has_permission(self, request, view):
        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')

        if access_token:
            try:
                AccessToken(access_token)
                return True
            except TokenError:
                logger.info("Token de acceso inválido, intentando refrescar.")

        if refresh_token:
            try:
                refresh = RefreshToken(refresh_token)
                new_access_token = str(refresh.access_token)
                
                # Actualizar el token de acceso en la cookie
                self.set_access_token_cookie(request, new_access_token)
                
                return True
            except TokenError as e:
                logger.error(f"Error al refrescar el token: {str(e)}")
                return False

        logger.warning("No hay tokens disponibles")
        return False

    def set_access_token_cookie(self, request, access_token):
        request.COOKIES['access_token'] = access_token


# from rest_framework.permissions import BasePermission
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt.exceptions import TokenError

# class authenticationRefresh(BasePermission):
#     """
#     Permitir el acceso solo si el token de acceso es válido o se puede refrescar.
#     """

#     def has_permission(self, request, view):
#         actual_token = request.COOKIES.get('Set-Cookie')
#         refresh_token = request.COOKIES.get('refresh_token')
#         print(actual_token)
#         print(refresh_token)

#         if actual_token is not None:
#             # Aquí puedes agregar lógica para verificar el token actual
#             return True  # Asumir que el token es válido por simplicidad

#         # Si no hay un token de acceso, intentar refrescarlo
#         if refresh_token is not None:
#             try:
#                 refresh = RefreshToken(refresh_token)
#                 new_access_token = str(refresh.access_token)
#                 # Opcional: Aquí puedes almacenar el nuevo token de acceso en la cookie
#                 request.COOKIES['access_token'] = new_access_token  # Modifica como sea necesario
#                 return True  # Permitir acceso después de refrescar
#             except TokenError:
#                 print(TokenError)
#                 return False  # Token de refresco no válido               
#         print("Unexpected error sesion")

#         return False  # No hay tokens disponibles
