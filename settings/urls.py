from django.contrib import admin
from django.urls import path

from settings.views import College_Detail, Target_Value, assessment_uploadview,attainment_uploadView, co_uploadview, po_uplodview, pso_uploadview, unit_datail

urlpatterns = [
    path('create-college/',College_Detail.as_view(), name='create-college'),
    path('get-college/<id>/',College_Detail.as_view(), name='get-college'),
    path('put-college/<id>/',College_Detail.as_view(), name='put-college'),
    path('delete-college/<id>/',College_Detail.as_view(), name='delete-college'),

    path('upload-co/',co_uploadview.as_view(), name='upload-co'),
    path('export-co/',co_uploadview.as_view(), name='export-co'),
    path('put-co/<id>/',co_uploadview.as_view(), name='put-co'),
    path('delete-co/<id>/',co_uploadview.as_view(), name='delete-co'),

    path('upload-po/',po_uplodview.as_view(), name='upload-po'),
    path('export-po/',po_uplodview.as_view(), name='export-po'),
    path('put-po/<id>/',po_uplodview.as_view(), name='put-po'),
    path('delete-po/<id>/',po_uplodview.as_view(), name='delete-po'),

    path('upload-pso/',pso_uploadview.as_view(), name='upload-pso'),
    path('export-pso/',pso_uploadview.as_view(), name='export-pso'),
    path('put-pso/<id>/',pso_uploadview.as_view(), name='put-pso'),
    path('delete-pso/<id>/',pso_uploadview.as_view(), name='delete-pso'),

    path('upload-attainment/',attainment_uploadView.as_view(), name='upload-attainment'),
    path('get-attainment/',attainment_uploadView.as_view(), name='get-attainment'),
    path('update-attainment/<id>/', attainment_uploadView.as_view(), name='update-attainment'),
    path('delete-attainment/<id>/', attainment_uploadView.as_view(), name='delete-attainment'),

    path('upload-assessment/',assessment_uploadview.as_view(), name='upload-assessment'),
    path('get-assessment/',assessment_uploadview.as_view(), name='get-assessment'),
    path('put-assessment/<id>/',assessment_uploadview.as_view(), name='put-assessment'),
    path('delete-assessment/<id>/',assessment_uploadview.as_view(), name='delete-assessment'),

    path('upload-units/',unit_datail.as_view(), name='upload-units'),
    path('get-units/',unit_datail.as_view(), name='get-units'),
    path('put-units/<id>/',unit_datail.as_view(), name='put-units'),
    path('delete-units/<id>/',unit_datail.as_view(), name='delete-units'),

    path('create-target/',Target_Value.as_view(), name='create-target'),
    path('get-target/',Target_Value.as_view(), name='get-target'),
    path('update-target/<id>/',Target_Value.as_view(), name='update-target'),
    path('delete-target/<id>/',Target_Value.as_view(), name='delete-target'),
]