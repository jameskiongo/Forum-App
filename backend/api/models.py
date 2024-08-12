from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class Role(models.Model):
    """Role Model"""

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{ self.name }"


class User(AbstractUser):
    """User Models"""

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=250, null=True)
    is_verified = models.BooleanField(default=False)
    google_token = models.CharField(max_length=250)
    twitter_token = models.CharField(max_length=250)
    roles = models.ManyToManyField(Role, related_name="users")
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", blank=True, null=True
    )
    profile_picture_url = models.URLField(max_length=255, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def get_profile_picture(self):
        if self.profile_picture:
            return self.profile_picture.upload_to
        if self.profile_picture_url:
            return self.profile_picture_url
        return "https://w7.pngwing.com/pngs/178/595/png-transparent-user-profile-computer-icons-login-user-avatars-thumbnail.png"

    def __str__(self):
        return f"{ self.username }"


class Category(models.Model):
    """Category Models"""

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{ self.name }"


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{ self.name }"


class Posts(models.Model):
    """Post model"""

    title = models.CharField(max_length=255, blank=False, null=False)
    content = models.TextField(blank=False, null=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )
    categories = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="posts"
    )
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return f"{ self.title }"


class Message(models.Model):
    """Messages model"""

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages"
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_messages",
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username} at {self.timestamp}"

    class Meta:
        ordering = ["-timestamp"]


class Group(models.Model):
    """Group Model"""

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_groups",
    )
    is_private = models.BooleanField(default=False)
    requires_verification = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{ self.name }"


class Membership(models.Model):
    """Membership Model"""

    ROLE_CHOICES = [
        ("creator", "Creator"),
        ("admin", "Admin"),
        ("member", "Member"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="memberships"
    )
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="memberships"
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="member")
    is_verified = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "group")

    def __str__(self):
        return f"{self.user.username} in {self.group.name}"
