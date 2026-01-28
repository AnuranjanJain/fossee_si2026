"""
Models for Chemical Equipment Parameter Visualizer.
"""
from django.db import models
from django.contrib.auth.models import User
import json


class UploadSession(models.Model):
    """Represents a single CSV upload session."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='upload_sessions')
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    record_count = models.IntegerField(default=0)
    summary_json = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.filename} ({self.uploaded_at.strftime('%Y-%m-%d %H:%M')})"
    
    @property
    def summary(self):
        """Parse and return the summary as a dictionary."""
        if self.summary_json:
            return json.loads(self.summary_json)
        return {}
    
    @summary.setter
    def summary(self, value):
        """Store the summary as JSON."""
        self.summary_json = json.dumps(value)
    
    @classmethod
    def cleanup_old_sessions(cls, user, keep_count=5):
        """Keep only the last N sessions for a user."""
        sessions = cls.objects.filter(user=user).order_by('-uploaded_at')
        if sessions.count() > keep_count:
            # Get IDs of sessions to delete
            ids_to_delete = sessions[keep_count:].values_list('id', flat=True)
            cls.objects.filter(id__in=list(ids_to_delete)).delete()


class Equipment(models.Model):
    """Chemical equipment with parameters."""
    EQUIPMENT_TYPES = [
        ('Pump', 'Pump'),
        ('Compressor', 'Compressor'),
        ('Valve', 'Valve'),
        ('HeatExchanger', 'Heat Exchanger'),
        ('Reactor', 'Reactor'),
        ('Condenser', 'Condenser'),
        ('Other', 'Other'),
    ]
    
    session = models.ForeignKey(UploadSession, on_delete=models.CASCADE, related_name='equipment')
    name = models.CharField(max_length=100)
    equipment_type = models.CharField(max_length=50, choices=EQUIPMENT_TYPES)
    flowrate = models.FloatField()
    pressure = models.FloatField()
    temperature = models.FloatField()
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Equipment'
    
    def __str__(self):
        return f"{self.name} ({self.equipment_type})"
