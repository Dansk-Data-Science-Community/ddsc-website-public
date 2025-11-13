# DDSC Open Source Award

## Overview
The DDSC Open Source Award is a collaborative initiative between Danish Data Science Community (DDSC), IDA (Danish Society of Engineers), and DDSA (Danish Data Science Academy) to recognize and reward excellence in the open source community.

## Features
- Beautiful landing page showcasing the award
- Information about the award categories
- Partner organization logos and information
- Nomination call-to-action
- December 1 deadline prominently displayed
- Responsive design for all devices

## Project Structure
```
ddsc_web/opensource/
├── __init__.py
├── apps.py                    # App configuration
├── admin.py                   # Django admin configuration
├── models.py                  # Database models (future use)
├── views.py                   # View logic
├── urls.py                    # URL routing
├── static/
│   └── opensource/
│       └── award.css          # Stylesheet for award page
└── templates/
    └── opensource/
        └── award.html         # Main award page template
```

## URL Configuration
The award page is accessible at: `/opensource-award/`

## Award Categories
1. **🚀 Innovation** - Projects that push boundaries and introduce groundbreaking solutions
2. **🤝 Community Impact** - Projects that make a significant difference in their communities
3. **📚 Documentation Excellence** - Projects with outstanding documentation and learning resources
4. **🌱 Rising Star** - Emerging projects with exceptional potential

## Partners
- **DDSC (Danish Data Science Community)** - Strengthening Denmark's open source culture
- **IDA** - Representing 175,000 engineers, science graduates, and IT specialists
- **DDSA (Danish Data Science Academy)** - Advancing data science education

## Setup Instructions

### 1. The app is already configured in settings.py:
```python
INSTALLED_APPS = [
    ...
    "opensource.apps.OpensourceConfig",
    ...
]
```

### 2. URL is already configured in ddsc_web/urls.py:
```python
path("opensource-award/", include("opensource.urls", namespace="opensource"), name="opensource"),
```

### 3. Run migrations (if any models are added in the future):
```bash
python manage.py makemigrations opensource
python manage.py migrate
```

### 4. Collect static files:
```bash
python manage.py collectstatic
```

## Docker Deployment

### Build the image:
```bash
docker build -t ddsc-web:opensource-award .
```

### Run locally:
```bash
docker-compose up
```

### Deploy to Azure:
The GitHub Actions workflow will automatically deploy when:
- A release is created
- Manual dispatch is triggered from the Actions tab

## Development

### Local Development
1. Activate virtual environment
2. Install requirements: `pip install -r requirements.txt`
3. Run server: `python manage.py runserver`
4. Visit: `http://localhost:8000/opensource-award/`

### Styling
The award page uses custom CSS located at `static/opensource/award.css`. The design features:
- DDSC brand colors (blue: #1f4e78)
- Gradient backgrounds
- Responsive cards and sections
- Smooth hover animations
- Mobile-first responsive design

## Future Enhancements
- Add nomination form with database backend
- Create admin interface for managing nominations
- Add email notifications for nominations
- Create voting system for community
- Display winner announcements
- Add past winners gallery

## Important Dates
- **Nomination Deadline**: December 1
- **Winner Announcement**: TBD

## Contact
For questions about the DDSC Open Source Award, please contact DDSC administration.

## License
This project is part of the DDSC website and follows the same license terms.
