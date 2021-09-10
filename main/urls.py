from django.urls import path
from . import views, auth

urlpatterns = [
    path('', views.index),
    path('register', auth.register),
    path('login', auth.login),
    path('logout', auth.logout),
    path('books', views.books),
    path('new_author', views.new_author),
    path('books/add', views.add),
    path('books/<id>', views.book_id),
    path('users/<id>', views.users_id),
    path('delete/<id>', views.delete_id)
]