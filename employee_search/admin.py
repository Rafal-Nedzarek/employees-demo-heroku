from django.contrib import admin
from employee_search.models import Titles, Departments, Employees
# Register your models here.
admin.site.register(Titles)


@admin.register(Employees)
class EmployeesAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'salary', 'title',
                    'department', 'manager')
    list_filter = ('title', 'department')


# the following two classes are added just for training
# getting the inlines can be pretty slow...
class EmployeesInline(admin.TabularInline):
    model = Employees
    extra = 0


@admin.register(Departments)
class DepartmentsAdmin(admin.ModelAdmin):
    inlines = [EmployeesInline]
