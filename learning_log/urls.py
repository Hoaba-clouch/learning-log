# learning_log/urls.py

"""learning_log URL Configuration
... (phần chú thích)
"""
from django.urls import include, path 
from django.contrib import admin

# XÓA BỎ DÒNG from . import views Ở ĐÂY HOÀN TOÀN

app_name = 'learning_log'
app_name = 'users' # Đệ đoán dòng này cũng thừa, chỉ cần app_name ở ứng dụng con

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', include('learning_logs.urls')),
]