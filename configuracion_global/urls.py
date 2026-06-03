from django.contrib import admin
from django.urls import path, include
from django.conf import settings             # <-- Nueva importación
from django.conf.urls.static import static   # <-- Nueva importación
from biblioteca import views as biblioteca_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/', include('django.contrib.auth.urls')),
    path('', biblioteca_views.inicio, name='inicio'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)