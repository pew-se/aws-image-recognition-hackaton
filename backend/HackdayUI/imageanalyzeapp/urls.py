from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from . import views
from django.views.static import serve
urlpatterns = [
    path('upload', views.upload, name='upload'),
    path('<int:id>/', views.detail, name='detail'),
    path('', views.index, name='index'),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]