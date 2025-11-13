"""Mobile API middleware"""
from django.utils.deprecation import MiddlewareMixin
import json

class MobileAPIMiddleware(MiddlewareMixin):
    """Middleware for mobile API requests"""
    
    def process_request(self, request):
        """Add mobile context"""
        if request.path.startswith('/api/'):
            request.is_mobile = True
            request.device_type = request.META.get('HTTP_X_DEVICE_TYPE', 'unknown')
            request.app_version = request.META.get('HTTP_X_APP_VERSION', '')
        return None
    
    def process_response(self, request, response):
        """Standardize API responses"""
        if request.path.startswith('/api/') and response['Content-Type'] == 'application/json':
            # Ensure all responses have success flag
            if response.status_code < 400:
                try:
                    data = json.loads(response.content)
                    if 'success' not in data:
                        data['success'] = True
                        response.content = json.dumps(data)
                except:
                    pass
        return response
