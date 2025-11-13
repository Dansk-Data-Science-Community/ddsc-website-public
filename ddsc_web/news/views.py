from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from .models import NewsSubscriber
from .forms import (
    NewsletterSubscribeForm,
    NewsletterWidgetForm,
    NewsletterPreferencesForm,
    NewsletterUnsubscribeForm,
)
from .utils import (
    generate_confirmation_token,
    get_subscriber_by_token,
    get_subscriber_by_email,
)
from .tasks import (
    send_confirmation_email,
    send_welcome_email,
    sync_subscriber_to_mailerlite,
    send_unsubscribe_confirmation_email,
    delete_mailerlite_subscriber,
)


def newsletter_landing(request):
    """Standalone newsletter landing page with full subscription form"""
    if request.method == "POST":
        form = NewsletterSubscribeForm(request.POST)
        if form.is_valid():
            subscriber = form.save(commit=False)
            subscriber.confirmation_token = generate_confirmation_token()
            subscriber.is_confirmed = False
            subscriber.save()

            # Send confirmation email asynchronously
            send_confirmation_email.delay(subscriber.id)

            return redirect('news:confirmation_pending')
    else:
        form = NewsletterSubscribeForm()

    return render(request, 'news/newsletter_landing.html', {
        'form': form,
        'section': 'newsletter',
    })


@require_http_methods(["GET", "POST"])
def subscribe_widget(request):
    """Handle newsletter widget form submissions (simplified)"""
    if request.method == "POST":
        form = NewsletterWidgetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data.get('name', '')

            # Check if subscriber already exists
            subscriber = get_subscriber_by_email(email)

            if subscriber:
                if subscriber.is_confirmed and subscriber.allow_newsletters:
                    messages.info(request, _('This email is already subscribed to our newsletter.'))
                elif not subscriber.is_confirmed:
                    # Resend confirmation email
                    send_confirmation_email.delay(subscriber.id)
                    messages.success(request, _('Confirmation email resent. Please check your inbox.'))
                else:
                    # Reactivate subscription
                    subscriber.allow_newsletters = True
                    subscriber.is_confirmed = False
                    subscriber.confirmation_token = generate_confirmation_token()
                    subscriber.save()
                    send_confirmation_email.delay(subscriber.id)
                    messages.success(request, _('Welcome back! Please confirm your email to resubscribe.'))
            else:
                # Create new subscriber with default preferences
                subscriber = NewsSubscriber.objects.create(
                    email=email,
                    name=name,
                    confirmation_token=generate_confirmation_token(),
                    is_confirmed=False,
                    event_types='all',
                    frequency='weekly',
                )
                send_confirmation_email.delay(subscriber.id)
                messages.success(request, _('Please check your email to confirm your subscription.'))

            # For AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})

            return redirect('news:confirmation_pending')
        else:
            # For AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)

            for error in form.errors.values():
                messages.error(request, error)
            return redirect(request.META.get('HTTP_REFERER', '/'))

    return redirect('news:newsletter_landing')


def confirm_subscription(request, token):
    """Handle email confirmation"""
    subscriber = get_subscriber_by_token(token)

    if not subscriber:
        messages.error(request, _('Invalid or expired confirmation link.'))
        return render(request, 'news/confirmation_failed.html', {
            'section': 'newsletter',
        })

    if subscriber.is_confirmed:
        messages.info(request, _('Your email has already been confirmed.'))
        return render(request, 'news/confirmation_success.html', {
            'section': 'newsletter',
            'subscriber': subscriber,
        })

    # Confirm subscription
    subscriber.is_confirmed = True
    subscriber.save()

    # Send welcome email and sync to MailerLite
    send_welcome_email.delay(subscriber.id)
    sync_subscriber_to_mailerlite.delay(subscriber.id)

    messages.success(request, _('Your subscription has been confirmed! Welcome to DDSC.'))
    return render(request, 'news/confirmation_success.html', {
        'section': 'newsletter',
        'subscriber': subscriber,
    })


def confirmation_pending(request):
    """Display confirmation pending page"""
    return render(request, 'news/confirmation_pending.html', {
        'section': 'newsletter',
    })


def update_preferences(request):
    """Manage newsletter preferences"""
    token = request.GET.get('token')

    if not token:
        messages.error(request, _('Invalid access. Please use the link from your email.'))
        return redirect('news:newsletter_landing')

    subscriber = get_subscriber_by_token(token)

    if not subscriber:
        messages.error(request, _('Invalid or expired link.'))
        return redirect('news:newsletter_landing')

    if request.method == "POST":
        form = NewsletterPreferencesForm(request.POST, instance=subscriber)
        if form.is_valid():
            form.save()

            # Sync to MailerLite if still active
            if subscriber.allow_newsletters and subscriber.is_confirmed:
                sync_subscriber_to_mailerlite.delay(subscriber.id)
            elif not subscriber.allow_newsletters:
                # Remove from MailerLite
                delete_mailerlite_subscriber.delay(subscriber.email)

            messages.success(request, _('Your preferences have been updated.'))
            return redirect(request.path + f'?token={token}')
    else:
        form = NewsletterPreferencesForm(instance=subscriber)

    return render(request, 'news/preferences.html', {
        'form': form,
        'subscriber': subscriber,
        'section': 'newsletter',
    })


def unsubscribe(request, token=None):
    """Handle unsubscribe requests"""
    subscriber = None

    if token:
        subscriber = get_subscriber_by_token(token)

    if request.method == "POST":
        if not subscriber:
            # Get email from form
            form = NewsletterUnsubscribeForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                subscriber = get_subscriber_by_email(email)

        if subscriber:
            # Unsubscribe
            subscriber.allow_newsletters = False
            subscriber.save()

            # Remove from MailerLite
            delete_mailerlite_subscriber.delay(subscriber.email)

            # Send confirmation email
            send_unsubscribe_confirmation_email.delay(subscriber.id)

            messages.success(request, _('You have been unsubscribed from our newsletter.'))
            return render(request, 'news/unsubscribe_success.html', {
                'section': 'newsletter',
                'subscriber': subscriber,
            })
        else:
            messages.error(request, _('Subscriber not found.'))
            return redirect('news:unsubscribe')

    # GET request - show confirmation form
    if subscriber:
        # Token-based unsubscribe - show simple confirmation
        return render(request, 'news/unsubscribe_confirm.html', {
            'subscriber': subscriber,
            'section': 'newsletter',
        })
    else:
        # Email-based unsubscribe - show form
        form = NewsletterUnsubscribeForm()
        return render(request, 'news/unsubscribe_form.html', {
            'form': form,
            'section': 'newsletter',
        })


def subscribe_success(request):
    """Legacy success page"""
    return redirect('news:confirmation_pending')


def resubscribe(request):
    """Handle resubscription requests"""
    if request.method == "POST":
        email = request.POST.get('email')
        subscriber = get_subscriber_by_email(email)

        if subscriber:
            # Reactivate subscription
            subscriber.allow_newsletters = True
            subscriber.is_confirmed = False
            subscriber.confirmation_token = generate_confirmation_token()
            subscriber.save()

            # Send confirmation email
            send_confirmation_email.delay(subscriber.id)

            messages.success(request, _('Welcome back! Please check your email to confirm your subscription.'))
            return redirect('news:confirmation_pending')
        else:
            messages.error(request, _('Email not found. Please subscribe as a new user.'))
            return redirect('news:newsletter_landing')

    return redirect('news:newsletter_landing')
