from django.db import models
from django.utils import timezone
from datetime import datetime
from core.logger import logger


class Quarter(models.Model):
    title = models.CharField(
        verbose_name='Название')
    start_period = models.CharField(
        verbose_name='Начало', help_text='Пример 20.08')
    end_period = models.CharField(
        verbose_name='Конец', help_text='Пример 20.08')
    start_send = models.CharField(
        verbose_name='Начало отправки', help_text='Пример 20.08')
    end_send = models.CharField(
        verbose_name='Конец отправки', help_text='Пример 20.08')

    class Meta:
        verbose_name = 'Квартал'
        verbose_name_plural = 'Кварталы'
        ordering = ('title',)

    def __str__(self):
        return self.title
    
    @property
    def is_last_quarter(self):
        quarter_ids = [q.id for q in Quarter.objects.all().order_by('title')]
        current_index = quarter_ids.index(self.pk)
        return current_index == len(quarter_ids) - 1
    
    def get_next(self):
        quarter_ids = [q.id for q in Quarter.objects.all().order_by('title')]
        current_index = quarter_ids.index(self.pk)
        next_index = ((current_index + 1) % len(quarter_ids))
        return Quarter.objects.get(pk=quarter_ids[next_index])
    
    @classmethod
    def get_by_date(cls, date):
        for q in Quarter.objects.all().order_by('title'):
            start, end = cls._get_period(q.start_send, q.end_send, date.year)
            if start.date() <= date.date() and end.date() >= date.date():
                return q
        for q in Quarter.objects.all().order_by('title'):
            start, end = cls._get_period(q.start_period, q.end_period, date.year)
            if start.date() <= date.date() and end.date() >= date.date():
                return q

    @classmethod
    def _get_period(cls, start, end, year):
        datetime.now()
        start_date = datetime.strptime(f'{start}.{year}', '%d.%m.%Y')
        end_date = datetime.strptime(f'{end}.{year}', '%d.%m.%Y')
        if start_date > end_date:
            start_date = datetime.strptime(f'{end}.{year - 1}', '%d.%m.%Y')
        return [start_date, end_date]


class Report(models.Model):
    is_sended = models.BooleanField(
        verbose_name='Отправлен', default=False)
    quarter = models.ForeignKey(
        Quarter, verbose_name='Квартал', on_delete=models.CASCADE, related_name='reports')
    year = models.PositiveIntegerField(
        verbose_name='Год')
    diocese = models.ForeignKey(
        'local_hierarchy.Diocese', verbose_name='Епархия', on_delete=models.CASCADE, related_name='reports')
    diaries = models.ManyToManyField(
        'diaries.Diary', verbose_name='Дневники', blank=True)
    
    start_period = models.DateField(
        verbose_name='Начало')
    end_period = models.DateField(
        verbose_name='Конец')
    start_send = models.DateField(
        verbose_name='Начало отправки')
    end_send = models.DateField(
        verbose_name='Конец отправки')
    
    class Meta:
        verbose_name = 'Отчет'
        verbose_name_plural = 'Отчеты'
        unique_together = (('quarter', 'year', 'diocese',),)

    def __str__(self):
        return f'{self.quarter.title} {self.year} {self.diocese.title}'
    
    def save(self, *args, **kwargs):
        if not self.start_period \
            or not self.end_period \
            or not self.start_send \
            or not self.start_send:
            self.start_period = datetime.strptime(f'{self.quarter.start_period}.{self.year}', '%d.%m.%Y').date()
            self.end_period = datetime.strptime(f'{self.quarter.end_period}.{self.year}', '%d.%m.%Y').date()
            self.start_send = datetime.strptime(f'{self.quarter.start_send}.{self.year}', '%d.%m.%Y').date()
            end_send_year = self.year
            if self.quarter.is_last_quarter and self.quarter.end_send.split('.')[1] == '01':
                end_send_year += 1
            self.end_send = datetime.strptime(f'{self.quarter.end_send}.{end_send_year}', '%d.%m.%Y').date()
        return super().save(*args, **kwargs)
    
    def toggle_diary(self, diary):
        if self.diaries.filter(id=diary.id).exists():
            self.diaries.set(self.diaries.exclude(id=diary.id))
        else:
            self.diaries.add(diary)
    
    @classmethod
    def get_current(cls, diocese, today=timezone.now()):
        current_reports = cls.objects.filter(diocese=diocese, start_period__lte=today.date(), end_send__gte=today.date())

        if current_reports.filter(is_sended=False).exists():
            # Возвращаем текущий не отправленный
            return current_reports.filter(is_sended=False).get()
        elif current_reports.filter(is_sended=True).exists():
            # Возвращаем следующий так как текущий отправлен
            curent_sended = current_reports.get(is_sended=True)
            year = curent_sended.year
            if curent_sended.quarter.is_last_quarter:
                year += 1
            return cls.objects.get_or_create(diocese=diocese, year=year, quarter=curent_sended.quarter.get_next())[0]
        else:
            # Текущий еще не создан, по этому создаем и возвращаем
            quarter = Quarter.get_by_date(today)
            year = today.year
            if quarter.is_last_quarter and today.month == 0:
                year -= 1
            return cls.objects.get_or_create(quarter=quarter, diocese=diocese, year=year)[0]