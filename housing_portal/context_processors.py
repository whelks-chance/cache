from cache import settings


def API_URL(request):
    return {'API_URL': settings.API_URL}