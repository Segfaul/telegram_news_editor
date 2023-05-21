from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from news_editor import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('posts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = 'posts.views.tr_handler403'
handler404 = 'posts.views.tr_handler404'
handler405 = 'posts.views.tr_handler405'
handler500 = 'posts.views.tr_handler500'
