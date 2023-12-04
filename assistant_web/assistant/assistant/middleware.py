from django.utils import translation
from django.conf import settings

LANGUAGE_SESSION_KEY = getattr(settings, "LANGUAGE_SESSION_KEY", "django_language")


class SetLanguageMiddleware:
    def __init__(self, get_response):
        """
        The __init__ function is called when the middleware class is instantiated.
        The get_response parameter represents the next middleware in the stack, or
        the view function if this is the last piece of middleware in a stack.

        :param self: Represent the instance of the class
        :param get_response: Get the response from the view
        :return: A get_response function
        :doc-author: Trelent
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        The __call__ function is called when the middleware is used as a function.
        This happens when it's passed to the Django application object, which calls
        the __call__ method on each middleware in turn. The __call__ method should
        return an HttpResponse object.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :return: A response object
        :doc-author: Trelent
        """
        self.process_request(request)
        response = self.get_response(request)
        language = request.GET.get("lang")
        if language:
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
        return response

    def process_request(self, request):
        """
        The process_request function is called on every request. It gets the current language from the request,
        activates it and saves it in the session.

        :param self: Represent the instance of the object itself
        :param request: Get the language from the get request
        :return: None
        :doc-author: Trelent
        """
        language = request.GET.get("lang")

        if (
            not language
        ):  # If the language is not specified in the GET request, try to find it in cookies
            language = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)

        if language:
            translation.activate(language)
            request.session[LANGUAGE_SESSION_KEY] = language
