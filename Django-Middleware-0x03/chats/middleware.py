import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename='requests.log',  # Log file name
    level=logging.INFO,  # Log level
    format='%(asctime)s - %(message)s',  # Log format
)

class RequestLoggingMiddleware:
    """Middleware to log user requests."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the user from the request
        user = request.user if request.user.is_authenticated else 'Anonymous'

        # Log the request details
        logging.info(f"User: {user} - Path: {request.path}")

        # Call the next middleware or view
        response = self.get_response(request)

        return response
