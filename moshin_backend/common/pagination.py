# pagination.py
from django.conf import settings
from django.db import models
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from api.cars.models import Cars


class DynamicPagination(PageNumberPagination):
    page_size = settings.PAGE_SIZE
    page_size_query_param = "limit"
    max_page_size = 100


class CarsPagination(DynamicPagination):
    def get_paginated_response(self, data):
        prices = Cars.objects.aggregate(
            min_price=models.Min("price"), max_price=models.Max("price")
        )
        return Response(
            {
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "min_price": prices["min_price"],
                "max_price": prices["max_price"],
                "results": data,
            }
        )
