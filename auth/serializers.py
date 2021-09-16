from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password',})

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2',)
        extra_kwargs = {
            'password' : {'write_only' : True},
            'email' : {'required': True}
        }
    
    def save(self):
        user = User(
            email = self.validated_data['email'],
            username = self.validated_data['username'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': "Passwords must match."})
        user.set_password(password)
        user.save()
        return user