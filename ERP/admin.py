from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

admin.site.register(Employee, UserAdmin)



class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'budget')
    search_fields = ('name',)

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    search_fields = ('name',)

admin.site.register(Department, DepartmentAdmin)
admin.site.register(Project, ProjectAdmin)
