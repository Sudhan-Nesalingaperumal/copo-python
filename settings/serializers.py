from rest_framework import serializers

from settings.models import Attainment, College_Details, assessment, co_import, po_import, pso_import, target_value, unit_details


class college_serializer(serializers.ModelSerializer):
    class Meta:
        model = College_Details
        fields = '__all__'

class co_serializer(serializers.ModelSerializer):
    class Meta:
        model = co_import
        fields = '__all__'

class po_serializer(serializers.ModelSerializer):
    class Meta:
        model = po_import
        fields = '__all__'

class pso_serializer(serializers.ModelSerializer):
    class Meta:
        model = pso_import
        fields = '__all__'

class coimport_serializer(serializers.ModelSerializer):
    class Meta:
        model = co_import
        fields = ['co_number']

class assessment_serializer(serializers.ModelSerializer):
    co_name = coimport_serializer()
    class Meta:
        model = assessment
        fields = '__all__'

class units_serializer(serializers.ModelSerializer):
    co_name = coimport_serializer()
    class Meta:
        model = unit_details
        fields = '__all__'

class Target_serializer(serializers.ModelSerializer):

    class Meta:
        model = target_value
        fields = ['target_value']

class attainment_serializer(serializers.ModelSerializer):
    co_name = coimport_serializer()
    class Meta:
        model = Attainment
        fields = '__all__'

