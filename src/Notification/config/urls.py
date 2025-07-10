from django.urls import path, include

urlpatterns = [
    path("EmailService/", include("email_service.urls")),
]
