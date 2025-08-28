from rest_framework import generics, permissions, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from .models import Department, Employee, Project
from .serializers import DepartmentSerializer, EmployeeSerializer, ProjectSerializer
from rest_framework import status
from .permissions import IsAdminManagerEmployeePermission
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny

# CRUD for Department
class DepartmentListCreate(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAdminManagerEmployeePermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class DepartmentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAdminManagerEmployeePermission]



 # CRUD for Employee
class EmployeeDetail(APIView):
    permission_classes = [IsAdminManagerEmployeePermission]

    def get(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        self.check_object_permissions(request, employee)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    def put(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        self.check_object_permissions(request, employee)
        serializer = EmployeeSerializer(employee, data=request.data)
        serializer.context['request'] = request
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        self.check_object_permissions(request, employee)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class EmployeeList(APIView):
    permission_classes = [IsAdminManagerEmployeePermission]

    def get(self, request):
        user = request.user
        if user.role == 'Admin':
            employees = Employee.objects.all()
        elif user.role == 'Manager':
            employees = Employee.objects.filter(department=user.department)
        else:  # Employee role can only see self
            employees = Employee.objects.filter(pk=user.pk)
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        serializer.context['request'] = request
        if serializer.is_valid():
            # Manager cannot assign Admin role checked in serializer validation
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# CRUD for Project
class ProjectListCreate(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminManagerEmployeePermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

class ProjectRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminManagerEmployeePermission]

# Report: Employees by department
class EmployeesByDepartment(APIView):
    permission_classes = [IsAdminManagerEmployeePermission]

    def get(self, request):
        result = {}
        for dept in Department.objects.all():
            employees = Employee.objects.filter(department=dept)
            result[dept.name] = EmployeeSerializer(employees, many=True).data
        return Response(result)

# Report: Salary cost per department
class DepartmentSalaryCost(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        cost = Department.objects.annotate(total_salary=Sum('employees__salary')).values('name', 'total_salary')
        return Response(cost)

# Report: Active Projects List
class ActiveProjects(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        active = Project.objects.filter(is_active=True)
        return Response(ProjectSerializer(active, many=True).data)




