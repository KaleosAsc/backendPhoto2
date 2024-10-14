from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import User, Post, Interaction
from .serializer import UserSerializer, PostSerializer, InteractionSerializer
from rest_framework.permissions import IsAuthenticated

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
    permission_classes = [IsAuthenticated] #Authentication request for access API(give access token from api/token endpoint)
    #Method for have the users data 
    def get(self,request, pk=None):
        #Bring all the users save in databse model
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
    permission_classes = [IsAuthenticated] #Authentication request for access API(give access token from api/token endpoint)
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
    permission_classes = [IsAuthenticated] #Authentication request for access API(give access token from api/token endpoint)
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
    
