# -*- encoding: utf-8 -*-


from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    # Chacking PODs
    path('get_pod_status/<int:pod_id>/', views.get_pod_status, name='get_pod_status'),
    path('get_pod_events/<int:pod_id>/', views.get_pod_events, name='get_pod_events'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]

import apps.home.startup as startup

startup.event_listener()
