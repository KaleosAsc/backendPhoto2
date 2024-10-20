from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import User, Post, Interaction
from .serializer import UserSerializer, PostSerializer, InteractionSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from myapp.authentication import authenticationRefresh



class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)  # Obtiene la respuesta original

        # Extrae el token de acceso y de actualización del cuerpo de la respuesta
        access_token = response.data.get('access')
        refresh_token = response.data.get('refresh')

        # Crea una nueva respuesta sin los tokens en el cuerpo
        response = Response({"message": "Login successful. Tokens are set in cookies."})

        # Establece el token de acceso como una cookie HTTP-only
        response.set_cookie(
            key='access_token',  # Nombre de la cookie
            value=access_token,
            httponly=True,       # Evita que JavaScript acceda a la cookie
            # secure=True,         # Asegura que solo se envíe por HTTPS
            samesite='Lax'       # Opcional, restringe el envío de la cookie
        )

        # También puedes guardar el refresh token como una cookie
        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=True,
            # secure=True,
            samesite='Lax'
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
    
# class loginUser(APIView):
#     permission_classes = []
#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')
#         user = authenticate(email=email ,password = password)
        
#         if user is not None:

#             tokens = create_jwt_pair_for_user(user)

#             response = {"message": "Login Successfull", "tokens": tokens}
#             return Response(data=response, status=status.HTTP_200_OK)

#         else:
#             return Response(data={"message": "Invalid email or password"})

#     def get(self, request: Request):
#         content = {"user": str(request.user), "auth": str(request.auth)}

#         return Response(data=content, status=status.HTTP_200_OK)
        # serializer = UserSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # print(serializer.errors)
        # return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    
    
class UserDetail(APIView):    
    permission_classes = [authenticationRefresh] #Authentication request for access API(give access token from api/token endpoint)
    #Method for have the users data 
    def get(self,request, pk=None):
        users = User.objects.all()
        #Indicate all the serilializer json for user and many model objects
        serializer = UserSerializer(users, many=True)
        #Return a response with json data and 200 status
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
    permission_classes = [authenticationRefresh] #Authentication request for access API(give access token from api/token endpoint)
    def get(self, request, pk=None):
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
    permission_classes = [authenticationRefresh]  #Authentication request for access API(give access token from api/token endpoint)
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
    
