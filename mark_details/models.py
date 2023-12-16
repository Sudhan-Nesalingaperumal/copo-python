from django.db import models
from academic.models import student

from generic_method.models import Common

# Create your models here.

class Mark_Details(Common):
 
    student_id = models.ForeignKey(student,on_delete = models.CASCADE,related_name = 'student_marks')
    unit = models.IntegerField()
    question = models.JSONField()

    class Meta:
        verbose_name_plural = 'Mark_Details'

    def __str__(self):
        return str(self.student_id)
    
class CO_Data(Common):

    student_id = models.ForeignKey(student,on_delete = models.CASCADE,related_name = 'student_details')
    au_results = models.CharField(max_length=50)
    Assignment_1 = models.IntegerField()
    Assignment_2 = models.IntegerField()
    Assignment_3 = models.IntegerField()
    Assignment_4 = models.IntegerField()
    Assignment_5 = models.IntegerField()

    class Meta:
        verbose_name_plural = 'CO_Data'

    def __str__(self):
        return str(self.student_id)
