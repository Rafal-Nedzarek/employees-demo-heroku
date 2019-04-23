# Generated by Django 2.2 on 2019-04-22 22:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('employee_search', '0001_initial'), ('employee_search', '0002_auto_20190422_2152'), ('employee_search', '0003_auto_20190422_2325')]

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Departments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dept_name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'departments',
            },
        ),
        migrations.CreateModel(
            name='Titles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'titles',
            },
        ),
        migrations.CreateModel(
            name='Employees',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=25)),
                ('last_name', models.CharField(max_length=25)),
                ('gender', models.CharField(max_length=1)),
                ('birth_date', models.DateField()),
                ('hire_date', models.DateField()),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='employee_search.Departments')),
                ('salary', models.IntegerField()),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='employee_search.Titles')),
            ],
            options={
                'db_table': 'employees',
            },
        ),
        migrations.CreateModel(
            name='Dept_Manager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='employee_search.Departments')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='employee_search.Employees')),
            ],
            options={
                'db_table': 'dept_manager',
            },
        ),
    ]