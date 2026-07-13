from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "Administration dashboard"
admin.site.index_title = "Welcome to admin dashboard"

urlpatterns = [
    path('', RedirectView.as_view(url='/blog/', permanent=False)),
    path('admin/', admin.site.urls),

    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),

    # HTML Blog
    path('blog/', include('blog.urls')),

    # Polls
    path('polls/', include('polls.urls')),

    # REST API
    path('api/', include('blog.api_urls')),

    # DRF Login/Logout
    path("api-auth/", include("rest_framework.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)