from django.db import models


class Country(models.Model):
    is_active = models.BooleanField(
        verbose_name='Активность', default=True)
    title = models.CharField(
        verbose_name='Название')

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

    def __str__(self):
        return self.title
    

class Region(models.Model):
    is_active = models.BooleanField(
        verbose_name='Активность', default=True)
    country = models.ForeignKey(
        Country, verbose_name='Страна', on_delete=models.CASCADE, related_name='regions')
    title = models.CharField(
        verbose_name='Название')

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'

    def __str__(self):
        return self.title
    

class Metropolis(models.Model):
    is_active = models.BooleanField(
        verbose_name='Активность', default=True)
    region = models.ForeignKey(
        Region, verbose_name='Регион', on_delete=models.CASCADE, related_name='metropolises')
    title = models.CharField(
        verbose_name='Название')

    class Meta:
        verbose_name = 'Метрополия'
        verbose_name_plural = 'Метрополии'

    def __str__(self):
        return self.title
    

class Diocese(models.Model):
    is_active = models.BooleanField(
        verbose_name='Активность', default=True)
    metropolis = models.ForeignKey(
        Metropolis, verbose_name='Метрополия', on_delete=models.CASCADE, related_name='dioceses')
    title = models.CharField(
        verbose_name='Название')
    admin = models.OneToOneField(
        'users.User', verbose_name='Администрация', on_delete=models.SET_NULL, related_name="admin_in", null=True, blank=True)
    chief = models.OneToOneField(
        'users.User', verbose_name='Ответственный за ЕМО', on_delete=models.SET_NULL, related_name="chief_in", null=True, blank=True)
    
    class Meta:
        verbose_name = 'Епархия'
        verbose_name_plural = 'Епархии'
        
    def __str__(self):
        return self.title
    
    def _set_role(self, user, role):
        user.is_active = True
        user.diocese = self
        user.save()
        if role in ['chief', 'admin']:
            setattr(self, role, user)
            self.save()
    
    def set_role(self, user, role):
        roles = [
            'missionary',
            'chief',
            'admin',
        ]
        if role not in roles:
            return [False, 'Такая роль отсутствует']
        if role in ['chief', 'admin'] and getattr(self, role):
            return [False, 'Епархия уже имеет пользователя с этой ролью']
        if not user.is_active:
            self._set_role(user, role)
            return [True, 'Пользователь восстановлен и роль установлена']
        else:
            if user.status in ['chief', 'admin', 'root']:
                return [False, 'Пользователь уже имеет управляющую роль']
            elif user.status == 'missionary' and role == 'missionary':
                return [False, 'Пользователь уже является миссионером']
            else:
                self._set_role(user, role)
                return [True, 'Пользователю установлена новая роль']
                
            
