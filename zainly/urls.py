from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
# from dashboard.views import error_404_view, error_500_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('social-auth/', include('social_django.urls',namespace='social')),
    # path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('', include('home.urls')),
    path('', include('dashboard.urls')),
]
if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
