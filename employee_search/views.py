from django.shortcuts import render
from employee_search.models import Employees
from employee_search.forms import (SearchEmployeesForm,
                                   SearchTitlesForm,
                                   SearchDepartmentsForm,
                                   SearchDeptManagerForm,
                                   AddEmployeeForm,
                                   RegisterUserForm)
from django.views.generic import (TemplateView,
                                  ListView,
                                  CreateView,
                                  DetailView,
                                  UpdateView,
                                  DeleteView)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class IndexView(TemplateView):
    template_name = 'employee_search/index.html'


class RegistrationView(CreateView):
    form_class = RegisterUserForm
    success_url = reverse_lazy('login')
    template_name = 'employee_search/registration.html'

    def form_valid(self, form):
        user = form.save()
        user.set_password(user.password)
        user.save()
        # TODO: double-check if this return is correct
        return super().form_valid(form)
    # TODO: get_context_data to override context name 'form'?


class AddEmployeeView(LoginRequiredMixin, CreateView):
    form_class = AddEmployeeForm
    success_url = reverse_lazy('employee_search:query_form')
    template_name = 'employee_search/employee-add.html'
    # TODO: get_context_data to override context name 'form'?


class EmployeeDetailsView(LoginRequiredMixin, DetailView):
    model = Employees
    context_object_name = 'emp_details'
    template_name = 'employee_search/employee-details.html'
    # TODO: add related fields; maybe a query with select_related?


class EmployeeUpdateView(LoginRequiredMixin, UpdateView):
    model = Employees
    form_class = AddEmployeeForm
    template_name = 'employee_search/employee-update.html'
    # TODO: get_context_data to override context name 'form'?


class EmployeeDeleteView(DeleteView):
    model = Employees
    context_object_name = 'employee'
    success_url = reverse_lazy('employee_search:query_form')
    template_name = 'employee_search/employee-delete.html'


@login_required
def query_form(request):
    welcome_msg = True
    employees_form = SearchEmployeesForm()
    titles_form = SearchTitlesForm()
    departments_form = SearchDepartmentsForm()
    # used prefix to diferentiate field values from outside the employees form
    dept_manager_form = SearchDeptManagerForm(prefix='manager_')
    if request.method == "POST":
        welcome_msg = False
        employees_form = SearchEmployeesForm(request.POST)
        titles_form = SearchTitlesForm(request.POST)
        departments_form = SearchDepartmentsForm(request.POST)
        dept_manager_form = SearchDeptManagerForm(request.POST,
                                                  prefix='manager_')

        if employees_form.is_valid() and \
           titles_form.is_valid() and \
           departments_form.is_valid() and \
           dept_manager_form.is_valid():

            # ignored line lenght limit for readability (lines 91-104)
            # TODO: prioritize Django style over PEP8, apply to all files
            # TODO: maybe loop through cleaned forms to create this dict?
            test_filters = {
                'first_name__iexact': employees_form.cleaned_data.get('first_name'),
                'last_name__iexact': employees_form.cleaned_data.get('last_name'),
                'gender': employees_form.cleaned_data.get('gender'),
                'birth_date': employees_form.cleaned_data.get('birth_date'),
                'hire_date': employees_form.cleaned_data.get('hire_date'),
                'salary': employees_form.cleaned_data.get('salary'),
                'title_id__title': titles_form.cleaned_data.get('title'),
                'department_id__dept_name': departments_form.cleaned_data.get('dept_name'),
                'manager_id__first_name__iexact': dept_manager_form.cleaned_data.get('first_name'),
                'manager_id__last_name__iexact': dept_manager_form.cleaned_data.get('last_name')
            }

            # exclude empty form fields
            test_filters_used = {key: val for key, val in test_filters.items() if val}

            # query the database
            employees_queryset = Employees.objects \
                .filter(**test_filters_used) \
                .values(
                    'id',
                    'first_name',
                    'last_name',
                    'gender',
                    'birth_date',
                    'hire_date',
                    'salary',
                    'title_id__title',
                    'department_id__dept_name',
                    'manager_id__first_name',
                    'manager_id__last_name') \
                .order_by('first_name',
                          'last_name')

            results_count = employees_queryset.count()

            return render(request,
                          'employee_search/results.html',
                          {'employees_form': employees_form,
                           'titles_form': titles_form,
                           'departments_form': departments_form,
                           'dept_manager_form': dept_manager_form,
                           'results': employees_queryset,
                           'results_count': results_count,
                           'welcome_msg': welcome_msg})
        else:
            print('FORM INVALID')
    return render(request,
                  'employee_search/results.html',
                  {'employees_form': employees_form,
                   'titles_form': titles_form,
                   'departments_form': departments_form,
                   'dept_manager_form': dept_manager_form,
                   'welcome_msg': welcome_msg})
