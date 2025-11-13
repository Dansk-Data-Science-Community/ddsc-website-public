# Technical Requirements Specification (TRS)
## Danish Data Science Community Website

**Version:** 1.0
**Last Updated:** October 30, 2025
**Status:** Active Production System

---

## 1. Technical Overview

### System Architecture

The DDSC Website is built as a **monolithic Django web application** following the Model-View-Template (MVT) architectural pattern. The system uses a traditional three-tier architecture:

1. **Presentation Layer**: Server-rendered HTML templates with Bootstrap UI
2. **Application Layer**: Django business logic, views, and forms
3. **Data Layer**: PostgreSQL relational database with Redis caching

### Architecture Diagram (Conceptual)

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                         │
│  Browser (Desktop/Mobile) → HTML/CSS/JS (Bootstrap/jQuery) │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTPS
┌───────────────────────────┴─────────────────────────────────┐
│                     WEB SERVER LAYER                        │
│              Nginx/Apache (Reverse Proxy)                   │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────┴─────────────────────────────────┐
│                   APPLICATION LAYER                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │         Gunicorn (WSGI Server)                      │   │
│  │  ┌──────────────────────────────────────────────┐  │   │
│  │  │     Django 4.1.5 Application                 │  │   │
│  │  │  ┌────────┬────────┬────────┬──────────┐   │  │   │
│  │  │  │ Users  │ Events │Members │  Polls   │   │  │   │
│  │  │  │  App   │  App   │  App   │   App    │   │  │   │
│  │  │  └────────┴────────┴────────┴──────────┘   │  │   │
│  │  │  ┌────────┬────────┬────────────────────┐  │  │   │
│  │  │  │ News   │ Stats  │     Shared         │  │  │   │
│  │  │  │  App   │  App   │   Utilities        │  │  │   │
│  │  │  └────────┴────────┴────────────────────┘  │  │   │
│  │  └──────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │         Celery Workers (Async Tasks)                │   │
│  │  - Email Delivery                                   │   │
│  │  - QR Code Generation                               │   │
│  │  - Newsletter Sync                                  │   │
│  └─────────────────────────────────────────────────────┘   │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────┴─────────────────────────────────┐
│                      DATA LAYER                             │
│  ┌──────────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   PostgreSQL 13  │  │    Redis     │  │ DigitalOcean │ │
│  │   (Primary DB)   │  │ (Cache/Queue)│  │   Spaces     │ │
│  │                  │  │              │  │  (S3 Storage)│ │
│  └──────────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            │
┌───────────────────────────┴─────────────────────────────────┐
│                   EXTERNAL SERVICES                         │
│  - Gmail SMTP (Email Delivery)                              │
│  - MailerLite (Newsletter Campaigns)                        │
│  - GitHub OAuth (Social Auth - Optional)                    │
│  - Slack OAuth (Social Auth - Optional)                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Technology Stack

### Backend Framework

**Django 4.1.5**
- Python web framework following MVT pattern
- Built-in ORM for database abstraction
- Admin interface for content management
- Form handling and validation
- Template engine for server-side rendering
- Security features (CSRF, XSS protection, SQL injection prevention)
- Internationalization (i18n) support

**Python 3.11.9**
- Primary programming language
- Type hints support with MyPy
- Async/await support (for future use)

### Database

**PostgreSQL 13**
- Primary relational database
- ACID compliance
- Full-text search capabilities
- JSON field support
- Robust indexing and query optimization
- Connection: psycopg2 2.9.5 driver

**SQLite3**
- Development fallback (not recommended)
- Used for local testing only

### Caching & Message Queue

**Redis**
- Session storage
- Application-level caching (view caching, query caching)
- Celery message broker
- Rate limiting backend
- Volatile storage for temporary data

**Celery 5.2.7**
- Distributed task queue
- Async email delivery
- Background job processing
- Scheduled tasks (future: periodic surveys, cleanup)
- Redis as broker and result backend

### File Storage

**DigitalOcean Spaces** (Production/Staging)
- S3-compatible object storage
- Public bucket: Static files, event images, profile images
- Private bucket: QR code tickets, sensitive documents
- CDN integration for fast delivery
- Library: django-storages 1.13.2, boto3 1.26.50

**MinIO** (Development)
- S3-compatible local storage
- Docker container (port 9000/9001)
- Mimics production storage behavior
- Bucket auto-creation on startup

### Frontend Technologies

**Bootstrap 4.3.1**
- Responsive CSS framework
- Grid system (12 columns)
- Pre-built components (cards, modals, forms, navbar)
- Utility classes
- Mobile-first design

**jQuery 3.3.1**
- DOM manipulation
- AJAX requests
- Event handling
- Plugin integration

**Chart.js 2.8.0**
- Data visualization library
- Bar charts, line charts, pie charts
- Used in statistics dashboard and salary survey
- Interactive tooltips and animations

**Tempusdominus Bootstrap 4**
- DateTime picker widget
- Integration with Bootstrap styling
- User-friendly date/time selection for events

**Font Awesome 6.1.1**
- Icon library (web fonts)
- UI icons throughout the application

**TinyMCE 3.5.0** (via django-tinymce)
- WYSIWYG rich text editor
- Used for event descriptions, news content
- Image upload support
- HTML editing capability

### Key Python Packages

**Core Django Extensions:**
- `django-crispy-forms 1.14.0` - Bootstrap 4 form rendering
- `django-image-cropping 1.7` - Image cropping interface
- `django-storages 1.13.2` - S3/cloud storage backends
- `django-import-export 4.0.3` - Admin data export (CSV, JSON, Excel)
- `django-markdownfield 0.10.0` - Markdown field support
- `python-social-auth[django]` - Social authentication framework

**Image Processing:**
- `Pillow 9.4.0` - Image manipulation (resize, crop, convert)
- `easy-thumbnails 2.8.3` - Thumbnail generation

**Utilities:**
- `qrcode 7.3.1` - QR code generation for event tickets
- `python-dotenv 0.21.0` - Environment variable management
- `requests 2.28.2` - HTTP client for API integrations
- `gunicorn 20.1.0` - WSGI HTTP server

**Development Tools:**
- `black 22.12.0` - Code formatter (88 char line length)
- `mypy 0.942` - Static type checking
- `radon 5.1.0` - Code complexity metrics
- `xenon 0.9.0` - Complexity enforcement (max: A)

### Email Service

**Gmail SMTP** (Production/Staging)
- Host: smtp.gmail.com
- Port: 587 (TLS)
- Authentication: Email + App Password
- Rate limits: ~500 emails/day

**Console Backend** (Development)
- Prints emails to console
- No actual delivery

### CI/CD

**GitHub Actions**
- Workflow: `.github/workflows/django.yml`
- Triggers: Push to main/staging/dev/feature branches
- Steps: Dependencies → Tests → System Checks → Complexity Check
- Python version: 3.11
- Test framework: Django's built-in unittest

**Code Quality:**
- Black formatting check (`.github/workflows/black.yml`)
- MyPy type checking (in CI)
- Xenon complexity threshold enforcement

---

## 3. Project Structure

```
ddsc-website/
├── ddsc_web/                          # Django project root
│   ├── ddsc_web/                      # Project configuration package
│   │   ├── settings/
│   │   │   ├── settings.py            # Base settings (shared)
│   │   │   ├── dev.py                 # Development environment
│   │   │   ├── prod.py                # Production environment
│   │   │   └── custom_storages.py     # S3 storage configurations
│   │   ├── celery.py                  # Celery app configuration
│   │   ├── wsgi.py                    # WSGI application entry
│   │   ├── asgi.py                    # ASGI application entry (future)
│   │   └── urls.py                    # Root URL routing
│   │
│   ├── users/                         # User authentication & profiles
│   │   ├── models.py                  # User, Profile, ProfileImage
│   │   ├── views.py                   # Auth views (login, register, dashboard)
│   │   ├── forms.py                   # User registration, profile forms
│   │   ├── admin.py                   # Admin interface customization
│   │   ├── tasks.py                   # Celery tasks (email activation, reset)
│   │   ├── urls.py                    # User URL patterns
│   │   ├── tokens.py                  # Email verification token generator
│   │   ├── fields.py                  # Custom form fields
│   │   ├── managers.py                # Custom User manager
│   │   ├── migrations/                # Database migrations
│   │   ├── templates/users/           # User-specific templates
│   │   └── tests.py                   # Unit tests
│   │
│   ├── events/                        # Event management system
│   │   ├── models.py                  # Event, EventImage, EventRegistration
│   │   ├── views.py                   # Event CRUD, registration logic
│   │   ├── forms.py                   # Event creation/edit forms
│   │   ├── admin.py                   # Admin with export functionality
│   │   ├── tasks.py                   # Celery tasks (send tickets)
│   │   ├── urls.py                    # Event URL patterns
│   │   ├── signing.py                 # Cryptographic signing for tickets
│   │   ├── decorators.py              # Custom view decorators
│   │   ├── managers.py                # Custom QuerySet managers
│   │   ├── management/commands/
│   │   │   └── event_groups.py        # Setup EventEditor/TicketConsumer groups
│   │   ├── migrations/                # Database migrations
│   │   ├── templates/events/          # Event-specific templates
│   │   └── tests.py                   # Unit tests
│   │
│   ├── members/                       # Membership management
│   │   ├── models.py                  # Member, Address
│   │   ├── views.py                   # Member registration, profile
│   │   ├── forms.py                   # Member forms
│   │   ├── admin.py                   # Admin interface
│   │   ├── tasks.py                   # Celery tasks (welcome email)
│   │   ├── urls.py                    # Member URL patterns
│   │   ├── decorators.py              # Access control decorators
│   │   ├── migrations/                # Database migrations
│   │   ├── templates/members/         # Member-specific templates
│   │   └── tests.py                   # Unit tests
│   │
│   ├── news/                          # Newsletter subscriptions
│   │   ├── models.py                  # NewsSubscriber
│   │   ├── views.py                   # Subscription handling
│   │   ├── admin.py                   # Admin with subscriber export
│   │   ├── tasks.py                   # Newsletter sync tasks
│   │   ├── signals.py                 # Django signal handlers
│   │   ├── mailerlite.py              # MailerLite API client
│   │   ├── urls.py                    # News URL patterns
│   │   ├── migrations/                # Database migrations
│   │   ├── templates/news/            # Newsletter templates
│   │   └── tests.py                   # Unit tests
│   │
│   ├── polls/                         # Polling system
│   │   ├── models.py                  # Pollsession, Question, Choice, Answer
│   │   ├── views.py                   # Poll list, detail, vote, results
│   │   ├── forms.py                   # Poll voting forms
│   │   ├── admin.py                   # Admin interface
│   │   ├── urls.py                    # Poll URL patterns
│   │   ├── migrations/                # Database migrations
│   │   ├── templates/polls/           # Poll templates
│   │   └── tests.py                   # Unit tests
│   │
│   ├── stats/                         # Statistics & analytics
│   │   ├── models.py                  # SurveyData
│   │   ├── views.py                   # Dashboard, salary survey views
│   │   ├── forms.py                   # Filter forms
│   │   ├── queries.py                 # Statistics query helpers
│   │   ├── admin.py                   # Admin interface
│   │   ├── urls.py                    # Stats URL patterns
│   │   ├── management/commands/       # Data import commands
│   │   ├── migrations/                # Database migrations
│   │   ├── templates/stats/           # Stats templates
│   │   └── tests.py                   # Unit tests
│   │
│   ├── shared/                        # Shared utilities
│   │   ├── models.py                  # AbstractAddress base model
│   │   ├── forms.py                   # Shared form components
│   │   ├── emails.py                  # Email utility functions
│   │   ├── validators.py              # Custom validators
│   │   └── layouts.py                 # Crispy form layouts
│   │
│   ├── home/                          # Base templates & static pages
│   │   ├── base.html                  # Main base template
│   │   ├── home.html                  # Homepage
│   │   ├── header_navbar.html         # Navigation bar
│   │   ├── footer.html                # Footer
│   │   ├── messages.html              # Django messages display
│   │   ├── base_email.html            # Email template base
│   │   ├── base_error.html            # Error pages base
│   │   ├── 400.html                   # Bad Request error
│   │   ├── 403.html                   # Forbidden error
│   │   ├── 404.html                   # Not Found error
│   │   ├── 500.html                   # Server Error
│   │   └── 503.html                   # Service Unavailable
│   │
│   ├── locale/                        # Internationalization
│   │   ├── da/LC_MESSAGES/            # Danish translations
│   │   │   ├── django.po              # Translation strings
│   │   │   └── django.mo              # Compiled translations
│   │   └── en/LC_MESSAGES/            # English translations
│   │       ├── django.po
│   │       └── django.mo
│   │
│   ├── static/                        # Static assets (dev)
│   │   ├── css/
│   │   │   └── main.css               # Custom styles
│   │   ├── event_pics_color/          # Event placeholder images
│   │   ├── favicon.ico                # Site favicon
│   │   └── apple-touch-icon.png       # iOS icon
│   │
│   ├── media/                         # User-uploaded files (dev)
│   │   ├── profile_images/            # Profile photos
│   │   ├── event_images/              # Event photos
│   │   └── qrcodes/                   # Generated QR codes
│   │
│   └── manage.py                      # Django CLI management script
│
├── salary_survey/                     # Salary survey preprocessor
│   ├── preprocessor.py                # CSV to JSON conversion
│   ├── requirements.txt               # Specific dependencies (pandas)
│   └── README.md                      # Preprocessor documentation
│
├── deployment/                        # Deployment configurations
│   ├── celery.service                 # Systemd service file
│   ├── celeryd                        # Celery daemon script
│   ├── install_celery.sh              # Installation script
│   └── readme.md                      # Deployment guide
│
├── docker-compose.yml                 # Local development services
├── Dockerfile                         # Production container image
├── requirements.txt                   # Python dependencies
├── dev_requirements.txt               # Dev dependencies (black, mypy, etc.)
├── pyproject.toml                     # Black configuration
├── .env                               # Environment variables (gitignored)
├── .gitignore                         # Git ignore patterns
├── .github/workflows/                 # CI/CD workflows
│   ├── django.yml                     # Django CI pipeline
│   └── black.yml                      # Code formatting check
└── README.md                          # Project documentation
```

---

## 4. Data Model Specification

### Database Schema

#### Users App

**User** (Custom `AbstractBaseUser`)
```python
Fields:
- id: AutoField (Primary Key)
- email: EmailField (unique=True, max_length=100, indexed)
- first_name: CharField (max_length=50)
- last_name: CharField (max_length=50)
- is_active: BooleanField (default=True)
- is_staff: BooleanField (default=False)
- is_superuser: BooleanField (default=False)
- is_verified: BooleanField (default=False)
- date_joined: DateTimeField (auto_now_add=True)
- groups: ManyToManyField (Group)
- user_permissions: ManyToManyField (Permission)

Constraints:
- USERNAME_FIELD = 'email'
- REQUIRED_FIELDS = ['first_name', 'last_name']

Indexes:
- email (unique index)
- is_active, is_staff (query optimization)

Methods:
- get_full_name() -> str
- get_short_name() -> str
- email_user(subject, message, from_email=None)
```

**Profile** (One-to-One with User)
```python
Fields:
- id: AutoField (Primary Key)
- user: OneToOneField (User, on_delete=CASCADE)
- birthdate: DateField (null=True, blank=True)

Properties:
- age: int (calculated from birthdate)

Signals:
- post_save(User) → creates Profile automatically
```

**ProfileImage** (One-to-One with Profile)
```python
Fields:
- id: AutoField (Primary Key)
- profile: OneToOneField (Profile, on_delete=CASCADE)
- image: ImageField (upload_to='profile_images/', S3 storage)
- cropping: ImageRatioField (easy-thumbnails)
  - 150x150 (thumbnail)
  - 300x300 (medium)
  - 600x600 (large)

Methods:
- get_image_url() -> str
```

---

#### Events App

**Event**
```python
Fields:
- id: AutoField (Primary Key)
- title: CharField (max_length=200, unique=True)
- slug: SlugField (max_length=200, unique=True, auto-generated)
- location: CharField (max_length=500)
- start_datetime: DateTimeField
- end_datetime: DateTimeField
- description: HTMLField (TinyMCE editor)
- summary: TextField (max_length=500)
- signup_type: CharField (choices=[('DDSC', 'DDSC Event'), ('External', 'External')])
- maximum_attendees: PositiveIntegerField (null=True, blank=True)
- draft: BooleanField (default=False)
- registration_terms: ForeignKey (RegistrationTerms, null=True, on_delete=SET_NULL)
- created: DateTimeField (auto_now_add=True)
- updated: DateTimeField (auto_now=True)

Constraints:
- title unique
- slug unique
- start_datetime < end_datetime (validation)
- maximum_attendees > 0 (validation)

Indexes:
- slug (unique index for URL lookups)
- start_datetime (for event listing queries)
- draft (for filtering published events)

Methods:
- save(self, *args, **kwargs): Auto-generate slug from title
- has_available_tickets() -> bool
- is_sold_out() -> bool
- get_registration_count() -> int
- get_attended_count() -> int

Related Names:
- registrations: EventRegistration.objects.filter(event=self)
- images: EventImage.objects.filter(event=self)
- address: Address.objects.get(event=self)
```

**EventImage**
```python
Fields:
- id: AutoField (Primary Key)
- event: ForeignKey (Event, on_delete=CASCADE, related_name='images')
- image: ImageCropField (upload_to='event_images/', S3 storage)
- cropping_detail: ImageRatioField (1850x900)
- cropping_list: ImageRatioField (900x600)
- order: PositiveIntegerField (default=0)

Meta:
- ordering = ['order', 'id']

Methods:
- get_detail_image_url() -> str
- get_list_image_url() -> str
```

**Address** (Inherits AbstractAddress)
```python
Fields:
- id: AutoField (Primary Key)
- event: OneToOneField (Event, on_delete=CASCADE)
- street: CharField (max_length=200)
- postal_code: CharField (max_length=10)
- city: CharField (max_length=100)
- region: CharField (max_length=100, null=True, blank=True)

Methods:
- get_full_address() -> str
```

**EventRegistration**
```python
Fields:
- id: AutoField (Primary Key)
- event: ForeignKey (Event, on_delete=CASCADE, related_name='registrations')
- user: ForeignKey (User, on_delete=CASCADE, related_name='event_registrations')
- qr_code: ImageField (upload_to='qrcodes/', private S3 storage)
- token: CharField (max_length=64, unique=True)
- status: CharField (choices=[('Pending', 'Pending'), ('Attended', 'Attended')], default='Pending')
- slug: SlugField (unique=True, auto-generated)
- created: DateTimeField (auto_now_add=True)

Constraints:
- unique_together = ['event', 'user']
- token unique
- slug unique

Indexes:
- event, user (composite unique index)
- token (for ticket validation)
- slug (for URL lookups)
- status (for attendance queries)

Methods:
- save(self, *args, **kwargs): Generate token, slug, QR code
- generate_qrcode() -> None
- get_signed_data() -> dict
- verify_ticket(signed_data) -> bool (classmethod)

Signals:
- post_save → send_ticket_mail.delay(registration_id)
```

**RegistrationTerms**
```python
Fields:
- id: AutoField (Primary Key)
- terms: HTMLField (TinyMCE editor)
- type: CharField (max_length=100)
- name: CharField (max_length=200)
- created: DateTimeField (auto_now_add=True)
- updated: DateTimeField (auto_now=True)

Meta:
- ordering = ['-created']
```

---

#### Members App

**Member**
```python
Fields:
- id: AutoField (Primary Key)
- user: OneToOneField (User, on_delete=CASCADE, related_name='member')
- title: CharField (choices=[
    ('Formand', 'Formand'),
    ('Næstformand', 'Næstformand'),
    ('Board member', 'Board member'),
    ('Regular member', 'Regular member'),
    ('Substitute', 'Substitute')
  ], default='Regular member')
- job_title: CharField (max_length=200, null=True, blank=True)
- status: CharField (choices=[('Pending', 'Pending'), ('Active', 'Active')], default='Pending')
- slug: SlugField (unique=True, auto-generated)
- created: DateTimeField (auto_now_add=True)

Constraints:
- user unique (one member per user)
- slug unique

Indexes:
- user (unique index)
- slug (for URL lookups)
- status (for filtering active members)
- title (for board member queries)

Methods:
- save(self, *args, **kwargs): Auto-generate slug
- is_board_member() -> bool

Related Names:
- address: Address.objects.get(member=self)

Signals:
- post_save → send_welcome_email.delay(member_id)
```

**Address** (for Members, inherits AbstractAddress)
```python
Fields:
- id: AutoField (Primary Key)
- member: OneToOneField (Member, on_delete=CASCADE)
- street: CharField (max_length=200)
- postal_code: CharField (max_length=10)
- city: CharField (max_length=100)
- region: CharField (max_length=100, null=True, blank=True)

Methods:
- get_full_address() -> str
```

---

#### News App

**NewsSubscriber**
```python
Fields:
- id: AutoField (Primary Key)
- user: OneToOneField (User, on_delete=CASCADE, null=True, blank=True)
- allow_newsletters: BooleanField (default=True)
- created: DateTimeField (auto_now_add=True)

Constraints:
- user unique (nullable, for non-user subscribers)

Indexes:
- user (unique index)
- allow_newsletters (for filtering subscribers)

Methods:
- get_email() -> str: Returns user.email or raises error

Signals:
- post_save → Sync to MailerLite (optional)
```

---

#### Polls App

**Pollsession**
```python
Fields:
- id: AutoField (Primary Key)
- title: CharField (max_length=200)
- description: TextField (max_length=1000, null=True, blank=True)
- author: ForeignKey (User, on_delete=SET_NULL, null=True)
- active: BooleanField (default=True)
- anonymous: BooleanField (default=False)
- created: DateTimeField (auto_now_add=True)

Indexes:
- active (for filtering active polls)
- author (for user's polls)

Methods:
- user_has_completed(user) -> bool
- get_poll_results() -> dict
- get_participation_count() -> int

Related Names:
- questions: Question.objects.filter(poll_session=self)
- voter_sessions: VoterSession.objects.filter(poll_session=self)
```

**VoterSession**
```python
Fields:
- id: AutoField (Primary Key)
- user: ForeignKey (User, on_delete=CASCADE, related_name='voter_sessions')
- poll_session: ForeignKey (Pollsession, on_delete=CASCADE, related_name='voter_sessions')
- vote_started_at: DateTimeField (auto_now_add=True)
- vote_completed_at: DateTimeField (null=True, blank=True)

Constraints:
- unique_together = ['user', 'poll_session']

Indexes:
- user, poll_session (composite unique index)
- vote_completed_at (for completion queries)

Properties:
- is_completed: bool (vote_completed_at is not None)

Methods:
- mark_completed() -> None
```

**Question**
```python
Fields:
- id: AutoField (Primary Key)
- poll_session: ForeignKey (Pollsession, on_delete=CASCADE, related_name='questions')
- text: CharField (max_length=500)
- created: DateTimeField (auto_now_add=True)

Indexes:
- poll_session (for poll's questions)

Methods:
- get_choice_vote_results() -> list[dict]
- get_total_votes() -> int

Related Names:
- choices: Choice.objects.filter(question=self)
- answers: Answer.objects.filter(question=self)
```

**Choice**
```python
Fields:
- id: AutoField (Primary Key)
- question: ForeignKey (Question, on_delete=CASCADE, related_name='choices')
- text: CharField (max_length=200)

Indexes:
- question (for question's choices)

Methods:
- get_vote_count() -> int
- get_choice_vote_proportion() -> float

Related Names:
- answers: Answer.objects.filter(choice=self)
```

**Answer**
```python
Fields:
- id: AutoField (Primary Key)
- voter: ForeignKey (User, on_delete=CASCADE, related_name='poll_answers')
- question: ForeignKey (Question, on_delete=CASCADE, related_name='answers')
- choice: ForeignKey (Choice, on_delete=CASCADE, related_name='answers')
- created: DateTimeField (auto_now_add=True)

Constraints:
- unique_together = ['voter', 'question']  # One answer per question per user

Indexes:
- voter, question (composite unique index)
- choice (for vote counting)
- created (for time-series analysis)
```

---

#### Stats App

**SurveyData**
```python
Fields:
- id: AutoField (Primary Key)
- user_id: IntegerField (anonymized ID, not FK)
- question: CharField (max_length=500)
- answer: CharField (max_length=500)
- year: IntegerField
- monthly_salary: IntegerField (null=True, blank=True)
- created_at: DateTimeField (auto_now_add=True)

Indexes:
- question, year (composite index for filtering)
- answer (for aggregation queries)
- monthly_salary (for statistical queries)

Meta:
- ordering = ['-year', '-created_at']

Methods:
- get_statistics_by_answer() -> dict (classmethod)
- get_salary_distribution() -> list (classmethod)
```

---

### Database Relationships Summary

```
User (1) ←→ (1) Profile ←→ (1) ProfileImage
User (1) ←→ (1) Member ←→ (1) Address
User (1) ←→ (1) NewsSubscriber
User (1) ←→ (∞) EventRegistration ←→ (1) Event ←→ (1) Address
Event (1) ←→ (∞) EventImage
Event (1) ←→ (1) RegistrationTerms
User (1) ←→ (∞) VoterSession ←→ (1) Pollsession ←→ (∞) Question ←→ (∞) Choice
User (1) ←→ (∞) Answer ←→ (1) Question
User (1) ←→ (∞) Answer ←→ (1) Choice
Pollsession (1) ←→ (∞) User (author, nullable)
```

---

## 5. API & URL Routing

### URL Structure

Base URL: `https://ddsc.io/`

#### Authentication URLs (`/users/`)
```
GET  /users/register/                   - User registration form
POST /users/register/                   - Create user account
GET  /users/login/                      - Login form
POST /users/login/                      - Authenticate user
GET  /users/logout/                     - Logout user
GET  /users/dashboard/                  - User dashboard (authenticated)
GET  /users/edit/                       - Profile edit form (authenticated)
POST /users/edit/                       - Update profile
GET  /users/edit_image/                 - Profile image edit (authenticated)
POST /users/edit_image/                 - Update profile image
GET  /users/password_reset/             - Password reset form
POST /users/password_reset/             - Send reset email
GET  /users/password_reset_done/        - Reset email sent confirmation
GET  /users/password_reset_confirm/     - Password reset form (from email)
POST /users/password_reset_confirm/     - Set new password
GET  /users/password_reset_complete/    - Password reset success
GET  /users/password_change/            - Change password (authenticated)
POST /users/password_change/            - Update password
GET  /users/activate/<uidb64>/<token>/  - Email activation link
```

#### Event URLs (`/events/`)
```
GET  /events/                           - List upcoming events (paginated)
GET  /events/<id>/<slug>/               - Event detail page
POST /events/register/<id>/<slug>/      - Register for event (authenticated)
POST /events/unregister/<id>/<slug>/    - Cancel registration (authenticated)
GET  /events/create/                    - Event creation form (EventEditor)
POST /events/create/                    - Create new event (EventEditor)
GET  /events/edit/<id>/<slug>/          - Edit event form (EventEditor)
POST /events/edit/<id>/<slug>/          - Update event (EventEditor)
POST /events/delete/<pk>/               - Delete event (EventEditor)
GET  /events/minimeetup/                - Mini-meetup landing page
POST /events/consume/<token>/           - Consume QR code ticket (TicketConsumer)
GET  /events/share/<id>/<slug>/         - Event sharing page (social cards)
```

#### Member URLs (`/members/`)
```
GET  /members/register/                 - Member registration (authenticated, non-member)
POST /members/register/                 - Create member profile
GET  /members/edit/                     - Edit member profile (member only)
POST /members/edit/                     - Update member profile
GET  /members/unsubscribe/              - Newsletter unsubscribe
GET  /members/board/                    - View board members
GET  /members/articles/                 - Member articles list
GET  /members/salary/                   - Redirect to salary survey
```

#### News URLs (`/news/`)
```
POST /news/success/                     - Newsletter subscription success
```

#### Poll URLs (`/polls/`)
```
GET  /polls/                            - List active polls (authenticated)
GET  /polls/<poll_session_id>/          - Poll detail page (authenticated)
POST /polls/<voter_session_id>/vote/    - Submit vote (authenticated)
GET  /polls/<poll_session_id>/results/  - View poll results (after voting)
```

#### Stats URLs (`/stats/`)
```
GET  /stats/dashboard/                  - Statistics dashboard (public)
GET  /stats/salary-survey/              - Salary survey visualization (public, cached)
```

#### Admin URLs (`/admin/`)
```
GET  /admin/                            - Django admin login
GET  /admin/<app>/<model>/              - Model list view
GET  /admin/<app>/<model>/<id>/change/  - Model edit view
GET  /admin/<app>/<model>/add/          - Model create view
POST /admin/<app>/<model>/<id>/delete/  - Model delete
```

---

### Request/Response Flow

#### Example: Event Registration

**Request:**
```http
POST /events/register/42/data-science-meetup/
Content-Type: application/x-www-form-urlencoded
Cookie: sessionid=abc123...

accept_terms=on
```

**Processing:**
1. Middleware: Check CSRF token
2. Middleware: Load user session (authenticate)
3. View: Validate user logged in (redirect if not)
4. View: Load Event object (id=42, slug='data-science-meetup')
5. View: Check if sold out (redirect if full)
6. View: Check if user already registered (redirect if duplicate)
7. View: Validate form (terms accepted)
8. View: Create EventRegistration object
9. Model save: Generate token, slug
10. Model save: Generate QR code image
11. Model save: Upload QR code to private S3
12. Signal: Trigger post_save signal
13. Task: Queue send_ticket_mail.delay(registration_id)
14. View: Redirect to event detail with success message
15. Template: Render event page with "You're registered!" message

**Async Task (Celery):**
1. Worker receives send_ticket_mail task
2. Load EventRegistration from database
3. Download QR code from private S3
4. Download event image from public S3
5. Render email template with context
6. Send email via Gmail SMTP
7. Mark task as complete

**Response:**
```http
HTTP/1.1 302 Found
Location: /events/42/data-science-meetup/
Set-Cookie: messages=["You are now registered!"]
```

---

## 6. Authentication & Authorization

### Authentication Flow

#### Email/Password Registration
1. User submits registration form (email, first_name, last_name, password)
2. Validate email uniqueness
3. Hash password (Django's PBKDF2 algorithm)
4. Create User object (is_verified=False, is_active=True)
5. Generate email verification token (TimestampSigner)
6. Queue send_activation_email.delay(user_id)
7. Display "Check your email" message
8. User clicks activation link in email
9. Verify token and timestamp (max age: 24 hours)
10. Set is_verified=True
11. Auto-login user
12. Redirect to dashboard

#### Login Flow
1. User submits login form (email, password)
2. Authenticate via Django's authenticate()
3. Check is_active=True and is_verified=True
4. Create session (store in Redis)
5. Set session cookie (HttpOnly, Secure in prod)
6. Redirect to 'next' URL or dashboard

#### Password Reset Flow
1. User submits email for reset
2. Check if user exists
3. Generate password reset token (PasswordResetTokenGenerator)
4. Queue send_password_reset_email.delay(user_id)
5. User clicks reset link in email
6. Verify token (max age: 24 hours)
7. Display password reset form
8. User submits new password
9. Hash and save new password
10. Invalidate all existing sessions
11. Display success message with login link

### Authorization Model

#### Permission Groups

**EventEditor Group**
- Permissions:
  - `events.add_event`
  - `events.change_event`
  - `events.delete_event`
  - `events.view_event`
  - `events.view_eventregistration`
- Created by: `python manage.py event_groups`
- Assignment: Admin manually assigns users

**TicketConsumer Group**
- Permissions:
  - `events.change_eventregistration` (status field only)
- Created by: `python manage.py event_groups`
- Assignment: Admin assigns to check-in volunteers

#### Decorators

**`@login_required`** (Django built-in)
```python
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    # Only authenticated users can access
    ...
```

**`@user_passes_test`** (Django built-in)
```python
from django.contrib.auth.decorators import user_passes_test

def user_is_eventeditor(user):
    return user.groups.filter(name="Eventeditor").exists() or user.is_superuser

@user_passes_test(user_is_eventeditor)
def create_event(request):
    # Only EventEditor group or superuser
    ...
```

**Custom Decorators (events/decorators.py)**
```python
@login_required_with_next
# Stores current URL in 'next' param before redirect

@redirect_when_sold_out
# Checks if event is sold out before allowing registration

@redirect_members
# Redirects existing members away from registration page
```

#### View-Level Authorization

**Class-Based Views:**
```python
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class EventCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'events.add_event'
    # Automatically checks permissions
```

**Function-Based Views:**
```python
def consume_ticket(request, token):
    if not request.user.groups.filter(name="TicketConsumer").exists():
        return HttpResponseForbidden()
    # Only TicketConsumer group can access
```

---

## 7. Email System Architecture

### Email Configuration

**Development:**
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# Prints emails to console
```

**Production/Staging:**
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD')
DEFAULT_FROM_EMAIL = 'Danish Data Science Community <noreply@ddsc.io>'
```

### Email Templates

Located in `<app>/templates/<app>/emails/`

**Structure:**
```
base_email.html              # Base template with header/footer
├── activation_email.html    # Email verification
├── password_reset_email.html
├── ticket_email.html        # Event ticket with QR code
└── welcome_email.html       # Member welcome
```

**Template Context Variables:**
```python
# activation_email.html
{
    'user': User object,
    'domain': 'ddsc.io',
    'uid': Base64 encoded user ID,
    'token': Activation token,
    'protocol': 'https',
}

# ticket_email.html
{
    'user': User object,
    'event': Event object,
    'registration': EventRegistration object,
    'qr_code_cid': Content ID for embedded image,
    'event_image_cid': Content ID for event image,
}
```

### Celery Tasks

**Task: send_activation_email**
- File: `users/tasks.py`
- Triggered by: User registration (post_save signal)
- Parameters: user_id
- Process:
  1. Load User from database
  2. Generate activation token
  3. Render email template
  4. Send via Gmail SMTP
  5. Log success/failure
- Retry: 3 attempts, exponential backoff

**Task: send_ticket_mail**
- File: `events/tasks.py`
- Triggered by: EventRegistration creation (post_save signal)
- Parameters: registration_id
- Process:
  1. Load EventRegistration, Event, User
  2. Download QR code from private S3
  3. Download event image from public S3
  4. Create email with embedded images (inline attachments)
  5. Render ticket_email.html template
  6. Send via Gmail SMTP
  7. Log success/failure
- Retry: 5 attempts, exponential backoff
- Priority: High (user-facing)

**Task: send_welcome_email**
- File: `members/tasks.py`
- Triggered by: Member approval (status change to Active)
- Parameters: member_id
- Process:
  1. Load Member and User
  2. Render welcome template
  3. Send via Gmail SMTP
  4. Log success/failure
- Retry: 3 attempts

---

## 8. File Storage Architecture

### Storage Backends

**Development (MinIO):**
```python
# custom_storages.py
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

class PublicMediaStorage(S3Boto3Storage):
    location = 'public'
    default_acl = 'public-read'
    file_overwrite = False
    custom_domain = 'localhost:9000/media-public'

class PrivateMediaStorage(S3Boto3Storage):
    location = 'private'
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False
```

**Production (DigitalOcean Spaces):**
```python
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'ddsc-media'
AWS_S3_REGION_NAME = 'fra1'  # Frankfurt region
AWS_S3_ENDPOINT_URL = 'https://fra1.digitaloceanspaces.com'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.fra1.cdn.digitaloceanspaces.com'
AWS_DEFAULT_ACL = None
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',  # 24 hours
}
```

### File Upload Paths

```python
# Profile images
profile_images/
  ├── user_123_abc123.jpg      # Original
  ├── user_123_abc123.150x150.jpg
  ├── user_123_abc123.300x300.jpg
  └── user_123_abc123.600x600.jpg

# Event images
event_images/
  ├── event_42_xyz789.jpg      # Original
  ├── event_42_xyz789.900x600.jpg   # List view
  └── event_42_xyz789.1850x900.jpg  # Detail view

# QR codes (private bucket)
qrcodes/
  └── registration_<slug>_<token>.png

# Static files (public bucket)
static/
  ├── css/
  │   └── main.css
  ├── event_pics_color/
  │   └── placeholder.png
  └── favicon.ico
```

### Image Processing

**Library: Pillow 9.4.0**

**Profile Image Upload:**
1. User selects image file
2. Form validation (file size < 5MB, format: JPG/PNG)
3. Upload to S3 public bucket (original)
4. Admin/user crops image (django-image-cropping UI)
5. Generate thumbnails: 150x150, 300x300, 600x600
6. Store cropping coordinates in database
7. On-demand thumbnail generation (easy-thumbnails)

**Event Image Upload:**
1. EventEditor uploads image
2. Validation (size < 10MB, format: JPG/PNG)
3. Upload to S3 public bucket
4. Crop to 1850x900 (detail view)
5. Crop to 900x600 (list view)
6. Generate thumbnails
7. Set display order

**QR Code Generation:**
```python
import qrcode

def generate_qrcode(registration):
    # Create QR code data (signed URL)
    data = f"https://ddsc.io/events/consume/{registration.token}/"

    # Generate QR code image
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Save to BytesIO
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    # Upload to private S3 bucket
    filename = f"registration_{registration.slug}_{registration.token}.png"
    registration.qr_code.save(filename, ContentFile(buffer.read()), save=False)
```

---

## 9. Security Implementation

### CSRF Protection

**Mechanism:** Django's built-in CSRF middleware
- Token generated per session
- Token embedded in forms ({% csrf_token %})
- Token validated on POST requests
- Rejected if missing or invalid

**Configuration:**
```python
MIDDLEWARE = [
    'django.middleware.csrf.CsrfViewMiddleware',
]
CSRF_COOKIE_SECURE = True  # Production only (HTTPS)
CSRF_COOKIE_HTTPONLY = True
```

### XSS Protection

**Template Auto-Escaping:**
```django
{{ user_input }}  <!-- Automatically escaped -->
{{ trusted_html|safe }}  <!-- Explicitly marked safe -->
```

**HTMLField Sanitization:**
- TinyMCE editor configured to strip dangerous tags
- Whitelist: `<p>, <a>, <strong>, <em>, <ul>, <ol>, <li>, <img>`
- Blacklist: `<script>, <iframe>, <object>, <embed>`

### SQL Injection Prevention

**ORM Parameterization:**
```python
# Safe (parameterized)
User.objects.filter(email=user_input)

# Unsafe (raw SQL)
cursor.execute(f"SELECT * FROM users WHERE email = '{user_input}'")  # Never do this
```

All database queries use Django ORM, which automatically parameterizes.

### Password Security

**Hashing Algorithm:** PBKDF2-SHA256 (Django default)
- Iterations: 260,000 (Django 4.1 default)
- Salt: Random per password
- Format: `pbkdf2_sha256$260000$<salt>$<hash>`

**Password Validation:**
```python
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
```

### Session Security

**Configuration:**
```python
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'  # Redis
SESSION_CACHE_ALIAS = 'default'
SESSION_COOKIE_SECURE = True  # HTTPS only (production)
SESSION_COOKIE_HTTPONLY = True  # No JavaScript access
SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection
SESSION_COOKIE_AGE = 1209600  # 2 weeks
```

### Cryptographic Signing

**QR Code Ticket Signing:**
```python
from django.core.signing import Signer, BadSignature

# Sign ticket data
signer = Signer()
signed_token = signer.sign(registration.token)

# Verify ticket (in consume view)
try:
    unsigned_token = signer.unsign(signed_token)
    # Valid ticket
except BadSignature:
    # Tampered or invalid ticket
    return HttpResponseForbidden()
```

### Rate Limiting

**Configuration (future enhancement):**
```python
# Using django-ratelimit
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/m', method='POST')
def register(request):
    # Max 5 registration attempts per minute per IP
    ...
```

### HTTPS Enforcement

**Production Settings:**
```python
SECURE_SSL_REDIRECT = True  # Redirect HTTP → HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### File Upload Security

**Validation:**
```python
# File size limit
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB

# Allowed extensions
ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif']

# Content-Type validation
def validate_image(file):
    if file.size > MAX_UPLOAD_SIZE:
        raise ValidationError("File too large")

    ext = os.path.splitext(file.name)[1].lower()
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValidationError("Invalid file type")

    # Validate image header (prevent spoofing)
    try:
        img = Image.open(file)
        img.verify()
    except Exception:
        raise ValidationError("Invalid image file")
```

### Environment Variables

**Sensitive Configuration:**
```bash
# .env file (gitignored)
SECRET_KEY=<50-char random string>
DB_PASSWORD=<database password>
EMAIL_USER=<gmail address>
EMAIL_PASSWORD=<gmail app password>
AWS_ACCESS_KEY_ID=<spaces key>
AWS_SECRET_ACCESS_KEY=<spaces secret>
MAILERLITE_API_KEY=<api key>
SOCIAL_AUTH_GITHUB_KEY=<oauth key>
SOCIAL_AUTH_GITHUB_SECRET=<oauth secret>
```

**Loading:**
```python
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
```

---

## 10. Performance Optimization

### Caching Strategy

**Cache Backend: Redis**
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'ddsc',
        'TIMEOUT': 3600,  # 1 hour default
    }
}
```

**View Caching:**
```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 60)  # Cache for 1 hour
def salary_survey(request):
    # Expensive query
    stats = SurveyData.objects.aggregate(...)
    return render(request, 'stats/salary_survey.html', {'stats': stats})
```

**Template Fragment Caching:**
```django
{% load cache %}

{% cache 3600 event_list %}
  {% for event in events %}
    ...
  {% endfor %}
{% endcache %}
```

**Query Optimization:**
```python
# Bad: N+1 queries
events = Event.objects.all()
for event in events:
    print(event.registrations.count())  # Separate query for each event

# Good: Single query with annotation
events = Event.objects.annotate(reg_count=Count('registrations'))
for event in events:
    print(event.reg_count)  # No additional query
```

### Database Optimization

**Indexes:**
```python
class Event(models.Model):
    slug = models.SlugField(unique=True, db_index=True)
    start_datetime = models.DateTimeField(db_index=True)
    draft = models.BooleanField(default=False, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['start_datetime', 'draft']),  # Composite index
        ]
```

**Select Related / Prefetch Related:**
```python
# Select Related (ForeignKey, OneToOne)
registrations = EventRegistration.objects.select_related('user', 'event')

# Prefetch Related (ManyToMany, reverse ForeignKey)
events = Event.objects.prefetch_related('registrations', 'images')
```

**Bulk Operations:**
```python
# Bad: Individual saves
for data in survey_data:
    SurveyData.objects.create(**data)

# Good: Bulk create
SurveyData.objects.bulk_create([SurveyData(**data) for data in survey_data])
```

### Static File Optimization

**Compression:**
```python
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
# Adds content hash to filenames for cache busting
# main.css → main.abc123.css
```

**CDN Delivery:**
```python
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.fra1.cdn.digitaloceanspaces.com'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
```

**Minification (future):**
- Django Compressor for CSS/JS minification
- Whitenoise for static file serving

### Async Task Processing

**Celery Configuration:**
```python
# celery.py
app = Celery('ddsc_web')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# settings.py
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Copenhagen'
```

**Task Priorities:**
```python
# High priority: User-facing tasks
send_ticket_mail.apply_async(args=[registration_id], priority=9)

# Low priority: Background sync
upsert_subscribers.apply_async(priority=1)
```

### Connection Pooling

**Database Connection Pooling:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'CONN_MAX_AGE': 600,  # 10 minutes connection reuse
        'OPTIONS': {
            'connect_timeout': 10,
            'options': '-c statement_timeout=30000'  # 30 seconds
        }
    }
}
```

**Redis Connection Pooling:**
```python
CACHES = {
    'default': {
        'OPTIONS': {
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 50,
                'retry_on_timeout': True
            }
        }
    }
}
```

---

## 11. Development Environment Setup

### Prerequisites

- Python 3.11.9
- PostgreSQL 13
- Redis
- DigitalOcean Spaces account (or MinIO for local)
- Gmail account with App Password

### Local Setup Steps

**1. Clone Repository**
```bash
git clone https://github.com/Dansk-Data-Science-Community/ddsc-website.git
cd ddsc-website
```

**2. Create Virtual Environment**
```bash
python3.11 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
pip install -r dev_requirements.txt  # Optional: dev tools
```

**4. Start Development Services (Docker)**
```bash
docker-compose up -d
# Starts PostgreSQL, Redis, MinIO
```

**5. Configure Environment Variables**
```bash
cp .env.example .env
# Edit .env with your credentials
```

**6. Run Migrations**
```bash
cd ddsc_web
python manage.py migrate
```

**7. Create Superuser**
```bash
python manage.py createsuperuser
```

**8. Setup Permission Groups**
```bash
python manage.py event_groups
```

**9. Load Initial Data (optional)**
```bash
python manage.py loaddata fixtures/events.json
```

**10. Run Development Server**
```bash
export DJANGO_SETTINGS_MODULE=ddsc_web.settings.dev
python manage.py runserver
# Access: http://localhost:8000
```

**11. Start Celery Worker (separate terminal)**
```bash
celery -A ddsc_web worker -l info
```

### Development Tools

**Run Tests:**
```bash
python manage.py test
```

**Code Formatting:**
```bash
black .
```

**Type Checking:**
```bash
mypy ddsc_web
```

**Code Complexity:**
```bash
xenon --max-absolute A --max-modules A --max-average A ddsc_web
```

**Django Shell:**
```bash
python manage.py shell
```

**Database Shell:**
```bash
python manage.py dbshell
```

**Create Migrations:**
```bash
python manage.py makemigrations
```

**Collect Static Files:**
```bash
python manage.py collectstatic
```

---

## 12. Deployment Architecture

### Production Environment

**Hosting:** DigitalOcean Droplet (or similar VPS)
**OS:** Ubuntu 20.04 LTS
**Web Server:** Nginx (reverse proxy)
**App Server:** Gunicorn (WSGI)
**Database:** PostgreSQL 13 (managed or self-hosted)
**Cache:** Redis (managed or self-hosted)
**Storage:** DigitalOcean Spaces (S3-compatible)

### Deployment Workflow

**1. SSH to Server**
```bash
ssh django@ddsc.io
```

**2. Navigate to Project**
```bash
cd /var/www/ddsc-website
```

**3. Activate Virtual Environment**
```bash
source venv/bin/activate
```

**4. Pull Latest Code**
```bash
git pull origin main  # or staging branch
```

**5. Install Dependencies**
```bash
pip install -r requirements.txt
```

**6. Run Migrations**
```bash
cd ddsc_web
python manage.py migrate
```

**7. Collect Static Files**
```bash
python manage.py collectstatic --noinput
# Uploads to DigitalOcean Spaces
```

**8. Restart Services**
```bash
sudo systemctl restart gunicorn
sudo systemctl restart celery
```

**9. Check Status**
```bash
sudo systemctl status gunicorn
sudo systemctl status celery
```

### Systemd Service Files

**Gunicorn Service (`/etc/systemd/system/gunicorn.service`):**
```ini
[Unit]
Description=Gunicorn daemon for DDSC Website
After=network.target

[Service]
User=django
Group=www-data
WorkingDirectory=/var/www/ddsc-website/ddsc_web
Environment="PATH=/var/www/ddsc-website/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=ddsc_web.settings.prod"
ExecStart=/var/www/ddsc-website/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/run/gunicorn.sock \
    ddsc_web.wsgi:application

[Install]
WantedBy=multi-user.target
```

**Celery Service (`/etc/systemd/system/celery.service`):**
```ini
[Unit]
Description=Celery Service for DDSC Website
After=network.target

[Service]
Type=forking
User=django
Group=django
WorkingDirectory=/var/www/ddsc-website/ddsc_web
Environment="PATH=/var/www/ddsc-website/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=ddsc_web.settings.prod"
ExecStart=/var/www/ddsc-website/venv/bin/celery multi start worker \
    -A ddsc_web \
    --pidfile=/var/run/celery/%n.pid \
    --logfile=/var/log/celery/%n.log \
    --loglevel=info

[Install]
WantedBy=multi-user.target
```

**Nginx Configuration (`/etc/nginx/sites-available/ddsc`):**
```nginx
upstream ddsc_app {
    server unix:/run/gunicorn.sock fail_timeout=0;
}

server {
    listen 80;
    server_name ddsc.io www.ddsc.io;

    # Redirect HTTP to HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name ddsc.io www.ddsc.io;

    # SSL certificates (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/ddsc.io/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/ddsc.io/privkey.pem;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    client_max_body_size 10M;

    location / {
        proxy_pass http://ddsc_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        # Static files served from S3/CDN
        return 301 https://ddsc-media.fra1.cdn.digitaloceanspaces.com$request_uri;
    }
}
```

### Environment Configuration

**Production Settings (`ddsc_web/settings/prod.py`):**
```python
from .settings import *

DEBUG = False
ALLOWED_HOSTS = ['ddsc.io', 'www.ddsc.io']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ddsc_prod',
        'USER': 'ddsc_user',
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Storage (DigitalOcean Spaces)
DEFAULT_FILE_STORAGE = 'ddsc_web.settings.custom_storages.PublicMediaStorage'
PRIVATE_FILE_STORAGE = 'ddsc_web.settings.custom_storages.PrivateMediaStorage'
```

### CI/CD Pipeline

**GitHub Actions Workflow (`.github/workflows/django.yml`):**
```yaml
name: Django CI

on:
  push:
    branches: [ main, staging, dev, 'feature/**' ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.11]

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install Dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r dev_requirements.txt

    - name: Run Tests
      env:
        SECRET_KEY: ${{ secrets.SECRET_KEY }}
        EMAIL_USER: ${{ secrets.EMAIL_USER }}
        EMAIL_PASSWORD: ${{ secrets.EMAIL_PASSWORD }}
      run: |
        cd ddsc_web
        python manage.py test

    - name: Django System Checks
      run: |
        cd ddsc_web
        python manage.py check

    - name: Code Complexity Check
      run: |
        xenon --max-absolute A --max-modules A --max-average A ddsc_web
```

**Auto-Deployment (future enhancement):**
- Use GitHub Actions to SSH and deploy on push to `main`
- Or use Docker + Kubernetes for container orchestration

---

## 13. Monitoring & Logging

### Logging Configuration

**Development:**
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```

**Production:**
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/ddsc/django.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'celery_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/ddsc/celery.log',
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 5,
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
        'celery': {
            'handlers': ['celery_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```

### Error Monitoring (Future Enhancement)

**Sentry Integration:**
```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.1,
    send_default_pii=True
)
```

### Application Monitoring

**Health Check Endpoint:**
```python
# urls.py
path('health/', health_check, name='health_check'),

# views.py
from django.db import connection
from django.http import JsonResponse

def health_check(request):
    # Check database
    try:
        connection.ensure_connection()
        db_status = "ok"
    except Exception as e:
        db_status = f"error: {str(e)}"

    # Check cache
    try:
        cache.set('health_check', 'ok', 10)
        cache_status = "ok" if cache.get('health_check') == 'ok' else "error"
    except Exception as e:
        cache_status = f"error: {str(e)}"

    return JsonResponse({
        'status': 'ok' if db_status == 'ok' and cache_status == 'ok' else 'error',
        'database': db_status,
        'cache': cache_status,
    })
```

### Performance Monitoring

**Django Debug Toolbar (Development):**
```python
# Only in dev settings
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
INTERNAL_IPS = ['127.0.0.1']
```

**Query Monitoring:**
```python
from django.db import connection

# Log slow queries
if len(connection.queries) > 10:
    logger.warning(f"View executed {len(connection.queries)} queries")
```

---

## 14. Testing Strategy

### Unit Tests

**Location:** `<app>/tests.py`

**Test Structure:**
```python
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass123'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_verified)

    def test_get_full_name(self):
        self.assertEqual(self.user.get_full_name(), 'Test User')
```

**Run Tests:**
```bash
python manage.py test                    # All tests
python manage.py test events             # Specific app
python manage.py test events.tests.EventModelTest  # Specific test class
```

### Integration Tests

**Example: Event Registration Flow**
```python
from django.test import TestCase, Client
from django.urls import reverse

class EventRegistrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(...)
        self.event = Event.objects.create(...)

    def test_registration_flow(self):
        # Login
        self.client.login(email='test@example.com', password='testpass123')

        # Register for event
        response = self.client.post(
            reverse('events:register', args=[self.event.id, self.event.slug]),
            {'accept_terms': True}
        )

        # Check redirect
        self.assertEqual(response.status_code, 302)

        # Verify registration created
        self.assertTrue(
            EventRegistration.objects.filter(
                user=self.user,
                event=self.event
            ).exists()
        )
```

### Test Coverage

**Generate Coverage Report:**
```bash
coverage run --source='.' manage.py test
coverage report
coverage html  # HTML report in htmlcov/
```

**Coverage Goals:**
- Models: 90%+
- Views: 80%+
- Forms: 80%+
- Utilities: 90%+

---

## 15. Localization & Internationalization

### Language Support

**Supported Languages:**
- Danish (da) - Primary
- English (en) - Secondary

**Configuration:**
```python
LANGUAGE_CODE = 'da'
LANGUAGES = [
    ('da', 'Danish'),
    ('en', 'English'),
]
USE_I18N = True
USE_L10N = True
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]
```

### Translation Workflow

**1. Mark Strings for Translation:**
```python
from django.utils.translation import gettext_lazy as _

class Event(models.Model):
    title = models.CharField(_("Title"), max_length=200)
```

**2. Extract Translatable Strings:**
```bash
python manage.py makemessages -l da
python manage.py makemessages -l en
```

**3. Edit Translation Files:**
```
locale/da/LC_MESSAGES/django.po
locale/en/LC_MESSAGES/django.po
```

**4. Compile Translations:**
```bash
python manage.py compilemessages
```

**5. Template Usage:**
```django
{% load i18n %}

<h1>{% trans "Welcome to DDSC" %}</h1>

{% blocktrans with name=user.first_name %}
  Hello, {{ name }}!
{% endblocktrans %}
```

### Regional Settings

**Timezone:**
```python
TIME_ZONE = 'Europe/Copenhagen'
USE_TZ = True  # Store in UTC, display in local timezone
```

**Date/Time Formats:**
```python
# Danish format
DATE_FORMAT = 'd-m-Y'
DATETIME_FORMAT = 'd-m-Y H:i'
SHORT_DATE_FORMAT = 'd/m/Y'
```

---

## 16. Future Technical Enhancements

### Short-Term (Next 6 Months)

1. **API Development**
   - Django REST Framework integration
   - RESTful API for mobile apps
   - JWT authentication
   - API documentation (Swagger/OpenAPI)

2. **Search Functionality**
   - Full-text search for events, members
   - Elasticsearch integration
   - Autocomplete suggestions

3. **Email Improvements**
   - HTML email templates with inline CSS
   - Email preview in admin
   - Unsubscribe link tracking
   - Email analytics (open rates, click rates)

4. **Performance**
   - Database query optimization audit
   - Redis caching expansion
   - CDN for static assets
   - Lazy loading for images

5. **Testing**
   - Increase test coverage to 80%+
   - Integration tests for critical flows
   - Performance testing (load testing)

### Medium-Term (6-12 Months)

1. **Microservices Migration (Optional)**
   - Extract email service to separate microservice
   - Extract stats/analytics to separate service
   - API Gateway (Kong, Traefik)

2. **Mobile App Backend**
   - GraphQL API (Graphene-Django)
   - Push notification support (FCM)
   - Mobile-optimized endpoints

3. **Advanced Analytics**
   - Google Analytics integration
   - Custom event tracking
   - User behavior analysis
   - A/B testing framework

4. **Payment Integration**
   - Stripe integration for paid events
   - Payment webhooks
   - Refund handling

5. **Real-Time Features**
   - WebSockets (Django Channels)
   - Live poll results
   - Real-time event capacity updates

### Long-Term (12+ Months)

1. **Containerization & Orchestration**
   - Docker multi-stage builds
   - Kubernetes deployment
   - Helm charts
   - Auto-scaling

2. **Advanced Security**
   - Two-factor authentication (TOTP)
   - OAuth2 provider (allow third-party apps)
   - Security audit and penetration testing
   - OWASP compliance

3. **AI/ML Features**
   - Event recommendation engine
   - Member matching for networking
   - Salary prediction model
   - Spam detection

4. **Infrastructure**
   - Multi-region deployment
   - Database read replicas
   - Global CDN
   - Disaster recovery plan

---

## 17. Technical Constraints & Limitations

### Current Limitations

1. **Scalability**
   - Monolithic architecture limits horizontal scaling
   - Single database instance (no sharding)
   - Session affinity required for Gunicorn workers

2. **Performance**
   - Server-side rendering (no SPA)
   - Limited client-side caching
   - No lazy loading for images
   - Synchronous views (no async views yet)

3. **Features**
   - No real-time updates
   - No mobile apps
   - Limited offline support
   - No payment processing

4. **Deployment**
   - Manual deployment process
   - No blue-green deployment
   - Single-server deployment (no load balancing)

5. **Monitoring**
   - Limited error tracking (no Sentry yet)
   - Basic logging (no centralized log aggregation)
   - No APM (Application Performance Monitoring)

### Technical Debt

1. **Code Quality**
   - Some views need refactoring (too complex)
   - Missing docstrings in some modules
   - Type hints not comprehensive

2. **Testing**
   - Test coverage below 60%
   - Missing integration tests for some flows
   - No end-to-end tests

3. **Dependencies**
   - Some outdated packages (Django 4.1.5 → 4.2 LTS)
   - Need to audit security vulnerabilities

4. **Documentation**
   - Limited inline code documentation
   - Missing API documentation
   - Deployment guide needs updating

---

## 18. Appendix

### Glossary

- **MVT**: Model-View-Template (Django's architectural pattern)
- **ORM**: Object-Relational Mapping (database abstraction)
- **WSGI**: Web Server Gateway Interface (Python web standard)
- **CSRF**: Cross-Site Request Forgery (security vulnerability)
- **XSS**: Cross-Site Scripting (security vulnerability)
- **S3**: Simple Storage Service (object storage standard)
- **CDN**: Content Delivery Network (distributed file delivery)
- **JWT**: JSON Web Token (authentication standard)
- **SMTP**: Simple Mail Transfer Protocol (email sending)

### Key File References

| Component | File Path | Lines | Purpose |
|-----------|-----------|-------|---------|
| Main Settings | `ddsc_web/ddsc_web/settings/settings.py` | ~200 | Base configuration |
| URL Routing | `ddsc_web/ddsc_web/urls.py` | ~50 | Main URL patterns |
| User Model | `ddsc_web/users/models.py` | 129 | Custom user model |
| Event Model | `ddsc_web/events/models.py` | 233 | Event management |
| Event Views | `ddsc_web/events/views.py` | ~400 | Event CRUD logic |
| Member Model | `ddsc_web/members/models.py` | 71 | Membership model |
| Poll Model | `ddsc_web/polls/models.py` | 145 | Polling system |
| Stats Views | `ddsc_web/stats/views.py` | ~300 | Analytics dashboard |
| Celery Config | `ddsc_web/ddsc_web/celery.py` | ~40 | Async tasks config |
| Email Tasks | `ddsc_web/users/tasks.py` | ~100 | Email delivery tasks |
| Ticket Tasks | `ddsc_web/events/tasks.py` | ~150 | Ticket email with QR |
| Base Template | `ddsc_web/home/base.html` | ~150 | Main HTML template |

### Environment Variables Reference

| Variable | Type | Required | Purpose |
|----------|------|----------|---------|
| `SECRET_KEY` | String | Yes | Django secret key (50+ chars) |
| `DB_PASSWORD` | String | Prod only | PostgreSQL password |
| `EMAIL_USER` | String | Yes | Gmail address |
| `EMAIL_PASSWORD` | String | Yes | Gmail app password |
| `AWS_ACCESS_KEY_ID` | String | Yes | DigitalOcean Spaces key |
| `AWS_SECRET_ACCESS_KEY` | String | Yes | Spaces secret key |
| `MAILERLITE_API_KEY` | String | Optional | Newsletter API key |
| `SOCIAL_AUTH_GITHUB_KEY` | String | Optional | GitHub OAuth client ID |
| `SOCIAL_AUTH_GITHUB_SECRET` | String | Optional | GitHub OAuth secret |
| `SOCIAL_AUTH_SLACK_KEY` | String | Optional | Slack OAuth client ID |
| `SOCIAL_AUTH_SLACK_SECRET` | String | Optional | Slack OAuth secret |
| `SALARY_URL` | String | Optional | External salary survey URL |
| `SLACK_INVITATION_LINK` | String | Optional | Slack community invite |

### Port Reference

| Service | Port | Protocol | Purpose |
|---------|------|----------|---------|
| Django Dev Server | 8000 | HTTP | Local development |
| PostgreSQL | 5432 | TCP | Database |
| Redis | 6379 | TCP | Cache/Queue |
| MinIO | 9000 | HTTP | S3 API |
| MinIO Console | 9001 | HTTP | Admin UI |
| Gunicorn | Unix Socket | - | Production WSGI |
| Nginx | 80, 443 | HTTP/HTTPS | Reverse proxy |

---

## 19. Conclusion

The Danish Data Science Community Website is built on a solid, modern tech stack with Django 4.1.5 at its core. The monolithic architecture provides simplicity and rapid development while maintaining scalability for the current user base. The system leverages industry-standard technologies (PostgreSQL, Redis, S3, Celery) and follows Django best practices for security, performance, and maintainability.

Key technical strengths:
- **Modular Django apps** for separation of concerns
- **Async task processing** for email delivery and background jobs
- **Cloud storage integration** for scalable file management
- **Comprehensive security** with CSRF, XSS, and authentication protections
- **CI/CD pipeline** for automated testing and quality checks
- **Internationalization** support for Danish and English

The architecture supports the current feature set while providing clear paths for future enhancements such as API development, real-time features, and mobile app support.

**For Implementation Questions:**
- Refer to specific file paths in Section 3 (Project Structure)
- Check database schema in Section 4 (Data Model Specification)
- Review API endpoints in Section 5 (API & URL Routing)
- Consult security implementation in Section 9 (Security Implementation)

**For Development Setup:**
- Follow Section 11 (Development Environment Setup)

**For Deployment:**
- Reference Section 12 (Deployment Architecture)
