from django.apps import AppConfig


class LocalHierarchyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    verbose_name = 'Иерархия епархий'
    name = 'apps.local_hierarchy'
