from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import get_template
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import View
from django.views.generic import TemplateView, CreateView

from account.forms import RegisterForm
from account.models import EmailVerificationToken
from bcb22 import settings


# Create your views here.
class AccountHomeTemplateView(TemplateView):
    template_name = 'account/account_home.html'


class LoginTemplateView(TemplateView):
    template_name = 'account/login.html'


class RegisterCreateView(CreateView):
    form_class = RegisterForm
    template_name = 'account/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        try:
            # Create verification token
            verification_token = EmailVerificationToken(user=user)
            verification_token.save()

            # Send verification email
            current_site = get_current_site(self.request)
            mail_subject = 'Activate your account'
            to_email = form.cleaned_data.get('email')
            from_email = settings.EMAIL_HOST_USER
            verrification_url = reverse('verify_email',
                                        args=[urlsafe_base64_encode(force_bytes(user.pk)), verification_token.token])
            comp_verification_url = f'{current_site.domain}{verrification_url}'
            context_obj = {
                'user': user,
                'url': comp_verification_url,
            }
            message = get_template('account/verification_email.html').render(context=context_obj)
            mail = EmailMessage(
                subject=mail_subject,
                body=message,
                from_email=from_email,
                to=[to_email]
            )
            mail.content_subtype = 'html'
            mail.send(fail_silently=False)
            messages.success(self.request, 'Account created successfully. Please check your email for verification.')

        except Exception as e:
            print(e)
            pass
        return super(RegisterCreateView, self).form_valid(form)

    def form_invalid(self, form):
        error_message = form.errors.as_text()
        raise ValidationError(error_message)


class VerifyEmailView(View):
    def get(self, request, user_id, token, *args, **kwargs):
        User = get_user_model()
        user = get_object_or_404(User, pk=urlsafe_base64_encode(user_id))
        verification_token = EmailVerificationToken.objects.filter(user=user).first()
        if verification_token and verification_token.token == token:
            user.is_active = True
            user.save()
            verification_token.delete()
            return redirect('login')
