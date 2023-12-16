from django.db import models
from generic_method.models import Common



# Create your models here.
class user(Common):
    employee_id = models.CharField('employee_id',max_length=100, unique = True)
    username = models.CharField('username', max_length=100)
    email = models.EmailField('email',unique = True)
    department = models.CharField('department', max_length=100)
    designation = models.CharField('designation', max_length=100)
    password = models.CharField('password', max_length=100)
    role = models.CharField('role',max_length=100)

    class Meta:
        verbose_name_plural = "user"

    def __str__(self):
        return str(self.username)