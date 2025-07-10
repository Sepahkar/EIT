import time

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.core.validators import validate_email
from django.template import Context, Template

from .models import EmailLog, EmailTemplate, EmailVariable, EmailSendRequest


def _is_valid_email(email):
    """Validate email format using Django's validator."""
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def prepare_context(template: EmailTemplate, context: dict) -> dict:
    """
    Every template contains certain variables that may exist in the message,
    subject, to, cc, and bcc. The method of filling these variables is important.
    User-provided variables take first priority. If any variables are missing from
    the user's context, they should be filled using the EmailVariable model.

    Notice: Do not worry about the variables that are not in both context and EmailVariable model,
    if the code reach this point, it means that the serializer has already checked for the
    presence of all required variables in the context and EmailVariable model.
    """
    prepared_context = context.copy()

    # Collect all variable names needed by the template
    required_variables = set()

    # Add email address variables
    required_variables.update(set(template.get_to_emails))
    required_variables.update(set(template.get_cc_emails))
    required_variables.update(set(template.get_bcc_emails))

    # Add variables from body and subject
    required_variables.update(template.get_subject_variables)
    required_variables.update(template.get_body_variables)

    # Fill in missing variables from EmailVariable model
    for var_name in required_variables:
        if var_name not in prepared_context:
            try:
                email_var = EmailVariable.objects.get(code=var_name)
                prepared_context[var_name] = email_var.value
            except EmailVariable.DoesNotExist:
                # This should never happen, because the serializer has already checked for the
                # presence of all required variables in the EmailVariable model.
                raise Exception(
                    f"Variable '{var_name}' not found in EmailVariable model"
                )

    return prepared_context


def _extract_email_addresses(
    template: EmailTemplate, context: dict
) -> tuple[set, set, set]:
    """
    Extract and validate email addresses from template fields using the provided context.
    """
    to = set()
    cc = set()
    bcc = set()

    def validate_and_add_emails(
        email_vars: set, target_set: set, field_name: str
    ):
        for var in email_vars:
            emails = context.get(var, set())

            # sometimes the variable is a string, not a set of emails
            if isinstance(emails, str):
                emails = [emails]

            for email in emails:
                if not _is_valid_email(email):
                    msg = f"Invalid email format in {field_name} field: {email}"
                    raise Exception(msg)
                target_set.add(email)

    validate_and_add_emails(template.get_to_emails, to, "TO")
    validate_and_add_emails(template.get_cc_emails, cc, "CC")
    validate_and_add_emails(template.get_bcc_emails, bcc, "BCC")

    return to, cc, bcc


def send_template_email(template_name: str, context: dict, request_by: str):
    """
    Send a template email.
    """
    template = EmailTemplate.objects.get(code=template_name)

    # Using dynamic(user-provided) and static(EmailVariable) variables
    prepared_context = prepare_context(template, context)

    to, cc, bcc = _extract_email_addresses(template, prepared_context)

    # Render the body and subject templates with the provided context
    context_obj = Context(prepared_context)

    body_template = Template(template.body)
    subject_template = Template(template.subject)

    message = body_template.render(context_obj)
    subject = subject_template.render(context_obj)

    # So far, so good! Now we can send the email, but first,
    # we need to create an email request object in the database
    # (for status tracking).
    email_recipients = {
        "to": list(to),
        "cc": list(cc),
        "bcc": list(bcc),
    }
    email_request = EmailSendRequest.objects.create(
        template=template,
        user_provided_variables=context,
        prepared_variables=prepared_context,
        email_recipients=email_recipients,
        email_subject=subject,
        email_body=message,
        status="PENDING",
        request_by=request_by,
    )

    # now we can send the email
    _send_with_retry(
        to,
        cc,
        bcc,
        subject,
        message,
        3,
        5,
        email_request,
    )


def _send_with_retry(
    to,
    cc,
    bcc,
    subject,
    message,
    max_retries,
    delay,
    email_request: EmailSendRequest,
):
    """Send email with retry logic."""

    # HOT RETRY
    for attempt in range(max_retries):
        try:
            email = EmailMessage(
                subject=subject,
                body=message,
                to=list(to),
                cc=list(cc) if cc else None,
                bcc=list(bcc) if bcc else None,
                from_email=settings.DEFAULT_FROM_EMAIL,
            )
            email.content_subtype = 'html'
            email.send(fail_silently=False)

            email_request.status = "SUCCESS"
            email_request.save()

            EmailLog.objects.create(
                email_send_request=email_request,
                status="SUCCESS",
                error_message=None,
            )

            return

        except Exception as e:
            error_msg = str(e)
            attempt_num = attempt + 1

            email_request.status = "HOT_RETRY"
            email_request.save()

            EmailLog.objects.create(
                email_send_request=email_request,
                status="FAILURE",
                error_message=error_msg,
            )

            # If we have more retries, wait before trying again
            if attempt_num < max_retries:
                time.sleep(delay)
            else:
                email_request.status = "COLD_RETRY"
                email_request.save()    

                msg = (
                    "HOT_RETRY failed after %d attempts for email request %s"
                    % (max_retries, email_request.id)
                )
                raise Exception(msg)
