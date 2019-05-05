from django.db import models
from django.urls import reverse

# TODO: add constraints to rule out duplicates
# TODO: check if population_script.py needs updating after that
# TODO: model forms might be affected as well


class Titles(models.Model):
    title = models.CharField(max_length=50)

    class Meta:
        db_table = 'titles'

    def __str__(self):
        return self.title


class Departments(models.Model):
    dept_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'departments'

    def __str__(self):
        return self.dept_name


class Employees(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    # TODO: add choices for gender; update forms accordingly
    gender = models.CharField(max_length=1)
    birth_date = models.DateField()
    hire_date = models.DateField()
    salary = models.IntegerField()
    # TODO: provide related_name for foreign keys?
    # TODO: would on_delete PROTECT make sense here?
    title = models.ForeignKey(Titles,
                              models.DO_NOTHING)
    department = models.ForeignKey(Departments,
                                   models.DO_NOTHING)
    manager = models.ForeignKey('self',
                                models.SET_NULL,
                                null=True,)

    class Meta:
        db_table = 'employees'

    def __str__(self):
        full_name = ' '.join([self.first_name, self.last_name])
        return full_name

    def get_absolute_url(self):
        return reverse('employee_search:emp_details', kwargs={'pk': self.pk})
