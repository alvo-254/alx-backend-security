import datetime
import requests
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden
from django.core.cache import cache

from .models import RequestLog, BlockedIP


class IPLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip = self.get_client_ip(request)

        # 🚫 Block blacklisted IPs
        if BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Your IP is blocked.")

        # 🌍 Get location (cached for 24h)
        geo_data = cache.get(ip)
        if not geo_data:
            try:
                response = requests.get(f"https://ipinfo.io/{ip}/json", timeout=3)
                data = response.json()
                geo_data = {
                    "country": data.get("country"),
                    "city": data.get("city")
                }
                cache.set(ip, geo_data, 86400)  # 24h
            except Exception:
                geo_data = {"country": None, "city": None}

        # 📝 Save log
        RequestLog.objects.create(
            ip_address=ip,
            path=request.path,
            timestamp=datetime.datetime.now(),
            country=geo_data["country"],
            city=geo_data["city"]
        )

    def get_client_ip(self, request):
        """Extract client IP (handles proxies)."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")
