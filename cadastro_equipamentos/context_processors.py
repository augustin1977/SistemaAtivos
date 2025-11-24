from django.conf import settings

def ambiente_context(request):
    return {
        'AMBIENTE_TESTE': getattr(settings, 'AMBIENTE_TESTE', False)
    }
