from rest_framework import serializers

from academic.models import course, question_pattern, student
from mark_details.models import CO_Data, Mark_Details
from settings.models import co_import

class course_detail_serializer(serializers.ModelSerializer):
    class Meta:
        model = course
        fields = ['department']

class student_serializer(serializers.ModelSerializer):
    course_details = course_detail_serializer()
    class Meta:
        model = student
        fields = "__all__"

class co_import_serializer(serializers.ModelSerializer):
    class Meta:
        model = co_import
        fields = ['co_number']

class question_serializer(serializers.ModelSerializer):
    co_number = co_import_serializer()
    class Meta:
        model = question_pattern
        fields = ['co_number','question','question_no']
        

class studentdetail_serializer(serializers.ModelSerializer):
    class Meta:
        model = student
        fields = ["register_number","roll_number","student_name","academic_year"]

class mark_serializer(serializers.ModelSerializer):
    student_id = studentdetail_serializer()
    class Meta:
        model = Mark_Details
        fields = "__all__"

class Student_Detail_serializer(serializers.ModelSerializer):
    class Meta:
        model = student
        fields = ["register_number","roll_number","student_name","academic_year"]


class CO_serializer(serializers.ModelSerializer):

    student_id = Student_Detail_serializer()
    class Meta:
        model = CO_Data
        fields = "__all__"