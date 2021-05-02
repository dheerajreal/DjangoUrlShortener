from django.urls import path

from . import views

urlpatterns = [
    path('', views.url_record_create, name="index"),
    path('<str:urltag>/', views.resolve, name="resolve"),


]
