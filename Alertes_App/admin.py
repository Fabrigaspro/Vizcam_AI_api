from django.contrib import admin
from .models import AgentUser, Camera, Alert, Rapport, Notification, Compte

class AgentUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'matricule', 'role', 'phone_number', 'image_url')
    list_filter = ('matricule', 'role')
    search_fields = ('user__name', 'matricule')

class CameraAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'location')
    ordering = ('-created_at',)

class AlertAdmin(admin.ModelAdmin):
    list_display = ('camera', 'taken_by', 'pourc_ai', 'description_ai', 'severity', 'status', 'timestamp', 'video_url')
    list_filter = ('status', 'severity', 'camera')
    search_fields = ('camera__name', 'status')
    ordering = ('-timestamp',)
    date_hierarchy = 'timestamp'

class RapportAdmin(admin.ModelAdmin):
    list_display = ('alert', 'author', 'description', 'timestamp')
    list_filter = ('alert', 'author')
    search_fields = ('alert_name', 'author_name', 'timestamp')
    ordering = ('-timestamp',)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'alert', 'title', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('alert_name', 'user_name', 'is_read')
    ordering = ('-created_at',)

class CompteAdmin(admin.ModelAdmin):
    list_display = ('agent', 'langue', 'sensibility_alert', 'notifications_on', 'vibration_on', 'son_notif_on')
    list_filter = ('agent', 'sensibility_alert')
    search_fields = ('agent__name', 'sensibility_alert')

# Enregistrement avec la personnalisation
admin.site.register(AgentUser, AgentUserAdmin)
admin.site.register(Camera, CameraAdmin)
admin.site.register(Alert, AlertAdmin)
admin.site.register(Rapport, RapportAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Compte, CompteAdmin)