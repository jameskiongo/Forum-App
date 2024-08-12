from rest_framework import serializers

from .models import Category, Message, Posts, Role, User


class RoleSerializer(serializers.ModelSerializer):
    """Role Serializer"""

    class Meta:
        model = Role
        fields = ["name"]


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""

    role = serializers.StringRelatedField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "full_name",
            "email",
            "profile_picture",
            "profile_picture_url",
            "role",
        ]


class PostSerializer(serializers.ModelSerializer):
    """Post Serializer"""

    author = UserSerializer(read_only=True)
    category = serializers.StringRelatedField()  # Display category name instead of ID
    tags = serializers.StringRelatedField(
        many=True
    )  # Assuming tags are a ManyToMany field

    class Meta:
        model = Posts
        fields = [
            "id",
            "title",
            "content",
            "author",
            "created_at",
            "updated_at",
            "category",
            "tags",
        ]


class CategorySerializer(serializers.ModelSerializer):
    """Category serializer"""

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
        ]


class MessageSerializer(serializers.ModelSerializer):
    """Message Serializer"""

    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ["id", "sender", "receiver", "content", "timestamp", "is_read"]
