from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tasks.models import Team, UserProfile, Company, Contact, Deal, Task
from django.utils import timezone
from datetime import timedelta
import random


class Command(BaseCommand):
    help = 'Populate database with comprehensive sample data including teams and user profiles'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting data population...')
        
        # Clear existing data
        self.stdout.write('Clearing existing data...')
        Task.objects.all().delete()
        Deal.objects.all().delete()
        Contact.objects.all().delete()
        Company.objects.all().delete()
        UserProfile.objects.all().delete()
        Team.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        self.stdout.write(self.style.SUCCESS('Data cleared'))
        
        # Create Teams
        self.stdout.write('Creating teams...')
        teams_data = [
            {
                'name': 'East Coast Sales',
                'description': 'Handles all accounts in Eastern US and Canada. Focus on enterprise clients in finance and healthcare.'
            },
            {
                'name': 'West Coast Sales',
                'description': 'Manages West Coast territory including California, Oregon, Washington. Tech and startup focus.'
            },
            {
                'name': 'Enterprise Sales',
                'description': 'Focuses on large enterprise accounts with $100K+ deal sizes. Cross-functional team.'
            },
            {
                'name': 'SMB Sales',
                'description': 'Small and Medium Business sales team. High-velocity sales with shorter sales cycles.'
            },
            {
                'name': 'Customer Success',
                'description': 'Post-sale customer management, retention, and upsell opportunities.'
            },
        ]
        
        team_objects = []
        for team_data in teams_data:
            team = Team.objects.create(**team_data)
            team_objects.append(team)
            self.stdout.write(f'  Created team: {team.name}')
        
        # Create Users with Profiles
        self.stdout.write('Creating users with profiles...')
        users_data = [
            {
                'username': 'john.smith',
                'email': 'john.smith@company.com',
                'first_name': 'John',
                'last_name': 'Smith',
                'team': team_objects[0],  # East Coast
                'role': 'manager',
                'phone': '+1-555-0101'
            },
            {
                'username': 'sarah.johnson',
                'email': 'sarah.j@company.com',
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'team': team_objects[0],  # East Coast
                'role': 'sales_rep',
                'phone': '+1-555-0102'
            },
            {
                'username': 'mike.davis',
                'email': 'mike.d@company.com',
                'first_name': 'Mike',
                'last_name': 'Davis',
                'team': team_objects[0],  # East Coast
                'role': 'sales_rep',
                'phone': '+1-555-0103'
            },
            {
                'username': 'emily.chen',
                'email': 'emily.chen@company.com',
                'first_name': 'Emily',
                'last_name': 'Chen',
                'team': team_objects[1],  # West Coast
                'role': 'manager',
                'phone': '+1-555-0201'
            },
            {
                'username': 'david.kim',
                'email': 'david.k@company.com',
                'first_name': 'David',
                'last_name': 'Kim',
                'team': team_objects[1],  # West Coast
                'role': 'sales_rep',
                'phone': '+1-555-0202'
            },
            {
                'username': 'lisa.brown',
                'email': 'lisa.b@company.com',
                'first_name': 'Lisa',
                'last_name': 'Brown',
                'team': team_objects[2],  # Enterprise
                'role': 'manager',
                'phone': '+1-555-0301'
            },
            {
                'username': 'robert.taylor',
                'email': 'robert.t@company.com',
                'first_name': 'Robert',
                'last_name': 'Taylor',
                'team': team_objects[2],  # Enterprise
                'role': 'sales_rep',
                'phone': '+1-555-0302'
            },
            {
                'username': 'viewer.user',
                'email': 'viewer@company.com',
                'first_name': 'View',
                'last_name': 'Only',
                'team': None,
                'role': 'viewer',
                'phone': '+1-555-0401'
            },
        ]
        
        user_objects = []
        for user_data in users_data:
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password='password123',
                first_name=user_data['first_name'],
                last_name=user_data['last_name']
            )
            
            # Update the auto-created profile
            profile = user.profile
            profile.team = user_data['team']
            profile.role = user_data['role']
            profile.phone = user_data['phone']
            profile.save()
            
            user_objects.append(user)
            team_name = profile.team.name if profile.team else "No Team"
            self.stdout.write(f'  {user.username} ({profile.get_role_display()}) - Team: {team_name}')
        
        # Create admin user if not exists
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@company.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            admin_user.profile.role = 'admin'
            admin_user.profile.phone = '+1-555-0001'
            admin_user.profile.save()
            self.stdout.write('  admin (Administrator) - Superuser')
        
        # Create Companies
        self.stdout.write('Creating companies...')
        companies_data = [
            {'name': 'Acme Corporation', 'industry': 'Technology', 'website': 'https://acme.com', 
             'phone': '+1-555-1001', 'email': 'info@acme.com', 'address': '123 Tech Street, San Francisco, CA'},
            {'name': 'TechStart Inc', 'industry': 'Software', 'website': 'https://techstart.io',
             'phone': '+1-555-1002', 'email': 'contact@techstart.io', 'address': '456 Innovation Ave, New York, NY'},
            {'name': 'Global Industries', 'industry': 'Manufacturing', 'website': 'https://globalind.com',
             'phone': '+1-555-1003', 'email': 'sales@globalind.com', 'address': '789 Factory Road, Chicago, IL'},
            {'name': 'MegaCorp Ltd', 'industry': 'Finance', 'website': 'https://megacorp.com',
             'phone': '+1-555-1004', 'email': 'info@megacorp.com', 'address': '321 Wall Street, New York, NY'},
            {'name': 'StartupXYZ', 'industry': 'Technology', 'website': 'https://startupxyz.com',
             'phone': '+1-555-1005', 'email': 'hello@startupxyz.com', 'address': '555 Startup Lane, Austin, TX'},
            {'name': 'Enterprise Solutions', 'industry': 'Consulting', 'website': 'https://enterprisesol.com',
             'phone': '+1-555-1006', 'email': 'contact@enterprisesol.com', 'address': '777 Business Blvd, Boston, MA'},
        ]
        
        company_objects = []
        for i, company_data in enumerate(companies_data):
            # Distribute companies among team members
            creator = user_objects[i % len(user_objects)]
            company = Company.objects.create(**company_data, created_by=creator)
            company_objects.append(company)
            self.stdout.write(f'  {company.name} (by {creator.username})')
        
        # Create Contacts
        self.stdout.write('Creating contacts...')
        contacts_data = [
            {'first_name': 'John', 'last_name': 'Doe', 'email': 'john.doe@acme.com', 
             'phone': '+1-555-2001', 'position': 'VP of Sales', 'company': company_objects[0]},
            {'first_name': 'Jane', 'last_name': 'Wilson', 'email': 'jane.wilson@acme.com',
             'phone': '+1-555-2002', 'position': 'CTO', 'company': company_objects[0]},
            {'first_name': 'Bob', 'last_name': 'Anderson', 'email': 'bob.anderson@techstart.io',
             'phone': '+1-555-2003', 'position': 'CEO', 'company': company_objects[1]},
            {'first_name': 'Alice', 'last_name': 'Thompson', 'email': 'alice.t@globalind.com',
             'phone': '+1-555-2004', 'position': 'Procurement Manager', 'company': company_objects[2]},
            {'first_name': 'Charlie', 'last_name': 'Brown', 'email': 'charlie@megacorp.com',
             'phone': '+1-555-2005', 'position': 'Director of Operations', 'company': company_objects[3]},
            {'first_name': 'Diana', 'last_name': 'Prince', 'email': 'diana@startupxyz.com',
             'phone': '+1-555-2006', 'position': 'Founder & CEO', 'company': company_objects[4]},
        ]
        
        contact_objects = []
        for i, contact_data in enumerate(contacts_data):
            creator = user_objects[i % len(user_objects)]
            contact = Contact.objects.create(**contact_data, created_by=creator)
            contact_objects.append(contact)
            self.stdout.write(f'  {contact.full_name} at {contact.company.name}')
        
        # Create Deals
        self.stdout.write('Creating deals...')
        deals_data = [
            # Active Deals - Lead Stage
            {'title': 'Cloud Migration Project', 'amount': 200000, 'stage': 'lead',
             'probability': 30, 'company': company_objects[3], 'contact': contact_objects[4],
             'days_old': 25, 'user_index': 0},
            {'title': 'Training Package', 'amount': 15000, 'stage': 'lead',
             'probability': 40, 'company': company_objects[1], 'contact': contact_objects[2],
             'days_old': 7, 'user_index': 1},
            {'title': 'Security Audit Services', 'amount': 45000, 'stage': 'lead',
             'probability': 35, 'company': company_objects[2], 'contact': contact_objects[3],
             'days_old': 15, 'user_index': 2},
            {'title': 'Mobile App Development', 'amount': 120000, 'stage': 'lead',
             'probability': 25, 'company': company_objects[4], 'contact': contact_objects[5],
             'days_old': 3, 'user_index': 3},
            {'title': 'Data Analytics Platform', 'amount': 85000, 'stage': 'lead',
             'probability': 30, 'company': company_objects[0], 'contact': contact_objects[0],
             'days_old': 10, 'user_index': 4},
            
            # Active Deals - Qualified Stage
            {'title': 'Q1 Software License', 'amount': 50000, 'stage': 'qualified',
             'probability': 60, 'company': company_objects[0], 'contact': contact_objects[0],
             'days_old': 5, 'user_index': 0},
            {'title': 'Custom Development', 'amount': 95000, 'stage': 'qualified',
             'probability': 55, 'company': company_objects[5], 'contact': contact_objects[0],
             'days_old': 32, 'user_index': 1},
            {'title': 'API Integration Project', 'amount': 65000, 'stage': 'qualified',
             'probability': 65, 'company': company_objects[1], 'contact': contact_objects[2],
             'days_old': 12, 'user_index': 2},
            {'title': 'Infrastructure Upgrade', 'amount': 110000, 'stage': 'qualified',
             'probability': 50, 'company': company_objects[3], 'contact': contact_objects[4],
             'days_old': 20, 'user_index': 3},
            {'title': 'ERP Implementation', 'amount': 180000, 'stage': 'qualified',
             'probability': 60, 'company': company_objects[2], 'contact': contact_objects[3],
             'days_old': 8, 'user_index': 4},
            {'title': 'Cybersecurity Package', 'amount': 72000, 'stage': 'qualified',
             'probability': 58, 'company': company_objects[5], 'contact': contact_objects[0],
             'days_old': 14, 'user_index': 5},
            
            # Active Deals - Proposal Stage
            {'title': 'Enterprise Platform Implementation', 'amount': 150000, 'stage': 'proposal',
             'probability': 70, 'company': company_objects[1], 'contact': contact_objects[2],
             'days_old': 12, 'user_index': 0},
            {'title': 'Annual Support Contract', 'amount': 25000, 'stage': 'proposal',
             'probability': 75, 'company': company_objects[0], 'contact': contact_objects[1],
             'days_old': 18, 'user_index': 1},
            {'title': 'CRM Customization', 'amount': 55000, 'stage': 'proposal',
             'probability': 68, 'company': company_objects[4], 'contact': contact_objects[5],
             'days_old': 9, 'user_index': 2},
            {'title': 'Marketing Automation Setup', 'amount': 42000, 'stage': 'proposal',
             'probability': 72, 'company': company_objects[3], 'contact': contact_objects[4],
             'days_old': 6, 'user_index': 3},
            {'title': 'Business Intelligence Suite', 'amount': 130000, 'stage': 'proposal',
             'probability': 65, 'company': company_objects[2], 'contact': contact_objects[3],
             'days_old': 11, 'user_index': 4},
            {'title': 'DevOps Transformation', 'amount': 98000, 'stage': 'proposal',
             'probability': 70, 'company': company_objects[5], 'contact': contact_objects[0],
             'days_old': 15, 'user_index': 5},
            
            # Active Deals - Negotiation Stage
            {'title': 'Consulting Services Agreement', 'amount': 75000, 'stage': 'negotiation',
             'probability': 85, 'company': company_objects[2], 'contact': contact_objects[3],
             'days_old': 8, 'user_index': 0},
            {'title': 'Multi-Year License Deal', 'amount': 225000, 'stage': 'negotiation',
             'probability': 88, 'company': company_objects[1], 'contact': contact_objects[2],
             'days_old': 5, 'user_index': 1},
            {'title': 'Managed Services Contract', 'amount': 165000, 'stage': 'negotiation',
             'probability': 80, 'company': company_objects[4], 'contact': contact_objects[5],
             'days_old': 4, 'user_index': 2},
            {'title': 'Enterprise Support Upgrade', 'amount': 48000, 'stage': 'negotiation',
             'probability': 90, 'company': company_objects[0], 'contact': contact_objects[1],
             'days_old': 3, 'user_index': 3},
            {'title': 'Professional Services Package', 'amount': 87000, 'stage': 'negotiation',
             'probability': 82, 'company': company_objects[3], 'contact': contact_objects[4],
             'days_old': 7, 'user_index': 4},
            
            # Won Deals - Recent
            {'title': 'Product Bundle Sale', 'amount': 35000, 'stage': 'won',
             'probability': 100, 'company': company_objects[4], 'contact': contact_objects[5],
             'days_old': 45, 'user_index': 0},
            {'title': 'Q4 Licensing Agreement', 'amount': 62000, 'stage': 'won',
             'probability': 100, 'company': company_objects[0], 'contact': contact_objects[0],
             'days_old': 30, 'user_index': 0},
            {'title': 'Renewal Contract', 'amount': 38000, 'stage': 'won',
             'probability': 100, 'company': company_objects[1], 'contact': contact_objects[2],
             'days_old': 22, 'user_index': 1},
            {'title': 'Premium Support Package', 'amount': 28000, 'stage': 'won',
             'probability': 100, 'company': company_objects[2], 'contact': contact_objects[3],
             'days_old': 35, 'user_index': 1},
            {'title': 'Starter Implementation', 'amount': 42000, 'stage': 'won',
             'probability': 100, 'company': company_objects[3], 'contact': contact_objects[4],
             'days_old': 18, 'user_index': 2},
            {'title': 'System Integration', 'amount': 78000, 'stage': 'won',
             'probability': 100, 'company': company_objects[5], 'contact': contact_objects[0],
             'days_old': 40, 'user_index': 2},
            {'title': 'Cloud Storage Upgrade', 'amount': 52000, 'stage': 'won',
             'probability': 100, 'company': company_objects[4], 'contact': contact_objects[5],
             'days_old': 25, 'user_index': 3},
            {'title': 'Analytics Dashboard', 'amount': 45000, 'stage': 'won',
             'probability': 100, 'company': company_objects[0], 'contact': contact_objects[1],
             'days_old': 28, 'user_index': 3},
            {'title': 'Training Program', 'amount': 22000, 'stage': 'won',
             'probability': 100, 'company': company_objects[1], 'contact': contact_objects[2],
             'days_old': 50, 'user_index': 4},
            {'title': 'Compliance Audit', 'amount': 58000, 'stage': 'won',
             'probability': 100, 'company': company_objects[2], 'contact': contact_objects[3],
             'days_old': 33, 'user_index': 4},
            {'title': 'Performance Optimization', 'amount': 67000, 'stage': 'won',
             'probability': 100, 'company': company_objects[3], 'contact': contact_objects[4],
             'days_old': 42, 'user_index': 5},
            {'title': 'Migration Services', 'amount': 95000, 'stage': 'won',
             'probability': 100, 'company': company_objects[5], 'contact': contact_objects[0],
             'days_old': 38, 'user_index': 5},
            
            # Won Deals - Older
            {'title': 'Legacy System Modernization', 'amount': 145000, 'stage': 'won',
             'probability': 100, 'company': company_objects[0], 'contact': contact_objects[0],
             'days_old': 75, 'user_index': 0},
            {'title': 'Backup Solution', 'amount': 32000, 'stage': 'won',
             'probability': 100, 'company': company_objects[1], 'contact': contact_objects[2],
             'days_old': 68, 'user_index': 1},
            {'title': 'Network Security Setup', 'amount': 88000, 'stage': 'won',
             'probability': 100, 'company': company_objects[2], 'contact': contact_objects[3],
             'days_old': 90, 'user_index': 2},
            {'title': 'Database Optimization', 'amount': 54000, 'stage': 'won',
             'probability': 100, 'company': company_objects[4], 'contact': contact_objects[5],
             'days_old': 82, 'user_index': 3},
            {'title': 'Workflow Automation', 'amount': 71000, 'stage': 'won',
             'probability': 100, 'company': company_objects[3], 'contact': contact_objects[4],
             'days_old': 95, 'user_index': 4},
            
            # Lost Deals
            {'title': 'Budget-Constrained Project', 'amount': 125000, 'stage': 'lost',
             'probability': 0, 'company': company_objects[0], 'contact': contact_objects[1],
             'days_old': 60, 'user_index': 0},
            {'title': 'Competitor Won Deal', 'amount': 92000, 'stage': 'lost',
             'probability': 0, 'company': company_objects[1], 'contact': contact_objects[2],
             'days_old': 55, 'user_index': 1},
            {'title': 'Timing Not Right', 'amount': 68000, 'stage': 'lost',
             'probability': 0, 'company': company_objects[2], 'contact': contact_objects[3],
             'days_old': 48, 'user_index': 2},
            {'title': 'Feature Mismatch', 'amount': 78000, 'stage': 'lost',
             'probability': 0, 'company': company_objects[5], 'contact': contact_objects[0],
             'days_old': 70, 'user_index': 3},
            {'title': 'Went with Internal Solution', 'amount': 110000, 'stage': 'lost',
             'probability': 0, 'company': company_objects[4], 'contact': contact_objects[5],
             'days_old': 52, 'user_index': 4},
        ]
        
        deal_objects = []
        for i, deal_data in enumerate(deals_data):
            days_old = deal_data.pop('days_old')
            user_index = deal_data.pop('user_index')
            creator = user_objects[user_index]
            
            deal = Deal.objects.create(**deal_data, created_by=creator)
            
            # Backdate the created_at and updated_at
            deal.created_at = timezone.now() - timedelta(days=days_old)
            deal.updated_at = timezone.now() - timedelta(days=days_old if days_old < 30 else random.randint(7, 14))
            deal.expected_close_date = (timezone.now() + timedelta(days=random.randint(10, 60))).date()
            deal.save()
            
            deal_objects.append(deal)
            self.stdout.write(f'  {deal.title} - ${deal.amount:,.0f} ({deal.get_stage_display()}) (by {creator.username})')
        
        # Create Tasks
        self.stdout.write('Creating tasks...')
        tasks_data = [
            {'title': 'Follow up call with John', 'description': 'Discuss Q1 contract details',
             'status': 'pending', 'priority': 'high', 'contact': contact_objects[0],
             'deal': deal_objects[0], 'due_days': 2},
            {'title': 'Prepare proposal for TechStart', 'description': 'Include pricing and timeline',
             'status': 'in_progress', 'priority': 'high', 'contact': contact_objects[2],
             'deal': deal_objects[1], 'due_days': 5},
            {'title': 'Schedule demo for Global Industries', 'description': 'Product demonstration',
             'status': 'completed', 'priority': 'medium', 'contact': contact_objects[3],
             'deal': deal_objects[2], 'due_days': -3},
            {'title': 'Send contract to MegaCorp', 'description': 'Final contract review',
             'status': 'pending', 'priority': 'urgent', 'contact': contact_objects[4],
             'deal': deal_objects[3], 'due_days': -1},
            {'title': 'Thank you email to StartupXYZ', 'description': 'Post-sale follow up',
             'status': 'completed', 'priority': 'low', 'contact': contact_objects[5],
             'deal': deal_objects[4], 'due_days': -10},
            {'title': 'Technical call with Acme CTO', 'description': 'Address integration questions',
             'status': 'pending', 'priority': 'high', 'contact': contact_objects[1],
             'deal': deal_objects[5], 'due_days': 1},
        ]
        
        for i, task_data in enumerate(tasks_data):
            due_days = task_data.pop('due_days')
            creator = user_objects[i % len(user_objects)]
            assigned = user_objects[(i + 1) % len(user_objects)]
            
            task = Task.objects.create(
                **task_data,
                created_by=creator,
                assigned_to=assigned,
                due_date=timezone.now() + timedelta(days=due_days)
            )
            
            self.stdout.write(f'  {task.title} - {task.status} (assigned to {assigned.username})')
        
        # Display summary
        self.stdout.write('\n' + '-' * 50)
        self.stdout.write(self.style.SUCCESS('Database populated successfully'))
        self.stdout.write('-' * 50)
        
        self.stdout.write('\nSummary:')
        self.stdout.write(f'  • Teams: {Team.objects.count()}')
        self.stdout.write(f'  • Users: {User.objects.count()} (including admin)')
        self.stdout.write(f'  • Companies: {Company.objects.count()}')
        self.stdout.write(f'  • Contacts: {Contact.objects.count()}')
        self.stdout.write(f'  • Deals: {Deal.objects.count()}')
        self.stdout.write(f'  • Tasks: {Task.objects.count()}')
        
        self.stdout.write('\nLogin Credentials:')
        self.stdout.write('  Admin: username=admin, password=admin123')
        self.stdout.write('  Manager: username=john.smith, password=password123')
        self.stdout.write('  Sales Rep: username=sarah.johnson, password=password123')
        self.stdout.write('  Viewer: username=viewer.user, password=password123')
        
        self.stdout.write('\nAI Features:')
        self.stdout.write(f'  • Deal scoring algorithm analyzing {Deal.objects.count()} deals')
        self.stdout.write('  • Next-action recommendations for each deal')
        self.stdout.write('  • Pipeline health scoring')
        self.stdout.write('  • Team performance insights')
        
        self.stdout.write('\nTest Scenarios:')
        self.stdout.write('  - Fresh deals (< 7 days) for high AI scores')
        self.stdout.write('  - Stale deals (> 21 days) for urgent actions')
        self.stdout.write('  - Overdue tasks for priority alerts')
        self.stdout.write('  - Multi-stage pipeline for conversion analysis')
        self.stdout.write('  - Cross-team collaboration scenarios')
        self.stdout.write(f'  - {Deal.objects.filter(stage="won").count()} won deals for historical analysis')
        self.stdout.write(f'  - {Deal.objects.filter(stage="lost").count()} lost deals for learning insights')
        
        self.stdout.write('\n' + '-' * 50)
        self.stdout.write(self.style.SUCCESS('Ready to start: python manage.py runserver'))
        self.stdout.write('-' * 50 + '\n')
