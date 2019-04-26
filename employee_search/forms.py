from django import forms
from django.core import validators
from employee_search.models import Titles, Departments, Employees


class SearchEmployeesForm(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    gender = forms.ChoiceField(choices=[("", ""),
                                        ("F", "Female"),
                                        ("M", "Male")],
                               required=False)
    birth_date = forms.DateField(label="Birth date (yyyy-mm-dd)",
                                 required=False)
    hire_date = forms.DateField(label="Hire date (yyyy-mm-dd)",
                                required=False)
    salary = forms.IntegerField(required=False)
    botcatcher = forms.CharField(required=False,
                                 widget=forms.HiddenInput,
                                 validators=[validators.MaxLengthValidator(0)])

    class Meta:
        model = Employees
        # used fields instead of exclude to control field order
        fields = ['first_name',
                  'last_name',
                  'gender',
                  'birth_date',
                  'hire_date',
                  'salary']


# NEED CONSTRAINT UNIQUE?????????????????????????????????????????????
class SearchTitlesForm(forms.ModelForm):
    title = forms.CharField(required=False)

    class Meta:
        model = Titles
        fields = ['title']


# STILL NEED CONSTRAINT UNIQUE???????????????????????????????????????
# can't search by name because of the model's unique=True clause
# using Form instead of ModelForm as a workaround
class SearchDepartmentsForm(forms.Form):
    dept_name = forms.CharField(required=False,
                                label="Department name",
                                validators=[validators.MaxLengthValidator(50)])


class SearchDeptManagerForm(forms.Form):
    first_name = forms.CharField(required=False,
                                 label="Manager's first name")
    last_name = forms.CharField(required=False,
                                label="Manager's last name")

    class Meta:
        model = Employees
        fields = ['first_name',
                  'last_name']
