
from django.contrib import admin
from .models import Incident


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'incident_type',
        'priority',
        'severity',
        'status',
        'created_at',
    )

    list_filter = (
        'incident_type',
        'priority',
        'status',
    )

    search_fields = (
        'title',
        'description',
        'location',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )
