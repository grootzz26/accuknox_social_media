from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("user/v1/", include("apps.user_app.urls")),
    path("connect/v1/", include("apps.friends.urls")),
]
