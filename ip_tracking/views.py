from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from ratelimit.decorators import ratelimit

@ratelimit(key="ip", rate="5/m", block=True)
def anonymous_view(request):
    return JsonResponse({"message": "Hello Anonymous!"})

@login_required
@ratelimit(key="ip", rate="10/m", block=True)
def login_view(request):
    return JsonResponse({"message": "Hello Authenticated User!"})
