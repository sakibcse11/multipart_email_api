from django.conf import settings
from rest_framework import serializers
from PIL import Image


class EmailSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=True)
    education = serializers.CharField(required=True)
    contact = serializers.CharField(max_length=50, required=True)
    address = serializers.CharField(required=True)
    project_idea = serializers.CharField(required=True)
    screenshot = serializers.ImageField(required=True)
    recipients = serializers.ListField(
        child=serializers.EmailField(),
        required=True
    )

    def validate_screenshot(self, value):
        try:
            img = Image.open(value)
            img.verify()  # verify that it is an image
            value.seek(0)

            # Check format
            if img.format not in ['JPEG', 'PNG']:
                raise serializers.ValidationError("Only JPG and PNG files are allowed.")

            # Check file size (limit to 5MB)
            if value.size > 5 * 1024 * 1024:
                raise serializers.ValidationError("Image size should not exceed 5MB.")

            return value
        except Exception:
            raise serializers.ValidationError("Invalid image file.")

    def validate_recipients(self, recipients):
        if not recipients:
            raise serializers.ValidationError("At least one recipient is required.")

        allowed_domains = settings.ALLOWED_EMAIL_DOMAINS
        allowed_special_emails = settings.ALLOWED_SPECIAL_EMAILS

        invalid_emails = []

        for email in recipients:
            # Check if it's a special allowed email
            if email in allowed_special_emails:
                continue

            # Check domain
            domain = email.split('@')[-1].lower() if '@' in email else None
            if not domain or domain not in allowed_domains:
                invalid_emails.append(email)

        if invalid_emails:
            raise serializers.ValidationError(
                f"Only Gmail, Hotmail, Yahoo, and careers@accelx.net are allowed. "
                f"Invalid emails: {', '.join(invalid_emails)}"
            )

        return recipients