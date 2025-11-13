from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import NewsSubscriber


class NewsletterSubscribeForm(forms.ModelForm):
    """Form for new newsletter subscriptions"""

    class Meta:
        model = NewsSubscriber
        fields = ['email', 'name', 'event_types', 'frequency']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': _('Enter your email address'),
                'required': True,
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Enter your name (optional)'),
            }),
            'event_types': forms.Select(attrs={
                'class': 'form-control',
            }),
            'frequency': forms.Select(attrs={
                'class': 'form-control',
            }),
        }
        labels = {
            'email': _('Email Address'),
            'name': _('Name'),
            'event_types': _('Event Types'),
            'frequency': _('Email Frequency'),
        }
        help_texts = {
            'email': _('We will send you a confirmation email'),
            'event_types': _('Choose which types of events you want to hear about'),
            'frequency': _('How often would you like to receive newsletters?'),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower().strip()
            # Check if email already exists
            if NewsSubscriber.objects.filter(email=email).exists():
                raise ValidationError(
                    _('This email address is already subscribed to our newsletter.')
                )
        return email


class NewsletterWidgetForm(forms.Form):
    """Simplified form for newsletter widget (email and name only)"""

    email = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter email'),
            'required': True,
        })
    )
    name = forms.CharField(
        label=_('Name'),
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Name (optional)'),
        })
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower().strip()
            # Check if email already exists and is active
            existing = NewsSubscriber.objects.filter(email=email).first()
            if existing and existing.allow_newsletters:
                raise ValidationError(
                    _('This email is already subscribed.')
                )
        return email


class NewsletterPreferencesForm(forms.ModelForm):
    """Form for updating newsletter preferences"""

    class Meta:
        model = NewsSubscriber
        fields = ['name', 'event_types', 'frequency', 'allow_newsletters']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'event_types': forms.Select(attrs={
                'class': 'form-control',
            }),
            'frequency': forms.Select(attrs={
                'class': 'form-control',
            }),
            'allow_newsletters': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
        labels = {
            'name': _('Name'),
            'event_types': _('Event Types'),
            'frequency': _('Email Frequency'),
            'allow_newsletters': _('I want to receive newsletters'),
        }


class NewsletterUnsubscribeForm(forms.Form):
    """Form for unsubscribing from newsletter"""

    email = forms.EmailField(
        label=_('Email Address'),
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your email address'),
        })
    )
    confirm = forms.BooleanField(
        label=_('Yes, I want to unsubscribe from all newsletters'),
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        })
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower().strip()
            # Check if email exists
            if not NewsSubscriber.objects.filter(email=email).exists():
                raise ValidationError(
                    _('This email address is not in our subscriber list.')
                )
        return email
