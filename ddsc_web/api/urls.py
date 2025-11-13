"""Mobile API URL routing"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MobileAuthTokenView, MobileUserViewSet, PageMobileViewSet,
    OSSProjectMobileViewSet, WaitlistMobileViewSet, EngagementMobileViewSet
)

router = DefaultRouter()
router.register(r'users', MobileUserViewSet, basename='user')
router.register(r'pages', PageMobileViewSet, basename='page')
router.register(r'projects', OSSProjectMobileViewSet, basename='project')
router.register(r'waitlist', WaitlistMobileViewSet, basename='waitlist')
router.register(r'engagement', EngagementMobileViewSet, basename='engagement')

urlpatterns = [
    path('auth/login/', MobileAuthTokenView.as_view(), name='mobile-login'),
    path('', include(router.urls)),
]
