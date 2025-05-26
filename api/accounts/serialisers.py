from rest_framework import serializers
from . models import *

class UserSerialiser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserProfileSerialiser(serializers.ModelSerializer):
    user = UserSerialiser(read_only=True)

    class Meta:
        model = UserProfile
        #fields = "__all__"
        fields = ['id', 'user', 'role', 'gender', 'phone_number', 'address', 'bio_data', 'image']
        #depth = 1

    def update(self, instance, validated_data):
        # Extract and update user data separately
        user_data = validated_data.pop('user', None)

        if user_data:
            user_instance = instance.user  # Get related User object
            for key, value in user_data.items():
                setattr(user_instance, key, value)
            user_instance.save()  # Save User model updates

        # Update UserProfile fields
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()  # Save UserProfile model
        return instance