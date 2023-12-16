from django.contrib import admin
from settings.models import Attainment, College_Details, assessment, co_import, po_import, pso_import, target_value, unit_details


# Register your models here.
admin.site.register(College_Details)
admin.site.register(co_import)
admin.site.register(po_import)
admin.site.register(pso_import)
admin.site.register(assessment)
admin.site.register(unit_details)
admin.site.register(target_value)
admin.site.register(Attainment)
