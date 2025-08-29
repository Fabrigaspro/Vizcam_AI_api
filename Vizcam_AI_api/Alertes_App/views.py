from django.shortcuts import render
# Creation des views.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import AgentUser, Camera, Alert, Rapport, Notification, Compte
from .serializers import (
    AgentUserSerializer, CameraSerializer,
    AlertSerializer, RapportSerializer, NotificationSerializer,
    CompteSerializer
)

# IsAuthenticated garantit que seuls les utilisateurs connectés peuvent accéder à ces données
class AgentUserViewSet(viewsets.ModelViewSet):
    queryset = AgentUser.objects.all()
    serializer_class = AgentUserSerializer
    permission_classes = [IsAuthenticated]

class CameraViewSet(viewsets.ModelViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer
    permission_classes = [IsAuthenticated]

class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all().order_by('-timestamp')
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def take_alert(self, request, pk=None):
        alert = self.get_object()
        agent_user = AgentUser.objects.get(user=request.user)
        alert.taken_by = agent_user
        alert.status = 'in_progress'
        alert.save()
        return Response({'status': 'alert Prise et en cours...'})
    
    @action(detail=True, methods=['post'])
    def close_alert(self, request, pk=None):
        alert = self.get_object()
        alert.status = 'closed'
        alert.save()
        return Response({'status': 'alert cloturée !'})

class RapportViewSet(viewsets.ModelViewSet):
    queryset = Rapport.objects.all()
    serializer_class = RapportSerializer
    permission_classes = [IsAuthenticated]

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'notification read'})

class CompteViewSet(viewsets.ModelViewSet):
    queryset = Compte.objects.all()
    serializer_class = CompteSerializer
    permission_classes = [IsAuthenticated]