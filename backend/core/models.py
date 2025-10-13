from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_migrate
from django.dispatch import receiver


class SortableMixin(models.Model):
    sort = models.PositiveIntegerField(
        verbose_name='Соритровка', default=0)

    class Meta:
        abstract = True
        ordering = ('sort', 'pk',)

    def get_sortable_queryset(self):
        # Кверисет относительно которого сортируется каждый элемент, изначально все объекты модели
        return self._meta.model.objects.all()
    
    def save(self, *args, **kwargs):
        save = super().save(*args, **kwargs)
        if not self.sort:
            sortable_pool = self.get_sortable_queryset()
            max_sort = sortable_pool.order_by('-sort')[0].sort
            self.sort = (max_sort // 10 + 1) * 10
            self.save()
        return save
    
    @classmethod
    def set_default_sort(cls, sender, **kwargs):
        for object in cls.objects.filter(sort=0):
            object.save()

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        post_migrate.connect(cls.set_default_sort, weak=False)


class SeoBase(models.Model):
    seo_fields = ['meta_title', 'meta_description']

    meta_title = models.CharField(
        verbose_name="SEO заголовок", default='',
        blank=True, max_length=300)
    meta_description = models.TextField(
        verbose_name="Meta Description", null=True, blank=True)

    class Meta:
        abstract = True


class TimestampModelMixin(models.Model):
    created_at = models.DateTimeField(
        verbose_name='Создан', default=timezone.now)
    updated_at = models.DateTimeField(
        verbose_name='Обновлен', auto_now=True)
    
    class Meta:
        abstract = True


""" Используется в wishlish и cart для получения и создания объектов как авторизованных пользователей так и не авторизованных"""
class UniversalUserMixin(models.Model):
    SESSION_KEY = None
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        blank=True, null=True)
    
    class Meta:
        abstract = True

    @classmethod
    def get_from_request(cls, request):
        """ Получение объекта из реквеста """

        if request.user.is_authenticated:
            return cls._get_or_create_for_auth_user(request)
        else:
            return cls._get_or_create_for_unauth_user(request)

    @classmethod
    def _get_or_create_for_auth_user(cls, request):
        """ Получение или создание объекта авторизированного пользователя """
        obj, _ = cls.objects.get_or_create(user=request.user)
        return obj

    @classmethod
    def _get_or_create_for_unauth_user(cls, request):
        """ Получение или создание объекта для неавторизованного юзера """
        pk = request.session.get(cls.SESSION_KEY)
        try:
            return cls.objects.get(pk=pk)
        except cls.DoesNotExist:
            return cls._create_for_unauth_user(request)

    @classmethod
    def _create_for_unauth_user(cls, request):
        """Создание объекта для неавторизованного пользователя"""
        obj = cls.objects.create()
        request.session[cls.SESSION_KEY] = obj.pk
        request.session.modified = True
        return obj