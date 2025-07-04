from django.urls import path , include

from . import views

urlpatterns = [
    path('', views.userhome),
    path('cpuser/', views.cpuser),
    path('epuser/', views.epuser),
    path('viewcategory/', views.viewcategory),
    path('viewsubcategory/', views.viewsubcategory),
    path('addproduct/', views.addproduct),
    path('viewproduct/', views.viewproduct),
    path('funds/', views.funds),
    path('payment/', views.payment),
    path('success/', views.success),
    path('cancel/', views.cancel),
    path('viewbiddingstatus/', views.viewbiddingstatus),
    path('bid/', views.bid),
    path('viewbid/', views.viewbid)
]
