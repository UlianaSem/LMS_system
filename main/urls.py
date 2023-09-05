from django.urls import path
from main.views import StudentListView, contacts, StudentDetailView, StudentCraeteView, StudentUpdateView, StudentDeleteView, toggle_activity
from main.apps import MainConfig

app_name = MainConfig.name

urlpatterns = [
    path('', StudentListView.as_view(), name='home'),
    path('contacts/', contacts, name='contacts'),
    path('student/<int:pk>/', StudentDetailView.as_view(), name='student_view'),
    path('create/', StudentCraeteView.as_view(), name='create_student'),
    path('edit/<int:pk>/', StudentUpdateView.as_view(), name='update_student'),
    path('delete/<int:pk>/', StudentDeleteView.as_view(), name='delete_student'),
    path('activity/<int:pk>/', toggle_activity, name='toggle_activity'),
]