from rest_framework import serializers


class RefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.IntegerField(read_only=True)
