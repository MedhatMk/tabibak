from django.urls import path

from .views import AppointMentCreateAPIView,send_contact

app_name = 'core'

urlpatterns = [
    path('create-appointment/',AppointMentCreateAPIView.as_view(),name='create_appointment'),
    path('contact/',send_contact,name='send_contact'),
]
