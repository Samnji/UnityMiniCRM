"""
AI Sales Assistant - Sales insights and recommendations
"""
from django.db.models import Avg, Count, Sum, Q
from django.utils import timezone
from datetime import timedelta


class SalesAssistant:
    
    @staticmethod
    def calculate_deal_score(deal):
        """Calculate AI deal score (0-100) based on multiple factors"""
        from .models import Deal, Task
        
        score = 50
        
        # Time in current stage
        days_in_stage = (timezone.now() - deal.updated_at).days
        if days_in_stage < 7:
            score += 10
        elif days_in_stage > 30:
            score -= 20
        elif days_in_stage > 14:
            score -= 10
            
        # Historical win rate for this company
        if deal.company:
            company_deals = Deal.objects.filter(company=deal.company)
            total_deals = company_deals.count()
            won_deals = company_deals.filter(stage='won').count()
            
            if total_deals > 1:
                win_rate = (won_deals / total_deals) * 100
                if win_rate > 50:
                    score += 15
                elif win_rate < 20:
                    score -= 10
                else:
                    score += (win_rate - 25) * 0.3
        
        # Task completion rate
        tasks = Task.objects.filter(deal=deal)
        total_tasks = tasks.count()
        completed_tasks = tasks.filter(status='completed').count()
        
        if total_tasks > 0:
            completion_rate = (completed_tasks / total_tasks) * 100
            score += (completion_rate / 100) * 20
        
        # Deal amount vs average
        avg_amount = Deal.objects.aggregate(Avg('amount'))['amount__avg'] or 0
        if avg_amount > 0:
            if deal.amount > float(avg_amount) * 2:
                score += 15
            elif deal.amount > float(avg_amount) * 1.5:
                score += 10
            elif deal.amount < float(avg_amount) * 0.5:
                score -= 5
        
        # Stage-specific bonuses
        stage_multipliers = {
            'lead': 0.7,
            'qualified': 0.85,
            'proposal': 1.0,
            'negotiation': 1.15,
            'won': 1.0,
            'lost': 0.0,
        }
        score *= stage_multipliers.get(deal.stage, 1.0)
        
        # Contact engagement
        if deal.contact:
            contact_tasks = Task.objects.filter(contact=deal.contact, status='completed').count()
            score += min(contact_tasks * 2, 10)
        
        return max(0, min(100, int(score)))
    
    @staticmethod
    def get_next_actions(deal):
        """Generate smart recommendations for a deal"""
        from .models import Task
        
        actions = []
        days_in_stage = (timezone.now() - deal.updated_at).days
        
        # Stage-based actions
        stage_actions = {
            'lead': {
                'action': 'Qualify this lead',
                'description': 'Schedule a discovery call to understand their needs and budget',
                'priority': 'high',
                'icon': 'mdi-phone-outline'
            },
            'qualified': {
                'action': 'Create and send proposal',
                'description': 'Prepare a detailed proposal with pricing and timeline',
                'priority': 'high',
                'icon': 'mdi-file-document-outline'
            },
            'proposal': {
                'action': 'Follow up on proposal',
                'description': 'Check if they have reviewed the proposal and address questions',
                'priority': 'medium',
                'icon': 'mdi-email-outline'
            },
            'negotiation': {
                'action': 'Address objections',
                'description': 'Schedule a meeting to discuss pricing or terms concerns',
                'priority': 'high',
                'icon': 'mdi-account-voice'
            },
        }
        
        if deal.stage in stage_actions:
            actions.append(stage_actions[deal.stage])
        
        # Time-based urgency
        if days_in_stage > 21:
            actions.append({
                'action': 'Urgent: Re-engage immediately',
                'description': f'This deal has been in {deal.get_stage_display()} for {days_in_stage} days. Risk of going cold.',
                'priority': 'urgent',
                'icon': 'mdi-alert-circle-outline'
            })
        elif days_in_stage > 14:
            actions.append({
                'action': 'Check in with contact',
                'description': f'Deal has been in {deal.get_stage_display()} for {days_in_stage} days',
                'priority': 'high',
                'icon': 'mdi-message-outline'
            })
        
        # Task-based actions
        pending_tasks = Task.objects.filter(
            deal=deal, 
            status='pending'
        ).order_by('due_date')
        
        overdue_tasks = pending_tasks.filter(due_date__lt=timezone.now()).count()
        upcoming_tasks = pending_tasks.filter(
            due_date__gte=timezone.now(),
            due_date__lte=timezone.now() + timedelta(days=3)
        ).count()
        
        if overdue_tasks > 0:
            actions.append({
                'action': f'Complete {overdue_tasks} overdue task{"s" if overdue_tasks > 1 else ""}',
                'description': 'You have overdue tasks that may be blocking this deal',
                'priority': 'urgent',
                'icon': 'mdi-alert'
            })
        elif upcoming_tasks > 0:
            actions.append({
                'action': f'{upcoming_tasks} task{"s" if upcoming_tasks > 1 else ""} due soon',
                'description': 'Complete these to keep the deal moving forward',
                'priority': 'high',
                'icon': 'mdi-checkbox-marked-circle-outline'
            })
        
        # Contact engagement actions
        if deal.contact:
            last_task = Task.objects.filter(
                Q(contact=deal.contact) | Q(deal=deal),
                status='completed'
            ).order_by('-updated_at').first()
            
            if last_task:
                days_since_contact = (timezone.now() - last_task.updated_at).days
                if days_since_contact > 7:
                    actions.append({
                        'action': 'Re-establish contact',
                        'description': f'Last interaction was {days_since_contact} days ago',
                        'priority': 'medium',
                        'icon': 'mdi-account-clock-outline'
                    })
        
        # Expected close date warnings
        if deal.expected_close_date:
            days_until_close = (deal.expected_close_date - timezone.now().date()).days
            if days_until_close < 0:
                actions.append({
                    'action': 'Update expected close date',
                    'description': f'This deal is {abs(days_until_close)} days past expected close',
                    'priority': 'medium',
                    'icon': 'mdi-calendar-alert'
                })
            elif days_until_close < 7 and deal.stage not in ['won', 'negotiation']:
                actions.append({
                    'action': 'Accelerate deal progress',
                    'description': f'Only {days_until_close} days until expected close',
                    'priority': 'high',
                    'icon': 'mdi-rocket-launch-outline'
                })
        
        # Default action
        if not actions:
            actions.append({
                'action': 'Keep momentum going',
                'description': 'Deal is on track. Continue regular follow-ups.',
                'priority': 'low',
                'icon': 'mdi-check-circle-outline'
            })
        
        return actions
    
    @staticmethod
    def get_insights_summary(user):
        """Get comprehensive AI insights for user dashboard"""
        from .models import Deal, Task
        
        # Get user's deals
        if hasattr(user, 'profile'):
            if user.profile.role == 'admin':
                deals = Deal.objects.all()
            elif user.profile.role == 'manager' and user.profile.team:
                from django.contrib.auth.models import User
                team_users = User.objects.filter(profile__team=user.profile.team)
                deals = Deal.objects.filter(created_by__in=team_users)
            else:
                deals = Deal.objects.filter(created_by=user)
        else:
            deals = Deal.objects.filter(created_by=user)
        
        active_deals = deals.exclude(stage__in=['won', 'lost'])
        
        # Deals needing attention
        stale_deals = active_deals.filter(
            updated_at__lt=timezone.now() - timedelta(days=14)
        ).count()
        
        # High-value opportunities
        avg_amount = deals.aggregate(Avg('amount'))['amount__avg'] or 0
        high_value = active_deals.filter(
            amount__gte=max(10000, float(avg_amount) * 1.5),
            stage__in=['qualified', 'proposal', 'negotiation']
        ).count()
        
        # Win rate
        total = deals.count()
        won = deals.filter(stage='won').count()
        lost = deals.filter(stage='lost').count()
        win_rate = (won / (won + lost) * 100) if (won + lost) > 0 else 0
        
        # Pipeline health score
        pipeline_health = 50
        if stale_deals == 0:
            pipeline_health += 20
        elif stale_deals > 5:
            pipeline_health -= 20
        
        if win_rate > 50:
            pipeline_health += 20
        elif win_rate < 20:
            pipeline_health -= 15
        
        active_count = active_deals.count()
        if active_count > 10:
            pipeline_health += 10
        elif active_count < 3:
            pipeline_health -= 10
        
        pipeline_health = max(0, min(100, pipeline_health))
        
        # Tasks insights
        user_tasks = Task.objects.filter(assigned_to=user) if not hasattr(user, 'profile') or user.profile.role != 'admin' else Task.objects.all()
        overdue_tasks = user_tasks.filter(
            due_date__lt=timezone.now(),
            status__in=['pending', 'in_progress']
        ).count()
        
        # Top deals by AI score
        top_deals = []
        for deal in active_deals.order_by('-updated_at')[:10]:
            score = SalesAssistant.calculate_deal_score(deal)
            top_deals.append({
                'id': deal.id,
                'title': deal.title,
                'score': score,
                'stage': deal.stage,
                'amount': float(deal.amount)
            })
        
        top_deals.sort(key=lambda x: x['score'], reverse=True)
        
        return {
            'stale_deals_count': stale_deals,
            'high_value_opportunities': high_value,
            'win_rate': round(win_rate, 1),
            'total_pipeline_value': float(active_deals.aggregate(Sum('amount'))['amount__sum'] or 0),
            'pipeline_health_score': pipeline_health,
            'overdue_tasks': overdue_tasks,
            'active_deals_count': active_count,
            'top_deals': top_deals[:5],
            'total_deals': total,
            'won_deals': won,
            'lost_deals': lost,
        }
    
    @staticmethod
    def get_team_insights(team):
        """Get team-level AI insights for managers"""
        from .models import Deal, Task
        from django.contrib.auth.models import User
        
        if not team:
            return None
        
        team_users = User.objects.filter(profile__team=team)
        team_deals = Deal.objects.filter(created_by__in=team_users)
        
        # Team performance metrics
        active_deals = team_deals.exclude(stage__in=['won', 'lost'])
        won_deals = team_deals.filter(stage='won').count()
        total_closed = team_deals.filter(stage__in=['won', 'lost']).count()
        team_win_rate = (won_deals / total_closed * 100) if total_closed > 0 else 0
        
        # Member performance
        member_stats = []
        for user in team_users:
            user_deals = Deal.objects.filter(created_by=user)
            user_won = user_deals.filter(stage='won').count()
            user_closed = user_deals.filter(stage__in=['won', 'lost']).count()
            user_win_rate = (user_won / user_closed * 100) if user_closed > 0 else 0
            
            member_stats.append({
                'user_id': user.id,
                'username': user.get_full_name() or user.username,
                'active_deals': user_deals.exclude(stage__in=['won', 'lost']).count(),
                'win_rate': round(user_win_rate, 1),
                'total_value': float(user_deals.exclude(stage__in=['won', 'lost']).aggregate(Sum('amount'))['amount__sum'] or 0),
            })
        
        return {
            'team_name': team.name,
            'member_count': team_users.count(),
            'active_deals': active_deals.count(),
            'total_pipeline_value': float(active_deals.aggregate(Sum('amount'))['amount__sum'] or 0),
            'team_win_rate': round(team_win_rate, 1),
            'members': member_stats,
        }
