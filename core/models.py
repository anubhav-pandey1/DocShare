from django.db import models

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

    name = models.CharField(
        max_length=254, null=False, blank=False, unique=True)

    description = models.TextField(max_length=512, null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class Permission(models.Model):

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    document_id = models.ForeignKey(Document, on_delete=models.CASCADE)
    access_level_id = models.ForeignKey(AccessLevel, on_delete=models.CASCADE)

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
