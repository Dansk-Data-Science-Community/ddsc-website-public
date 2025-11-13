from django.test import TestCase
from .models import OpenSourceProject

class OSSProjectTest(TestCase):
    def setUp(self):
        self.project = OpenSourceProject.objects.create(
            name="Test Project",
            github_url="https://github.com/testuser/testproject",
            description="A test project",
            github_stars=100,
            languages="Python, Django"
        )
    
    def test_project_creation(self):
        self.assertEqual(self.project.name, "Test Project")
        self.assertTrue(self.project.active)
    
    def test_slug_generation(self):
        self.assertEqual(self.project.slug, "test-project")
    
    def test_github_owner_repo(self):
        self.assertEqual(self.project.github_owner_repo, "testuser/testproject")
