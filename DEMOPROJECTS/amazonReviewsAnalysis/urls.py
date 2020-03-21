from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home-page'),
    path('comments', views.comments, name='response'),
    path('about.html', views.about, name='aboutus'),
    path('homepage.html', views.homepage, name='home-page'),
    path('login.html', views.login, name='login-page'),
    #path('login/visualization', views.visualization, name=''),
    path('adminPage', views.visualization, name=''),
    path('getfigure', views.getfigure, name=''),
    #url(r'^getimg/$', views.getfigure2),
]