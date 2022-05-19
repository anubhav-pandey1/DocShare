from django.contrib import admin

from core.models import User, Permission, Document, AccessLevel

# Register your models here.

admin.site.register(User)
admin.site.register(Permission)
admin.site.register(Document)
admin.site.register(AccessLevel)
