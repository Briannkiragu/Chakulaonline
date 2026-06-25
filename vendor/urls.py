from django.urls import path
from . import views



urlpatterns = [
    path('', views.vendorDashboard, name='vendor'),
    path('profile/', views.vprofile, name='vprofile'),
]

