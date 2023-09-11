from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from materials.models import Materials
from django.urls import reverse_lazy, reverse
from pytils.translit import slugify


class MaterialsCreateView(LoginRequiredMixin, CreateView):
    model = Materials
    fields = ('title', 'body', )
    success_url = reverse_lazy('materials:list')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)


class MaterialsUpdateView(LoginRequiredMixin, UpdateView):
    model = Materials
    fields = ('title', 'body', )
    success_url = reverse_lazy('materials:list')

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

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class MaterialsDetailView(LoginRequiredMixin, DetailView):
    model = Materials

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class MaterialsDeleteView(LoginRequiredMixin, DeleteView):
    model = Materials
    success_url = reverse_lazy('materials:list')
