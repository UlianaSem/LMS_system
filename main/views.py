from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse

from main.forms import StudentForm, SubjectForm
from main.models import Student, Subject
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from main.services import get_cached_subjects_for_student


class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    extra_context = {
        'title': "Список студентов"
    }


@login_required
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


class StudentDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Student
    permission_required = 'main.view_student'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['subjects'] = get_cached_subjects_for_student(self.object.pk)

        context_data['title'] = f'Студент {self.object.first_name} {self.object.last_name}'

        return context_data


class StudentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    permission_required = 'main.add_student'
    success_url = reverse_lazy('main:home')
    extra_context = {
        'title': "Добавление студента"
    }


class StudentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Student
    permission_required = 'main.change_student'
    form_class = StudentForm
    extra_context = {
        'title': "Изменение информации о студенте"
    }

    def get_success_url(self):
        return reverse('main:update_student', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        SubjectFormset = inlineformset_factory(Student, Subject, form=SubjectForm, extra=1)

        if self.request.method == 'POST':
            formset = SubjectFormset(self.request.POST, instance=self.object)
        else:
            formset = SubjectFormset(instance=self.object)

        context_data['formset'] = formset

        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        print(context_data)
        formset = context_data['formset']
        self.object = form.save()
        
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        
        return super().form_valid(form)


class StudentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Student
    success_url = reverse_lazy('main:home')

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = f'Удаление студента {self.object.first_name} {self.object.last_name}'

        return context_data


@login_required
@permission_required(perm='main:change_student', login_url='main:home')
def toggle_activity(request, pk):
    student_item = get_object_or_404(Student, pk=pk)

    if student_item.is_active:
        student_item.is_active = False
    else:
        student_item.is_active = True

    student_item.save()

    return redirect(reverse('main:home'))
