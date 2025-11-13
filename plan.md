# Newsletter Subscription System Implementation Plan

## Project Overview
Implement a comprehensive newsletter subscription system to address the barrier of "lack of awareness of events" for DDSC members.

## Current State Analysis

### Existing Components
- **Models**: `NewsSubscriber` model exists but minimal (only user, created, allow_newsletters)
- **MailerLite Integration**: Already implemented in `news/mailerlite.py` with functions for:
  - `subscribe_to_newsletter()`
  - `get_newsletter_subscriber_id()`
  - `forget_newsletter_subscriber()`
- **Celery Tasks**: Basic tasks exist in `news/tasks.py`:
  - `upsert_mailerlite_subscriber`
  - `delete_mailerlite_subscriber`
- **Templates**: Basic templates exist but need enhancement
- **Views**: Minimal view in `news/views.py` needs expansion

### What Needs to Be Built
1. Enhanced database model with email and preferences
2. Forms for subscription management
3. Confirmation email workflow
4. Subscription preference system
5. Unsubscribe workflow
6. Widget for homepage/footer
7. Standalone landing page
8. Mobile-responsive design

---

## Implementation Plan

### Phase 1: Database & Models

#### Task 1.1: Extend NewsSubscriber Model
**File**: `ddsc_web/news/models.py`

Add the following fields:
- `email` (EmailField, unique=True) - Required for non-authenticated users
- `name` (CharField) - Subscriber's name
- `is_confirmed` (BooleanField) - Email confirmation status
- `confirmation_token` (CharField) - Token for email verification
- `event_types` (CharField with choices) - Types: all, meetup, workshop, conference, webinar
- `frequency` (CharField with choices) - Options: immediate, daily, weekly, monthly
- `updated` (DateTimeField) - Track last update

**Methods to add**:
- `__str__()` - Display email and frequency
- `get_active_subscribers()` - Get confirmed, active subscribers
- Update `get_mailing_list()` to filter by is_confirmed=True

#### Task 1.2: Create Database Migration
**Command**: `python manage.py makemigrations news`

This will generate migration for new fields with proper defaults.

---

### Phase 2: Forms

#### Task 2.1: Create forms.py
**File**: `ddsc_web/news/forms.py` (new file)

**Forms to create**:

1. **NewsletterSubscribeForm**
   - Fields: email, name (optional), event_types, frequency
   - Validation: Check if email already subscribed
   - Clean methods for email validation

2. **NewsletterPreferencesForm**
   - Fields: event_types, frequency, allow_newsletters
   - For existing subscribers to update preferences

3. **NewsletterUnsubscribeForm**
   - Field: email
   - Simple form for unsubscribe requests

---

### Phase 3: Email Templates & Confirmation Flow

#### Task 3.1: Create Email Templates
**Directory**: `ddsc_web/news/templates/news/emails/`

**Templates needed**:
1. `confirmation_email.html` - HTML version
2. `confirmation_email.txt` - Plain text version
3. `welcome_email.html` - After confirmation
4. `welcome_email.txt` - Plain text version
5. `unsubscribe_confirmation.html` - Unsubscribe confirmation
6. `unsubscribe_confirmation.txt` - Plain text version

**Email content should include**:
- Confirmation link with token
- Subscription preferences summary
- Unsubscribe link
- DDSC branding

#### Task 3.2: Create Celery Tasks for Emails
**File**: `ddsc_web/news/tasks.py`

**New tasks to add**:
1. `send_confirmation_email(subscriber_id)` - Send confirmation email with token
2. `send_welcome_email(subscriber_id)` - Send after email confirmation
3. `sync_subscriber_to_mailerlite(subscriber_id)` - Sync to MailerLite after confirmation

**Update existing tasks**:
- Ensure `upsert_mailerlite_subscriber` only syncs confirmed subscribers

---

### Phase 4: Views & URL Routing

#### Task 4.1: Update views.py
**File**: `ddsc_web/news/views.py`

**Views to create/update**:

1. **newsletter_landing** - Standalone landing page
   - Display subscription form with all preferences
   - POST: Create subscriber, generate token, send confirmation email
   - Redirect to success page

2. **subscribe_widget** - Handle widget form submissions
   - Simpler than landing page (email + name only)
   - POST: Create subscriber, send confirmation
   - AJAX-friendly response

3. **confirm_subscription** - Handle email confirmation
   - GET with token parameter
   - Validate token, activate subscription
   - Sync to MailerLite
   - Display success message

4. **update_preferences** - Manage existing subscription
   - GET: Display current preferences
   - POST: Update preferences, sync to MailerLite
   - Requires email or token

5. **unsubscribe** - Handle unsubscribe requests
   - GET with token/email: Display confirmation page
   - POST: Deactivate subscription, remove from MailerLite
   - Display farewell message

6. **resubscribe** - Handle resubscription
   - Allow previously unsubscribed users to rejoin

#### Task 4.2: Update urls.py
**File**: `ddsc_web/news/urls.py`

**URL patterns to add**:
```python
urlpatterns = [
    path('newsletter/', views.newsletter_landing, name='newsletter_landing'),
    path('subscribe/', views.subscribe_widget, name='subscribe_widget'),
    path('confirm/<str:token>/', views.confirm_subscription, name='confirm_subscription'),
    path('preferences/', views.update_preferences, name='update_preferences'),
    path('unsubscribe/', views.unsubscribe, name='unsubscribe'),
    path('unsubscribe/<str:token>/', views.unsubscribe, name='unsubscribe_token'),
    path('resubscribe/', views.resubscribe, name='resubscribe'),
    path('success/', views.subscribe_success, name='subscribe_success'),
]
```

---

### Phase 5: Templates

#### Task 5.1: Create Newsletter Landing Page
**File**: `ddsc_web/news/templates/news/newsletter_landing.html`

**Features**:
- Hero section explaining newsletter benefits
- Full subscription form with all preference options
- Visual examples of newsletter content
- Privacy policy link
- Mobile-responsive design
- Bootstrap 4 styling (matching site theme)

#### Task 5.2: Create Newsletter Widget Template
**File**: `ddsc_web/news/templates/news/newsletter_widget.html`

**Features**:
- Compact inline form
- Email and name fields
- Submit button
- Link to full landing page for preferences
- Can be included in footer or navbar

#### Task 5.3: Update Footer Template
**File**: `ddsc_web/home/footer.html`

**Changes**:
- Add newsletter widget inclusion
- Style to fit existing footer design
- Ensure mobile responsiveness

#### Task 5.4: Create Confirmation Templates
**Files to create**:
1. `news/templates/news/confirmation_pending.html` - After initial signup
2. `news/templates/news/confirmation_success.html` - After email confirmed
3. `news/templates/news/unsubscribe_confirm.html` - Unsubscribe confirmation page
4. `news/templates/news/unsubscribe_success.html` - After unsubscribed
5. `news/templates/news/preferences.html` - Manage preferences page

#### Task 5.5: Update Existing Success Template
**File**: `ddsc_web/news/templates/news/subscribe_success.html`

Update to show:
- Check your email message
- What to expect in confirmation email
- Link to resend confirmation

---

### Phase 6: Helper Functions & Utils

#### Task 6.1: Create utils.py
**File**: `ddsc_web/news/utils.py` (new file)

**Functions to create**:
1. `generate_confirmation_token()` - Generate unique token using secrets
2. `get_subscriber_by_token(token)` - Retrieve subscriber by token
3. `is_valid_email(email)` - Email validation
4. `build_confirmation_url(token)` - Build full URL for confirmation link
5. `build_unsubscribe_url(token)` - Build unsubscribe URL

---

### Phase 7: Admin Interface

#### Task 7.1: Update admin.py
**File**: `ddsc_web/news/admin.py`

**Enhancements**:
- List display: email, name, is_confirmed, event_types, frequency, created
- List filters: is_confirmed, event_types, frequency, allow_newsletters
- Search fields: email, name
- Actions: Export subscribers, Send test newsletter, Bulk confirm
- Readonly fields: created, updated, confirmation_token

---

### Phase 8: Integration & Testing

#### Task 8.1: Update Settings
**File**: `ddsc_web/ddsc_web/settings/settings.py`

**Add/verify**:
- Email backend configuration
- MailerLite API credentials
- Site URL for confirmation links
- Email sender configuration

#### Task 8.2: Create Signals
**File**: `ddsc_web/news/signals.py`

**Signals to create**:
- `post_save` on NewsSubscriber - Trigger confirmation email for new subscribers
- `post_save` on User - Sync with NewsSubscriber if email changes

#### Task 8.3: Manual Testing Checklist
- [ ] Subscribe with new email (widget)
- [ ] Subscribe with new email (landing page)
- [ ] Receive and click confirmation email
- [ ] Check MailerLite sync
- [ ] Update preferences
- [ ] Unsubscribe workflow
- [ ] Resubscribe workflow
- [ ] Mobile responsiveness on all pages
- [ ] Email rendering in multiple clients
- [ ] Error handling (duplicate email, invalid token, etc.)

---

## Success Criteria (from prompt.md)

- [x] Newsletter signup form on homepage
- [x] Standalone landing page created
- [x] MailerLite integration working
- [x] Confirmation emails sent
- [x] Mobile responsive
- [x] User preferences saved

---

## Technical Specifications

### Tech Stack
- **Backend**: Django 3.2+
- **Frontend**: HTML/CSS, Bootstrap 4
- **Email**: Django email system with HTML templates
- **Task Queue**: Celery with Redis
- **External API**: MailerLite API
- **Database**: PostgreSQL/SQLite (existing)

### Security Considerations
1. CSRF protection on all forms
2. Token-based email confirmation (use secrets module)
3. Rate limiting on subscription endpoints
4. Email validation and sanitization
5. SQL injection prevention (Django ORM handles this)
6. GDPR compliance - easy unsubscribe, data deletion

### Performance Considerations
1. Async email sending via Celery
2. Database indexing on email and token fields
3. Cache subscription counts
4. Batch MailerLite API calls where possible

---

## File Structure

```
ddsc_web/news/
├── models.py (updated)
├── forms.py (new)
├── views.py (updated)
├── urls.py (updated)
├── tasks.py (updated)
├── utils.py (new)
├── admin.py (updated)
├── signals.py (updated/new)
├── templates/
│   └── news/
│       ├── newsletter_landing.html (new)
│       ├── newsletter_widget.html (new)
│       ├── confirmation_pending.html (new)
│       ├── confirmation_success.html (new)
│       ├── preferences.html (new)
│       ├── unsubscribe_confirm.html (new)
│       ├── unsubscribe_success.html (new)
│       ├── subscribe_success.html (updated)
│       └── emails/
│           ├── confirmation_email.html (new)
│           ├── confirmation_email.txt (new)
│           ├── welcome_email.html (new)
│           ├── welcome_email.txt (new)
│           ├── unsubscribe_confirmation.html (new)
│           └── unsubscribe_confirmation.txt (new)
└── migrations/
    └── 000X_add_newsletter_fields.py (new)
```

---

## Implementation Order

### Recommended Sequence:
1. **Models** - Foundation for everything else
2. **Migrations** - Update database schema
3. **Forms** - Handle user input
4. **Utils** - Helper functions
5. **Views** - Business logic
6. **URLs** - Routing
7. **Templates** - User interface
8. **Email Templates** - Communication
9. **Tasks** - Background processing
10. **Admin** - Management interface
11. **Signals** - Automation
12. **Testing** - Validation

---

## Estimated Timeline

- **Phase 1** (Models & Migrations): 30 minutes
- **Phase 2** (Forms): 30 minutes
- **Phase 3** (Emails): 45 minutes
- **Phase 4** (Views & URLs): 1 hour
- **Phase 5** (Templates): 1.5 hours
- **Phase 6** (Utils): 20 minutes
- **Phase 7** (Admin): 20 minutes
- **Phase 8** (Testing): 30 minutes

**Total Estimated Time**: ~5 hours

---

## Notes

- Use existing `shared/emails.py` patterns for email creation
- Follow existing template structure and Bootstrap styling
- Leverage existing MailerLite integration
- Ensure translations for Danish/English (use {% translate %} tags)
- Test on mobile devices before finalizing
- Consider adding analytics tracking for newsletter signups
