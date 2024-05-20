from django.utils.deprecation import MiddlewareMixin

class MobileDetectionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        request.is_mobile = "mobi" in user_agent
