import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from email_service.services import send_template_email

from .serializers import TemplateEmailSendSerializer

logger = logging.getLogger("EMAIL_SERVICE")

class SendEmailView(APIView):
    def post(self, request):
        serializer = TemplateEmailSendSerializer(data=request.data)
        if not serializer.is_valid():
            logger.exception(serializer.errors, extra={"request": request})
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        template_code = data.get("template_code")
        variables = data.get("variables")

        try:
            send_template_email(
                template_name=template_code,
                context=variables,
                request_by=request.user.national_code,
            )
            return Response(status=200)

        except Exception as e:
            logger.exception(f"Error sending email: {e}", extra={"request": request})
            return Response({"status": "error", "error": str(e)}, status=500)
