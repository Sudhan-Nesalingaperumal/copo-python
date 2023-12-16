from django.contrib import admin
from django.urls import path

from academic.views import  course_uploadview, coursename_uploadview, department_uploadview, question_uploadview, student_uploadview, subject_uploadview

urlpatterns = [
    path('create-course/',course_uploadview.as_view(), name='create-course'),
    path('get-course/',course_uploadview.as_view(), name='get-course'),
    path('update-course/<id>/',course_uploadview.as_view(), name='update-course'),
    path('delete-course/<id>/',course_uploadview.as_view(), name='delete-course'),


    # path('post-degree/',degree_uploadview.as_view(), name='get-degree'),
    path('get-coursename/',coursename_uploadview.as_view(), name='get-coursename'),
    path('get-department/',department_uploadview.as_view(), name='get-department'),


    path('create-subject/',subject_uploadview.as_view(), name='create-subject'),
    path('get-subject/',subject_uploadview.as_view(), name='get-subject'),
    path('update-subject/<id>/',subject_uploadview.as_view(), name='update-subject'),
    path('delete-subject/<id>/',subject_uploadview.as_view(), name='delete-subject'),

    path('create-student/',student_uploadview.as_view(), name='create-student'),
    path('get-student/',student_uploadview.as_view(), name='get-student'),
    path('update-student/<id>/',student_uploadview.as_view(), name='update-student'),
    path('delete-student/<id>/',student_uploadview.as_view(), name='delete-student'),

    path('create-question/',question_uploadview.as_view(), name='create-question'),
    path('get-question/',question_uploadview.as_view(), name='get-question'),
    path('update-question/<id>/',question_uploadview.as_view(), name='update-question'),
    path('delete-question/<id>/',question_uploadview.as_view(), name='delete-question'),




]