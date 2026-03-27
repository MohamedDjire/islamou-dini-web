from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Report, Ban
from .serializers import ReportSerializer, BanSerializer

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Report.objects.all()
        return Report.objects.filter(reporter=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAdminUser])
    def pending(self, request):
        pending_reports = Report.objects.filter(status='pending')
        serializer = self.get_serializer(pending_reports, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def resolve(self, request, pk=None):
        report = self.get_object()
        action_taken = request.data.get('action_taken', False)
        report.status = 'resolved' if action_taken else 'dismissed'
        report.save()
        return Response({'status': report.status})

class BanViewSet(viewsets.ModelViewSet):
    queryset = Ban.objects.all()
    serializer_class = BanSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def perform_create(self, serializer):
        serializer.save(moderator=self.request.user)
    
    @action(detail=True, methods=['post'])
    def unban(self, request, pk=None):
        ban = self.get_object()
        ban.is_active = False
        ban.save()
        return Response({'status': 'User unbanned'})
