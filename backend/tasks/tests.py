from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from decimal import Decimal
from datetime import timedelta
from .models import Company, Contact, Deal, Task


class AuthenticationTests(APITestCase):
    """Test authentication endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )

    def test_login_success(self):
        """Test successful login"""
        response = self.client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['username'], 'testuser')

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = self.client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)

    def test_logout(self):
        """Test logout endpoint"""
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        
        response = self.client.post('/api/auth/logout/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify token is deleted
        self.assertFalse(Token.objects.filter(user=self.user).exists())


class CompanyTests(APITestCase):
    """Test Company CRUD operations"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        self.company_data = {
            'name': 'Test Company',
            'industry': 'Technology',
            'website': 'https://testcompany.com',
            'phone': '+1-555-0100',
            'email': 'info@testcompany.com',
            'address': '123 Test Street',
            'notes': 'Test notes'
        }

    def test_create_company(self):
        """Test creating a new company"""
        response = self.client.post('/api/companies/', self.company_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Test Company')
        self.assertEqual(response.data['industry'], 'Technology')
        
        # Verify created_by is set
        company = Company.objects.get(id=response.data['id'])
        self.assertEqual(company.created_by, self.user)

    def test_list_companies(self):
        """Test listing all companies"""
        Company.objects.create(**self.company_data, created_by=self.user)
        Company.objects.create(
            name='Another Company',
            industry='Finance',
            created_by=self.user
        )

        response = self.client.get('/api/companies/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_company(self):
        """Test retrieving a single company"""
        company = Company.objects.create(**self.company_data, created_by=self.user)
        
        response = self.client.get(f'/api/companies/{company.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Company')
        self.assertIn('contacts_count', response.data)
        self.assertIn('deals_count', response.data)

    def test_update_company(self):
        """Test updating a company"""
        company = Company.objects.create(**self.company_data, created_by=self.user)
        
        updated_data = self.company_data.copy()
        updated_data['name'] = 'Updated Company Name'
        
        response = self.client.put(f'/api/companies/{company.id}/', updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Company Name')

    def test_delete_company(self):
        """Test deleting a company"""
        company = Company.objects.create(**self.company_data, created_by=self.user)
        
        response = self.client.delete(f'/api/companies/{company.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Company.objects.filter(id=company.id).exists())

    def test_unauthorized_access(self):
        """Test that unauthenticated users cannot access companies"""
        self.client.credentials()  # Remove authentication
        
        response = self.client.get('/api/companies/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ContactTests(APITestCase):
    """Test Contact CRUD operations"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        self.company = Company.objects.create(
            name='Test Company',
            created_by=self.user
        )

        self.contact_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone': '+1-555-0200',
            'position': 'CEO',
            'company': self.company.id,
            'notes': 'Test contact'
        }

    def test_create_contact(self):
        """Test creating a new contact"""
        response = self.client.post('/api/contacts/', self.contact_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['first_name'], 'John')
        self.assertEqual(response.data['last_name'], 'Doe')
        self.assertEqual(response.data['full_name'], 'John Doe')

    def test_list_contacts(self):
        """Test listing all contacts"""
        Contact.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            created_by=self.user
        )
        Contact.objects.create(
            first_name='Jane',
            last_name='Smith',
            email='jane@example.com',
            created_by=self.user
        )

        response = self.client.get('/api/contacts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_contact(self):
        """Test retrieving a single contact"""
        contact = Contact.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            company=self.company,
            created_by=self.user
        )

        response = self.client.get(f'/api/contacts/{contact.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['full_name'], 'John Doe')
        self.assertEqual(response.data['company_name'], 'Test Company')

    def test_update_contact(self):
        """Test updating a contact"""
        contact = Contact.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            created_by=self.user
        )

        updated_data = {
            'first_name': 'John',
            'last_name': 'Smith',
            'email': 'john.smith@example.com',
            'position': 'CTO'
        }

        response = self.client.patch(f'/api/contacts/{contact.id}/', updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['last_name'], 'Smith')
        self.assertEqual(response.data['position'], 'CTO')

    def test_delete_contact(self):
        """Test deleting a contact"""
        contact = Contact.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            created_by=self.user
        )

        response = self.client.delete(f'/api/contacts/{contact.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Contact.objects.filter(id=contact.id).exists())

    def test_unique_email_constraint(self):
        """Test that email must be unique"""
        Contact.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            created_by=self.user
        )

        # Try to create another contact with same email
        response = self.client.post('/api/contacts/', {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'john@example.com'  # Duplicate email
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DealTests(APITestCase):
    """Test Deal CRUD operations"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        self.company = Company.objects.create(
            name='Test Company',
            created_by=self.user
        )

        self.contact = Contact.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            company=self.company,
            created_by=self.user
        )

        self.deal_data = {
            'title': 'Test Deal',
            'amount': '50000.00',
            'stage': 'lead',
            'probability': 25,
            'expected_close_date': (timezone.now() + timedelta(days=30)).date().isoformat(),
            'company': self.company.id,
            'contact': self.contact.id,
            'notes': 'Test deal notes'
        }

    def test_create_deal(self):
        """Test creating a new deal"""
        response = self.client.post('/api/deals/', self.deal_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Test Deal')
        self.assertEqual(Decimal(response.data['amount']), Decimal('50000.00'))

    def test_list_deals(self):
        """Test listing all deals"""
        Deal.objects.create(
            title='Deal 1',
            amount=Decimal('10000'),
            company=self.company,
            created_by=self.user
        )
        Deal.objects.create(
            title='Deal 2',
            amount=Decimal('20000'),
            company=self.company,
            created_by=self.user
        )

        response = self.client.get('/api/deals/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_deal(self):
        """Test retrieving a single deal"""
        deal = Deal.objects.create(
            title='Test Deal',
            amount=Decimal('50000'),
            company=self.company,
            contact=self.contact,
            created_by=self.user
        )

        response = self.client.get(f'/api/deals/{deal.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Deal')
        self.assertEqual(response.data['company_name'], 'Test Company')
        self.assertEqual(response.data['contact_name'], 'John Doe')

    def test_update_deal_stage(self):
        """Test updating deal stage"""
        deal = Deal.objects.create(
            title='Test Deal',
            amount=Decimal('50000'),
            stage='lead',
            company=self.company,
            created_by=self.user
        )

        response = self.client.patch(f'/api/deals/{deal.id}/', {
            'stage': 'qualified',
            'probability': 50
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['stage'], 'qualified')
        self.assertEqual(response.data['probability'], 50)

    def test_delete_deal(self):
        """Test deleting a deal"""
        deal = Deal.objects.create(
            title='Test Deal',
            amount=Decimal('50000'),
            company=self.company,
            created_by=self.user
        )

        response = self.client.delete(f'/api/deals/{deal.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Deal.objects.filter(id=deal.id).exists())

    def test_deal_stage_choices(self):
        """Test that only valid stages are accepted"""
        invalid_deal_data = self.deal_data.copy()
        invalid_deal_data['stage'] = 'invalid_stage'

        response = self.client.post('/api/deals/', invalid_deal_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TaskTests(APITestCase):
    """Test Task CRUD operations"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        self.company = Company.objects.create(
            name='Test Company',
            created_by=self.user
        )

        self.contact = Contact.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            created_by=self.user
        )

        self.deal = Deal.objects.create(
            title='Test Deal',
            amount=Decimal('50000'),
            company=self.company,
            created_by=self.user
        )

        self.task_data = {
            'title': 'Follow up call',
            'description': 'Call client to discuss proposal',
            'status': 'pending',
            'priority': 'high',
            'due_date': (timezone.now() + timedelta(days=7)).isoformat(),
            'contact': self.contact.id,
            'deal': self.deal.id,
            'assigned_to': self.user.id
        }

    def test_create_task(self):
        """Test creating a new task"""
        response = self.client.post('/api/tasks/', self.task_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Follow up call')
        self.assertEqual(response.data['priority'], 'high')

    def test_list_tasks(self):
        """Test listing all tasks"""
        Task.objects.create(
            title='Task 1',
            created_by=self.user
        )
        Task.objects.create(
            title='Task 2',
            created_by=self.user
        )

        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_task(self):
        """Test retrieving a single task"""
        task = Task.objects.create(
            title='Test Task',
            contact=self.contact,
            deal=self.deal,
            assigned_to=self.user,
            created_by=self.user
        )

        response = self.client.get(f'/api/tasks/{task.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Task')

    def test_update_task_status(self):
        """Test updating task status"""
        task = Task.objects.create(
            title='Test Task',
            status='pending',
            created_by=self.user
        )

        response = self.client.patch(f'/api/tasks/{task.id}/', {
            'status': 'in_progress'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'in_progress')

    def test_complete_task(self):
        """Test marking task as completed"""
        task = Task.objects.create(
            title='Test Task',
            status='in_progress',
            created_by=self.user
        )

        response = self.client.patch(f'/api/tasks/{task.id}/', {
            'status': 'completed'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'completed')

    def test_delete_task(self):
        """Test deleting a task"""
        task = Task.objects.create(
            title='Test Task',
            created_by=self.user
        )

        response = self.client.delete(f'/api/tasks/{task.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=task.id).exists())

    def test_task_priority_choices(self):
        """Test that only valid priorities are accepted"""
        invalid_task_data = self.task_data.copy()
        invalid_task_data['priority'] = 'invalid_priority'

        response = self.client.post('/api/tasks/', invalid_task_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DashboardTests(APITestCase):
    """Test dashboard statistics endpoint"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        # Create sample data
        self.company = Company.objects.create(
            name='Test Company',
            created_by=self.user
        )

        self.contact = Contact.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            created_by=self.user
        )

        Deal.objects.create(
            title='Deal 1',
            amount=Decimal('10000'),
            stage='lead',
            company=self.company,
            created_by=self.user
        )
        Deal.objects.create(
            title='Deal 2',
            amount=Decimal('20000'),
            stage='won',
            company=self.company,
            created_by=self.user
        )

        Task.objects.create(
            title='Task 1',
            status='pending',
            created_by=self.user
        )

    def test_dashboard_stats(self):
        """Test dashboard statistics endpoint"""
        response = self.client.get('/api/dashboard/stats/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check all required fields are present
        self.assertIn('total_contacts', response.data)
        self.assertIn('total_companies', response.data)
        self.assertIn('total_deals', response.data)
        self.assertIn('total_tasks', response.data)
        self.assertIn('deals_by_stage', response.data)
        self.assertIn('total_deal_value', response.data)
        self.assertIn('won_deals_value', response.data)
        self.assertIn('pending_tasks', response.data)

        # Verify counts
        self.assertEqual(response.data['total_contacts'], 1)
        self.assertEqual(response.data['total_companies'], 1)
        self.assertEqual(response.data['total_deals'], 2)
        self.assertEqual(response.data['total_tasks'], 1)
        self.assertEqual(response.data['pending_tasks'], 1)

        # Verify deal values
        self.assertEqual(float(response.data['total_deal_value']), 30000.0)
        self.assertEqual(float(response.data['won_deals_value']), 20000.0)

    def test_dashboard_unauthorized(self):
        """Test that dashboard requires authentication"""
        self.client.credentials()  # Remove authentication
        
        response = self.client.get('/api/dashboard/stats/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ModelTests(TestCase):
    """Test model methods and properties"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_company_str(self):
        """Test Company __str__ method"""
        company = Company.objects.create(
            name='Test Company',
            created_by=self.user
        )
        self.assertEqual(str(company), 'Test Company')

    def test_contact_full_name_property(self):
        """Test Contact full_name property"""
        contact = Contact.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            created_by=self.user
        )
        self.assertEqual(contact.full_name, 'John Doe')

    def test_contact_str(self):
        """Test Contact __str__ method"""
        contact = Contact.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            created_by=self.user
        )
        self.assertEqual(str(contact), 'John Doe')

    def test_deal_str(self):
        """Test Deal __str__ method"""
        company = Company.objects.create(
            name='Test Company',
            created_by=self.user
        )
        deal = Deal.objects.create(
            title='Test Deal',
            amount=Decimal('50000'),
            company=company,
            created_by=self.user
        )
        self.assertEqual(str(deal), 'Test Deal')

    def test_task_default_values(self):
        """Test Task default values"""
        task = Task.objects.create(
            title='Test Task',
            created_by=self.user
        )
        self.assertEqual(task.status, 'pending')
        self.assertEqual(task.priority, 'medium')
