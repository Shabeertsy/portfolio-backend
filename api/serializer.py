from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'email', 'password', 'profile_image', 'bio','first_name','last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Profile(
            username=validated_data['email'],
            email=validated_data['email'],
            profile_image=validated_data.get('profile_image'),
            bio=validated_data.get('bio')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user