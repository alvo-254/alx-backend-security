from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from .models import RequestLog, SuspiciousIP


@shared_task
def send_alert_email(ip, reason):
    """
    Send an alert email when a suspicious IP is detected.
    """
    subject = f"Suspicious IP Detected: {ip}"
    message = f"Reason: {reason}"
    send_mail(
        subject,
        message,
        "admin@example.com",
        ["security@example.com"],
        fail_silently=True,
    )
    return f"Alert sent for {ip}"


@shared_task
def detect_anomalies():
    """
    Detect anomalies such as:
    - Too many requests per IP in the last hour.
    - Accessing sensitive paths like /admin or /login.
    """
    one_hour_ago = timezone.now() - timedelta(hours=1)
    logs = RequestLog.objects.filter(timestamp__gte=one_hour_ago)

    ip_counts = {}
    for log in logs:
        # Count requests per IP
        ip_counts[log.ip_address] = ip_counts.get(log.ip_address, 0) + 1

        # Flag sensitive paths
        if log.path in ["/admin", "/login"]:
            suspicious, created = SuspiciousIP.objects.get_or_create(
                ip_address=log.ip_address,
                reason="Accessed sensitive path"
            )
            if created:
                send_alert_email.delay(log.ip_address, "Accessed sensitive path")

    # Flag excessive traffic
    for ip, count in ip_counts.items():
        if count > 100:
            suspicious, created = SuspiciousIP.objects.get_or_create(
                ip_address=ip,
                reason="Exceeded 100 requests/hour"
            )
            if created:
                send_alert_email.delay(ip, "Exceeded 100 requests/hour")

    return "Anomaly detection complete"
