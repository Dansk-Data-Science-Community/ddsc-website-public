from django.views.generic import ListView, DetailView
from .models import OpenSourceProject

class OSSListView(ListView):
    """Display all active OSS projects"""
    model = OpenSourceProject
    template_name = 'oss/project_list.html'
    context_object_name = 'projects'
    paginate_by = 20
    queryset = OpenSourceProject.objects.filter(active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured'] = OpenSourceProject.objects.filter(featured=True, active=True)[:3]
        return context

class OSSDetailView(DetailView):
    """Display single OSS project details"""
    model = OpenSourceProject
    template_name = 'oss/project_detail.html'
    slug_field = 'slug'
    queryset = OpenSourceProject.objects.filter(active=True)
