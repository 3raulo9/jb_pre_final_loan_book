
from django.contrib import admin
from django.urls import path, include
from base import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('library/', include('base.urls')),
    path('book_profile/', views.random_book_profile, name='random_book_profile'),

]
