from django.urls import path
from ERP import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('departments/', views.DepartmentListCreate.as_view(), name='department-list-create'),
    path('departments/<int:pk>/', views.DepartmentRetrieveUpdateDestroy.as_view(), name='department-detail'),
    path('employees/', views.EmployeeList.as_view(), name='employee-list'),
    path('employees/<int:pk>/', views.EmployeeDetail.as_view(), name='employee-detail'),
    path('projects/', views.ProjectListCreate.as_view(), name='project-list-create'),
    path('projects/<int:pk>/', views.ProjectRetrieveUpdateDestroy.as_view(), name='project-detail'),
    path('reports/employees-by-department/', views.EmployeesByDepartment.as_view(), name='report-employees-by-department'),
    path('reports/salary-cost-per-department/', views.DepartmentSalaryCost.as_view(), name='report-salary-cost'),
    path('reports/active-projects/', views.ActiveProjects.as_view(), name='report-active-projects'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
