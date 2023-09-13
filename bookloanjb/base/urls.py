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
    path('book_profile/<str:bookname>/', views.book_profile, name='book_profile'),
    path('book_profile/<bookname>/<ratefilter>', views.book_profile, name='book_profile'),
    path('deletereview/<review_id>/',views.delete_review,name='delete_review'),
    path('updatereview/<review_id>',views.update_review,name='update_review'),

    
     path('deleteloan/<bookname>/',views.delete_loan,name='delete_loan'),
   
    path('loanbook/<bookname>/<loan_type>', views.loan_book, name='loan_book'),

    path('profile', views.user_profile, name='user_profile'),
    path('userdelete', views.delete_user, name='delete_user'),
   

    path('author/<authorname>', views.author_profile, name='author_profile'),


    path('random_authors/', views.random_authors, name='random_authors'),

]