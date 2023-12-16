from django.db import models
from generic_method.models import Common
from settings.models import co_import

# Create your models here.
class course(Common):
    department = models.CharField(max_length=100)
    course_code = models.CharField(max_length=100)
    course_name = models.CharField(max_length=100)
    semester = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    academic_year = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "course"

    def __str__(self):
        return str(self.course_name)
    

class subject(Common):
    course_details = models.ForeignKey(course,on_delete = models.CASCADE,related_name="course")
    subject_code = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    staff_name = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "subject"

    def __str__(self):
        return str(self.subject)
    

class student(Common):
    course_details = models.ForeignKey(course,on_delete = models.CASCADE,related_name="student_course")
    register_number = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=100)
    student_name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'student'

    def __str__(self):
        return str(self.roll_number)
    

class question_pattern(Common):
    
    department = models.ForeignKey(course,on_delete = models.CASCADE,related_name = 'depart_question')
    co_number = models.ForeignKey(co_import,on_delete=models.CASCADE,related_name = 'co_question')
    unit = models.IntegerField()
    question_no = models.CharField(max_length=100)
    question = models.CharField(max_length=100)
    marks_allotted = models.IntegerField()
    exam_date = models.DateField()

    class Meta:
        verbose_name_plural = 'question_pattern'

    def __str__(self):
        return str(self.question)
    
    