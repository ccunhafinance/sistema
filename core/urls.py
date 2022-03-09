from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myauth.urls', namespace="login")),
    path('dashboard/', include('dashboard.urls', namespace="dashboard")),
    path('ofertas/', include('offers.urls', namespace="offers")),
    path('clientes/', include('clients.urls', namespace="clients")),
    path('mail/', include('mail.urls', namespace="mail")),
    path('chat/', include('chat.urls', namespace="chat")),
    path('assessores/', include('assessores.urls', namespace="assessores")),
    path('usuarios/', include('users.urls', namespace="users")),
    path('ajax/', include('ajax.urls', namespace="ajax")),
    path('summernote/', include('django_summernote.urls')),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)