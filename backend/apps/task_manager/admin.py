import time
from . import models
from django.contrib import admin
from django.urls import path, reverse
from django.http import HttpResponseRedirect
from django_apscheduler.models import DjangoJob, DjangoJobExecution


admin.site.unregister(DjangoJob)
@admin.register(models.DjangoJobProxy)
class DjangoJobAdmin(admin.ModelAdmin):

    def has_module_permission(self, request):
        return request.user.is_authenticated and request.user.task_permission
    
    def has_add_permission(self, request):
        return False


admin.site.unregister(DjangoJobExecution)
@admin.register(models.DjangoJobExecutionProxy)
class DjangoJobExecutionAdmin(admin.ModelAdmin):

    def has_module_permission(self, request):
        return request.user.is_authenticated and request.user.task_permission
    
    def has_add_permission(self, request):
        return False


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    change_form_template = 'admin/task_change.html'
    
    readonly_fields = (
        'func_name',
        'func_args',
        'func_kwargs',
        'result',
        'status',
        'pid',
        'error',
        'created_at',
        'closed_at',
    )
    fields = readonly_fields

    def has_module_permission(self, request):
        return request.user.is_authenticated and request.user.task_permission
    
    def has_add_permission(self, request):
        return False
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'restart_task/<int:object_id>/',
                self.admin_site.admin_view(self.restart_task),
                name='restart_task',
            ),
        ]
        return custom_urls + urls
    
    def restart_task(self, request, object_id):
        obj = self.get_object(request, object_id)
        obj.start_as_task()
        self.message_user(request, "Задача перезапущена. Это новая задача")
        # Асинхронно задача не успевает создаваться, при таком костыле она создается и редиректится на новую задачу
        time.sleep(1)
        return HttpResponseRedirect(reverse('admin:task_manager_task_change', args=[models.Task.objects.all().order_by('-pk')[0].pk]))

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, object_id)
        obj.watched = True
        obj.save()
        extra_context = extra_context or {}
        extra_context['custom_action_url'] = reverse('admin:restart_task', args=[object_id])
        extra_context['show_save'] = False
        return super().change_view(request, object_id, form_url, extra_context=extra_context)
    
    def get_model_perms(self, request):
        perms = super().get_model_perms(request)
        if perms['view']:
            self.model._meta.verbose_name_plural = f"Задачи {self.model.unwatched_errors() if self.model.unwatched_errors() else ''}"
        return perms