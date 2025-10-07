# apps/authentication/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer, UserSerializer
from .permissions import IsOwnerOrAdmin
from drf_spectacular.utils import extend_schema, OpenApiResponse

User = get_user_model()

@extend_schema(
    tags=['Authentication'],
    request=UserRegistrationSerializer,
    responses={
        201: UserSerializer,
        400: OpenApiResponse(description='Bad Request')
    }
)
class RegisterView(generics.CreateAPIView):
    """
    Register a new user account
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user_data = UserSerializer(user).data
        return Response(user_data, status=status.HTTP_201_CREATED)

@extend_schema(
    tags=['Authentication'],
    responses={200: UserSerializer}
)
class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Get or update user profile
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    
    def get_object(self):
        return self.request.user

@extend_schema(
    tags=['Authentication'],
    responses={200: UserSerializer(many=True)}
)
class UserListView(generics.ListAPIView):
    """
    List all users (Admin only)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_admin():
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)