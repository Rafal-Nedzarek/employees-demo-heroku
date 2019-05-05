from django import forms
from django.core import validators
from employee_search.models import Titles, Departments, Employees
from django.contrib.auth.models import User

# TODO: add choice b/w iexact and icontains


class SearchEmployeesForm(forms.ModelForm):
    # TODO: use ModelChoiceField for title and department?
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


class SearchTitlesForm(forms.ModelForm):
    title = forms.ModelChoiceField(queryset=Titles.objects.all(),
                                   required=False)

    class Meta:
        model = Titles
        fields = ['title']


class SearchDepartmentsForm(forms.ModelForm):
    dept_name = forms.ModelChoiceField(queryset=Departments.objects.all(),
                                       required=False,
                                       label="Department")

    class Meta:
        model = Departments
        fields = ['dept_name']


class SearchDeptManagerForm(forms.ModelForm):
    first_name = forms.CharField(required=False,
                                 label="Manager's first name")
    last_name = forms.CharField(required=False,
                                label="Manager's last name")

    class Meta:
        model = Employees
        fields = ['first_name',
                  'last_name']


class RegisterUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    botcatcher = forms.CharField(required=False,
                                 widget=forms.HiddenInput,
                                 validators=[validators.MaxLengthValidator(0)])

    class Meta:
        model = User
        fields = ['first_name',
                  'last_name',
                  'email',
                  'username',
                  'password']


class AddEmployeeForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=[("", ""),
                                        ("F", "Female"),
                                        ("M", "Male")])
    manager = forms.ModelChoiceField(queryset=Employees.objects
                                     .filter(title_id=1))
    botcatcher = forms.CharField(required=False,
                                 widget=forms.HiddenInput,
                                 validators=[validators.MaxLengthValidator(0)])

    class Meta:
        model = Employees
        fields = '__all__'
