from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from core.models import User, Document, Permission, AccessLevel
from core.choices import AccessLevelChoices
from core.validators import AccessValidator
from core.serializers import UserSerializer, DocumentSerializer, PermissionSerializer

# Create your views here.


class CreateDocument(APIView):

    def post(self, request):
        params = dict(request.data)
        serializer = DocumentSerializer(data=params)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        document = serializer.save()
        self.__make_owner(request, serializer.validated_data)
        return Response(
            f"Document created with id {document.id}", status=status.HTTP_202_ACCEPTED
        )

    def __make_owner(self, request, validated_data):
        name = validated_data['name']
        document = Document.objects.get(name=name)
        owner_level = AccessLevel.objects.get(id=AccessLevelChoices.OWNER)
        author_email = request.data.get('author_email')
        author, created = User.objects.get_or_create(email=author_email)
        Permission.objects.create(
            user=author, document=document, access_level=owner_level)


class GetDocument(APIView):

    def get(self, request):
        params = dict(request.query_params)
        viewer_email = params.get('viewer_email')[0]
        viewer, created = User.objects.get_or_create(email=viewer_email)

        try:
            document_id = params.get('id')[0]
            document = Document.objects.get(id=document_id)
        except:
            return Response("Doc not found, give a valid ID", status=status.HTTP_400_BAD_REQUEST)

        if not AccessValidator.is_viewer(viewer, document):
            return Response(
                "Not allowed to access this document",
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(data={"document": document.name}, status=status.HTTP_200_OK)


class UpdateDocument(APIView):

    def put(self, request):
        params = dict(request.data)
        editor_email = params.get('editor_email')
        editor, created = User.objects.get_or_create(email=editor_email)

        try:
            document_id = params.get('id')
            document = Document.objects.get(id=document_id)
        except:
            return Response("Doc not found, give a valid ID", status=status.HTTP_400_BAD_REQUEST)

        if not AccessValidator.is_editor(editor, document):
            return Response(
                "Not allowed to edit this document",
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = DocumentSerializer(instance=document, data=params)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(data={"message": "Doc updated", "document": document.name}, status=status.HTTP_200_OK)


class DeleteDocument(APIView):

    def delete(self, request):
        params = dict(request.query_params)
        owner_email = params.get('owner_email')[0]
        owner, created = User.objects.get_or_create(email=owner_email)

        try:
            document_id = params.get('id')[0]
            document = Document.objects.get(id=document_id)
        except:
            return Response("Doc not found, give a valid ID", status=status.HTTP_400_BAD_REQUEST)

        if not AccessValidator.is_owner(owner, document):
            return Response(
                "Not allowed to delete this document",
                status=status.HTTP_401_UNAUTHORIZED
            )

        document.delete()
        return Response("Doc deleted", status=status.HTTP_200_OK)


class SetAccessLevel(APIView):

    def put(self, request):
        params = dict(request.data)

        try:
            requester_email = params.get('requester_email')
            requester = User.objects.get(email=requester_email)
        except:
            return Response("Owner for requester email not found, give a valid email",
                            status=status.HTTP_400_BAD_REQUEST)

        receiver_email = params.get('receiver_email')
        receiver, created = User.objects.get_or_create(
            email=receiver_email)

        try:
            document_id = params.get('id')
            document = Document.objects.get(id=document_id)
        except:
            return Response("Doc not found, give a valid ID", status=status.HTTP_400_BAD_REQUEST)

        self.__validate_ownership(requester, receiver, document)

        requested_level = str(params.get('access_level'))
        level_id, is_valid_level = self.__get_level_id_from_str(
            requested_level)
        if not is_valid_level:
            return Response(
                "Access level change request is improper",
                status=status.HTTP_400_BAD_REQUEST
            )

        access_level = AccessLevel.objects.get(id=level_id)
        self.__update_or_create_permission(receiver, document, access_level)

        return Response(
            f"Permission granted for {requested_level.lower()}",
            status=status.HTTP_200_OK
        )

    def __get_level_id_from_str(self, requested_level):
        level_id = AccessLevelChoices.UNAUTHORIZED
        is_valid_level = False
        if requested_level.lower() in ['edit', 'write']:
            level_id = AccessLevelChoices.EDITOR
            is_valid_level = True
        elif requested_level.lower() in ['view', 'read']:
            level_id = AccessLevelChoices.VIEWER
            is_valid_level = True
        return level_id, is_valid_level

    def __update_or_create_permission(self, receiver, document, access_level):
        try:
            Permission.objects.create(
                user=receiver, document=document, access_level=access_level
            )
        except IntegrityError:
            Permission.objects.filter(
                user=receiver, document=document
            ).update(access_level=access_level)

    def __validate_ownership(self, requester, receiver, document):
        # NOTE: Multiple owners for a single document are allowed in DB but not at application layer
        if not AccessValidator.is_owner(requester, document):
            return Response(
                "Not allowed to set access level for this document",
                status=status.HTTP_401_UNAUTHORIZED
            )

        if AccessValidator.is_owner(receiver, document):
            return Response(
                "Not allowed to change access level for an owner",
                status=status.HTTP_400_BAD_REQUEST
            )
