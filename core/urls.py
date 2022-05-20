from django.urls import path

from core import views

urlpatterns = [
    path('create/', views.CreateDocument.as_view(), name='create-document'),
    path('', views.GetDocument.as_view(), name='get-document'),
    path('update/', views.UpdateDocument.as_view(), name='update-document'),
    path('delete/', views.DeleteDocument.as_view(), name='delete-document'),
    path('access/', views.SetAccessLevel.as_view(), name='set-access'),
]
