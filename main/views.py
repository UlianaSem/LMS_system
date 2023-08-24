from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse

from main.models import Student
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


class StudentListView(ListView):
    model = Student


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')

        print(f'Свяжитесь с {name} {email}')

    context = {
        'object_list': Student.objects.all(),
        'title': "Наши контакты"
    }
    return render(request, 'main/contacts.html', context)


class StudentDetailView(DetailView):
    model = Student


class StudentCraeteView(CreateView):
    model = Student
    fields = ('first_name', 'last_name', 'profile_photo',)
    success_url = reverse_lazy('main:home')


class StudentUpdateView(UpdateView):
    model = Student
    fields = ('first_name', 'last_name', 'profile_photo',)
    success_url = reverse_lazy('main:home')


class StudentDeleteView(DeleteView):
    model = Student
    success_url = reverse_lazy('main:home')


def toggle_activity(request, pk):
    student_item = get_object_or_404(Student, pk=pk)

    if student_item.is_active:
        student_item.is_active = False
    else:
        student_item.is_active = True

    student_item.save()

    return redirect(reverse('main:home'))
