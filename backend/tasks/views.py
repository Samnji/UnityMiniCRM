from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Count, Sum, Q
from django.utils import timezone
from .models import Company, Contact, Deal, Task, Team, UserProfile
from .serializers import (
    CompanySerializer, ContactSerializer, DealSerializer,
    TaskSerializer, UserSerializer, TeamSerializer, UserProfileSerializer
)
from .ai_assistant import SalesAssistant


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def logout_view(request):
    if request.user.is_authenticated:
        request.user.auth_token.delete()
    return Response({'message': 'Logged out successfully'})


@api_view(['GET'])
def dashboard_stats(request):
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

    stats = {
        'total_contacts': Contact.objects.count(),
        'total_companies': Company.objects.count(),
        'total_deals': Deal.objects.count(),
        'total_tasks': Task.objects.count(),
        'deals_by_stage': list(Deal.objects.values('stage').annotate(count=Count('id'))),
        'total_deal_value': Deal.objects.aggregate(total=Sum('amount'))['total'] or 0,
        'won_deals_value': Deal.objects.filter(stage='won').aggregate(total=Sum('amount'))['total'] or 0,
        'pending_tasks': Task.objects.filter(status='pending').count(),
        'overdue_tasks': Task.objects.filter(
            due_date__lt=timezone.now(),
            status__in=['pending', 'in_progress']
        ).count() if 'timezone' in dir() else 0,
    }
    return Response(stats)


@api_view(['GET'])
def ai_insights(request):
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
    
    insights = SalesAssistant.get_insights_summary(request.user)
    return Response(insights)


@api_view(['GET'])
def team_insights(request):
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
    
    if not hasattr(request.user, 'profile') or not request.user.profile.team:
        return Response({'error': 'User not assigned to a team'}, status=status.HTTP_400_BAD_REQUEST)
    
    if request.user.profile.role not in ['manager', 'admin']:
        return Response({'error': 'Only managers can view team insights'}, status=status.HTTP_403_FORBIDDEN)
    
    insights = SalesAssistant.get_team_insights(request.user.profile.team)
    return Response(insights)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        team = self.get_object()
        profiles = UserProfile.objects.filter(team=team)
        serializer = UserProfileSerializer(profiles, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def insights(self, request, pk=None):
        team = self.get_object()
        insights = SalesAssistant.get_team_insights(team)
        return Response(insights)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        if hasattr(request.user, 'profile'):
            serializer = self.get_serializer(request.user.profile)
            return Response(serializer.data)
        return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['patch'])
    def update_me(self, request):
        if hasattr(request.user, 'profile'):
            serializer = self.get_serializer(request.user.profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)


class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_superuser or (hasattr(user, 'profile') and user.profile.role == 'admin'):
            return Company.objects.all()
        
        if hasattr(user, 'profile') and user.profile.role == 'manager' and user.profile.team:
            team_users = User.objects.filter(profile__team=user.profile.team)
            return Company.objects.filter(created_by__in=team_users)
        
        if hasattr(user, 'profile') and user.profile.role == 'viewer':
            return Company.objects.all()
        
        return Company.objects.filter(created_by=user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter contacts based on user role"""
        user = self.request.user
        
        if user.is_superuser or (hasattr(user, 'profile') and user.profile.role in ['admin', 'viewer']):
            return Contact.objects.all()
        
        if hasattr(user, 'profile') and user.profile.role == 'manager' and user.profile.team:
            team_users = User.objects.filter(profile__team=user.profile.team)
            return Contact.objects.filter(created_by__in=team_users)
        
        return Contact.objects.filter(created_by=user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class DealViewSet(viewsets.ModelViewSet):
    serializer_class = DealSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter deals based on user role"""
        user = self.request.user
        
        if user.is_superuser or (hasattr(user, 'profile') and user.profile.role in ['admin', 'viewer']):
            return Deal.objects.all()
        
        if hasattr(user, 'profile') and user.profile.role == 'manager' and user.profile.team:
            team_users = User.objects.filter(profile__team=user.profile.team)
            return Deal.objects.filter(created_by__in=team_users)
        
        return Deal.objects.filter(created_by=user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['get'])
    def ai_score(self, request, pk=None):
        deal = self.get_object()
        
        return Response({
            'deal_id': deal.id,
            'score': SalesAssistant.calculate_deal_score(deal),
            'next_actions': SalesAssistant.get_next_actions(deal),
            'stage': deal.stage,
            'amount': float(deal.amount),
            'days_in_stage': (timezone.now() - deal.updated_at).days,
        })


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_superuser or (hasattr(user, 'profile') and user.profile.role in ['admin', 'viewer']):
            return Task.objects.all()
        
        if hasattr(user, 'profile') and user.profile.role == 'manager' and user.profile.team:
            team_users = User.objects.filter(profile__team=user.profile.team)
            return Task.objects.filter(Q(created_by__in=team_users) | Q(assigned_to__in=team_users)).distinct()
        
        return Task.objects.filter(Q(created_by=user) | Q(assigned_to=user)).distinct()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
