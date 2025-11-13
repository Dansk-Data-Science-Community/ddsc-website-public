"""Custom authentication backend for mobile API"""
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class MobileTokenAuthentication(TokenAuthentication):
    """Token auth with expiration and device tracking"""
    keyword = 'Bearer'
    
    def authenticate_credentials(self, key):
        """Authenticate token with expiration check"""
        try:
            token = self.get_model().objects.get(key=key)
        except self.get_model().DoesNotExist:
            raise AuthenticationFailed('Invalid token.')
        
        if not token.user.is_active:
            raise AuthenticationFailed('User inactive or deleted.')
        
        # Check token expiration (30 days)
        if timezone.now() - token.created > timedelta(days=30):
            token.delete()
            raise AuthenticationFailed('Token expired.')
        
        return (token.user, token)


class MobileDeviceAuthSerializer:
    """Serialize device info for auth"""
    @staticmethod
    def get_device_info(request):
        """Extract device info from request"""
        return {
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            'device_type': request.META.get('HTTP_X_DEVICE_TYPE', 'unknown'),
            'app_version': request.META.get('HTTP_X_APP_VERSION', ''),
        }
