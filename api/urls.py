from django.urls import path, re_path
from . import views

urlpatterns = [ 
    path('create/account', views.createAccount, name='api.createAccount'),
    path('redirect/', views.redirect, name='api.redirect'),
    path('history/<str:id>', views.history, name='api.history'),
    path('order/<str:id>', views.order, name='api.order'),
] 