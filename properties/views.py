# properties/views.py
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .utils import get_all_properties

@cache_page(60 * 15)  # Cache entire view for 15 minutes
def property_list(request):
    properties = get_all_properties()
    data = [
        {
            "id": p.id,
            "title": p.title,
            "price": p.price,
            "location": p.location,
        }
        for p in properties
    ]
    return JsonResponse(data, safe=False)
