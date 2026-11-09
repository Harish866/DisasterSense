from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Count

from .forms import IncidentReportForm
from .models import Incident


def submit_incident(request):
    if request.method == 'POST':
        form = IncidentReportForm(request.POST)

        if form.is_valid():
            incident = form.save()

            try:
                from ml_models.predict import predict_incident
                result = predict_incident(incident.description)
                incident.ai_predicted_type = result["predicted_type"]
                incident.ai_confidence = result["model_score"]
                incident.ai_explanation = (
                    f"AI predicted {result['predicted_type']} with a model score of "
                    f"{result['model_score'] * 100:.2f}%. "
                    "This is advisory and requires human review."
                )
            except Exception as error:
                print("AI classification error:", error)

            try:
                from ml_models.priority_engine import assess_priority
                priority_result = assess_priority(incident)
                incident.priority_score = priority_result["score"]
                incident.suggested_priority = priority_result["priority"]
                incident.priority_explanation = priority_result["explanation"]
            except Exception as error:
                print("Priority assessment error:", error)

            try:
                from ml_models.information_extractor import extract_information
                intelligence = extract_information(incident.description)
                incident.people_trapped = intelligence["people_trapped"]
                incident.injuries_reported = intelligence["injuries_reported"]
                incident.injured_count = intelligence["injured_count"]
                incident.rescue_required = intelligence["rescue_required"]
                incident.evacuation_required = intelligence["evacuation_required"]
                incident.intelligence_summary = intelligence["summary"]
            except Exception as error:
                print("Information extraction error:", error)

            # AI suggestions never overwrite the coordinator's operational priority.
            incident.save()
            messages.success(request, f"Emergency report #{incident.id} submitted successfully.")

            if incident.ai_predicted_type:
                messages.info(request, f"AI category: {incident.ai_predicted_type}")
            if incident.priority_explanation:
                messages.info(
                    request,
                    f"Recommended priority: {incident.suggested_priority} "
                    f"(Score: {incident.priority_score}/100)"
                )
            if incident.intelligence_summary:
                messages.info(request, "Incident intelligence extracted successfully.")

            return redirect('submit_incident')
    else:
        form = IncidentReportForm()

    return render(request, 'emergency_report.html', {'form': form})


def dashboard(request):
    all_incidents = Incident.objects.all()

    # Global operational statistics (independent of search/filter selections).
    total_incidents = all_incidents.count()
    active_incidents = all_incidents.exclude(status='RESOLVED').count()
    critical_incidents = all_incidents.filter(priority='CRITICAL').count()
    resolved_incidents = all_incidents.filter(status='RESOLVED').count()
    unassessed_incidents = all_incidents.filter(priority='UNASSESSED').count()
    under_review_incidents = all_incidents.filter(status='UNDER_REVIEW').count()

    category_counts = (
        all_incidents.values('incident_type')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    # Apply filters to the incident queue and map, not to global KPI totals.
    incidents = all_incidents
    search_query = request.GET.get('search', '').strip()
    selected_type = request.GET.get('type', '')
    selected_priority = request.GET.get('priority', '')
    selected_status = request.GET.get('status', '')

    if search_query:
        incidents = incidents.filter(
            Q(title__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(location__icontains=search_query)
        )
    if selected_type:
        incidents = incidents.filter(incident_type=selected_type)
    if selected_priority:
        incidents = incidents.filter(priority=selected_priority)
    if selected_status:
        incidents = incidents.filter(status=selected_status)

    incident_list = list(incidents.order_by('-created_at')[:100])

    for incident in incident_list:
        incident.ai_score_percent = (
            round(incident.ai_confidence * 100, 2)
            if incident.ai_confidence is not None else None
        )

    latest_incident = all_incidents.first()
    if latest_incident and latest_incident.ai_confidence is not None:
        latest_incident.ai_score_percent = round(latest_incident.ai_confidence * 100, 2)
    elif latest_incident:
        latest_incident.ai_score_percent = None

    context = {
        'total_incidents': total_incidents,
        'active_incidents': active_incidents,
        'critical_incidents': critical_incidents,
        'resolved_incidents': resolved_incidents,
        'unassessed_incidents': unassessed_incidents,
        'under_review_incidents': under_review_incidents,
        'category_counts': category_counts,
        'incident_list': incident_list,
        'latest_incident': latest_incident,
        'search_query': search_query,
        'selected_type': selected_type,
        'selected_priority': selected_priority,
        'selected_status': selected_status,
        'incident_types': Incident.INCIDENT_TYPES,
        'priority_levels': Incident.PRIORITY_LEVELS,
        'status_choices': Incident.STATUS_CHOICES,
    }
    return render(request, 'dashboard.html', context)


def incident_detail(request, incident_id):
    incident = get_object_or_404(Incident, id=incident_id)

    if request.method == 'POST':
        incident_type = request.POST.get('incident_type', '')
        priority = request.POST.get('priority', '')
        status = request.POST.get('status', '')

        valid_types = {value for value, label in Incident.INCIDENT_TYPES}
        # UNASSESSED is an initial state, not a completed coordinator decision.
        valid_priorities = {
            value for value, label in Incident.PRIORITY_LEVELS
            if value != 'UNASSESSED'
        }
        valid_statuses = {value for value, label in Incident.STATUS_CHOICES}

        if (
            incident_type not in valid_types
            or priority not in valid_priorities
            or status not in valid_statuses
        ):
            messages.error(request, "Invalid review information. Please check your selections.")
        else:
            incident.incident_type = incident_type
            incident.priority = priority
            incident.status = status
            incident.save()
            messages.success(request, f"Incident #{incident.id} has been updated successfully.")
            return redirect('incident_detail', incident_id=incident.id)

    ai_score_percent = (
        round(incident.ai_confidence * 100, 2)
        if incident.ai_confidence is not None else None
    )
    context = {
        'incident': incident,
        'incident_types': Incident.INCIDENT_TYPES,
        'priority_levels': [
            (value, label) for value, label in Incident.PRIORITY_LEVELS
            if value != 'UNASSESSED'
        ],
        'status_choices': Incident.STATUS_CHOICES,
        'ai_score_percent': ai_score_percent,
    }
    return render(request, 'incident_detail.html', context)
