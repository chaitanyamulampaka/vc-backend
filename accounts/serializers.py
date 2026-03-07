from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile

class RegisterSerializer(serializers.ModelSerializer):

    role = serializers.ChoiceField(
        choices=Profile.ROLE_CHOICES,
        write_only=True
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        role = validated_data.pop('role')

        user = User.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        # 🔥 Update profile role
        user.profile.role = role
        user.profile.save()

        return user

from rest_framework import serializers
from .models import Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = ["user"]