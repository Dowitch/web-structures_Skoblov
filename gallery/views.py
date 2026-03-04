import base64
from django.core.files.base import ContentFile
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Asset
from .forms import AssetForm
from django.db.models import Q
from django.core.paginator import Paginator 
from django.contrib import messages 
def about(request):
    context_data = {
        'page_title': 'О проекте',
        #'assets': fake_database, # Передаем весь список
    }
    return render(request, 'gallery/about.html', context_data) 

def home(request):

    search_query = request.GET.get('q', '')
    ordering = request.GET.get('ordering', 'new')
    assets = Asset.objects.all()

    if search_query:
        assets = assets.filter(title__icontains=search_query)

    if ordering == 'old':
        assets = assets.order_by('created_at') # От старых к новым
    elif ordering == 'name':
        assets = assets.order_by('title') # По алфавиту
    else:
    # По умолчанию (new) - свежие сверху
        assets = assets.order_by('-created_at')
    # 5. Отдаем результат
    paginator = Paginator(assets, 8)
# Получаем номер страницы из URL (например, ?page=2)
    page_number = request.GET.get('page')
# Получаем конкретный кусочек данных (объект Page)
    page_obj = paginator.get_page(page_number)
    context_data = {
    'page_title': 'Главная Галерея',
    'page_obj': page_obj,
}
    return render(request, 'gallery/index.html', context_data)

def upload(request):
    if request.method == 'POST':
        form = AssetForm(request.POST, request.FILES)
        if form.is_valid():
            # 1. Создаем объект, но пока НЕ сохраняем в базу (commit=False)
            new_asset = form.save(commit=False)
            
            # 2. Обрабатываем картинку из скрытого поля
            image_data = request.POST.get('image_data') # Получаем строку Base64
            
            if image_data:
                # Формат строки: "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
                # Нам нужно отрезать заголовок "data:image/jpeg;base64,"
                format, imgstr = image_data.split(';base64,')
                ext = format.split('/')[-1] # получаем "jpeg"
                
                # Декодируем текст в байты
                data = base64.b64decode(imgstr)
                
                # Создаем имя файла (берем имя модели + .jpg)
                file_name = f"{new_asset.title}_thumb.{ext}"
                
                # Сохраняем байты в поле image
                # ContentFile превращает байты в объект, который понимает Django FileField
                new_asset.image.save(file_name, ContentFile(data), save=False)
            # 3. Финальное сохранение в БД
            new_asset.save()
            messages.success(request, f'Модель "{new_asset.title}" успешно загружена!')
            return redirect('home')
    else:
        form = AssetForm()
    return render(request, 'gallery/upload.html', {'form': form})