from django.urls import path
from . import views

app_name = 'employee_search'
urlpatterns = [
    path('', views.index_view, name='index_view'),
    path('search/', views.query_form, name='query_form'),
    path('results/', views.query_form, name='query_results'),
    path('registration/', views.registration, name='registration'),
    path('add/', views.add_employee, name='add_employee')
]
