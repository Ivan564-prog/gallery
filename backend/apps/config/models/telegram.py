from django.db import models
from solo.models import SingletonModel
import requests


class Bot(SingletonModel):
    access_token = models.CharField(
        verbose_name='Токен',
        help_text='Получается у BotFather в телеграм пишем команду /newbot и после его имя оканчивающееся на _bot, в поле вставляем полученный токен'
    )
    chat_ids = models.TextField(
        verbose_name='Ид чатов',
        help_text='Получается у userinfobot, пишем /start и забираем от туда поле Id'
    )

    class Meta:
        verbose_name = 'Настройки телеграм бота'
        verbose_name_plural = 'Настройки телеграм бота'

    def __str__(self):
        return 'Настройки телеграм бота'

    def send_message(self, msg):
        for chat_id in self.chat_ids.split('\n'):
            url = f'https://api.telegram.org/bot{self.access_token}/sendMessage'
            requests.post(url, data={'chat_id': chat_id, 'text': msg})

