from rest_framework import serializers
from .models import AgentUser, Camera, Alert, Rapport, Notification, Compte
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class AgentUserSerializer(serializers.ModelSerializer):
    user = UserSerializer() # Affiche les détails du User imbriqué
    class Meta:
        model = AgentUser
        fields = ['id', 'user', 'matricule', 'role', 'phone_number', 'image_url']

class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = '__all__'

class AlertSerializer(serializers.ModelSerializer):
    # Affiche le nom de la caméra et le nom de l'agent, pas seulement leurs IDs
    camera = serializers.StringRelatedField()
    taken_by = serializers.StringRelatedField()

    class Meta:
        model = Alert
        fields = ['id', 'camera', 'taken_by', 'pourc_ai', 'description_ai', 'severity', 'status', 'timestamp', 'video_url']

class RapportSerializer(serializers.ModelSerializer):
    alert = serializers.StringRelatedField()
    author = serializers.StringRelatedField()

    class Meta:
        model = Rapport
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    alert = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = Notification
        fields = '__all__'

class CompteSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Compte
        fields = '__all__'
    