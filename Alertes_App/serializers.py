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
        fields = [
            'id',
            'status',
            'severity',
            'timestamp',
            'description_ai',
            'pourc_ai',
            'video_url',
            'camera', # ID de la caméra
            'taken_by', # ID de l'AgentUser
        ]

class AlertDetailSerializer(serializers.ModelSerializer):
    # On récupère le nom de la caméra via la relation ForeignKey
    camera_name = serializers.CharField(source='camera.name', read_only=True)
    camera_location = serializers.CharField(source='camera.location', read_only=True)

    # On va chercher le nom de l'utilisateur via la double relation : Alert -> AgentUser -> User
    taken_by_username = serializers.CharField(source='taken_by.user.username', read_only=True, allow_null=True)
    user_matricule = serializers.CharField(source='taken_by.matricule', read_only=True, allow_null=True)
    user_Role = serializers.CharField(source='taken_by.role', read_only=True, allow_null=True)
    
    class Meta:
        model = Alert
        fields = [
            'id',
            'status',
            'severity',
            'timestamp',
            'description_ai',
            'pourc_ai',
            'video_url',
            'camera_name', # Nom de la caméra
            'camera_location', # Emplacement de la caméra
            'taken_by_username', # Nom de l'utilisateur qui a pris l'alerte
            'user_matricule', # Matricule de l'agent
            'user_Role', # Rôle de l'agent
        ]

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
    