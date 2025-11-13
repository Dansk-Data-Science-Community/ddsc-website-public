"""Custom mobile API permissions"""
from rest_framework.permissions import BasePermission, IsAuthenticated

class IsMobileApp(BasePermission):
    """Only allow requests from mobile app"""
    message = "Only mobile app requests allowed."
    
    def has_permission(self, request, view):
        return request.META.get('HTTP_X_DEVICE_TYPE') in ['ios', 'android']

class IsTokenValid(BasePermission):
    """Verify token validity and not expired"""
    message = "Invalid or expired token."
    
    def has_permission(self, request, view):
        # Token validation handled by authentication backend
        return request.user and request.user.is_authenticated

class ReadOnlyMobile(BasePermission):
    """Read-only for mobile (PUT/POST/DELETE restricted)"""
    message = "Mobile app can only read data."
    
    def has_permission(self, request, view):
        return request.method in ['GET', 'HEAD', 'OPTIONS']
