from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, permissions, status, views
from rest_framework.request import Request
from rest_framework.response import Response

from api.referral.services import referral_service
from common.permissions import OnlyRenterPermission


class GetReferralLinkView(views.APIView):
    permission_classes = (permissions.IsAuthenticated, OnlyRenterPermission)

    def get(self, request: Request, *args, **kwargs):

        try:
            links = referral_service.get_user_ref_links(request.user)
        except referral_service.NoReferralError:
            raise exceptions.NotFound([_("Неудалось получить ссылку")])

        return Response(links, status=status.HTTP_200_OK)
