from rest_framework import serializers

from api.cars.models import CarFleet
from api.locations.models import Location
from api.locations.serializers import LocationSerializer


class CarFleetSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = CarFleet
        fields = ["id", "name", "owner_phone_number", "location"]

    def create(self, validated_data):
        location_data = validated_data.pop("location")
        location = Location.objects.create(**location_data)
        return CarFleet.objects.create(location=location, **validated_data)

    def update(self, instance, validated_data):
        location_data = validated_data.pop("location", None)

        if location_data:
            location = instance.location
            for attr, value in location_data.items():
                setattr(location, attr, value)
            location.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
