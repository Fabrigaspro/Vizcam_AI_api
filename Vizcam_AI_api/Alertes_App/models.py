# api/models.py
from django.db import models
from django.contrib.auth.models import User # SUGGESTION: Utiliser le User de base de Django
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

# SUGGESTION : Il est souvent plus simple de lier un profil au modèle User de Django.
# Cela vous donne gratuitement la gestion des mots de passe, des permissions, etc. 670906465 C:\Users\Fabpro\Pictures\AESP.jpg
class AgentUser(models.Model):
    ROLE_CHOICES = [
        ('agent', 'Agent de Sécurité'),
        ('admin', 'Administrateur'),
        ('manager', 'Manager'),
    ]
    
    # On lie ce profil à un utilisateur Django. OneToOneField garantit un seul profil par utilisateur.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matricule = models.CharField(max_length=50, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='agent')
    phone_number = models.CharField(max_length=20, blank=True)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Camera(models.Model):
    LOCATION_CHOICES = [
        ('entree', 'Entrée'),
        ('caisse', 'Caisses'),
        ('rayon', 'Rayon'),
        ('parking', 'Parking'),
        ('reserve', 'Réserve'),
    ]

    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=20, choices=LOCATION_CHOICES)
    ip_address = models.GenericIPAddressField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.location})"

class Alert(models.Model):
    STATUS_CHOICES = [
        ('new', 'Nouvelle'),
        ('in_progress', 'En cours'),
        ('closed', 'Clôturée'),
    ]
    SEVERITY_CHOICES = [
        ('low', 'Faible'),
        ('medium', 'Moyenne'),
        ('high', 'Élevée'),
        ('critical', 'Critique'),
    ]

    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name='alerts')
    taken_by = models.ForeignKey(AgentUser, on_delete=models.SET_NULL, null=True, blank=True)
    pourc_ai = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], help_text="Pourcentage de confiance de l'IA")
    description_ai = models.TextField(max_length=200)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    timestamp = models.DateTimeField(default=timezone.now)
    video_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Alerte ({self.severity}) sur {self.camera.name} le {self.timestamp.strftime('%d/%m/%Y %H:%M')}"

class Rapport(models.Model):
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, related_name='reports')
    author = models.ForeignKey(AgentUser, on_delete=models.CASCADE)
    description = models.TextField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rapport pour l'alerte {self.alert.id} par {self.author}"

class Notification(models.Model):
    user = models.ForeignKey(AgentUser, on_delete=models.CASCADE, related_name='notifications')
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification pour {self.user}: {self.title}"

# NOTE: Ce modèle gére les préférences utilisateur. On le lie à AgentUser.
class Compte(models.Model):
    LANGUAGE_CHOICES = [
        ('fr', 'Francais'),
        ('en', 'English'),
    ]
    agent = models.OneToOneField(AgentUser, on_delete=models.CASCADE, related_name='account_settings')
    langue = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='fr')
    sensibility_alert = models.IntegerField(default=70, validators=[MinValueValidator(0), MaxValueValidator(100)])
    notifications_on = models.BooleanField(default=True)
    vibration_on = models.BooleanField(default=True)
    son_notif_on = models.BooleanField(default=True)

    def __str__(self):
        return f"Paramètres pour {self.agent}"