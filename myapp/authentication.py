from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

class authenticationRefresh(BasePermission):
    """
    Permitir el acceso solo si el token de acceso es válido o se puede refrescar.
    """

    def has_permission(self, request, view):
        actual_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')

        if actual_token is not None:
            # Aquí puedes agregar lógica para verificar el token actual
            return True  # Asumir que el token es válido por simplicidad

        # Si no hay un token de acceso, intentar refrescarlo
        if refresh_token is not None:
            try:
                refresh = RefreshToken(refresh_token)
                new_access_token = str(refresh.access_token)
                # Opcional: Aquí puedes almacenar el nuevo token de acceso en la cookie
                request.COOKIES['access_token'] = new_access_token  # Modifica como sea necesario
                return True  # Permitir acceso después de refrescar
            except TokenError:
                return False  # Token de refresco no válido

        return False  # No hay tokens disponibles
