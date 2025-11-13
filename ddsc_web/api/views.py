"""Mobile API ViewSets - REST endpoints"""
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User
from django.utils import timezone
from pages.models import Page
from oss.models import OpenSourceProject
from waitlist.models import EventWaitlist
from engagement.models import ParticipationLevel, ActivityLog
from engagement.services import EngagementService
from .serializers import (
    UserMobileSerializer, PageMobileSerializer, OSSProjectMobileSerializer,
    WaitlistMobileSerializer, AuthTokenSerializer, APIErrorSerializer
)

class MobileAuthTokenView(ObtainAuthToken):
    """Mobile login endpoint - returns token + user info"""
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        # Log login activity
        EngagementService.log_activity(user, 'event_attend', description='Mobile app login')
        
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'expires_in': '30 days',
            'success': True,
        })

class MobileUserViewSet(viewsets.ReadOnlyModelViewSet):
    """User profile endpoint"""
    queryset = User.objects.all()
    serializer_class = UserMobileSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        """Logout - delete token"""
        Token.objects.filter(user=request.user).delete()
        return Response({'success': True, 'message': 'Logged out'})

class PageMobileViewSet(viewsets.ReadOnlyModelViewSet):
    """Pages endpoint - lightweight responses"""
    queryset = Page.objects.filter(published=True)
    serializer_class = PageMobileSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    
    def list(self, request, *args, **kwargs):
        """List pages with minimal payload"""
        pages = self.get_queryset()
        serializer = self.get_serializer(pages, many=True)
        return Response({
            'success': True,
            'count': pages.count(),
            'results': serializer.data,
        })

class OSSProjectMobileViewSet(viewsets.ReadOnlyModelViewSet):
    """OSS Projects endpoint - lightweight"""
    queryset = OpenSourceProject.objects.filter(active=True).order_by('-github_stars')
    serializer_class = OSSProjectMobileSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured projects only"""
        projects = self.get_queryset().filter(featured=True)[:5]
        serializer = self.get_serializer(projects, many=True)
        return Response({
            'success': True,
            'results': serializer.data,
        })
    
    @action(detail=False, methods=['get'])
    def trending(self, request):
        """Get trending projects by stars"""
        projects = self.get_queryset()[:10]
        serializer = self.get_serializer(projects, many=True)
        return Response({
            'success': True,
            'results': serializer.data,
        })

class WaitlistMobileViewSet(viewsets.ModelViewSet):
    """Waitlist endpoints - join and check status"""
    serializer_class = WaitlistMobileSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def join(self, request):
        """Join event waitlist"""
        email = request.data.get('email')
        event_name = request.data.get('event_name')
        
        if not email or not event_name:
            return Response({'success': False, 'error': 'Email and event_name required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Get next position
        last = EventWaitlist.objects.filter(event_name=event_name).order_by('-position').first()
        position = (last.position + 1) if last else 1
        
        waitlist = EventWaitlist.objects.create(
            email=email, event_name=event_name, position=position
        )
        serializer = self.get_serializer(waitlist)
        return Response({
            'success': True,
            'message': f'Added to waitlist at position #{position}',
            'data': serializer.data,
        })
    
    @action(detail=False, methods=['get'])
    def status(self, request):
        """Check waitlist status by email"""
        email = request.query_params.get('email')
        event = request.query_params.get('event')
        
        if not email:
            return Response({'success': False, 'error': 'Email parameter required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        entries = EventWaitlist.objects.filter(email=email)
        if event:
            entries = entries.filter(event_name=event)
        
        serializer = self.get_serializer(entries, many=True)
        return Response({
            'success': True,
            'count': entries.count(),
            'results': serializer.data,
        })

class EngagementMobileViewSet(viewsets.ViewSet):
    """Engagement stats endpoint"""
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get user engagement statistics"""
        stats = EngagementService.get_user_stats(request.user)
        return Response({
            'success': True,
            'data': stats,
        })
    
    @action(detail=False, methods=['get'])
    def leaderboard(self, request):
        """Get leaderboard (top 10)"""
        leaderboard = EngagementService.get_leaderboard(10)
        data = [
            {
                'rank': i + 1,
                'username': item.user.username,
                'level': item.level,
                'score': item.score,
            }
            for i, item in enumerate(leaderboard)
        ]
        return Response({
            'success': True,
            'results': data,
        })
