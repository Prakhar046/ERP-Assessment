from rest_framework import serializers
from .models import Department, Employee, Project


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'



class EmployeeSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Employee
        fields = ('id', 'username', 'email', 'password', 'department', 'salary', 'role')

    def validate(self, attrs):
        request = self.context.get('request')

        # If creating (POST), password must be provided
        if self.instance is None and 'password' not in attrs:
            raise serializers.ValidationError({"password": "Password is required for creating a user."})

        # Manager department validation as before
        if request and request.user.role == 'Manager':
            employee = self.instance  # Existing user object during update
            # Use provided department or existing one on update
            employee_department = attrs.get('department', employee.department if employee else None)
            manager_department = request.user.department

            if employee_department != manager_department:
                raise serializers.ValidationError({
                    "department": "Managers can only assign employees to their own department."
                })

            # Prevent managers from assigning Admin role
            role = attrs.get('role', employee.role if employee else None)
            if role == 'Admin':
                    raise serializers.ValidationError(
                    {'role': 'Managers cannot assign Admin role.'}
                )
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Employee(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)  # Only update password if provided
        instance.save()
        return instance

    
    
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
