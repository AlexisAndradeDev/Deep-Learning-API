from django.http import JsonResponse

def custom404(request, exception=None):
    return JsonResponse({
        'error': f'Bad request.',
        }, status=400,
    )

def custom404(request, exception=None):
    return JsonResponse({
        'error': f'The url was not found.',
        }, status=404,
    )

def custom500(request, exception=None):
    return JsonResponse({
        'error': f'Internal server error.',
        }, status=500,
    )
