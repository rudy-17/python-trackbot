from payment.utils import checkSubscription

class MyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.checkSubscription = checkSubscription
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.user.is_authenticated:
            result = checkSubscription(request)
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        return response
