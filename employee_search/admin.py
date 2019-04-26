from django.contrib import admin
from employee_search.models import Titles, Departments, Employees
# Register your models here.
admin.site.register(Titles)
admin.site.register(Departments)
admin.site.register(Employees)
