from django.shortcuts import *
from django.http import *
from django.views.decorators.http import *
from .models import *
from django_ratelimit.decorators import ratelimit
from django.conf import settings


# Create your views here.
@require_safe
@ratelimit(group='Main', key='ip', rate=settings.DEFAULT_VIEW_RATE_LIMIT, method=ratelimit.ALL, block=True)
def home(request):
    context = {
        'countries': Country_Code.objects.all(),
    }
    return render(request, "index.html", context=context)

@require_safe
@ratelimit(group='Main', key='ip', rate=settings.DEFAULT_VIEW_RATE_LIMIT, method=ratelimit.ALL, block=True)
def apiSearch(request):
    try:
        name = request.GET.get("name", '')
        short_name = request.GET.get('short_name', '')
        dial_code = request.GET.get("dial_code", '')
        filter_value = {
            'name': name,
            'short_name': short_name,
            'dial_code': dial_code,
        }
        kwargs = {}
        for k, v in filter_value.items():
            if v != '':
                kwargs[k] = v
        data = Country_Code.objects.filter(**kwargs)
        response_data = {}
        status = None
        if data.count() > 0:
            if kwargs:
                data = data.first()
                response_data = {
                    "success": True,
                    'name': data.name,
                    'short_name': data.short_name,
                    'dial_code': data.dial_code,
                    'flag': data.flag
                }
                status = 200 # Ok
            else:
                response_data = {
                    "success": True,
                    'country_codes': list(data.values('name', 'short_name', 'dial_code', 'flag'))
                }
                status = 200 # Ok
        else:
            response_data = {
                "success": False,
                'error': 404,
                'message': "No data found with the given query."
            }
            status = 404 # Not Found
        return JsonResponse(response_data, status=status)
    except:
        response_data = {}
        response_data["error"] = "500"
        response_data["success"] = False
        response_data["message"] = "Server Error"
        status = 500 # Internal Server Error
        return JsonResponse(response_data, status=status)