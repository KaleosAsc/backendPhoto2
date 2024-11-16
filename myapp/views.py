from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from .models import User, Post, Interaction
from .serializer import UserSerializer, PostSerializer, InteractionSerializer, UserDataSerializer
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)  # Obtiene la respuesta original

        # Extrae los tokens de acceso y de actualización del cuerpo de la respuesta
        access_token = response.data.get('access')
        refresh_token = response.data.get('refresh')
        
        # Accede al user_id a partir del token de acceso
        try:
            user_id = AccessToken(access_token)['user_id']
        except Exception as e:
            return Response({"error": "Invalid token"}, status=400)

        # Retorna una respuesta personalizada con los tokens, el mensaje y el user_id
        return Response({
            "message": "Login successful.",
            "user_id": user_id,
            "access": access_token,
            "refresh": refresh_token
        })

class RegisterUsers(APIView):
    #Method for create user in database
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    

class UserDetail(APIView):    
    permission_classes = [IsAuthenticated] #Authentication request for access API(give access token from api/token endpoint)
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
    permission_classes = [IsAuthenticated] #Authentication request for access API(give access token from api/token endpoint)
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
    permission_classes = [IsAuthenticated]  #Authentication request for access API(give access token from api/token endpoint)
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

#Servicio Especial actualización
class UpdatePostRating(APIView):
    permission_classes = [IsAuthenticated] 
    def post(self, request):
        # Extraer la calificación y el post_id del cuerpo de la solicitud
        post_id = request.data.get("post_id")
        rating = request.data.get("rating")  # Debes asegurarte de que la calificación sea un valor de 1 a 5
        
        if post_id is None or rating not in [1, 2, 3, 4, 5]:
            return Response({"error": "post_id and valid rating (1-5) are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Obtener el post correspondiente
        try:
            post = Post.objects.get(post_id=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Actualizar la calificación del post basado en la calificación recibida
        if rating == 1:
            post.one_starts += 1
        elif rating == 2:
            post.two_starts += 1
        elif rating == 3:
            post.three_starts += 1
        elif rating == 4:
            post.four_starts += 1
        elif rating == 5:
            post.five_starts += 1

        # Guardar el post con la nueva calificación
        post.save()

        # Retornar una respuesta exitosa
        return Response(PostSerializer(post).data, status=status.HTTP_200_OK)

#Servicio Especial Estimación
class EstimateRating(APIView):
    permission_classes = [IsAuthenticated] 
    def get(self, request, pk=None):
        """
        Este endpoint calcula el estimado ponderado de las calificaciones de un post.
        """
        if pk is None:
            return Response({"error": "post_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Obtener el post con el post_id especificado
        post = Post.objects.filter(post_id=pk).first()

        if not post:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        # Realizar el cálculo ponderado de la calificación
        total_stars = (post.five_starts + post.four_starts + post.three_starts +
                       post.two_starts + post.one_starts)
        
        if total_stars == 0:
            return Response({"error": "No ratings available for this post"}, status=status.HTTP_400_BAD_REQUEST)
        
        weighted_sum = (post.five_starts * 5) + (post.four_starts * 4) + \
                       (post.three_starts * 3) + (post.two_starts * 2) + \
                       (post.one_starts * 1)

        estimated_rating = round(weighted_sum / total_stars, 2)
        
        # Regresar el estimado ponderado
        return Response({"post_id": post.post_id, "estimated_rating": estimated_rating}, status=status.HTTP_200_OK)
#Servicio Search
class UsernameSearchView(APIView):
    permission_classes = [IsAuthenticated] 
    def get(self, request):
        query = request.GET.get('query', '')  # Obtén el parámetro de búsqueda
        if not query:
            return Response({'error': 'Se requiere un parámetro de búsqueda'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Filtra los usuarios cuyo nombre de usuario contiene la cadena 'query'
        users = User.objects.filter(username__icontains=query).values_list('username', flat=True)
        return Response({'usernames': list(users)}, status=status.HTTP_200_OK)