"""
Views for Social API (Posts, Reels, Comments, Feed)
"""

from django.db.models import Q
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import Post, PostMedia, Reel, Comment, Like, Bookmark, Share, Hashtag
from .serializers import (
    PostListSerializer, PostDetailSerializer, PostCreateSerializer,
    ReelListSerializer, ReelDetailSerializer, ReelCreateSerializer,
    CommentSerializer, CommentCreateSerializer, HashtagSerializer
)


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet for posts."""
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = Post.objects.filter(
            status='published'
        ).select_related('author').prefetch_related('media')
        
        # Filter by author
        author_id = self.request.query_params.get('author')
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        
        # Search
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(content__icontains=search) |
                Q(author__full_name__icontains=search)
            )
        
        return queryset.order_by('-created_at')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return PostCreateSerializer
        return PostDetailSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        Post.objects.filter(pk=instance.pk).update(
            views_count=instance.views_count + 1
        )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post', 'delete'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        """Like/unlike a post."""
        post = self.get_object()
        
        if request.method == 'POST':
            like, created = Like.objects.get_or_create(user=request.user, post=post)
            if created:
                Post.objects.filter(pk=post.pk).update(likes_count=post.likes_count + 1)
                return Response({'message': 'Post aime'}, status=status.HTTP_201_CREATED)
            return Response({'message': 'Deja aime'})
        
        elif request.method == 'DELETE':
            deleted, _ = Like.objects.filter(user=request.user, post=post).delete()
            if deleted:
                Post.objects.filter(pk=post.pk).update(likes_count=max(0, post.likes_count - 1))
                return Response({'message': 'Like retire'})
            return Response({'message': 'Non aime'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post', 'delete'], permission_classes=[IsAuthenticated])
    def bookmark(self, request, pk=None):
        """Bookmark/unbookmark a post."""
        post = self.get_object()
        
        if request.method == 'POST':
            bookmark, created = Bookmark.objects.get_or_create(user=request.user, post=post)
            if created:
                return Response({'message': 'Post sauvegarde'}, status=status.HTTP_201_CREATED)
            return Response({'message': 'Deja sauvegarde'})
        
        elif request.method == 'DELETE':
            deleted, _ = Bookmark.objects.filter(user=request.user, post=post).delete()
            if deleted:
                return Response({'message': 'Sauvegarde retiree'})
            return Response({'message': 'Non sauvegarde'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def share(self, request, pk=None):
        """Record a share."""
        post = self.get_object()
        platform = request.data.get('platform', '')
        
        Share.objects.create(user=request.user, post=post, platform=platform)
        Post.objects.filter(pk=post.pk).update(shares_count=post.shares_count + 1)
        
        return Response({'message': 'Partage enregistre'})
    
    @action(detail=True, methods=['get', 'post'])
    def comments(self, request, pk=None):
        """Get or create comments for a post."""
        post = self.get_object()
        
        if request.method == 'GET':
            comments = Comment.objects.filter(
                post=post, parent=None, is_hidden=False
            ).select_related('author')
            serializer = CommentSerializer(comments, many=True, context={'request': request})
            return Response(serializer.data)
        
        elif request.method == 'POST':
            if not post.allow_comments:
                return Response(
                    {'error': 'Les commentaires sont desactives'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            serializer = CommentCreateSerializer(
                data={**request.data, 'post': post.id},
                context={'request': request}
            )
            if serializer.is_valid():
                comment = serializer.save()
                
                # Update parent reply count if it's a reply
                if comment.parent:
                    Comment.objects.filter(pk=comment.parent.pk).update(
                        replies_count=comment.parent.replies_count + 1
                    )
                
                # Update post comment count
                Post.objects.filter(pk=post.pk).update(
                    comments_count=post.comments_count + 1
                )
                
                return Response(
                    CommentSerializer(comment, context={'request': request}).data,
                    status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReelViewSet(viewsets.ModelViewSet):
    """ViewSet for reels."""
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = Reel.objects.filter(
            status='published'
        ).select_related('author')
        
        # Filter by author
        author_id = self.request.query_params.get('author')
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        
        return queryset.order_by('-created_at')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ReelListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ReelCreateSerializer
        return ReelDetailSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        Reel.objects.filter(pk=instance.pk).update(
            views_count=instance.views_count + 1
        )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def feed(self, request):
        """Get personalized reel feed."""
        queryset = self.get_queryset().order_by('?')[:20]  # Random for now
        serializer = ReelListSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['post', 'delete'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        """Like/unlike a reel."""
        reel = self.get_object()
        
        if request.method == 'POST':
            like, created = Like.objects.get_or_create(user=request.user, reel=reel)
            if created:
                Reel.objects.filter(pk=reel.pk).update(likes_count=reel.likes_count + 1)
                return Response({'message': 'Reel aime'}, status=status.HTTP_201_CREATED)
            return Response({'message': 'Deja aime'})
        
        elif request.method == 'DELETE':
            deleted, _ = Like.objects.filter(user=request.user, reel=reel).delete()
            if deleted:
                Reel.objects.filter(pk=reel.pk).update(likes_count=max(0, reel.likes_count - 1))
                return Response({'message': 'Like retire'})
            return Response({'message': 'Non aime'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post', 'delete'], permission_classes=[IsAuthenticated])
    def bookmark(self, request, pk=None):
        """Bookmark/unbookmark a reel."""
        reel = self.get_object()
        
        if request.method == 'POST':
            bookmark, created = Bookmark.objects.get_or_create(user=request.user, reel=reel)
            if created:
                return Response({'message': 'Reel sauvegarde'}, status=status.HTTP_201_CREATED)
            return Response({'message': 'Deja sauvegarde'})
        
        elif request.method == 'DELETE':
            deleted, _ = Bookmark.objects.filter(user=request.user, reel=reel).delete()
            if deleted:
                return Response({'message': 'Sauvegarde retiree'})
            return Response({'message': 'Non sauvegarde'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['get', 'post'])
    def comments(self, request, pk=None):
        """Get or create comments for a reel."""
        reel = self.get_object()
        
        if request.method == 'GET':
            comments = Comment.objects.filter(
                reel=reel, parent=None, is_hidden=False
            ).select_related('author')
            serializer = CommentSerializer(comments, many=True, context={'request': request})
            return Response(serializer.data)
        
        elif request.method == 'POST':
            if not reel.allow_comments:
                return Response(
                    {'error': 'Les commentaires sont desactives'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            serializer = CommentCreateSerializer(
                data={**request.data, 'reel': reel.id},
                context={'request': request}
            )
            if serializer.is_valid():
                comment = serializer.save()
                Reel.objects.filter(pk=reel.pk).update(
                    comments_count=reel.comments_count + 1
                )
                return Response(
                    CommentSerializer(comment, context={'request': request}).data,
                    status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet for comments."""
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        return Comment.objects.filter(is_hidden=False).select_related('author')
    
    @action(detail=True, methods=['post', 'delete'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        """Like/unlike a comment."""
        comment = self.get_object()
        
        if request.method == 'POST':
            like, created = Like.objects.get_or_create(user=request.user, comment=comment)
            if created:
                Comment.objects.filter(pk=comment.pk).update(likes_count=comment.likes_count + 1)
                return Response({'message': 'Commentaire aime'}, status=status.HTTP_201_CREATED)
            return Response({'message': 'Deja aime'})
        
        elif request.method == 'DELETE':
            deleted, _ = Like.objects.filter(user=request.user, comment=comment).delete()
            if deleted:
                Comment.objects.filter(pk=comment.pk).update(likes_count=max(0, comment.likes_count - 1))
                return Response({'message': 'Like retire'})
            return Response({'message': 'Non aime'}, status=status.HTTP_404_NOT_FOUND)


class FeedView(generics.ListAPIView):
    """Combined feed of posts and reels from followed users."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        from itertools import chain
        from users.models import UserFollow
        
        # Get followed users
        following_ids = UserFollow.objects.filter(
            follower=request.user
        ).values_list('following_id', flat=True)
        
        # Include own content
        user_ids = list(following_ids) + [request.user.id]
        
        # Get posts
        posts = Post.objects.filter(
            author_id__in=user_ids,
            status='published',
            visibility__in=['public', 'followers']
        ).select_related('author').prefetch_related('media')[:50]
        
        # Get reels
        reels = Reel.objects.filter(
            author_id__in=user_ids,
            status='published'
        ).select_related('author')[:50]
        
        # Combine and sort by date
        feed = sorted(
            chain(
                [{'type': 'post', 'item': p, 'date': p.created_at} for p in posts],
                [{'type': 'reel', 'item': r, 'date': r.created_at} for r in reels]
            ),
            key=lambda x: x['date'],
            reverse=True
        )[:30]
        
        # Serialize
        result = []
        for item in feed:
            if item['type'] == 'post':
                result.append({
                    'type': 'post',
                    'data': PostListSerializer(item['item'], context={'request': request}).data
                })
            else:
                result.append({
                    'type': 'reel',
                    'data': ReelListSerializer(item['item'], context={'request': request}).data
                })
        
        return Response(result)


class TrendingHashtagsView(generics.ListAPIView):
    """Get trending hashtags."""
    serializer_class = HashtagSerializer
    
    def get_queryset(self):
        return Hashtag.objects.order_by('-posts_count', '-reels_count')[:20]


class BookmarkedContentView(generics.ListAPIView):
    """Get user's bookmarked posts and reels."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Get bookmarked posts
        post_ids = Bookmark.objects.filter(
            user=request.user, post__isnull=False
        ).values_list('post_id', flat=True)
        posts = Post.objects.filter(id__in=post_ids).select_related('author')
        
        # Get bookmarked reels
        reel_ids = Bookmark.objects.filter(
            user=request.user, reel__isnull=False
        ).values_list('reel_id', flat=True)
        reels = Reel.objects.filter(id__in=reel_ids).select_related('author')
        
        return Response({
            'posts': PostListSerializer(posts, many=True, context={'request': request}).data,
            'reels': ReelListSerializer(reels, many=True, context={'request': request}).data
        })
