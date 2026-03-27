"""
Views for Formations API
"""

from django.utils import timezone
from django.db.models import Q
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import (
    Category, Formation, Module, Resource,
    Enrollment, ModuleProgress, FormationRating, FormationBookmark
)
from .serializers import (
    CategorySerializer, FormationListSerializer, FormationDetailSerializer,
    FormationCreateSerializer, ModuleListSerializer, ModuleDetailSerializer,
    ResourceSerializer, EnrollmentSerializer, ModuleProgressUpdateSerializer,
    FormationRatingSerializer
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for categories."""
    queryset = Category.objects.filter(is_active=True, parent=None)
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class FormationViewSet(viewsets.ModelViewSet):
    """ViewSet for formations."""
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    
    def get_queryset(self):
        queryset = Formation.objects.select_related('author', 'category')
        
        # Filter by status
        if self.action == 'list':
            queryset = queryset.filter(status='published')
        
        # Search
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(author__full_name__icontains=search)
            )
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Filter by level
        level = self.request.query_params.get('level')
        if level:
            queryset = queryset.filter(level=level)
        
        # Filter by price
        is_free = self.request.query_params.get('is_free')
        if is_free:
            queryset = queryset.filter(is_free=is_free.lower() == 'true')
        
        # Ordering
        ordering = self.request.query_params.get('ordering', '-created_at')
        if ordering in ['created_at', '-created_at', 'rating_average', '-rating_average', 
                        'students_count', '-students_count', 'title', '-title']:
            queryset = queryset.order_by(ordering)
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'list':
            return FormationListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return FormationCreateSerializer
        return FormationDetailSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count
        Formation.objects.filter(pk=instance.pk).update(
            views_count=instance.views_count + 1
        )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured formations."""
        queryset = self.get_queryset().filter(is_featured=True)[:10]
        serializer = FormationListSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Get popular formations."""
        queryset = self.get_queryset().order_by('-students_count')[:10]
        serializer = FormationListSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_formations(self, request):
        """Get formations created by current user."""
        queryset = Formation.objects.filter(author=request.user)
        serializer = FormationListSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def enroll(self, request, slug=None):
        """Enroll in a formation."""
        formation = self.get_object()
        
        enrollment, created = Enrollment.objects.get_or_create(
            user=request.user,
            formation=formation
        )
        
        if created:
            Formation.objects.filter(pk=formation.pk).update(
                students_count=formation.students_count + 1
            )
            return Response(
                {'message': 'Inscription reussie', 'enrollment_id': enrollment.id},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'message': 'Deja inscrit'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['post', 'delete'], permission_classes=[IsAuthenticated])
    def bookmark(self, request, slug=None):
        """Bookmark/unbookmark a formation."""
        formation = self.get_object()
        
        if request.method == 'POST':
            bookmark, created = FormationBookmark.objects.get_or_create(
                user=request.user,
                formation=formation
            )
            if created:
                return Response({'message': 'Formation sauvegardee'}, status=status.HTTP_201_CREATED)
            return Response({'message': 'Deja sauvegardee'})
        
        elif request.method == 'DELETE':
            deleted, _ = FormationBookmark.objects.filter(
                user=request.user,
                formation=formation
            ).delete()
            if deleted:
                return Response({'message': 'Sauvegarde supprimee'})
            return Response({'message': 'Non sauvegardee'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['get', 'post'], permission_classes=[IsAuthenticatedOrReadOnly])
    def ratings(self, request, slug=None):
        """Get or create ratings for a formation."""
        formation = self.get_object()
        
        if request.method == 'GET':
            ratings = FormationRating.objects.filter(formation=formation, is_approved=True)
            serializer = FormationRatingSerializer(ratings, many=True)
            return Response(serializer.data)
        
        elif request.method == 'POST':
            # Check if user is enrolled
            if not Enrollment.objects.filter(user=request.user, formation=formation).exists():
                return Response(
                    {'error': 'Vous devez etre inscrit pour noter cette formation'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            serializer = FormationRatingSerializer(
                data=request.data,
                context={'request': request}
            )
            if serializer.is_valid():
                # Update or create rating
                rating, created = FormationRating.objects.update_or_create(
                    user=request.user,
                    formation=formation,
                    defaults=serializer.validated_data
                )
                
                # Update formation rating average
                from django.db.models import Avg
                avg = FormationRating.objects.filter(formation=formation).aggregate(Avg('rating'))
                Formation.objects.filter(pk=formation.pk).update(
                    rating_average=avg['rating__avg'] or 0,
                    rating_count=FormationRating.objects.filter(formation=formation).count()
                )
                
                return Response(
                    FormationRatingSerializer(rating).data,
                    status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ModuleViewSet(viewsets.ModelViewSet):
    """ViewSet for modules within a formation."""
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        formation_slug = self.kwargs.get('formation_slug')
        return Module.objects.filter(
            formation__slug=formation_slug,
            is_published=True
        ).select_related('formation')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ModuleListSerializer
        return ModuleDetailSerializer
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def progress(self, request, formation_slug=None, pk=None):
        """Update module progress."""
        module = self.get_object()
        
        # Check enrollment
        enrollment = Enrollment.objects.filter(
            user=request.user,
            formation__slug=formation_slug
        ).first()
        
        if not enrollment:
            return Response(
                {'error': 'Non inscrit a cette formation'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = ModuleProgressUpdateSerializer(data=request.data)
        if serializer.is_valid():
            progress, created = ModuleProgress.objects.update_or_create(
                user=request.user,
                module=module,
                enrollment=enrollment,
                defaults={
                    'watch_time_seconds': serializer.validated_data['watch_time_seconds'],
                    'last_position_seconds': serializer.validated_data['last_position_seconds'],
                    'is_completed': serializer.validated_data.get('is_completed', False),
                    'completed_at': timezone.now() if serializer.validated_data.get('is_completed') else None
                }
            )
            
            # Update enrollment progress
            total_modules = module.formation.modules.count()
            completed_modules = ModuleProgress.objects.filter(
                enrollment=enrollment,
                is_completed=True
            ).count()
            
            progress_percent = int((completed_modules / total_modules) * 100) if total_modules > 0 else 0
            
            Enrollment.objects.filter(pk=enrollment.pk).update(
                progress_percent=progress_percent,
                last_module=module,
                last_position_seconds=serializer.validated_data['last_position_seconds'],
                is_completed=progress_percent == 100,
                completed_at=timezone.now() if progress_percent == 100 else None
            )
            
            return Response({
                'message': 'Progression mise a jour',
                'progress_percent': progress_percent,
                'module_completed': progress.is_completed
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EnrollmentViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for user enrollments."""
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Enrollment.objects.filter(
            user=self.request.user
        ).select_related('formation', 'formation__author', 'formation__category')
    
    @action(detail=False, methods=['get'])
    def in_progress(self, request):
        """Get formations in progress."""
        queryset = self.get_queryset().filter(
            is_completed=False,
            progress_percent__gt=0
        ).order_by('-last_accessed')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def completed(self, request):
        """Get completed formations."""
        queryset = self.get_queryset().filter(is_completed=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BookmarkListView(generics.ListAPIView):
    """List bookmarked formations."""
    serializer_class = FormationListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Formation.objects.filter(
            bookmarks__user=self.request.user
        ).select_related('author', 'category')
