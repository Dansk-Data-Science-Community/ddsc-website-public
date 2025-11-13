from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='OpenSourceProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('description', models.TextField()),
                ('github_url', models.URLField()),
                ('github_stars', models.IntegerField(default=0)),
                ('languages', models.CharField(help_text='Comma-separated: Python, JavaScript, etc', max_length=200)),
                ('featured', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'ordering': ['-github_stars', '-created_at'], 'verbose_name': 'Open Source Project'},
        ),
    ]
