import logging
from email.message import EmailMessage
from email.mime.image import MIMEImage

from django.conf import settings
from django.contrib.messages import success
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)

class EmailService:
    def send_email(self, data):
        subject, html_content, image_data = self.email_content(data)
        recipients = data['recipients']

        email_sent ,message,count = self.send_via_django_smtp(
            subject,html_content,image_data,recipients
        )
        if email_sent:
            return email_sent, message, count

        return False, "Failed to send email", 0


    @staticmethod
    def email_content(data):
        name = data['name']
        education = data['education']
        contact = data['contact']
        address = data['address']
        project_idea = data['project_idea']

        subject = f'Python Backend Engineer Selection Task - {name}'

        image_file = data['screenshot']
        image_file.seek(0)
        image_data = image_file.read()

        context = {
            'name': name,
            'education': education,
            'contact': contact,
            'address': address,
            'project_idea': project_idea
        }
        html_content = render_to_string('email_body.html', context=context)
        return subject, html_content, image_data
    @staticmethod
    def send_via_django_smtp(subject:str, html_content, image_data, recipients):
        try:
            email_message = EmailMultiAlternatives(
                subject= subject,
                body = '',
                from_email = settings.DEFAULT_FROM_EMAIL,
                to= recipients
            )
            email_message.attach_alternative(html_content, 'text/html')

            image = MIMEImage(image_data)
            image.add_header('Content-ID', '<github_screenshot>')
            image.add_header('Content-Disposition', 'inline', filename='github_profile_screenshot.png')
            email_message.attach(image)

            with get_connection() as connection:
                connection.send_messages([email_message])
            return True, "Email sent successfully via SMTP" , len(recipients)
        except Exception as e:
            logger.error(f'SMTP email sending failed : {str(e)}')
            return False, f'SMTP email sending failed : {str(e)}', 0