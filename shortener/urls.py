from django.urls import path

from . import views

urlpatterns = [
    path('', views.url_record_create, name="index"),
    path('detail/<str:urltag>/', views.detail, name="url_detail"),
    path('<str:urltag>/', views.resolve, name="resolve"),


]
