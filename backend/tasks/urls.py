from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CompanyViewSet, ContactViewSet, DealViewSet, TaskViewSet,
    TeamViewSet, UserProfileViewSet,
    login_view, logout_view, dashboard_stats, ai_insights, team_insights
)

router = DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='company')
router.register(r'contacts', ContactViewSet, basename='contact')
router.register(r'deals', DealViewSet, basename='deal')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'teams', TeamViewSet, basename='team')
router.register(r'profiles', UserProfileViewSet, basename='profile')

urlpatterns = [
    path('auth/login/', login_view, name='login'),
    path('auth/logout/', logout_view, name='logout'),
    path('dashboard/stats/', dashboard_stats, name='dashboard_stats'),
    path('ai/insights/', ai_insights, name='ai_insights'),
    path('ai/team-insights/', team_insights, name='team_insights'),
    path('', include(router.urls)),
]
