from django.urls import path
from . import views

urlpatterns = [

    # Display Routes
    path('', views.index),
    path('dashboard', views.display_dashboard),
    # path('edit/<int:id>', views.update_trip),
    path('new', views.display_make_new_trip),
    # path('detail/<int:id>', views.trip_detail),
    path('my_trips', views.display_my_trips),
    path('new_trail', views.display_make_new_trail),

    # Action Routes
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),

    # path('remove/<int:id>', views.remove),
    # path('update/<int:id>', views.update),
    path('create', views.create),
    path('create_trail', views.create_trail),
    # path('cancel/<int:id>', views.cancel),
    # path('join/<int:id>', views.join),

]