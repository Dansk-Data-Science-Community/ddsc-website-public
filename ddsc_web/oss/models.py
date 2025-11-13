from django.db import models

class OpenSourceProject(models.Model):
    """Showcase DDSC community open source projects"""
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    github_url = models.URLField()
    github_stars = models.IntegerField(default=0)
    languages = models.CharField(max_length=200, help_text="Comma-separated: Python, JavaScript, etc")
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-github_stars', '-created_at']
        verbose_name = 'Open Source Project'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    @property
    def github_owner_repo(self):
        """Extract owner/repo from GitHub URL"""
        if self.github_url:
            parts = self.github_url.strip('/').split('/')
            if len(parts) >= 2:
                return f"{parts[-2]}/{parts[-1]}"
        return ""
