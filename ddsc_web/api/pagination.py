"""Mobile-optimized pagination"""
from rest_framework.pagination import PageNumberPagination

class MobilePagePagination(PageNumberPagination):
    """Lightweight pagination for mobile"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'page'
    
    def get_paginated_response(self, data):
        """Mobile-optimized response format"""
        return Response({
            'success': True,
            'pagination': {
                'count': self.page.paginator.count,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'page_size': self.page_size,
            },
            'results': data,
        })

class MobileCursorPagination:
    """Cursor-based pagination for efficiency"""
    pass
