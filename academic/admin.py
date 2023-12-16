from django.contrib import admin

from academic.models import course, question_pattern, student, subject

# Register your models here.
admin.site.register(course)
admin.site.register(subject)
admin.site.register(student)
admin.site.register(question_pattern)