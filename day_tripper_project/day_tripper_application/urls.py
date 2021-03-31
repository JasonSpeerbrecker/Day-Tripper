from django.urls import path
from . import views

urlpatterns = [

    # Display Routes
    path('', views.index),
    path('dashboard', views.display_dashboard),
    path('trip/new', views.display_make_new_trip),
    # path('trip/detail/<int:id>', views.trip_detail),
    path('trip/my_trips', views.display_my_trips),
    path('trip/update/<int:id>', views.display_update_trip),
    path('trail/detail/<int:id>', views.display_trail_details),
    

    # Action Routes
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    # path('remove/<int:id>', views.remove),
    path('update/<int:id>', views.update_trip),
    path('create', views.create),
    # path('cancel/<int:id>', views.cancel),
    # path('join/<int:id>', views.join),

    ######## Admin Routes #########
    # path('edit/<int:id>', views.update_trail),
    path('new_trail', views.display_make_new_trail),
    path('create_trail', views.create_trail),

]