from django.shortcuts import render
from .models import Asset
def about(request):
    context_data = {
        'page_title': 'О проекте',
        #'assets': fake_database, # Передаем весь список
    }
    return render(request, 'gallery/about.html', context_data) 

def home(request):
# Имитация данных из базы (список словарей)
    assets = Asset.objects.all()

    context_data = {
        'page_title': 'Главная Галерея',
        'assets': assets, # Передаем весь список
    }
    return render(request, 'gallery/index.html', context_data)