import datetime
from django.utils.deprecation import MiddlewareMixin
from .models import RequestLog

class IPLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip = self.get_client_ip(request)
        path = request.path
        timestamp = datetime.datetime.now()

        RequestLog.objects.create(
            ip_address=ip,
            path=path,
            timestamp=timestamp
        )

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")
