from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = [
        migrations.CreateModel(
            name='EngagementOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('category', models.CharField(choices=[('event', 'Event Participation'), ('content', 'Content Creation'), ('community', 'Community Support'), ('learning', 'Learning & Development'), ('leadership', 'Leadership Role')], max_length=20)),
                ('description', models.TextField()),
                ('engagement_points', models.PositiveIntegerField(default=10)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'verbose_name': 'Engagement Option', 'verbose_name_plural': 'Engagement Options', 'ordering': ['category', 'name']},
        ),
        migrations.CreateModel(
            name='ParticipationLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('observer', 'Observer - Passive Viewing'), ('attendee', 'Attendee - Active Participation'), ('organizer', 'Organizer - Event Leadership'), ('contributor', 'Contributor - Content Creation'), ('ambassador', 'Ambassador - Community Leadership')], default='observer', max_length=20)),
                ('score', models.PositiveIntegerField(default=0)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='participation_level', to=settings.AUTH_USER_MODEL)),
            ],
            options={'verbose_name': 'Participation Level', 'verbose_name_plural': 'Participation Levels'},
        ),
        migrations.CreateModel(
            name='EngagementGoal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('target_points', models.PositiveIntegerField()),
                ('current_points', models.PositiveIntegerField(default=0)),
                ('status', models.CharField(choices=[('active', 'Active'), ('completed', 'Completed'), ('paused', 'Paused'), ('cancelled', 'Cancelled')], default='active', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='engagement_goals', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='EngagementTrend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('total_activities', models.PositiveIntegerField(default=0)),
                ('active_members', models.PositiveIntegerField(default=0)),
                ('average_engagement_score', models.FloatField(default=0.0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['-date'], 'unique_together': {('date',)}},
        ),
        migrations.CreateModel(
            name='ActivityLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_type', models.CharField(choices=[('event_attend', 'Event Attendance'), ('event_organize', 'Event Organization'), ('content_create', 'Content Created'), ('content_comment', 'Content Comment'), ('help_provided', 'Help/Support Provided'), ('skill_shared', 'Skill Shared'), ('feedback_given', 'Feedback Given'), ('challenge_completed', 'Challenge Completed')], max_length=20)),
                ('description', models.TextField(blank=True)),
                ('points_earned', models.PositiveIntegerField(default=0)),
                ('metadata', models.JSONField(blank=True, default=dict)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('engagement_option', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='engagement.engagementoption')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', to=settings.AUTH_USER_MODEL)),
            ],
            options={'verbose_name': 'Activity Log', 'verbose_name_plural': 'Activity Logs', 'ordering': ['-timestamp']},
        ),
        migrations.AddIndex(
            model_name='activitylog',
            index=models.Index(fields=['user', '-timestamp'], name='engagement_activity_user_timestamp_idx'),
        ),
        migrations.AddIndex(
            model_name='activitylog',
            index=models.Index(fields=['activity_type', '-timestamp'], name='engagement_activity_type_timestamp_idx'),
        ),
    ]
