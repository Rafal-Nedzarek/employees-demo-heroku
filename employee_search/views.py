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


def get_form_filters(search_form,
                     rel_prefix):
    '''
    Gets cleaned data from a search_form and adds it to the filter list
    used by the construct_query function. Adds a rel_prefix for keys
    from models related to the main model, e.g. \'title_id__\'.
    '''
    query_filters = ""
    for key, val in search_form.cleaned_data.items():
        if val is not None and str(val) != "":
            if not (isinstance(val, int) or isinstance(val, float)):
                val = "'" + str(val) + "'"
                query_filters += f"{rel_prefix}{key}__iexact={val}, "
            else:
                query_filters += f"{rel_prefix}{key}={val}, "
    return query_filters


def construct_query(search_model,
                    form_filters,
                    display_vals,
                    order_by):
    '''
    Constructs and runs a query of the search_model,
    putting form_filters into the filter() method
    and display_vals into the values() method. Orders data by order_by.
    '''
    # TODO: use select_related? check len(connection.queries)
    query_string = f"{search_model}.objects.filter({form_filters})\
                   .values({display_vals}).order_by({order_by})"
    return eval(query_string)


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
            # get data from forms and append the all_query_filters
            all_query_filters = get_form_filters(employees_form,
                                                 '')
            all_query_filters += get_form_filters(titles_form,
                                                  'title_id__')
            all_query_filters += get_form_filters(departments_form,
                                                  'department_id__')
            all_query_filters += get_form_filters(dept_manager_form,
                                                  'manager_id__')

            # provide values to be displayed
            all_display_vals = "'id',\
                                'first_name',\
                                'last_name',\
                                'gender',\
                                'birth_date',\
                                'hire_date',\
                                'salary',\
                                'title_id__title',\
                                'department_id__dept_name',\
                                'manager_id__first_name',\
                                'manager_id__last_name'"

            # query the DB
            employees_queryset = construct_query('Employees',
                                                 all_query_filters,
                                                 all_display_vals,
                                                 "'first_name', 'last_name'")
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
