from rest_framework import serializers
from .models import Post, Interaction, User

#Lista todos los campos de cada uno de los modelos de la base de datos
#Los transforma en formato JSON
class UserSerializer(serializers.ModelSerializer):
    #Define for serializer for field in model database except password
    class Meta:
        model=User
        fields='__all__'
        extra_kwargs = {
            'password' : {'write_only' : True}
        }
    #Method for encrypted  password data before save 
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
           instance.set_password(password)
           instance.save()
           return instance
       
class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','user_id','description']
class PostSerializer(serializers.ModelSerializer):
    image_link = serializers.FileField(max_length=1000000)

    class Meta:
        model = Post
        fields = ['post_id', 'user_id', 'image_link', 'description_photo', 'five_starts', 'four_starts', 'three_starts', 'two_starts', 'one_starts']
        
        
class InteractionSerializer(serializers.ModelSerializer):
   class Meta:
        model=Interaction
        fields='__all__'