from django.urls import path
from .views import JoinWaitlistView, WaitlistStatusView

app_name = 'waitlist'
urlpatterns = [
    path('join/', JoinWaitlistView.as_view(), name='join'),
    path('status/', WaitlistStatusView.as_view(), name='status'),
]
