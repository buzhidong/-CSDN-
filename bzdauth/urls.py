from django.urls import path
from . import views

app_name = 'bzdauth'
urlpatterns = [
    # path('', views.index, name='index'),
    path('login', views.bzdlogin, name='login'),
    path('logout', views.bzdlogout, name='logout'),
    path('register', views.register, name='register'),
    path('captcha', views.send_email_captcha, name='email_captcha'),
]
