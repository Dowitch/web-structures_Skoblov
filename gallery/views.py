from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Asset
from .forms import AssetForm

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


def upload(request):
    if request.method == 'POST':
        form = AssetForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Файл загружен')
            return redirect('home')
    else:
        form = AssetForm()
    return render(request, 'gallery/upload.html', {'form': form})
