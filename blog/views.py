# Create your views here.
from django.views.generic import TemplateView


class HomeTemplateView(TemplateView):
    template_name = 'blog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        context['body'] = 'This is the home page'
        return context
