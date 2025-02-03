from django.shortcuts import render
from .models import Category


def main_page(request):
    categories = Category.objects.all()
    return render(request, 'products/index.html.html', {'categories': categories})
