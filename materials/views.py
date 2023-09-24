from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from materials.models import Materials
from django.urls import reverse_lazy, reverse
from pytils.translit import slugify


class MaterialsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Materials
    permission_required = 'materials.add_materials'
    fields = ('title', 'body', )
    success_url = reverse_lazy('materials:list')
    extra_context = {
        'title': "Добавление учебного материала"
    }

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)


class MaterialsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Materials
    fields = ('title', 'body', )
    success_url = reverse_lazy('materials:list')
    permission_required = 'materials:change_materials'
    extra_context = {
        'title': "Обновление учебного материала"
    }

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            print(new_mat.title)
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('materials:view', args=[self.kwargs.get('pk')])


class MaterialsListView(LoginRequiredMixin, ListView):
    model = Materials
    extra_context = {
        'title': "Учебный материал"
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class MaterialsDetailView(LoginRequiredMixin, DetailView):
    model = Materials
    extra_context = {
        'title': "Просмотр материала"
    }

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class MaterialsDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Materials
    success_url = reverse_lazy('materials:list')
    permission_required = 'materials:delete_materials'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = f'Удаление материала {self.object.title}'

        return context_data
