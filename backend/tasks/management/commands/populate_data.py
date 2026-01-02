"""
Management command to populate the database with sample data
Run with: python manage.py populate_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from tasks.models import Company, Contact, Deal, Task


class Command(BaseCommand):
    help = 'Populates the database with sample data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before populating',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            Task.objects.all().delete()
            Deal.objects.all().delete()
            Contact.objects.all().delete()
            Company.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write(self.style.SUCCESS('Data cleared'))

        self.stdout.write('Creating sample data...')

        # Create users
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@unitycrm.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Created admin user (username: admin, password: admin123)'))
        
        sales_rep1, _ = User.objects.get_or_create(
            username='john_doe',
            defaults={
                'email': 'john@unitycrm.com',
                'first_name': 'John',
                'last_name': 'Doe'
            }
        )
        
        sales_rep2, _ = User.objects.get_or_create(
            username='jane_smith',
            defaults={
                'email': 'jane@unitycrm.com',
                'first_name': 'Jane',
                'last_name': 'Smith'
            }
        )

        # Create companies
        companies_data = [
            {
                'name': 'TechCorp Industries',
                'industry': 'Technology',
                'website': 'https://techcorp.com',
                'phone': '+1-555-0101',
                'email': 'info@techcorp.com',
                'address': '123 Tech Street, San Francisco, CA 94105',
                'notes': 'Fortune 500 technology company, interested in enterprise solutions'
            },
            {
                'name': 'Global Retail Solutions',
                'industry': 'Retail',
                'website': 'https://globalretail.com',
                'phone': '+1-555-0202',
                'email': 'contact@globalretail.com',
                'address': '456 Commerce Ave, New York, NY 10001',
                'notes': 'Large retail chain looking for CRM integration'
            },
            {
                'name': 'HealthFirst Medical',
                'industry': 'Healthcare',
                'website': 'https://healthfirst.com',
                'phone': '+1-555-0303',
                'email': 'info@healthfirst.com',
                'address': '789 Medical Plaza, Boston, MA 02101',
                'notes': 'Healthcare provider seeking patient management system'
            },
            {
                'name': 'EduTech Learning',
                'industry': 'Education',
                'website': 'https://edutech.com',
                'phone': '+1-555-0404',
                'email': 'hello@edutech.com',
                'address': '321 Campus Drive, Austin, TX 78701',
                'notes': 'EdTech startup, fast-growing company'
            },
            {
                'name': 'FinanceFlow Bank',
                'industry': 'Finance',
                'website': 'https://financeflow.com',
                'phone': '+1-555-0505',
                'email': 'business@financeflow.com',
                'address': '555 Wall Street, New York, NY 10005',
                'notes': 'Major financial institution, high security requirements'
            },
            {
                'name': 'GreenEnergy Solutions',
                'industry': 'Energy',
                'website': 'https://greenenergy.com',
                'phone': '+1-555-0606',
                'email': 'info@greenenergy.com',
                'address': '999 Solar Boulevard, Denver, CO 80201',
                'notes': 'Renewable energy company, environmentally conscious'
            }
        ]

        companies = []
        for company_data in companies_data:
            company = Company.objects.create(
                **company_data,
                created_by=admin_user
            )
            companies.append(company)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(companies)} companies'))

        # Create contacts
        contacts_data = [
            {
                'first_name': 'Michael',
                'last_name': 'Johnson',
                'email': 'mjohnson@techcorp.com',
                'phone': '+1-555-1001',
                'position': 'CEO',
                'company': companies[0],
                'notes': 'Decision maker, prefers email communication'
            },
            {
                'first_name': 'Sarah',
                'last_name': 'Williams',
                'email': 'swilliams@techcorp.com',
                'phone': '+1-555-1002',
                'position': 'CTO',
                'company': companies[0],
                'notes': 'Technical decision maker'
            },
            {
                'first_name': 'Robert',
                'last_name': 'Brown',
                'email': 'rbrown@globalretail.com',
                'phone': '+1-555-2001',
                'position': 'VP of Operations',
                'company': companies[1],
                'notes': 'Very responsive, prefers phone calls'
            },
            {
                'first_name': 'Emily',
                'last_name': 'Davis',
                'email': 'edavis@healthfirst.com',
                'phone': '+1-555-3001',
                'position': 'Director of IT',
                'company': companies[2],
                'notes': 'Interested in HIPAA compliance features'
            },
            {
                'first_name': 'David',
                'last_name': 'Martinez',
                'email': 'dmartinez@edutech.com',
                'phone': '+1-555-4001',
                'position': 'Founder & CEO',
                'company': companies[3],
                'notes': 'Young entrepreneur, very tech-savvy'
            },
            {
                'first_name': 'Lisa',
                'last_name': 'Anderson',
                'email': 'landerson@financeflow.com',
                'phone': '+1-555-5001',
                'position': 'Chief Operating Officer',
                'company': companies[4],
                'notes': 'Requires detailed compliance documentation'
            }
        ]

        contacts = []
        for contact_data in contacts_data:
            contact = Contact.objects.create(
                **contact_data,
                created_by=admin_user
            )
            contacts.append(contact)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(contacts)} contacts'))

        # Create deals
        deals_data = [
            {
                'title': 'Enterprise CRM Implementation - TechCorp',
                'amount': Decimal('125000.00'),
                'stage': 'negotiation',
                'probability': 75,
                'expected_close_date': timezone.now().date() + timedelta(days=15),
                'company': companies[0],
                'contact': contacts[0],
                'notes': 'Large enterprise deal, multiple stakeholders involved'
            },
            {
                'title': 'Retail Integration Package - Global Retail',
                'amount': Decimal('85000.00'),
                'stage': 'proposal',
                'probability': 60,
                'expected_close_date': timezone.now().date() + timedelta(days=30),
                'company': companies[1],
                'contact': contacts[2],
                'notes': 'Need to address integration concerns'
            },
            {
                'title': 'Healthcare CRM Solution - HealthFirst',
                'amount': Decimal('200000.00'),
                'stage': 'qualified',
                'probability': 40,
                'expected_close_date': timezone.now().date() + timedelta(days=60),
                'company': companies[2],
                'contact': contacts[3],
                'notes': 'High value deal, requires HIPAA compliance'
            },
            {
                'title': 'EdTech Startup Package - EduTech',
                'amount': Decimal('35000.00'),
                'stage': 'won',
                'probability': 100,
                'expected_close_date': timezone.now().date() - timedelta(days=5),
                'company': companies[3],
                'contact': contacts[4],
                'notes': 'Deal closed! Implementation starting next week'
            },
            {
                'title': 'Banking Solutions - FinanceFlow',
                'amount': Decimal('500000.00'),
                'stage': 'lead',
                'probability': 20,
                'expected_close_date': timezone.now().date() + timedelta(days=90),
                'company': companies[4],
                'contact': contacts[5],
                'notes': 'Initial discovery meeting scheduled'
            },
            {
                'title': 'Green Energy Platform - GreenEnergy',
                'amount': Decimal('75000.00'),
                'stage': 'lost',
                'probability': 0,
                'expected_close_date': timezone.now().date() - timedelta(days=10),
                'company': companies[5],
                'contact': None,
                'notes': 'Lost to competitor, budget constraints cited'
            }
        ]

        deals = []
        for deal_data in deals_data:
            deal = Deal.objects.create(
                **deal_data,
                created_by=admin_user
            )
            deals.append(deal)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(deals)} deals'))

        # Create tasks
        tasks_data = [
            {
                'title': 'Follow up call with Michael Johnson',
                'description': 'Discuss contract terms and timeline for implementation',
                'status': 'pending',
                'priority': 'high',
                'due_date': timezone.now() + timedelta(days=2),
                'contact': contacts[0],
                'deal': deals[0],
                'assigned_to': sales_rep1
            },
            {
                'title': 'Send proposal to Global Retail',
                'description': 'Prepare detailed proposal including integration specifics',
                'status': 'in_progress',
                'priority': 'high',
                'due_date': timezone.now() + timedelta(days=5),
                'contact': contacts[2],
                'deal': deals[1],
                'assigned_to': sales_rep1
            },
            {
                'title': 'Schedule demo for HealthFirst',
                'description': 'Coordinate demo with IT team, focus on HIPAA features',
                'status': 'pending',
                'priority': 'medium',
                'due_date': timezone.now() + timedelta(days=7),
                'contact': contacts[3],
                'deal': deals[2],
                'assigned_to': sales_rep2
            },
            {
                'title': 'Send thank you email to EduTech',
                'description': 'Thank them for their business and outline next steps',
                'status': 'completed',
                'priority': 'low',
                'due_date': timezone.now() - timedelta(days=2),
                'contact': contacts[4],
                'deal': deals[3],
                'assigned_to': sales_rep1
            },
            {
                'title': 'Research FinanceFlow requirements',
                'description': 'Deep dive into banking compliance requirements',
                'status': 'pending',
                'priority': 'medium',
                'due_date': timezone.now() + timedelta(days=10),
                'contact': contacts[5],
                'deal': deals[4],
                'assigned_to': sales_rep2
            },
            {
                'title': 'Update contact list for TechCorp',
                'description': 'Add additional stakeholders to the company profile',
                'status': 'pending',
                'priority': 'low',
                'due_date': timezone.now() + timedelta(days=3),
                'contact': contacts[1],
                'deal': None,
                'assigned_to': sales_rep1
            }
        ]

        tasks = []
        for task_data in tasks_data:
            task = Task.objects.create(
                **task_data,
                created_by=admin_user
            )
            tasks.append(task)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(tasks)} tasks'))

        # Summary
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))
        self.stdout.write(self.style.SUCCESS('='*50))
        self.stdout.write(f'Users: {User.objects.count()}')
        self.stdout.write(f'Companies: {Company.objects.count()}')
        self.stdout.write(f'Contacts: {Contact.objects.count()}')
        self.stdout.write(f'Deals: {Deal.objects.count()}')
        self.stdout.write(f'Tasks: {Task.objects.count()}')
        self.stdout.write(self.style.SUCCESS('='*50))
        self.stdout.write('\nLogin credentials:')
        self.stdout.write('  Username: admin')
        self.stdout.write('  Password: admin123')
        self.stdout.write(self.style.SUCCESS('='*50))
