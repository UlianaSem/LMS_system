from django.shortcuts import render
from main.models import Student


def home(request):
    context = {
        'object_list': Student.objects.all(),
        'title': "Главная"
    }
    return render(request, 'main/index.html', context)


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

