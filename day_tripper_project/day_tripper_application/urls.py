from django.urls import path
from . import views

urlpatterns = [

    # Display Routes
    path('', views.index),
    path('success', views.success),

    # Action Routes
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
]