from django.urls import path
from .views import PageListView, PageDetailView

app_name = 'pages'
urlpatterns = [
    path('', PageListView.as_view(), name='list'),
    path('<slug:slug>/', PageDetailView.as_view(), name='detail'),
]
