from django.urls import path

from . import views

urlpatterns = [
    path('', views.chatIndex),
    path('<slug:roomName>', views.chatConnect)
]
