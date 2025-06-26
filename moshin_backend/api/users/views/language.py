from rest_framework import permissions, response, status, views


class SetLanguageView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        lang = request.data.get("language")
        if lang not in ("ru", "uz", "en"):
            return response.Response(
                {"detail": "bad language"}, status=status.HTTP_400_BAD_REQUEST
            )
        request.user.language = lang
        request.user.save(update_fields=["language"])
        return response.Response({"detail": "ok"})
