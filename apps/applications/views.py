# apps/applications/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Application
from .serializers import (
    ApplicationCreateSerializer, ApplicationListSerializer,
    ApplicationDetailSerializer, ApplicationStatusUpdateSerializer
)
from .permissions import IsApplicantOrAdmin, IsAdminUser
from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    list=extend_schema(tags=['Applications'], description='List applications'),
    retrieve=extend_schema(tags=['Applications'], description='Get application details'),
    create=extend_schema(tags=['Applications'], description='Apply for a job'),
    update=extend_schema(tags=['Applications'], description='Update application'),
    partial_update=extend_schema(tags=['Applications'], description='Partially update application'),
    destroy=extend_schema(tags=['Applications'], description='Withdraw application'),
)
class ApplicationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing job applications
    """
    queryset = Application.objects.select_related('job', 'applicant', 'job__category')
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'job']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ApplicationCreateSerializer
        elif self.action == 'list':
            return ApplicationListSerializer
        elif self.action == 'update_status':
            return ApplicationStatusUpdateSerializer
        return ApplicationDetailSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Regular users only see their own applications
        if not self.request.user.is_admin():
            queryset = queryset.filter(applicant=self.request.user)
        return queryset
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsApplicantOrAdmin()]
        elif self.action == 'update_status':
            return [IsAdminUser()]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        serializer.save(applicant=self.request.user)
    
    @extend_schema(
        tags=['Applications'],
        description='Update application status (Admin only)',
        request=ApplicationStatusUpdateSerializer,
        responses={200: ApplicationDetailSerializer}
    )
    @action(detail=True, methods=['patch'], permission_classes=[IsAdminUser])
    def update_status(self, request, pk=None):
        application = self.get_object()
        serializer = ApplicationStatusUpdateSerializer(
            application, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(ApplicationDetailSerializer(application).data)
    
    @extend_schema(
        tags=['Applications'],
        description='Get applications for a specific job (Admin only)',
        responses={200: ApplicationListSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], url_path='job/(?P<job_id>[0-9]+)', 
            permission_classes=[IsAdminUser])
    def by_job(self, request, job_id=None):
        applications = self.get_queryset().filter(job_id=job_id)
        serializer = ApplicationListSerializer(applications, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        tags=['Applications'],
        description='Get current user\'s applications',
        responses={200: ApplicationListSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def my_applications(self, request):
        applications = Application.objects.filter(
            applicant=request.user
        ).select_related('job', 'job__category')
        serializer = ApplicationListSerializer(applications, many=True)
        return Response(serializer.data)