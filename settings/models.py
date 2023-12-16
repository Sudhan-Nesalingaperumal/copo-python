from django.db import models
from generic_method.models import Common

# Create your models here.

class College_Details(Common):
    college_name = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=20)
    email = models.EmailField()
    department = models.CharField(max_length=100)
    address = models.CharField(max_length=225)
    seat_allocated = models.IntegerField()
    img_name = models.TextField()

    class Meta:
        verbose_name_plural = 'College_Details'

    def __str__(self):
        return str(self.id)
    

class co_import(Common):
    co_number = models.CharField(max_length=100)
    course_outcome = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'co_import'

    def __str__(self):
        return str(self.co_number)
    

class po_import(Common):
    po_number = models.CharField(max_length=100)
    po = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'po_import'

    def __str__(self):
        return str(self.po_number)
    

class pso_import(Common):
    pso_number = models.CharField(max_length=100)
    pso = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'pso_import'

    def __str__(self):
        return str(self.pso_number)
    

class assessment(Common):
    co_name = models.ForeignKey(co_import,on_delete=models.CASCADE,related_name='assessment_name')
    course_outcome = models.CharField(max_length=100)
    assessment_tools = models.CharField(max_length=100)
    assessment_weightages = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "assessment"

    def __str__(self):
        return str(self.id)
    
class unit_details(Common):
    co_name = models.ForeignKey(co_import,on_delete=models.CASCADE,related_name='unit_co')
    unit_one = models.IntegerField()
    unit_two = models.IntegerField()
    unit_three = models.IntegerField()
    unit_four = models.IntegerField()
    unit_five = models.IntegerField()

    class Meta:
        verbose_name_plural = "unit_datails"

    def __str__(self):
        return str(self.id) 
    
class target_value(Common):
    target_value = models.IntegerField()
    grade_target_value = models.CharField(max_length=50)
    target_mark = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "target_value"

    def __str__(self):
        return str(self.id)
    
class Attainment(Common):

    co_name = models.ForeignKey(co_import,on_delete=models.CASCADE,related_name='attainment_name')
    po_details = models.JSONField()
    pso_details = models.JSONField()

    class Meta:
        verbose_name_plural = "Attainment"

    def __str__(self):
        return str(self.id)