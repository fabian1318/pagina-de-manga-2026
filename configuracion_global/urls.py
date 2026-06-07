from django.contrib import admin
from django.urls import path, include
from django.conf import settings             
from django.conf.urls.static import static   
from biblioteca import views as biblioteca_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/', include('django.contrib.auth.urls')),
    path('', biblioteca_views.inicio, name='inicio'),
    path('manga/<int:manga_id>/', biblioteca_views.detalle_manga, name='detalle_manga'),
    path('leer/<int:capitulo_id>/', biblioteca_views.leer_capitulo, name='leer_capitulo'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

