from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id','username','email','full_name','avatar','role','password']

    def create(self, data):
        user = User(
            username=data['username'],
            email=data['email'],
            full_name=data.get('full_name',''),
            avatar=data.get('avatar','👤'),
        )
        user.set_password(data['password'])
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','full_name','avatar','role','created_at']