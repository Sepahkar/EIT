from rest_framework import serializers

from email_service.models import EmailTemplate, EmailVariable
from email_service.utils import extract_variables


class EmailVariableValidator:
    """Validator to ensure all required template variables are provided."""

    def __init__(self, template_field="template_code"):
        self.template_field = template_field


    def __call__(self, data):
        template_code = data.get(self.template_field)
        variables = data.get("variables", {})
        
        try:
            template = EmailTemplate.objects.get(code=template_code)
            required_vars_body = extract_variables(template.body)
            required_vars_subject = extract_variables(template.subject)
            required_vars_to = set(template.get_to_emails)
            required_vars_cc = set(template.get_cc_emails)
            required_vars_bcc = set(template.get_bcc_emails)

            all_required_vars = (
                required_vars_body
                | required_vars_subject
                | required_vars_to
                | required_vars_cc
                | required_vars_bcc
            )

            missing_vars = all_required_vars - set(variables.keys())

            # try to find missing variables in the EmailVariable model
            static_vars = EmailVariable.objects.filter(code__in=missing_vars).values_list("code", flat=True)
            missing_vars = missing_vars - set(static_vars)

            # if there are still missing variables, raise an error
            if missing_vars:
                msg = f"Missing required variables for template '{template_code}': {', '.join(missing_vars)}"
                raise serializers.ValidationError(msg)

        except EmailTemplate.DoesNotExist:
            msg = f"Template '{template_code}' does not exist"
            raise serializers.ValidationError(msg)


class TemplateEmailSendSerializer(serializers.Serializer):
    template_code = serializers.CharField(required=True)
    variables = serializers.DictField(required=True)

    class Meta:
        validators = [EmailVariableValidator()]

