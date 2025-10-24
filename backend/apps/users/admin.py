from django.contrib import admin
from django import forms
from . import models
    

class UserForm(forms.ModelForm):
    new_password = forms.CharField(required=False, label='Новый пароль')

    class Meta:
        model = models.User
        fields = '__all__'

    
@admin.register(models.Invite)
class InviteAdmin(admin.ModelAdmin):
    pass


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'is_staff', 'is_superuser',)
    form = UserForm
    
    def get_fieldsets(self, request, obj=None):
        default_fields = (
            ['is_active'],
            'is_staff', 'is_superuser',
            'email',
            'name',
            'surname',
            'patronymic',
            'date_of_birth',
            'city',
            'phone',
            'image',
            'diocese',
            'new_password',)
        if request.user.is_authenticated and request.user.task_permission:
            default_fields[0].append('task_permission')
        return (
            (None, {
                'fields': default_fields,
            }),
        )
    def save_model(self, request, obj, form, change):
        password = request.POST.get('new_password')
        if password:
            obj.set_password(password)
            obj.save()
        super().save_model(request, obj, form, change)