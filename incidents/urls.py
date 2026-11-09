
from django.urls import path
from . import views

urlpatterns = [
    path('', views.submit_incident, name='submit_incident'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path(
        'incident/<int:incident_id>/',
        views.incident_detail,
        name='incident_detail'
    ),
]
