from django.contrib import admin
from django.urls import path

from usermanagement.views import LogIn, user_ListView, user_api

urlpatterns = [
    path('create-user/',user_api.as_view(), name='create-user'),
    path('get-user/<id>/',user_api.as_view(), name='get-user'),
    path('put-user/<id>/',user_api.as_view(), name='put-user'),
    path('delete-user/<id>/',user_api.as_view(), name='delete-user'),
    
    path('login/',LogIn.as_view(), name='login'),
    path('user_list/',user_ListView.as_view(), name='user_list'),
]