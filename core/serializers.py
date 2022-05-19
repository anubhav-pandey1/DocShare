from rest_framework import serializers

from core.models import User, Document, Permission, AccessLevel


class UserSerializer(serializers.ModelSerializer):
    """Used to create serialized User object"""

    class Meta:
        model = User


class DocumentSerializer(serializers.ModelSerializer):
    """Used to create serialized Document object"""

    class Meta:
        model = Document


class PermissionSerializer(serializers.ModelSerializer):
    """Used to create serialized Permission object"""

    user_id = serializers.PrimaryKeyRelatedField(
        many=False, read_only=False, queryset=User.objects.all()
    )

    document_id = serializers.PrimaryKeyRelatedField(
        many=False, read_only=False, queryset=Document.objects.all()
    )

    access_level_id = serializers.PrimaryKeyRelatedField(
        many=False, read_only=False, queryset=AccessLevel.objects.all()
    )

    class Meta:
        model = Permission
        fields = [
            "id",
            "user_id",
            "document_id",
            "access_level_id",
            "created_at",
            "updated_at",
        ]
