from rest_framework import viewsets
from . import models, serializers
from core.helpers import send_mail
from core.logger import logger
from django.template.loader import render_to_string
from rest_framework.response import Response
from rest_framework import status


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = models.Feedback.objects.none()
    serializer_class = serializers.FeedbackSerializer

    def send_notification(self, obj):
        subject = f'Обратная связь №{obj.pk}'
        message = render_to_string(
            'mails/feedback.html', {'obj': obj})
        to = [ae.email for ae in models.AdminEmail.objects.all()]
        send_mail.delay(subject, to, message)

    def perform_create(self, serializer):
        obj = serializer.save()
        self.send_notification(obj)