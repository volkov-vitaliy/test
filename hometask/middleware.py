from django.conf import settings


def extract_language(request):
    accept_language = request.headers.get('Accept-Language', settings.DEFAULT_LANGUAGE)
    return accept_language.split(',')[0].split('-')[0]


def current_language(get_response):
    """ Middleware to add to request current languages based on Accept-Language header"""
    def middleware(request):
        request.current_language = extract_language(request)
        return get_response(request)

    return middleware