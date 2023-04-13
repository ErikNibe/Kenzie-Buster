from rest_framework import serializers
from users.models import User
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    username = serializers.CharField(
        max_length=150,
        validators=[
            UniqueValidator(User.objects.all(), message="username already taken.")
        ],
    )
    password = serializers.CharField(max_length=127, write_only=True)

    email = serializers.EmailField(
        max_length=127,
        validators=[
            UniqueValidator(User.objects.all(), message="email already registered.")
        ],
    )
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    birthdate = serializers.DateField(allow_null=True, default=None)
    is_employee = serializers.BooleanField(allow_null=True, default=False)

    is_superuser = serializers.BooleanField(read_only=True)

    def create(self, validated_data: dict):
        if validated_data["is_employee"]:
            return User.objects.create_superuser(**validated_data)

        return User.objects.create_user(**validated_data)

    def update(self, instance: User, validated_data: dict):
        password_data = validated_data.pop("password", None)

        if password_data:
            instance.set_password(password_data)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
