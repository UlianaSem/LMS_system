from django.contrib import admin

from main.models import Student, Subject


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['pk', 'first_name', 'last_name']
    list_filter = ['is_active']
    search_fields = ['first_name', 'last_name']


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'description', 'student']
    list_filter = ['student']
    search_fields = ['title', 'description']
