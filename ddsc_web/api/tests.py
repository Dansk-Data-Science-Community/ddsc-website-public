"""Mobile API tests"""
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from pages.models import Page
from oss.models import OpenSourceProject

class MobileAuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='pass123', email='test@test.com')
    
    def test_login(self):
        response = self.client.post('/api/auth/login/', {'username': 'testuser', 'password': 'pass123'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json())
    
    def test_invalid_credentials(self):
        response = self.client.post('/api/auth/login/', {'username': 'testuser', 'password': 'wrong'})
        self.assertEqual(response.status_code, 400)

class MobilePageAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.page = Page.objects.create(title="Test", content="Content", published=True)
    
    def test_list_pages(self):
        response = self.client.get('/api/pages/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])
    
    def test_page_detail(self):
        response = self.client.get(f'/api/pages/{self.page.slug}/')
        self.assertEqual(response.status_code, 200)

class MobileOSSAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.project = OpenSourceProject.objects.create(
            name="Test Project", github_url="http://github.com/test", github_stars=10, active=True
        )
    
    def test_list_projects(self):
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, 200)
    
    def test_featured_endpoint(self):
        self.project.featured = True
        self.project.save()
        response = self.client.get('/api/projects/featured/')
        self.assertEqual(response.status_code, 200)

class MobileWaitlistAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_join_waitlist(self):
        response = self.client.post('/api/waitlist/join/', {
            'email': 'user@test.com',
            'event_name': 'Meetup'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])
    
    def test_check_status(self):
        response = self.client.get('/api/waitlist/status/?email=user@test.com')
        self.assertEqual(response.status_code, 200)
