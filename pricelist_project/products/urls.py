from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static

from .views import debug_headers

urlpatterns = [
    path('', views.category_list, name='category_list'),  # Список категорий
    path('category/<int:category_id>/', views.product_list, name='product_list'),  # Товары по категории
    path('search/', views.Search.as_view(), name='search'),
    path('create_category/', views.create_category, name='create_category'),
    path('category/<int:category_id>/create_product/', views.create_product, name='create_product'),
    path('category/<int:category_id>/product/<int:custom_id>/update/', views.ProductUpdateView.as_view(), name='product_update'),
    path('category/<int:category_id>/product/<int:custom_id>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),

    path('product/<int:custom_id>/update/', views.ProductUpdateView.as_view(), name='search_product_update'),
    path('product/<int:custom_id>/delete/', views.ProductDeleteView.as_view(), name='search_product_delete'),
    path("debug/", debug_headers),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)