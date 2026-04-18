from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_title = "Formatura Micaelle"
admin.site.site_header = "✦ Formatura Micaelle Menezes Moreira"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('formatura.core.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
