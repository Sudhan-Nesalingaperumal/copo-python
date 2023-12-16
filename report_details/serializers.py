from rest_framework import serializers
from academic.models import question_pattern, student, subject
from mark_details.models import CO_Data, Mark_Details
from settings.models import Attainment, College_Details, assessment, co_import, target_value, unit_details

class Report_One_serializer(serializers.ModelSerializer):

    class Meta:

        model = student
        fields = ["register_number","roll_number","student_name"]


class Report_One_serializer(serializers.ModelSerializer):
    student_id = Report_One_serializer()
    class Meta:

        model = Mark_Details
        fields = ["student_id","question"]

class subject_serializer(serializers.ModelSerializer):

    class Meta:
        model = subject
        fields = ["subject_code","subject","staff_name"]

class year_serializer(serializers.ModelSerializer):

    class Meta:
        model = student
        fields = ["academic_year"]

class co_import_serializer(serializers.ModelSerializer):
    class Meta:
        model = co_import
        fields = ['co_number']

class mark_serializer(serializers.ModelSerializer):
    co_number = co_import_serializer()
    class Meta:
        model = question_pattern
        fields = ['co_number','marks_allotted','question']

class Target_serializer(serializers.ModelSerializer):

    class Meta:
        model = target_value
        fields = '__all__'


class seatallocate_serializer(serializers.ModelSerializer):

    class Meta:
        model = College_Details
        fields = ['seat_allocated']

class attainment_serializer(serializers.ModelSerializer):

    class Meta:
        model = Attainment
        fields = '__all__'

class units_serializer(serializers.ModelSerializer):

    class Meta:
        model = unit_details
        fields = '__all__'


class Student_Detail_serializer(serializers.ModelSerializer):
    class Meta:
        model = student
        fields = ["register_number","roll_number","student_name","academic_year"]


class CO_serializer(serializers.ModelSerializer):
    student_id = Student_Detail_serializer()
    class Meta:
        model = CO_Data
        fields = "__all__"


class coimport_serializer(serializers.ModelSerializer):
    class Meta:
        model = co_import
        fields = ['co_number','course_outcome']

class assessment_serializer(serializers.ModelSerializer):
    co_name = coimport_serializer()
    class Meta:
        model = assessment
        fields = '__all__'

