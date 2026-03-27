"""
Views for Communities API
"""

from django.utils import timezone
from django.db.models import Q
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import (
    Community, CommunityMember, Group, Channel, Thread, ThreadReply,
    CommunityResource, Live, LiveQuestion, LiveQuestionVote, LiveChatMessage
)
from .serializers import (
    CommunityListSerializer, CommunityDetailSerializer, CommunityCreateSerializer,
    CommunityMemberSerializer, GroupSerializer, ChannelSerializer,
    ThreadListSerializer, ThreadDetailSerializer, ThreadCreateSerializer,
    ThreadReplySerializer, CommunityResourceSerializer,
    LiveListSerializer, LiveDetailSerializer, LiveCreateSerializer,
    LiveQuestionSerializer, LiveChatMessageSerializer
)


class CommunityViewSet(viewsets.ModelViewSet):
    """ViewSet for communities."""
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    
    def get_queryset(self):
        queryset = Community.objects.filter(is_active=True)
        
        # Filter by visibility for non-members
        if self.action == 'list':
            if self.request.user.is_authenticated:
                # Show public + communities user is member of
                member_communities = CommunityMember.objects.filter(
                    user=self.request.user, status='approved'
                ).values_list('community_id', flat=True)
                queryset = queryset.filter(
                    Q(visibility='public') | Q(id__in=member_communities)
                )
            else:
                queryset = queryset.filter(visibility='public')
        
        # Search
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
        
        return queryset.select_related('owner')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CommunityListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return CommunityCreateSerializer
        return CommunityDetailSerializer
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def join(self, request, slug=None):
        """Join a community."""
        community = self.get_object()
        
        # Check if already a member
        existing = CommunityMember.objects.filter(
            community=community, user=request.user
        ).first()
        
        if existing:
            if existing.status == 'banned':
                return Response(
                    {'error': 'Vous etes banni de cette communaute'},
                    status=status.HTTP_403_FORBIDDEN
                )
            if existing.status == 'approved':
                return Response({'message': 'Deja membre'})
            if existing.status == 'pending':
                return Response({'message': 'Demande en attente'})
        
        # Create membership
        member_status = 'pending' if community.requires_approval else 'approved'
        CommunityMember.objects.create(
            community=community,
            user=request.user,
            status=member_status
        )
        
        if member_status == 'approved':
            Community.objects.filter(pk=community.pk).update(
                members_count=community.members_count + 1
            )
            return Response({'message': 'Vous avez rejoint la communaute'}, status=status.HTTP_201_CREATED)
        
        return Response({'message': 'Demande envoyee'}, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
    def leave(self, request, slug=None):
        """Leave a community."""
        community = self.get_object()
        
        membership = CommunityMember.objects.filter(
            community=community, user=request.user
        ).first()
        
        if not membership:
            return Response({'error': 'Non membre'}, status=status.HTTP_404_NOT_FOUND)
        
        if membership.role == 'owner':
            return Response(
                {'error': 'Le proprietaire ne peut pas quitter'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        membership.delete()
        Community.objects.filter(pk=community.pk).update(
            members_count=max(0, community.members_count - 1)
        )
        
        return Response({'message': 'Vous avez quitte la communaute'})
    
    @action(detail=True, methods=['get'])
    def members(self, request, slug=None):
        """Get community members."""
        community = self.get_object()
        members = CommunityMember.objects.filter(
            community=community, status='approved'
        ).select_related('user')
        
        serializer = CommunityMemberSerializer(members, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def resources(self, request, slug=None):
        """Get community resources."""
        community = self.get_object()
        resources = CommunityResource.objects.filter(community=community)
        serializer = CommunityResourceSerializer(resources, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_communities(self, request):
        """Get communities user is member of."""
        member_ids = CommunityMember.objects.filter(
            user=request.user, status='approved'
        ).values_list('community_id', flat=True)
        
        communities = Community.objects.filter(id__in=member_ids)
        serializer = CommunityListSerializer(communities, many=True, context={'request': request})
        return Response(serializer.data)


class ChannelThreadViewSet(viewsets.ModelViewSet):
    """ViewSet for threads within a channel."""
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        channel_id = self.kwargs.get('channel_id')
        return Thread.objects.filter(channel_id=channel_id).select_related('author', 'last_reply_by')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ThreadListSerializer
        elif self.action == 'create':
            return ThreadCreateSerializer
        return ThreadDetailSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        Thread.objects.filter(pk=instance.pk).update(
            views_count=instance.views_count + 1
        )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def reply(self, request, channel_id=None, pk=None):
        """Reply to a thread."""
        thread = self.get_object()
        
        if thread.is_locked:
            return Response(
                {'error': 'Ce thread est verrouille'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        content = request.data.get('content')
        parent_id = request.data.get('parent')
        
        if not content:
            return Response(
                {'error': 'Le contenu est requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        reply = ThreadReply.objects.create(
            thread=thread,
            author=request.user,
            content=content,
            parent_id=parent_id
        )
        
        # Update thread stats
        Thread.objects.filter(pk=thread.pk).update(
            replies_count=thread.replies_count + 1,
            last_reply_at=timezone.now(),
            last_reply_by=request.user
        )
        
        # Update channel stats
        Channel.objects.filter(pk=thread.channel.pk).update(
            messages_count=thread.channel.messages_count + 1
        )
        
        return Response(
            ThreadReplySerializer(reply, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )


class LiveViewSet(viewsets.ModelViewSet):
    """ViewSet for lives."""
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = Live.objects.select_related('host', 'community')
        
        # Filter by community
        community_slug = self.request.query_params.get('community')
        if community_slug:
            queryset = queryset.filter(community__slug=community_slug)
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'list':
            return LiveListSerializer
        elif self.action == 'create':
            return LiveCreateSerializer
        return LiveDetailSerializer
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming lives."""
        queryset = self.get_queryset().filter(
            status='scheduled',
            scheduled_at__gte=timezone.now()
        ).order_by('scheduled_at')[:10]
        serializer = LiveListSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def live_now(self, request):
        """Get currently live streams."""
        queryset = self.get_queryset().filter(status='live')
        serializer = LiveListSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def start(self, request, pk=None):
        """Start a live stream."""
        live = self.get_object()
        
        if live.host != request.user:
            return Response(
                {'error': 'Seul l\'hote peut demarrer le live'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if live.status != 'scheduled':
            return Response(
                {'error': 'Ce live ne peut pas etre demarre'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        Live.objects.filter(pk=live.pk).update(
            status='live',
            started_at=timezone.now()
        )
        
        return Response({'message': 'Live demarre'})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def end(self, request, pk=None):
        """End a live stream."""
        live = self.get_object()
        
        if live.host != request.user:
            return Response(
                {'error': 'Seul l\'hote peut terminer le live'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        Live.objects.filter(pk=live.pk).update(
            status='ended',
            ended_at=timezone.now()
        )
        
        return Response({'message': 'Live termine'})
    
    @action(detail=True, methods=['get', 'post'])
    def questions(self, request, pk=None):
        """Get or submit questions for a live."""
        live = self.get_object()
        
        if request.method == 'GET':
            questions = live.questions.all()
            serializer = LiveQuestionSerializer(questions, many=True, context={'request': request})
            return Response(serializer.data)
        
        elif request.method == 'POST':
            content = request.data.get('content')
            if not content:
                return Response({'error': 'Contenu requis'}, status=status.HTTP_400_BAD_REQUEST)
            
            question = LiveQuestion.objects.create(
                live=live,
                author=request.user,
                content=content
            )
            
            return Response(
                LiveQuestionSerializer(question, context={'request': request}).data,
                status=status.HTTP_201_CREATED
            )
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated], url_path='questions/(?P<question_id>[^/.]+)/vote')
    def vote_question(self, request, pk=None, question_id=None):
        """Vote for a question."""
        try:
            question = LiveQuestion.objects.get(pk=question_id, live_id=pk)
        except LiveQuestion.DoesNotExist:
            return Response({'error': 'Question non trouvee'}, status=status.HTTP_404_NOT_FOUND)
        
        vote, created = LiveQuestionVote.objects.get_or_create(
            question=question,
            user=request.user
        )
        
        if created:
            LiveQuestion.objects.filter(pk=question.pk).update(
                votes_count=question.votes_count + 1
            )
            return Response({'message': 'Vote enregistre'}, status=status.HTTP_201_CREATED)
        
        return Response({'message': 'Deja vote'})
