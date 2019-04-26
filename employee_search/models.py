from django.db import models

# Create your models here.


class Titles(models.Model):
    title = models.CharField(max_length=50)

    class Meta:
        db_table = 'titles'


class Departments(models.Model):
    dept_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'departments'


class Employees(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    # add choices for gender
    gender = models.CharField(max_length=1)
    birth_date = models.DateField()
    hire_date = models.DateField()
    salary = models.IntegerField()
    title = models.ForeignKey(Titles,
                              models.DO_NOTHING)
    department = models.ForeignKey(Departments,
                                   models.DO_NOTHING)
    manager = models.ForeignKey('self',
                                models.SET_NULL,
                                null=True,)
    # manager: related_name???
    # recursive fk on_delete PROTECT?????????

    class Meta:
        db_table = 'employees'
