# users/urls.py

# PHẢI LÀ from django.urls import path, KHÔNG PHẢI url
from django.urls import path 

from . import views
# Các dòng import khác (nếu có)

app_name = 'users'

urlpatterns = [
    # TẤT CẢ PHẢI LÀ path()
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
]