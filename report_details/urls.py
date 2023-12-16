from django.contrib import admin
from django.urls import path

from report_details.views import  CO_Attainment, Co_Data, PO_Attainment, Report_Mark



urlpatterns = [

    path('get-units/',Report_Mark.as_view(), name='get-units'),
    path('get-Co-Data/',Co_Data.as_view(), name='get-Co-Data'),
    path('get-CO-Attainment/',CO_Attainment.as_view(), name='get-CO-Attainment'),
    path('get-PO-Attainment/',PO_Attainment.as_view(), name='get-PO-Attainment'),


]

