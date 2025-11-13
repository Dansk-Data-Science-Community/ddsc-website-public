from django.views.generic import TemplateView


class OpenSourceAwardView(TemplateView):
    template_name = "opensource/award.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'DDSC Open Source Award'
        return context
