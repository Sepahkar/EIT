import jdatetime
from django.db import models

from email_service.utils import extract_variables


class JalaliDateTime(models.Model):
    created_at = models.CharField(max_length=100, help_text="Jalali date")

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.created_at = jdatetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        super().save(*args, **kwargs)


class EmailTemplate(models.Model):
    code = models.CharField(max_length=10, unique=True, help_text="Template code should follow the convention: 3 characters project name, 3 characters app name, 4 characters unique name and it must be uppercase")
    subject = models.CharField(max_length=255, help_text="Supports Django template syntax: {{ variable }}")
    body = models.TextField(help_text="Supports Django template syntax: {{ variable }}")
    to = models.CharField(max_length=255, help_text="Comma-separated list of email addresses to send the email to, whitespaces will be removed")
    cc = models.CharField(max_length=255, null=True, help_text="Comma-separated list of email addresses to send the email to, whitespaces will be removed")
    bcc = models.CharField(max_length=255, null=True, help_text="Comma-separated list of email addresses to send the email to, whitespaces will be removed")
    
    # These will be used in django commands (running by windows task scheduler) to piriodically sending failed emails 
    max_retries = models.IntegerField(default=3, help_text="Maximum number of retries for sending the email")   
    retry_delay = models.IntegerField(default=10, help_text="Delay in minutes between retries")

    def __str__(self):
        return self.code

    def _get_comma_separated_values(self, field: str) -> list:
        if field:
            return [value.strip() for value in field.split(",")]
        return []

    @property
    def get_to_emails(self):
        return self._get_comma_separated_values(self.to)

    @property
    def get_cc_emails(self):
        return self._get_comma_separated_values(self.cc)

    @property
    def get_bcc_emails(self):
        return self._get_comma_separated_values(self.bcc)

    @property
    def get_subject_variables(self):
        return extract_variables(self.subject)

    @property
    def get_body_variables(self):
        return extract_variables(self.body)


STATUS_CHOICES = (
    ("PENDING", "Pending"),
    
    # Hot retry is when the email is sent immediately after the previous attempt failed,
    # actually every email can be sent as hot retry with 3 max_retries and 20 seconds delay
    # (it can be changed services._send_with_retry function). but cold retry is related to 
    # when django command take care of sending failed emails
    ("HOT_RETRY", "Hot Retry"),
    ("COLD_RETRY", "Cold Retry"),
    
    ("FAILURE", "Failure"),
    ("SUCCESS", "Success"),
)


class EmailSendRequest(JalaliDateTime):
    template = models.ForeignKey(EmailTemplate, on_delete=models.CASCADE)
    user_provided_variables = models.JSONField(help_text="User provided variables in the email request")
    prepared_variables = models.JSONField(help_text="Prepared variables in the email request using prepare_context()")
    email_recipients = models.JSONField(help_text="JSON containing to, cc, and bcc email addresses")
    email_subject = models.CharField(max_length=255, help_text="Rendered subject of the email")
    email_body = models.TextField(help_text="Rendered body of the email")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDING")
    request_by = models.CharField(max_length=10, help_text="National ID")
    last_attempt_at = models.DateTimeField(auto_now=True, help_text="Last attempt at")
    cold_attempt_count = models.IntegerField(default=0, help_text="Number of cold attempts")

    def __str__(self):
        return f"{self.template.code} - {self.created_at}"


class EmailLog(JalaliDateTime):
    email_send_request = models.ForeignKey(EmailSendRequest, on_delete=models.CASCADE)
    
    # it can only be one of the following statuses:
    # SUCCESS, FAILURE
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    
    error_message = models.TextField(null=True)
    attempt_at = models.DateTimeField(auto_now=True, help_text="Attempt at")



class EmailVariable(models.Model):
    code = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    def __str__(self):
        return self.code
