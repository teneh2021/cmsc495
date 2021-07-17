from django.urls import path
from django.urls.conf import include
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from . import views

app_name = 'WeightTrackers'

urlpatterns = [
    path('generate_pdf', views.generate_pdf, name ='generate_pdf'),
    path('test', views.test, name='test'),

    path('', views.welcome, name='welcome'),
    path('book/', views.WeightCreateView.as_view(), name='book'),
    path('book2/', views.AddActivityView.as_view(), name='book2'),
    path('home/', views.user_home, name='home'),
    path('user_settings', views.user_settings, name= 'user_settings'),
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('welcome/', views.welcome, name="welcome"),
    path('target/', views.target, name="target"),
    path('bmi/', views.bmi, name="bmi"),
    path('editProfile/', views.editProfile, name="profile"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path("favicon.ico", RedirectView.as_view(
        url=staticfiles_storage.url("favicon.ico")), ),
]


