from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home-page'),
    path('comments', views.comments, name='response'),
    path('about.html', views.about, name='aboutus'),
    path('homepage.html', views.homepage, name='home-page'),
    path('login.html', views.login, name='login-page'),
    path('adminPage', views.visualization, name=''),
    path('getPlot3', views.getPlot3, name=''),
    path('getPlot1', views.getPlot1, name=''),
    path('getPlot2', views.getPlot2, name=''),
    path('getPlot4', views.getPlot4, name=''),
]