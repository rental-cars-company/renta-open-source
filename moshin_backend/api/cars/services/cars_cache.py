from django.core.cache import cache
from rest_framework.response import Response

from common.constants import CACHE_TIMEOUT


def get_cached_list_response(
    viewset, request, base_cache_key, timeout=CACHE_TIMEOUT
):
    user_id = request.user.id if request.user.is_authenticated else "anon"
    full_cache_key = f"{base_cache_key}:user:{user_id}"

    cached = cache.get(full_cache_key)
    if cached:
        return Response(cached)

    response = viewset.list_original(request)
    cache.set(full_cache_key, response.data, timeout)
    return response


def get_cached_detail_response(viewset, request, pk, timeout=CACHE_TIMEOUT):
    cache_key = f"cars:detail:{pk}"
    cached = cache.get(cache_key)
    if cached:
        return Response(cached)

    response = viewset.retrieve_original(request, pk=pk)
    cache.set(cache_key, response.data, timeout)
    return response


def clear_car_cache(pk=None):
    if pk:
        cache.delete(f"cars:detail:{pk}")
    cache.delete_pattern("cars:list:*")
