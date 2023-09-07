from django.urls import path
from base import views

app_name = 'base'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login', views.user_login, name='user_login'),
    path('logout', views.user_logout, name='user_logout'),
    path('books', views.display_books, name='display_books'),
    path('authors', views.display_authors, name='display_authors'),
    path('book_profile/<bookid>/', views.book_profile, name='book_profile'),
    path('book_profile/<int:bookid>/', views.random_book_profile, name='random_book_profile'),





]