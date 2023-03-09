from django.utils.decorators import decorator_from_middleware_with_args
from django.middleware.time import TimezoneMiddleware

def timing(view_func):
    middleware = TimezoneMiddleware()

    def wrapper(request, *args, **kwargs):
        middleware.process_request(request)
        start = middleware._start_time()
        response = view_func(request, *args, **kwargs)
        duration = middleware.process_response(request, response)
        print(f"Tempo de resposta: {duration.total_seconds()} segundos")
        return response

    return decorator_from_middleware_with_args(middleware_class=type(middleware))(wrapper)