from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='EventWaitlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('event_name', models.CharField(max_length=200)),
                ('position', models.PositiveIntegerField()),
                ('status', models.CharField(choices=[('waiting', 'Waiting'), ('promoted', 'Promoted'), ('registered', 'Registered'), ('cancelled', 'Cancelled')], default='waiting', max_length=20)),
                ('joined_at', models.DateTimeField(auto_now_add=True)),
                ('promoted_at', models.DateTimeField(blank=True, null=True)),
                ('notified', models.BooleanField(default=False)),
            ],
            options={'ordering': ['position']},
        ),
        migrations.AddIndex(
            model_name='eventwaitlist',
            index=models.Index(fields=['event_name', 'status'], name='waitlist_even_event_n_status_idx'),
        ),
        migrations.AddIndex(
            model_name='eventwaitlist',
            index=models.Index(fields=['position'], name='waitlist_even_positio_idx'),
        ),
    ]
