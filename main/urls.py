from django.urls import path
from . import views, auth

urlpatterns = [
    path('', views.index),
    path('register', auth.register),
    path('login', auth.login),
    path('logout', auth.logout),
    path('travels', views.travels),
    path('travels/add', views.travels_add),
    path('travels/destination/<id>', views.travels_id),
    path('delete/<id>', views.delete_id)
]