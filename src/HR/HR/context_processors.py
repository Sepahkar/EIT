from django.conf import settings


def my_variable(request):
    return {
        "PROCESS_MANAGEMENT_STATIC_IMAGES":settings.PROCESS_MANAGEMENT_STATIC_IMAGES
    }
