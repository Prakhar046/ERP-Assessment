from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser, Group, Permission


class EmployeeManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'Admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('role') != 'Admin':
            raise ValueError('Superuser must have role=Admin.')

        return self.create_user(username, email, password, **extra_fields)


class Department(models.Model):
    name = models.CharField(max_length=255)
    budget = models.FloatField(default=0)



class Employee(AbstractUser):
    
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='employees', null=True, blank=True)
    salary = models.FloatField(default=0)
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Manager', 'Manager'),
        ('Employee', 'Employee')
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    groups = models.ManyToManyField(
        Group,
        related_name='employee_set',  
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
        related_query_name='employee'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='employee_set',  
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
        related_query_name='employee'
    )
    
    objects = EmployeeManager()

    def __str__(self):
        return self.username



class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    employees = models.ManyToManyField(Employee, related_name='projects')
