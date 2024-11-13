from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import User, Post, Interaction
from .serializer import UserSerializer, PostSerializer, InteractionSerializer, UserDataSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from myapp.AuthenticationRefresh import AuthenticationRefresh
from django.conf import settings


#Endpoint for LoginUser
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)  # Obtiene la respuesta original

        # Extrae el token de acceso y de actualización del cuerpo de la respuesta
        access_token = response.data.get('access')
        refresh_token = response.data.get('refresh')
        
        #Acces to user_id between access_token
        user_id = AccessToken(access_token)['user_id']

        # Crea una nueva respuesta sin los tokens en el cuerpo
        response = Response({"message": "Login successful. Tokens are set in cookies.",
                             "user_id": user_id
                            })

        # Establece el token de acceso como una cookie HTTP-only
        response.set_cookie(
            'access_token',
            access_token,
            max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
            httponly=True,
            samesite='Lax',
            secure=settings.DEBUG is False  # True en producción
            # key='access_token',  # Nombre de la cookie
            # value=access_token,
            # httponly=True,       # Evita que JavaScript acceda a la cookie
            # # secure=True,         # Asegura que solo se envíe por HTTPS
            # samesite='Lax'    # Opcional, restringe el envío de la cookie
        )

        # También puedes guardar el refresh token como una cookie
        response.set_cookie(
            'access_token',
            access_token,
            max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
            httponly=True,
            samesite='Lax',
            secure=settings.DEBUG is False  # True en producción
        )

        return response


class registerUsers(APIView):
    #Method for create user in database
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    

class UserDetail(APIView):    
    # permission_classes = [AuthenticationRefresh] #Authentication request for access API(give access token from api/token endpoint)
    #Method for have the users data 
    def get(self, request, pk=None):
        if pk is not None:
            # Si se proporciona pk, devolver datos específicos de un usuario
            user = User.objects.filter(user_id=pk).first()
            if user:
                serializer = UserDataSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Si no se proporciona pk, devolver datos de todos los usuarios
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    def put(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = User.objects.get(pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
#Request for Post model
class PostDetail(APIView):
    # permission_classes = [AuthenticationRefresh] #Authentication request for access API(give access token from api/token endpoint)
    def get(self, request, pk=None):
        if pk is not None:
            posts = Post.objects.filter(user_id_id=pk)
            if posts:
                 serializer = PostSerializer(posts, many=True)
                 return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND) 
        else:
            posts = Post.objects.all();
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
    
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():      
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)    
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class InteractionDetail(APIView):
    # permission_classes = [AuthenticationRefresh]  #Authentication request for access API(give access token from api/token endpoint)
    def get(self, request, pk=None):
        inter = Interaction.objects.all();
        serializer = InteractionSerializer(inter, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = InteractionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        inter = Interaction.objects.get(pk=pk)
        serializer = InteractionSerializer(inter, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        inter = Interaction.objects.get(pk=pk)
        inter.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
