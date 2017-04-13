from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()

from app import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register/', views.registerUser, name='register'),
    url(r'^login/', views.loginUser, name='login'),
    url(r'^home/', views.home, name='home'),
    url(r'^scanIPRange/', views.scanIPRange, name='ping'),
]
