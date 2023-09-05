
from django.contrib import admin
from django.urls import path, include
from base import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('library/', include('base.urls'))

]