from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('create/', views.create_customer, name='create_customer'),
    path('interact/<int:cid>', views.interact, name='interact'),
    path('summary/', views.summary, name='summary'),
]