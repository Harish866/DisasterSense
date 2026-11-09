document.addEventListener("DOMContentLoaded", function () {
    const mapElement = document.getElementById("incident-map");

    if (!mapElement) return;

    if (typeof L === "undefined") {
        mapElement.textContent =
            "Map library could not be loaded. Check your internet connection.";
        return;
    }

    // Initialize map
    const map = L.map(mapElement).setView([20.5937, 78.9629], 5);

    // OpenStreetMap tiles
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution:
            '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 19
    }).addTo(map);

    // Marker colours based on coordinator-assigned priority
    const colors = {
        CRITICAL: "#ef4444",
        HIGH: "#f97316",
        MEDIUM: "#eab308",
        LOW: "#22c55e",
        UNASSESSED: "#94a3b8"
    };

    // Read actual incident records rendered by Django
    const records = document.querySelectorAll(
        "#map-records .map-record"
    );

    const markers = [];

    records.forEach(function (record) {
        const lat = Number(record.dataset.lat);
        const lng = Number(record.dataset.lng);

        // Ignore missing or invalid coordinates
        if (
            !Number.isFinite(lat) ||
            !Number.isFinite(lng) ||
            lat < -90 ||
            lat > 90 ||
            lng < -180 ||
            lng > 180
        ) {
            return;
        }

        const priority = (
            record.dataset.priority || "UNASSESSED"
        ).toUpperCase();

        const markerColor = colors[priority] || "#94a3b8";

        // Create incident marker
        const marker = L.circleMarker([lat, lng], {
            radius: 8,
            color: markerColor,
            weight: 2,
            fillColor: markerColor,
            fillOpacity: 0.85
        }).addTo(map);

        // Create popup
        const popup = document.createElement("div");

        const title = document.createElement("strong");
        title.textContent =
            record.dataset.title || "Untitled report";

        const location = document.createElement("p");
        location.textContent =
            record.dataset.location || "Location not supplied";

        const priorityLine = document.createElement("p");
        priorityLine.textContent =
            "Coordinator priority: " + priority;

        const link = document.createElement("a");
        link.href = record.dataset.url || "#";
        link.textContent = "View report";

        popup.append(title, location, priorityLine, link);

        marker.bindPopup(popup);
        markers.push(marker);
    });

    // Fit map to incident locations
    if (markers.length > 0) {
        const markerGroup = L.featureGroup(markers);
        map.fitBounds(markerGroup.getBounds().pad(0.2));
    } else {
        const note = document.createElement("div");
        note.className = "map-empty-message";
        note.textContent =
            "No reports with valid coordinates are available to display.";

        mapElement.appendChild(note);
    }

    // Refresh map dimensions
    window.setTimeout(function () {
        map.invalidateSize();
    }, 200);
});