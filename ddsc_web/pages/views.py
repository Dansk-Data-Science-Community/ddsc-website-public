from django.views.generic import ListView, DetailView
from .models import Page

class PageListView(ListView):
    model = Page
    template_name = 'pages/page_list.html'
    context_object_name = 'pages'
    paginate_by = 20
    queryset = Page.objects.filter(published=True)

class PageDetailView(DetailView):
    model = Page
    template_name = 'pages/page_detail.html'
    slug_field = 'slug'
    queryset = Page.objects.filter(published=True)
