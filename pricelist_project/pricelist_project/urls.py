from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('home/', include('products.urls')),
    path('members/', include('django.contrib.auth.urls')),
    path('members/', include('members.urls')),
]

if settings.DEBUG:  # Только для режима разработки
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.http import JsonResponse

def debug_headers(request):
    # Ограничьте вывод только необходимыми заголовками
    headers = {
        'HTTP_HOST': request.META.get('HTTP_HOST'),
        'HTTP_X_FORWARDED_PROTO': request.META.get('HTTP_X_FORWARDED_PROTO'),
        'REMOTE_ADDR': request.META.get('REMOTE_ADDR'),
    }
    return JsonResponse(headers)

urlpatterns += [
    path('debug_headers/', debug_headers),
]
