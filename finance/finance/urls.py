from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings

FRONTEND_DIR = settings.BASE_DIR.parent / 'frontend'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('my_app.urls')),

    # Serve Login Page at http://127.0.0.1:8000/
    path('', lambda request: serve(request, 'login.html', document_root=FRONTEND_DIR)),

    # Serve static assets (css, js, images) directly
    re_path(r'^(?P<path>.*)$', serve, {'document_root': FRONTEND_DIR}),
]