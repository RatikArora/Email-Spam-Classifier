from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('', views.main,name="main"),
    # path('delete_last_row/', views.delete_last_row_view, name='delete_last_row'),
]