"""djProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from os import name
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from WeightTrackers import views
from WeightTrackers.views import line_chart, line_chart_json

urlpatterns = [
    

    path('admin/', admin.site.urls),

    # user related paths
    path('generate_pdf', views.generate_pdf, name='generate_pdf'),
    path('chart', line_chart, name='line_chart'),
    path('chartJSON', line_chart_json, name='line_chart_json'),
    path('', views.welcome, name='welcome'),
    path('home/', views.user_home, name='home'),
    path('user_settings', views.user_settings, name= 'user_settings'),
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('welcome/', views.welcome, name="welcome"),
    path('target/', views.target, name="target"),
    path('bmi/', views.bmi, name="bmi"),
    path('profile/', views.editProfile, name="profile"),
 
    path('dashboard/', views.dashboard, name="dashboard"),
    path("favicon.ico", RedirectView.as_view(
        url=staticfiles_storage.url("favicon.ico")), ),
    path('WeightTrakcers/', include('WeightTrackers.urls')),
    path('WeightTrackers/', include('django.contrib.auth.urls')),
   
    
   
   
]

  
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
