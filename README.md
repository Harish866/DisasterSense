# DisasterSense – Disaster Response Intelligence & Coordination System

AI-Assisted Disaster Incident Intelligence and Coordination

AURA is a Python and Django-based disaster response prototype designed to support emergency incident reporting, AI-assisted classification, priority recommendation, information extraction, and human coordinator review.

The system aims to transform unstructured emergency reports into structured information that can assist coordinators in understanding and reviewing incidents.

## Project Overview

During emergencies, information may arrive in unstructured formats and require rapid assessment. AURA provides a centralised interface where incident reports can be submitted, analysed, stored, and reviewed.

The application combines machine learning and rule-based analysis to assist the incident assessment workflow.

## Key Features

- **Emergency Incident Reporting:** Submit emergency reports with descriptions, locations, severity, and estimated affected population.
- **AI Incident Classification:** Predict incident categories using a Scikit-learn machine learning model.
- **Priority Recommendation:** Apply a rule-based engine to recommend incident priority.
- **Information Extraction:** Identify important details such as trapped people, injuries, rescue requirements, and evacuation requirements.
- **Incident Dashboard:** View incident statistics, category breakdowns, and submitted reports.
- **Search and Filtering:** Search and filter incidents by relevant fields.
- **Coordinator Review:** Allow a human coordinator to review incident information and update operational priority and status.
- **Database Management:** Store incident records using Django's database integration.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Django | Backend web framework |
| Scikit-learn | Machine learning classification |
| Pandas | Dataset processing |
| SQLite | Development database |
| HTML | Web page structure |
| CSS | User interface styling |
| JavaScript | Frontend interactions |

## System Workflow

1. An emergency report is submitted through the reporting interface.
2. Django processes and stores the incident.
3. The machine learning model predicts the incident category.
4. The priority engine generates a recommended priority score.
5. The information extraction module identifies important emergency details.
6. The dashboard displays the analysis results.
7. A human coordinator reviews the information and updates the incident's operational status and priority.

## Incident Categories

The application supports the following categories:

- Fire
- Flood
- Earthquake
- Medical Emergency
- Accident
- Building Collapse
- Landslide
- Other

## Project Structure

```text
DisasterResponseSystem/
│
├── config/                 # Django project configuration
├── incidents/              # Incident application
├── datasets/                # ML training datasets
├── ml_models/               # Classification and analysis modules
├── static/                  # CSS and JavaScript files
├── templates/               # HTML templates
│
├── manage.py                # Django management utility
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
├── .gitignore               # Git ignored files
└── .env.example             # Environment variable template
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/AURA-Disaster-Response.git
cd AURA-Disaster-Response
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. Start the development server

```bash
python manage.py runserver
```

Open the application at:

```text
http://127.0.0.1:8000/dashboard/
```

## AI and Analysis Modules

### Incident Classification

A machine learning classification pipeline using TF-IDF text features and Logistic Regression predicts the incident category from submitted descriptions.

### Priority Recommendation

A rule-based engine evaluates factors such as:
- Reported severity
- Estimated affected population
- Detected danger indicators
- Incident category

It produces a recommended priority and numerical score.

### Information Extraction

A rule-based text extraction module identifies relevant incident information, including:
- People trapped
- Injuries reported
- Number of injured people
- Rescue requirements
- Evacuation requirements

## Important Limitations

AURA is an experimental academic prototype.

- The machine learning classifier is trained on a small synthetic dataset and is not validated for real-world disaster classification.
- Priority recommendations are experimental and must not be treated as professional emergency triage.
- Information extraction uses rule-based techniques and may misunderstand complex descriptions.
- The application is not connected to live emergency services, field units, GPS tracking, or sensor networks.
- Human coordinators must independently assess incidents and make operational decisions.
- Production deployment requires additional security, authentication, database, and reliability improvements.

**AURA is intended for demonstration and educational purposes, not for real-world emergency operations.**

## Future Development

- Expand and validate the incident classification dataset.
- Improve contextual information extraction.
- Introduce secure multi-user authentication and role-based access.
- Integrate geographic incident intelligence.
- Explore integration with authorised emergency response services.
- Improve audit logging and incident history.

## Project Objective

To demonstrate how machine learning, rule-based analysis, and centralised incident management can work together to support disaster incident intelligence and human-coordinated response.

---

**AURA – Disaster Response Intelligence & Coordination System**

*Better Incident Intelligence. Better-Coordinated Response.*
