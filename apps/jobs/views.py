# apps/jobs/views.py
from rest_framework import viewsets, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Job, Category
from .serializers import (
    JobListSerializer, JobDetailSerializer, JobCreateUpdateSerializer,
    CategorySerializer
)
from .filters import JobFilter
from .permissions import IsAdminOrReadOnly
from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    list=extend_schema(tags=['Jobs'], description='List all jobs with filtering'),
    retrieve=extend_schema(tags=['Jobs'], description='Get job details'),
    create=extend_schema(tags=['Jobs'], description='Create a new job (Admin only)'),
    update=extend_schema(tags=['Jobs'], description='Update a job (Admin only)'),
    partial_update=extend_schema(tags=['Jobs'], description='Partially update a job (Admin only)'),
    destroy=extend_schema(tags=['Jobs'], description='Delete a job (Admin only)'),
)
class JobViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing job postings
    """
    queryset = Job.objects.select_related('category', 'posted_by').prefetch_related('applications')
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = JobFilter
    search_fields = ['title', 'description', 'company_name', 'requirements']
    ordering_fields = ['created_at', 'salary_min', 'salary_max', 'application_deadline']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return JobListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return JobCreateUpdateSerializer
        return JobDetailSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Non-admin users only see active jobs
        if not self.request.user.is_authenticated or not self.request.user.is_admin():
            queryset = queryset.filter(is_active=True)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)
    
    @extend_schema(
        tags=['Jobs'],
        description='Get jobs by category',
        responses={200: JobListSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], url_path='by-category/(?P<category_id>[0-9]+)')
    def by_category(self, request, category_id=None):
        jobs = self.get_queryset().filter(category_id=category_id)
        serializer = JobListSerializer(jobs, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        tags=['Jobs'],
        description='Get jobs posted by current user',
        responses={200: JobListSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_jobs(self, request):
        jobs = self.get_queryset().filter(posted_by=request.user)
        serializer = JobListSerializer(jobs, many=True)
        return Response(serializer.data)

@extend_schema_view(
    list=extend_schema(tags=['Categories'], description='List all categories'),
    retrieve=extend_schema(tags=['Categories'], description='Get category details'),
    create=extend_schema(tags=['Categories'], description='Create category (Admin only)'),
    update=extend_schema(tags=['Categories'], description='Update category (Admin only)'),
    partial_update=extend_schema(tags=['Categories'], description='Partially update category (Admin only)'),
    destroy=extend_schema(tags=['Categories'], description='Delete category (Admin only)'),
)
class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing job categories
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'