# learning_logs/urls.py

"""Defines URL patterns for learning_logs."""
# CHỈ IMPORT 'path' VÀ TỪ 'django.urls'
from django.urls import path 
from . import views

app_name = 'learning_logs'

urlpatterns = [
    # Trang chủ (Homepage) - url(r'^$', views.index, name='index')
    path('', views.index, name='index'),
    
    # Show all topics. - url(r'^topics/$', views.topics, name='topics')
    path('topics/', views.topics, name='topics'),

    # Detail page for a single topic - Cú pháp mới dùng <int:topic_id> thay cho regex
    # url(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic')
    path('topics/<int:topic_id>/', views.topic, name='topic'),

    # Page for adding a new topic - url(r'^new_topic/$', views.new_topic, name='new_topic')
    path('new_topic/', views.new_topic, name='new_topic'),

    # Page for adding a new entry - Cú pháp mới dùng <int:topic_id>
    # url(r'^new_entry/(?P<topic_id>\d+)/$', views.new_entry, name='new_entry')
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),

    # Page for editing an entry - Cú pháp mới dùng <int:entry_id>
    # url(r'^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry, name='edit_entry')
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
]