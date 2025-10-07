# apps/jobs/serializers.py
from rest_framework import serializers
from .models import Job, Category
from apps.authentication.serializers import UserSerializer

class CategorySerializer(serializers.ModelSerializer):
    jobs_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'slug', 'jobs_count', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_jobs_count(self, obj):
        return obj.jobs.filter(is_active=True).count()

class JobListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    posted_by_name = serializers.CharField(source='posted_by.full_name', read_only=True)
    
    class Meta:
        model = Job
        fields = [
            'id', 'title', 'company_name', 'location', 'job_type',
            'salary_min', 'salary_max', 'category_name', 'posted_by_name',
            'is_active', 'created_at', 'application_deadline'
        ]

class JobDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )
    posted_by = UserSerializer(read_only=True)
    applications_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description', 'category', 'category_id',
            'company_name', 'location', 'job_type', 'salary_min', 'salary_max',
            'requirements', 'responsibilities', 'benefits',
            'application_deadline', 'is_active', 'posted_by',
            'applications_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'posted_by', 'created_at', 'updated_at']
    
    def get_applications_count(self, obj):
        return obj.applications.count()

class JobCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            'title', 'description', 'category', 'company_name', 'location',
            'job_type', 'salary_min', 'salary_max', 'requirements',
            'responsibilities', 'benefits', 'application_deadline', 'is_active'
        ]
    
    def validate(self, data):
        if data.get('salary_min') and data.get('salary_max'):
            if data['salary_min'] > data['salary_max']:
                raise serializers.ValidationError(
                    "Minimum salary cannot be greater than maximum salary"
                )
        return data