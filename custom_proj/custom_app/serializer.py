from rest_framework import serializers
from .models import User

MIN_LENGTH = 8


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=MIN_LENGTH,
        error_messages={
            "min_length": f"password must be longer than {MIN_LENGTH} characters."
        }
    )
    confirm_password = serializers.CharField(
        write_only=True,
        min_length=MIN_LENGTH,
        error_messages={
            "min_length": f"password must be longer than {MIN_LENGTH} characters."
        }
    )

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("password does not match")
        return data

    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'mobile_number', 'IGL_Username', 'email', 'password', 'confirm_password',
            'Terms_and_condition_agreement', 'code_of_conduct_agreement')
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            first_name=validated_data['first_name'], last_name=validated_data['last_name'],
            mobile_number=validated_data['mobile_number'],
            email=validated_data['email'], password=validated_data['password'],
            confirm_password=validated_data['confirm_password'], IGL_Username=validated_data['IGL_Username'],
            Terms_and_condition_agreement=validated_data['Terms_and_condition_agreement'],
            code_of_conduct_agreement=validated_data['code_of_conduct_agreement'])
        return user


from rest_framework import serializers


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class Igl_Username_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", 'IGL_Username', 'profile_image',)
