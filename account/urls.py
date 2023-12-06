from django.urls import path

from account.views import AccountHomeTemplateView, LoginTemplateView

urlpatterns = [
    path('', AccountHomeTemplateView.as_view(), name='account-home'),
    path('login/', LoginTemplateView.as_view(), name='login'),
]
