from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.urls import reverse
from django.utils.timezone import now
from django.views.generic import ListView, DeleteView
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Category, Product
from .forms import CategoryForm, ProductForm


def category_list(request):
    categories = Category.objects.all()  # Получение всех категорий
    time = now().strftime("%Y%m%d%H%M%S")
    return render(request, 'products/category_list.html', {'categories': categories, 'timestamp': time})


def product_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)  # Получение категории
    products = Product.objects.filter(category=category)  # Товары в категории
    return render(request, 'products/product_list.html', {'category': category, 'products': products})


@login_required
def create_category(request):
    error = ''
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save()
            return redirect('product_list', category_id=category.id)
        else:
            error = 'Error in text'

    form = CategoryForm()

    data = {
        'form': form,
        'error': error
    }

    return render(request, 'products/create_category.html', data)


@login_required
def create_product(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    error = ''
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.category = category
            product.save()
            messages.success(request, 'Product added successfully!')
            return redirect('create_product', category_id=category.id)
        else:
            error = 'Error in text'

    form = ProductForm()

    data = {
        'form': form,
        'error': error,
        'category': category
    }

    return render(request, 'products/create_product.html', data)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'products/update_product.html'

    form_class = ProductForm

    pk_url_kwarg = 'custom_id'

    def get_object(self, queryset=None):
        return get_object_or_404(Product, custom_id=self.kwargs['custom_id'])

    def form_valid(self, form):
        messages.success(self.request, 'Product updated successfully!')
        search_query = self.request.GET.get('q', '')
        if search_query:
            form.save()
            # Если параметр 'q' существует, перенаправляем на страницу поиска
            return redirect(f'/home/search/?q={search_query}')
        else:
            return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'products/delete_product.html'
    success_url = '/home'
    pk_url_kwarg = 'custom_id'

    def get_object(self, queryset=None):
        try:
            category = get_object_or_404(Category, id=self.kwargs['category_id'])
            self.category = category
        except Exception:
            pass
        return get_object_or_404(Product, custom_id=self.kwargs['custom_id'])

    def get_success_url(self):
        search_query = self.request.GET.get('q', '')
        if search_query:
            return f'/home/search/?q={search_query}'
        else:
            return reverse('product_list', kwargs={'category_id': self.category.id})

    def form_valid(self, form):
        messages.success(self.request, 'Product deleted successfully!')
        return super().form_valid(form)


class Search(ListView):
    template_name = 'products/search_list.html'
    context_object_name = 'products'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query) | Q(custom_id__icontains=query)
        ) if query else []
        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        return context
