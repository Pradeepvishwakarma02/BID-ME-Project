from django.urls import path

from . import views

urlpatterns = [
    path('', views.adminhome),
    path('manageusers/', views.manageusers),
    path('manageuserstatus/', views.manageuserstatus),
    path('cpadmin/', views.cpadmin),
    path('epadmin/', views.epadmin),
    path('addcategory/', views.addcategory),
    path('addsubcategory/', views.addsubcategory)
]