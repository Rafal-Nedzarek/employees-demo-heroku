from django.urls import path
from . import views

app_name = 'employee_search'
urlpatterns = [
    path('', views.query_form, name='query_form'),
    path('results/', views.query_form, name='query_results'),
]
