from django.http import HttpResponseTooManyRequests
from django.utils import timezone
from collections import defaultdict
from datetime import timedelta

class MessageRateLimitMiddleware:
    """Middleware to limit the number of chat messages a user can send within a time window."""

    def __init__(self, get_response):
        self.get_response = get_response
        self.message_count = defaultdict(list)  # Dictionary to track message counts by IP

    def __call__(self, request):
        # Only track POST requests to the messaging endpoint
        if request.method == 'POST' and request.path == '/api/messages/':
            ip_address = self.get_client_ip(request)
            current_time = timezone.now()

            # Clean up old timestamps
            self.message_count[ip_address] = [
                timestamp for timestamp in self.message_count[ip_address]
                if timestamp > current_time - timedelta(minutes=1)
            ]

            # Check the number of messages sent in the last minute
            if len(self.message_count[ip_address]) >= 5:
                return HttpResponseTooManyRequests("You have exceeded the message limit. Please wait a minute before sending more messages.")

            # Log the current message timestamp
            self.message_count[ip_address].append(current_time)

        # Call the next middleware or view
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Get the client's IP address from the request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip