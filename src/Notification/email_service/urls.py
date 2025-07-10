from django.urls import path

from . import views

app_name = "email_service"

urlpatterns = [
    path("api/v1/send-template-mail/", views.SendEmailView.as_view(), name="send_email"),
]
