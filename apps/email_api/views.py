from django.contrib.messages import success
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.email_api.serializers import EmailSerializer
from apps.email_api.services import EmailService


# Create your views here.
class SendSelectionEmailView(APIView):
    parser_class = (MultiPartParser, FormParser)
    serializer_class = EmailSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email_service = EmailService()

            email_sent, message, recipient_count = email_service.send_email(serializer.validated_data)
            if email_sent:
                response_data = {
                    'status':'success',
                    'message':f'Email sent to {recipient_count} recipients',
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                    'status':'error',
                    'message': message,
                }
                return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            response_data = {
                'status':'error',
                'message': serializer.errors,
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)