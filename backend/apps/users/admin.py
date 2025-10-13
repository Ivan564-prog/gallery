from django.contrib import admin
from django import forms
from . import models
    

class UserForm(forms.ModelForm):
    new_password = forms.CharField(required=False, label='Новый пароль')

    class Meta:
        model = models.User
        fields = '__all__'


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'is_staff', 'is_superuser',)
    form = UserForm

    fieldsets = (
        (None, {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'email',
                'new_password',
            ),
        }),
    )
    
    def save_model(self, request, obj, form, change):
        password = request.POST.get('new_password')
        if password:
            obj.set_password(password)
            obj.save()
        super().save_model(request, obj, form, change)