from django.urls import path

from api.referral.views import GetReferralLinkView

urlpatterns = [
    path("my-link/", GetReferralLinkView.as_view()),
]
