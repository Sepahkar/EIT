import logging
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import EmailMessage
from django.conf import settings

from email_service.models import EmailSendRequest, EmailLog

logger = logging.getLogger("EMAIL_SERVICE")


class Command(BaseCommand):
    help = "Retries sending emails that are in COLD_STATUS state based on template retry settings"

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS("Starting cold email retry process...")
        )

        # Get all email requests in COLD_STATUS
        cold_emails = EmailSendRequest.objects.filter(
            status="COLD_RETRY"
        ).select_related('template')

        retry_count = 0
        skip_count = 0

        for email_request in cold_emails:
            template = email_request.template

            # Check if we have remaining retry attempts
            if email_request.cold_attempt_count >= template.max_retries:
                skip_count += 1
                continue

            # Check if enough time has passed since the last attempt
            time_since_last_attempt = (
                timezone.now() - email_request.last_attempt_at
            )
            required_delay = timedelta(minutes=template.retry_delay)

            if time_since_last_attempt < required_delay:
                skip_count += 1
                continue

            # All conditions met, retry sending the email
            try:
                self.stdout.write(f"Retrying email {email_request.id}...")

                email = EmailMessage(
                    subject=email_request.email_subject,
                    body=email_request.email_body,
                    to=list(email_request.email_recipients['to']),
                    cc=list(email_request.email_recipients['cc']) if email_request.email_recipients['cc'] else None,
                    bcc=list(email_request.email_recipients['bcc']) if email_request.email_recipients['bcc'] else None,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                )
                email.send(fail_silently=False)
                
                EmailLog.objects.create(
                    email_send_request=email_request,
                    status="SUCCESS",
                    error_message=None,
                )

                email_request.cold_attempt_count += 1
                email_request.status = "SUCCESS"
                email_request.save()
                self.stdout.write(self.style.SUCCESS(f"Email {email_request.id} sent successfully"))

            except Exception as e:
                msg = f"Email {email_request.id} sending failed {str(e)}"
                logger.error(msg, exc_info=True)
                EmailLog.objects.create(
                    email_send_request=email_request,
                    status="FAILURE",
                    error_message=msg,
                )
                self.stdout.write(self.style.WARNING(msg))

                email_request.cold_attempt_count += 1
                if email_request.cold_attempt_count >= template.max_retries:
                    email_request.status = "FAILURE"
                email_request.save()
            finally: 
                retry_count += 1


        self.stdout.write(
            self.style.SUCCESS(
                f"Completed cold email retry process. "
                f"Retried: {retry_count}, Skipped: {skip_count}"
            )
        )
