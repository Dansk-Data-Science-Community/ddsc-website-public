from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0003_auto_20220323_2017"),
    ]

    operations = [
        migrations.AddField(
            model_name="newssubscriber",
            name="confirm_token",
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AddField(
            model_name="newssubscriber",
            name="confirmed_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="newssubscriber",
            name="consent_timestamp",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="newssubscriber",
            name="email",
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="newssubscriber",
            name="full_name",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="newssubscriber",
            name="frequency",
            field=models.CharField(
                choices=[
                    ("weekly", "Weekly Highlights"),
                    ("monthly", "Monthly Roundup"),
                    ("events", "Event Alerts Only"),
                ],
                default="weekly",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="newssubscriber",
            name="interests",
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name="newssubscriber",
            name="unsubscribed_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
