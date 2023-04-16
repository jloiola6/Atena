from django.conf.urls import handler404, handler500, handler403, handler400
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views


handler404 = views.handler404
handler500 = views.handler500


urlpatterns = [
    path('', include('aplicacoes.core.urls')),
    path('administracao/', include('aplicacoes.administracao.urls')),
    path('api/', include('aplicacoes.api.urls')),
    path('usuario/', include('aplicacoes.usuario.urls')),
    path('tecnologia/', include('aplicacoes.tecnologia.urls')),
    path('dinem/', include('aplicacoes.dinem.urls')),
    path('atena/', include('aplicacoes.atena.urls')),
    path('lotacao/', include('aplicacoes.lotacao.urls')),
    path('terceirizacao/', include('aplicacoes.terceirizacao.urls')),
    path('fundiaria/', include('aplicacoes.fundiaria.urls')),
    path('coex/', include('aplicacoes.coex.urls')),
    path('contas/', include('aplicacoes.contas.urls')),
    path('dashboard/', include('aplicacoes.dashboard.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)