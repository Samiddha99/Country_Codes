from django.shortcuts import *
from django.http import *
from django.views.decorators.http import *
from .models import *
from django_ratelimit.decorators import ratelimit
from django.conf import settings
import traceback


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
        accuracy = request.GET.get("accuracy", '1')
        if accuracy == '3':
            accuracy = '__icontains'
        elif accuracy == '2':
            accuracy = '__iregex'
            if name != '':
                name = r"\y{0}\y".format(name)
            if short_name != '':
                short_name = r"\y{0}\y".format(short_name)
        else:
            accuracy = '__iexact'
        filter_value = {
            f'name{accuracy}': name,
            f'short_name{accuracy}': short_name,
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
            response_data = {
                "success": True,
                'total_results': data.count(),
                'countries': list(data.values('name', 'short_name', 'dial_code', 'flag'))
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
        traceback.print_exc()
        response_data = {}
        response_data["error"] = "500"
        response_data["success"] = False
        response_data["message"] = "Server Error"
        status = 500 # Internal Server Error
        return JsonResponse(response_data, status=status)