from django.urls import path

from . import views

urlpatterns = [
    path('', views.url_record_create, name="index"),
    path('urls/', views.urls_by_user_list_view, name="urls_by_user_list_view"),
    path('urls/expired', views.expired_urls_by_user_list_view, name="expired_urls_by_user_list_view"),
    path('detail/<str:urltag>/', views.detail, name="url_detail"),
    path('<str:urltag>/', views.resolve, name="resolve"),


]
