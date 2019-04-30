from django.shortcuts import render
from employee_search.forms import (SearchEmployeesForm,
                                   SearchTitlesForm,
                                   SearchDepartmentsForm,
                                   SearchDeptManagerForm,
                                   AddEmployeeForm,
                                   RegisterUserForm)
from employee_search.models import Employees
from django.contrib.auth.decorators import login_required

all_query_filters = ""


def get_form_filters(search_form,
                     rel_prefix):
    '''Gets cleaned data from a search_form and adds it to the filter list
    used by the construct_query function. Adds a rel_prefix for keys
    from models related to the main model, e.g. \'__salaries\'.'''
    global all_query_filters
    for key, val in search_form.cleaned_data.items():
        if val is not None and str(val) != "":
            if not (isinstance(val, int) or isinstance(val, float)):
                val = "'" + str(val) + "'"
            all_query_filters += f"{rel_prefix}{key}={val}, "


def construct_query(search_model,
                    form_filters,
                    display_vals,
                    order_by):
    '''Constructs and runs a query of the search_model,
    putting form_filters and add_criteria into the filter() method
    and display_vals into the values() method. Orders data by order_by.'''
    query_part_1 = f"{search_model}.objects.filter("
    query_part_2 = f"{form_filters}).values({display_vals})\
                   .order_by({order_by})"
    return eval(query_part_1 + query_part_2)

def index_view(request):
    return render(request,
                  'employee_search/index.html',
                  {})

@login_required
def query_form(request):
    global all_query_filters
    ROWS_LIMIT = 1000
    limit_warning = ""
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

            all_query_filters = ""

            # define values for display
            query_vals = "'first_name',\
                         'last_name',\
                         'gender',\
                         'birth_date',\
                         'hire_date',\
                         'salary',\
                         'title_id__title',\
                         'department_id__dept_name',\
                         'manager_id__first_name',\
                         'manager_id__last_name'"

            # get data from forms and append the all_query_filters
            get_form_filters(employees_form,
                             '')
            get_form_filters(titles_form,
                             'title_id__')
            get_form_filters(departments_form,
                             'department_id__')
            get_form_filters(dept_manager_form,
                             'manager_id__')

            # query the DB
            employees_queryset = construct_query('Employees',
                                                 all_query_filters,
                                                 query_vals,
                                                 "'first_name', 'last_name'")

            # if ROWS_LIMIT is exceeded, limit the results and pass a warning
            results_count = employees_queryset.count()
            if ROWS_LIMIT is not None and results_count > ROWS_LIMIT:
                employees_queryset = employees_queryset[:ROWS_LIMIT]
                limit_warning = f'The results have been limited to the first \
                                {ROWS_LIMIT} rows.'

            return render(request,
                          'employee_search/results.html',
                          {'employees_form': employees_form,
                           'titles_form': titles_form,
                           'departments_form': departments_form,
                           'dept_manager_form': dept_manager_form,
                           'results': employees_queryset,
                           'limit_warning': limit_warning,
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

def registration(request):
    registered = False
    registration_form = RegisterUserForm()
    if request.method == "POST":
        registration_form = RegisterUserForm(request.POST)

        if registration_form.is_valid():
            new_user = registration_form.save()
            new_user.set_password(new_user.password)
            new_user.save()
            registered = True
        else:
            print('FORM INVALID')
        
    return render(request,
                  'employee_search/registration.html',
                  {'registration_form': registration_form,
                   'registered': registered})

def add_employee(request):
    add_employee_form = AddEmployeeForm()
    if request.method == "POST":
        add_employee_form = AddEmployeeForm(request.POST)

        if add_employee_form.is_valid():
            new_employee = add_employee_form.save()
            new_employee.save()
        else:
            print('FORM INVALID')
    return render(request, 'employee_search/add-employee.html', {'add_employee_form': add_employee_form})