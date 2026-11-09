
from django.db import models


class Incident(models.Model):

    INCIDENT_TYPES = [
        ('FIRE', 'Fire'),
        ('FLOOD', 'Flood'),
        ('EARTHQUAKE', 'Earthquake'),
        ('MEDICAL', 'Medical Emergency'),
        ('ACCIDENT', 'Accident'),
        ('BUILDING_COLLAPSE', 'Building Collapse'),
        ('LANDSLIDE', 'Landslide'),
        ('OTHER', 'Other'),
    ]

    PRIORITY_LEVELS = [
    ('UNASSESSED', 'Unassessed'),
    ('CRITICAL', 'Critical'),
    ('HIGH', 'High'),
    ('MEDIUM', 'Medium'),
    ('LOW', 'Low'),
    ]

    STATUS_CHOICES = [
        ('RECEIVED', 'Received'),
        ('UNDER_REVIEW', 'Under Review'),
        ('CONFIRMED', 'Confirmed'),
        ('DISPATCHED', 'Dispatched'),
        ('RESOLVED', 'Resolved'),
    ]

    # BASIC INCIDENT INFORMATION
    title = models.CharField(max_length=200)
    description = models.TextField()

    incident_type = models.CharField(
        max_length=30,
        choices=INCIDENT_TYPES,
        default='OTHER'
    )

    location = models.CharField(max_length=255)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    severity = models.PositiveSmallIntegerField(default=1)
    people_affected = models.PositiveIntegerField(default=0)

    # OPERATIONAL PRIORITY
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_LEVELS,
        default='UNASSESSED'
    )

    priority_score = models.FloatField(default=0)

    suggested_priority = models.CharField(
        max_length=10,
        choices=PRIORITY_LEVELS,
        default='LOW'
    )

    priority_explanation = models.TextField(blank=True)

    # AI INCIDENT CLASSIFICATION
    ai_predicted_type = models.CharField(
        max_length=30,
        blank=True
    )

    ai_confidence = models.FloatField(
        null=True,
        blank=True
    )

    ai_explanation = models.TextField(blank=True)

    # INCIDENT INTELLIGENCE EXTRACTION
    people_trapped = models.BooleanField(
        null=True,
        blank=True
    )

    injuries_reported = models.BooleanField(
        null=True,
        blank=True
    )

    injured_count = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    rescue_required = models.BooleanField(
        null=True,
        blank=True
    )

    evacuation_required = models.BooleanField(
        null=True,
        blank=True
    )

    intelligence_summary = models.TextField(blank=True)

    # INCIDENT STATUS
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='RECEIVED'
    )

    # DUPLICATE DETECTION
    is_duplicate = models.BooleanField(default=False)

    duplicate_of = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='duplicate_reports'
    )

    # TIMESTAMPS
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.get_incident_type_display()}"
