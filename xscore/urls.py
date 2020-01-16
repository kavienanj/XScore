from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('handlehere/', admin.site.urls),
    path('paper/', include('exampaper.urls')),
    path('accounts/', include('user.urls')),
    path('', lambda request: render(request, 'index.html'), name='welcome'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
