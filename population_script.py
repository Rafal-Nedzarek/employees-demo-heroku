import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employees_demo_heroku.settings')

import django
django.setup()

from faker import Faker
from employee_search.models import Titles, Departments, Employees, Dept_Manager
import random

def generate_emp(sal_min, sal_max, title_fk, dept_fk):
    fake = Faker()
    gend = random.choice(['F','M'])
    if gend == 'F':
        fname = fake.first_name_female()
    else:
        fname = fake.first_name_male()
    emp = Employees(first_name=fname,
                    last_name=fake.last_name(),
                    gender=gend,
                    birth_date=fake.date_of_birth(minimum_age=35, maximum_age=65),
                    hire_date=fake.date_between(start_date='-10y'),
                    salary=random.randint(sal_min, sal_max),
                    title = Titles.objects.get(id=title_fk),
                    department = Departments.objects.get(id=dept_fk))
    emp.save()


Titles.objects.get_or_create(title='Manager')
Titles.objects.get_or_create(title='Team Lead')
Titles.objects.get_or_create(title='Senior Developer')
Titles.objects.get_or_create(title='Developer')
Titles.objects.get_or_create(title='Junior Developer')
Titles.objects.get_or_create(title='Senior Specialist')
Titles.objects.get_or_create(title='Specialist')
Titles.objects.get_or_create(title='Junior Specialist')



Departments.objects.get_or_create(dept_name='Development')
Departments.objects.get_or_create(dept_name='Customer Service')
Departments.objects.get_or_create(dept_name='Human Resources')
Departments.objects.get_or_create(dept_name='Marketing')
Departments.objects.get_or_create(dept_name='Finance')
Departments.objects.get_or_create(dept_name='Legal')


generate_emp(70000,75000,1,1)
for i in range(3):
    generate_emp(60000,65000,2,1)
for i in range(15):
    generate_emp(50000,55000,3,1)
for i in range(30):
    generate_emp(40000,45000,4,1)
for i in range(45):
    generate_emp(30000,35000,5,1)

generate_emp(60000,65000,1,2)
for i in range(4):
    generate_emp(50000,55000,2,2)
for i in range(20):
    generate_emp(40000,45000,6,2)
for i in range(40):
    generate_emp(30000,35000,7,2)
for i in range(60):
    generate_emp(20000,25000,8,2)

generate_emp(60000,65000,1,3)
for i in range(1):
    generate_emp(50000,55000,2,3)
for i in range(2):
    generate_emp(40000,45000,6,3)
for i in range(3):
    generate_emp(30000,35000,7,3)
for i in range(4):
    generate_emp(20000,25000,8,3)

generate_emp(60000,65000,1,4)
for i in range(2):
    generate_emp(50000,55000,2,4)
for i in range(10):
    generate_emp(40000,45000,6,4)
for i in range(20):
    generate_emp(30000,35000,7,4)
for i in range(30):
    generate_emp(20000,25000,8,4)

generate_emp(65000,70000,1,5)
for i in range(2):
    generate_emp(55000,60000,2,5)
for i in range(10):
    generate_emp(45000,50000,6,5)
for i in range(20):
    generate_emp(35000,40000,7,5)
for i in range(30):
    generate_emp(25000,30000,8,5)

generate_emp(65000,70000,1,6)
for i in range(2):
    generate_emp(55000,60000,2,6)
for i in range(10):
    generate_emp(45000,50000,6,6)
for i in range(20):
    generate_emp(35000,40000,7,6)
for i in range(30):
    generate_emp(25000,30000,8,6)