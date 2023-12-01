from django.urls import path

from account.views import AccountHomeTemplateView

urlpatterns = [
    path('', AccountHomeTemplateView.as_view(), name='account-home'),
]
