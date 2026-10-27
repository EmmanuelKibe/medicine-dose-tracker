from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.medicine_list, name='medicine_list'),
    path('edit/<int:pk>/', views.medicine_update, name='medicine_update'),
    path('delete/<int:pk>/', views.medicine_delete, name='medicine_delete'),
]