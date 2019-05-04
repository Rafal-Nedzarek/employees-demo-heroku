from django.urls import path
from . import views

app_name = 'employee_search'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index_view'),
    path('search/', views.query_form, name='query_form'),
    path('results/', views.query_form, name='query_results'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('add/', views.AddEmployeeView.as_view(), name='add_employee'),
    path('search/<int:pk>', views.EmployeeDetailsView.as_view(), name='emp_details'),
    path('search/<int:pk>/update', views.EmployeeUpdateView.as_view(), name='emp_update'),
    path('search/<int:pk>/delete', views.EmployeeDeleteView.as_view(), name='emp_delete'),
]
