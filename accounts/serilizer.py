from rest_framework import serializers
from .models import NewUser

class UserSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField( style={ 'input_type': 'password'},write_only=True)
    class Meta:
        model = NewUser
        fields = ('email', 'password', 'password2','user_name')
        extra_kwargs = {
            'password' : {'write_only' : True , 'style' : {'input_type': 'password'}}
        }

    def create(self,validated_data):

        password = validated_data.pop('password')
        password2 = validated_data.pop('password2')
        if(password != password2):
            raise serializers.ValidationError({ 'password' : "passwords do not match."})

        user = self.Meta.model(**validated_data)
        user.set_password(password)
        user.save()
        return user

class PostUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewUser
        fields = ('id','user_name')
