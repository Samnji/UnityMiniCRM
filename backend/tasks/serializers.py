from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Company, Contact, Deal, Task, Team, UserProfile


class TeamSerializer(serializers.ModelSerializer):
    member_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'member_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    full_name = serializers.SerializerMethodField()
    team_name = serializers.CharField(source='team.name', read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'username', 'email', 'first_name', 'last_name', 'full_name',
                  'team', 'team_name', 'role', 'role_display', 'phone', 'avatar', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
    
    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.username


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']
        read_only_fields = ['id']


class CompanySerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    contacts_count = serializers.SerializerMethodField()
    deals_count = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ['id', 'name', 'industry', 'website', 'phone', 'email', 'address',
                  'notes', 'created_at', 'updated_at', 'created_by', 'created_by_name',
                  'contacts_count', 'deals_count']
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']

    def get_contacts_count(self, obj):
        return obj.contacts.count()

    def get_deals_count(self, obj):
        return obj.deals.count()


class ContactSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    company_name = serializers.CharField(source='company.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Contact
        fields = ['id', 'first_name', 'last_name', 'full_name', 'email', 'phone',
                  'position', 'company', 'company_name', 'notes', 'created_at',
                  'updated_at', 'created_by', 'created_by_name']
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by', 'full_name']


class DealSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    contact_name = serializers.CharField(source='contact.full_name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Deal
        fields = ['id', 'title', 'amount', 'stage', 'probability', 'expected_close_date',
                  'company', 'company_name', 'contact', 'contact_name', 'notes',
                  'created_at', 'updated_at', 'created_by', 'created_by_name']
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']


class TaskSerializer(serializers.ModelSerializer):
    contact_name = serializers.CharField(source='contact.full_name', read_only=True)
    deal_title = serializers.CharField(source='deal.title', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.username', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority', 'due_date',
                  'contact', 'contact_name', 'deal', 'deal_title', 'assigned_to',
                  'assigned_to_name', 'created_at', 'updated_at', 'created_by',
                  'created_by_name']
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']
