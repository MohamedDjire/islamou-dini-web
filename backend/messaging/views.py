"""
Views for Messaging and Notifications API
"""

from django.utils import timezone
from django.db.models import Q
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Conversation, Message, MessageReaction, Notification, NotificationSetting
from .serializers import (
    ConversationSerializer, ConversationDetailSerializer,
    MessageSerializer, MessageCreateSerializer,
    NotificationSerializer, NotificationSettingSerializer
)


class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet for conversations/DMs."""
    permission_classes = [IsAuthenticated]
    serializer_class = ConversationSerializer
    
    def get_queryset(self):
        return Conversation.objects.filter(
            Q(participant_one=self.request.user) | Q(participant_two=self.request.user)
        ).select_related('participant_one', 'participant_two', 'last_message')
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ConversationDetailSerializer
        return ConversationSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Mark as read
        instance.mark_as_read(request.user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def start(self, request):
        """Start a new conversation with a user."""
        from users.models import User, UserBlock
        
        other_user_id = request.data.get('user_id')
        if not other_user_id:
            return Response(
                {'error': 'user_id requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            other_user = User.objects.get(pk=other_user_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'Utilisateur non trouve'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if other_user == request.user:
            return Response(
                {'error': 'Impossible de demarrer une conversation avec vous-meme'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if blocked
        if UserBlock.objects.filter(
            Q(blocker=request.user, blocked=other_user) |
            Q(blocker=other_user, blocked=request.user)
        ).exists():
            return Response(
                {'error': 'Conversation impossible'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if conversation exists
        conversation = Conversation.objects.filter(
            Q(participant_one=request.user, participant_two=other_user) |
            Q(participant_one=other_user, participant_two=request.user)
        ).first()
        
        if conversation:
            serializer = ConversationSerializer(conversation, context={'request': request})
            return Response(serializer.data)
        
        # Create new conversation
        conversation = Conversation.objects.create(
            participant_one=request.user,
            participant_two=other_user
        )
        
        serializer = ConversationSerializer(conversation, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get', 'post'])
    def messages(self, request, pk=None):
        """Get or send messages in a conversation."""
        conversation = self.get_object()
        
        # Check if blocked
        if (conversation.participant_one == request.user and conversation.is_blocked_by_two) or \
           (conversation.participant_two == request.user and conversation.is_blocked_by_one):
            return Response(
                {'error': 'Conversation bloquee'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if request.method == 'GET':
            messages = conversation.messages.filter(is_deleted=False).order_by('-created_at')
            
            # Pagination
            offset = int(request.query_params.get('offset', 0))
            limit = int(request.query_params.get('limit', 50))
            messages = messages[offset:offset + limit]
            
            serializer = MessageSerializer(messages, many=True, context={'request': request})
            return Response(serializer.data)
        
        elif request.method == 'POST':
            serializer = MessageCreateSerializer(data=request.data)
            if serializer.is_valid():
                message = Message.objects.create(
                    conversation=conversation,
                    sender=request.user,
                    **serializer.validated_data
                )
                
                # Update conversation
                conversation.last_message = message
                conversation.last_message_at = message.created_at
                
                # Update unread count for other user
                if conversation.participant_one == request.user:
                    conversation.unread_count_two += 1
                else:
                    conversation.unread_count_one += 1
                
                conversation.save()
                
                return Response(
                    MessageSerializer(message, context={'request': request}).data,
                    status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark conversation as read."""
        conversation = self.get_object()
        conversation.mark_as_read(request.user)
        return Response({'message': 'Marque comme lu'})
    
    @action(detail=True, methods=['post'])
    def block(self, request, pk=None):
        """Block the other user in conversation."""
        conversation = self.get_object()
        
        if conversation.participant_one == request.user:
            conversation.is_blocked_by_one = True
        else:
            conversation.is_blocked_by_two = True
        conversation.save()
        
        return Response({'message': 'Utilisateur bloque'})
    
    @action(detail=True, methods=['post'])
    def unblock(self, request, pk=None):
        """Unblock the other user in conversation."""
        conversation = self.get_object()
        
        if conversation.participant_one == request.user:
            conversation.is_blocked_by_one = False
        else:
            conversation.is_blocked_by_two = False
        conversation.save()
        
        return Response({'message': 'Utilisateur debloque'})


class MessageViewSet(viewsets.ModelViewSet):
    """ViewSet for messages."""
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer
    
    def get_queryset(self):
        return Message.objects.filter(
            Q(conversation__participant_one=self.request.user) |
            Q(conversation__participant_two=self.request.user),
            is_deleted=False
        )
    
    @action(detail=True, methods=['post'])
    def react(self, request, pk=None):
        """Add reaction to a message."""
        message = self.get_object()
        emoji = request.data.get('emoji')
        
        if not emoji:
            return Response({'error': 'emoji requis'}, status=status.HTTP_400_BAD_REQUEST)
        
        reaction, created = MessageReaction.objects.get_or_create(
            message=message,
            user=request.user,
            emoji=emoji
        )
        
        if created:
            return Response({'message': 'Reaction ajoutee'}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Reaction deja presente'})
    
    @action(detail=True, methods=['delete'])
    def unreact(self, request, pk=None):
        """Remove reaction from a message."""
        message = self.get_object()
        emoji = request.data.get('emoji')
        
        deleted, _ = MessageReaction.objects.filter(
            message=message,
            user=request.user,
            emoji=emoji
        ).delete()
        
        if deleted:
            return Response({'message': 'Reaction retiree'})
        return Response({'error': 'Reaction non trouvee'}, status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self, request, *args, **kwargs):
        """Soft delete a message."""
        message = self.get_object()
        
        if message.sender != request.user:
            return Response(
                {'error': 'Non autorise'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        message.is_deleted = True
        message.content = ''
        message.save()
        
        return Response({'message': 'Message supprime'})


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for notifications."""
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user
        ).select_related('actor')
    
    @action(detail=False, methods=['get'])
    def unread(self, request):
        """Get unread notifications."""
        notifications = self.get_queryset().filter(is_read=False)
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def count(self, request):
        """Get unread count."""
        count = self.get_queryset().filter(is_read=False).count()
        return Response({'unread_count': count})
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark notification as read."""
        notification = self.get_object()
        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save()
        return Response({'message': 'Marque comme lu'})
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all notifications as read."""
        self.get_queryset().filter(is_read=False).update(
            is_read=True,
            read_at=timezone.now()
        )
        return Response({'message': 'Toutes les notifications marquees comme lues'})


class NotificationSettingView(generics.RetrieveUpdateAPIView):
    """View for notification settings."""
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSettingSerializer
    
    def get_object(self):
        settings, created = NotificationSetting.objects.get_or_create(
            user=self.request.user
        )
        return settings
