from django.urls import path
from .views import SendSelectionEmailView

urlpatterns = [
    path('send-selection-email/', SendSelectionEmailView.as_view(), name='send-selection-email'),
]