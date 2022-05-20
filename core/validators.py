from core.models import Permission
from core.choices import AccessLevelChoices


class AccessValidator:

    @staticmethod
    def is_viewer(viewer, document):
        permission = Permission.objects.filter(
            user=viewer, document=document).first()
        return permission and permission.access_level.id >= AccessLevelChoices.VIEWER

    @staticmethod
    def is_editor(editor, document):
        permission = Permission.objects.filter(
            user=editor, document=document).first()
        return permission and permission.access_level.id >= AccessLevelChoices.EDITOR

    @staticmethod
    def is_owner(owner, document):
        permission = Permission.objects.filter(
            user=owner, document=document).first()
        return permission and permission.access_level.id >= AccessLevelChoices.OWNER
