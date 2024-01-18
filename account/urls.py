from django.urls import path

from account.views import AccountHomeTemplateView, LoginTemplateView, RegisterCreateView, VerifyEmailView

urlpatterns = [
    path('', AccountHomeTemplateView.as_view(), name='account-home'),
    path('login/', LoginTemplateView.as_view(), name='login'),
    path('register/', RegisterCreateView.as_view(), name='register'),
    path('verify-email/<str:user_id>/<str:token>/', VerifyEmailView.as_view(), name='verify_email'),
]
