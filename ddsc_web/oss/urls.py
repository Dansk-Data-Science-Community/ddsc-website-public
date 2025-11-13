from django.urls import path
from .views import OSSListView, OSSDetailView

app_name = 'oss'
urlpatterns = [
    path('', OSSListView.as_view(), name='list'),
    path('<slug:slug>/', OSSDetailView.as_view(), name='detail'),
]
