from rest_framework import views

from api.authentication.serializers import LoginResponseSerializer
from api.authentication.services import auth_service


class LoginViewBase(views.APIView):

    def get_validated_data(self, request) -> dict:
        serializer = self.get_request_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data: dict = serializer.validated_data  # type: ignore
        return validated_data

    def get_response_serializer(self, user) -> LoginResponseSerializer:
        token_data = auth_service.get_token_pair(user)
        return LoginResponseSerializer(data={**token_data, "user_id": user.id})

    def get_request_serializer(self, *args, **kwargs):
        raise NotImplementedError
