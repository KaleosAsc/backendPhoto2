from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import User, Post, Interaction
from .serializer import UserSerializer, PostSerializer, InteractionSerializer

class UserDetail(APIView):
    def get(self,request):
        #Bring all the users save in databse model
        users = User.objects.all()
        #Indicate all the serilializer json for user and many model objects
        serializer = UserSerializer(users, many=True)
        #Return a response with json data and 200 status
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    