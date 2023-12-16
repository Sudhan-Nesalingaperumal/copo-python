from django.contrib import admin
from django.urls import path

from mark_details.views import Co_Data, mark_detail, marks

urlpatterns = [

    path('get-user/',mark_detail.as_view(), name='get-user'),

    path('create-marks/',marks.as_view(), name='create-marks'),
    path('get-marks/',marks.as_view(), name='get-marks'),
    path('update-marks/<id>/',marks.as_view(), name='update-marks'),
    path('delete-marks/<id>/',marks.as_view(), name='delete-marks'),

    path('create-co-marks/',Co_Data.as_view(), name='create-co-marks'),
    path('get-co-marks/',Co_Data.as_view(), name='get-co-marks'),
    path('put-co-marks/<id>/',Co_Data.as_view(), name='put-co-marks'),
    path('delete-co-marks/<id>/',Co_Data.as_view(), name='delete-co-marks'),
]