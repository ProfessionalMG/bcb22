from django.views.generic import TemplateView


# Create your views here.
class AccountHomeTemplateView(TemplateView):
    template_name = 'account/account_home.html'


class LoginTemplateView(TemplateView):
    template_name = 'account/login.html'
