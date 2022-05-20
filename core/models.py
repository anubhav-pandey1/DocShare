from django.db import models

from core.choices import AccessLevelChoices

# Create your models here.


class User(models.Model):

    email = models.EmailField(
        max_length=254, null=False, blank=False, unique=True)

    def __str__(self) -> str:
        return self.email


class Document(models.Model):

    name = models.CharField(
        max_length=254, null=False, blank=False, unique=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self) -> str:
        return self.name


class AccessLevel(models.Model):

    id = models.IntegerField(primary_key=True, null=False,
                             blank=False, unique=True, choices=AccessLevelChoices.LIST)

    description = models.TextField(max_length=512, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.id)


class Permission(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    access_level = models.ForeignKey(AccessLevel, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        """Implement a unique together constraint for (user_id, document_id)"""

        constraints = [
            models.UniqueConstraint(
                fields=['user_id', 'document_id'], name='unique_document_per_user')
        ]

    def __str__(self) -> str:
        return f"Document {self.document_id}, User {self.user_id}, Access Level {self.access_level_id}"
