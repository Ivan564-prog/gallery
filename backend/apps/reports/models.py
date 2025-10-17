from django.db import models


class Quarter(models.Model):
    title = models.CharField(verbose_name='Название')
    start_period = models.CharField(verbose_name='Начало', help_text='Пример 20.08')
    end_period = models.CharField(verbose_name='Конец', help_text='Пример 20.08')
    start_send = models.CharField(verbose_name='Начало отправки', help_text='Пример 20.08')
    start_send = models.CharField(verbose_name='Конец отправки', help_text='Пример 20.08')

    class Meta:
        verbose_name = 'Квартал'
        verbose_name_plural = 'Кварталы'
        ordering = ('title',)

    def __str__(self):
        return self.title
    

class Report(models.Model):
    is_sended = models.BooleanField(
        verbose_name='Отправлен', default=False)
    quarter = models.ForeignKey(
        Quarter, verbose_name='Квартал', on_delete=models.CASCADE, related_name='reports')
    year = models.CharField(
        verbose_name='Год')
    diocese = models.ForeignKey(
        'local_hierarchy.Diocese', verbose_name='Епархия', on_delete=models.CASCADE, related_name='reports')
    diaries = models.ManyToManyField('diaries.Diary', verbose_name='Дневники', blank=True)
    
    class Meta:
        verbose_name = 'Отчет'
        verbose_name_plural = 'Отчеты'
        unique_together = (('quarter', 'year', 'diocese',),)

    def __str__(self):
        return f'{self.quarter.title} {self.year} {self.diocese.title}'