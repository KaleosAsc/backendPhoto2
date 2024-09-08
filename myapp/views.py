from rest_framework import viewsets
from .serializer import UserSerializer, PostSerializer, InteractionSerializer
from .models import User, Post, Interaction

# Lista todos los usuarios
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Lista todos los posts
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

# Lista todas las interacciones
class InteractionViewSet(viewsets.ModelViewSet):
    queryset = Interaction.objects.all()
    serializer_class = InteractionSerializer
