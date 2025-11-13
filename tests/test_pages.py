"""Test suite for pages (news/content) app"""
import pytest
from pages.models import Page

@pytest.mark.django_db
@pytest.mark.unit
class TestPages:
    """Page model tests"""
    
    def test_create_page(self):
        """Test creating a page"""
        page = Page.objects.create(
            title="Test Page",
            content="Test content",
            published=True
        )
        assert page.title == "Test Page"
        assert page.published is True
    
    def test_page_slug_generation(self):
        """Test slug auto-generation"""
        page = Page.objects.create(
            title="My Test Page",
            content="Content",
            published=True
        )
        assert page.slug == "my-test-page"
    
    def test_unpublished_pages_filter(self):
        """Test filtering published vs unpublished"""
        Page.objects.create(title="Published", content="Content", published=True)
        Page.objects.create(title="Draft", content="Content", published=False)
        
        published = Page.objects.filter(published=True)
        assert published.count() == 1
        assert published[0].title == "Published"
    
    @pytest.mark.api
    def test_page_list_endpoint(self, api_client):
        """Test page list API"""
        Page.objects.create(title="News 1", content="Content", published=True)
        response = api_client.get('/api/v1/pages/')
        assert response.status_code == 200
        assert response.json()['success'] is True
    
    @pytest.mark.api
    def test_page_detail_endpoint(self, api_client):
        """Test page detail API"""
        page = Page.objects.create(title="News", content="Content", published=True)
        response = api_client.get(f'/api/v1/pages/{page.slug}/')
        assert response.status_code == 200
