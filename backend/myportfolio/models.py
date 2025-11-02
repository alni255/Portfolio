from django.db import models
from django.core.validators import MinLengthValidator
import uuid
from django.utils import timezone

class ContactMessage(models.Model):
    # Identifiant unique pour plus de sécurité
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Informations de contact
    name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)],
        verbose_name="Nom complet"
    )
    email = models.EmailField(verbose_name="Adresse email")
    subject = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(5)],
        verbose_name="Sujet du message"
    )
    message = models.TextField(
        validators=[MinLengthValidator(10)],
        verbose_name="Message"
    )
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")
    is_read = models.BooleanField(default=False, verbose_name="Lu")
    is_archived = models.BooleanField(default=False, verbose_name="Archivé")
    
    # Pour le suivi des réponses
    replied_at = models.DateTimeField(null=True, blank=True, verbose_name="Date de réponse")
    admin_notes = models.TextField(blank=True, verbose_name="Notes administrateur")
    
    # IP et user agent pour la sécurité
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="Adresse IP")
    user_agent = models.TextField(blank=True, verbose_name="User Agent")
    
    # Statut du message
    STATUS_CHOICES = [
        ('new', 'Nouveau'),
        ('read', 'Lu'),
        ('replied', 'Répondu'),
        ('spam', 'Spam'),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name="Statut"
    )

    def __str__(self):
        return f"{self.name} - {self.subject}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['is_read']),
        ]

    @property
    def short_message(self):
        """Retourne un aperçu du message"""
        if len(self.message) > 100:
            return self.message[:100] + '...'
        return self.message

    def mark_as_read(self):
        """Marquer le message comme lu"""
        self.is_read = True
        self.status = 'read'
        self.save()

    def mark_as_replied(self):
        """Marquer le message comme répondu"""
        self.is_read = True
        self.status = 'replied'
        self.replied_at = timezone.now()
        self.save()

    def is_recent(self):
        """Vérifier si le message est récent (moins de 24h)"""
        return timezone.now() - self.created_at < timezone.timedelta(days=1)