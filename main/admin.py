from django.contrib import admin

from main.models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name']
    list_filter = ['is_active']
    search_fields = ['first_name', 'last_name']
