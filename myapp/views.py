from rest_framework import viewsets
from .serializer import UserSerializer, PostSerializer, InteractionSerializer
from .models import User, Post, Interaction

#Vista de peticiones desde el usuario
@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    """
    Retrieve, update or delete a user.
    """
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#Vista de peticiones desde publicaciones 
@api_view(['GET', 'PUT', 'DELETE'])
def post_detail(request, pk):
    """
    Retrieve, update or delete a post.
    """
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#Vista de peticiones desde interacciones
@api_view(['GET', 'PUT', 'DELETE'])
def interaccion_detail(request, pk):
    """
    Retrieve, update or delete an interaction.
    """
    try:
        interaccion = Interaccion.objects.get(pk=pk)
    except Interaccion.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = InteraccionSerializer(interaccion)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = InteraccionSerializer(interaccion, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        interaccion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# # Lista todos los usuarios
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# # Lista todos los posts
# class PostViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

# # Lista todas las interacciones
# class InteractionViewSet(viewsets.ModelViewSet):
#     queryset = Interaction.objects.all()
#     serializer_class = InteractionSerializer
