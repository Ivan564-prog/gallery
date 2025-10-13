from django.db import models


class ActivedQueryset(models.QuerySet):

    def active(self):
        return self.filter(is_active=True)
    

class ActivedManager(models.Manager):

    def get_queryset(self):
        return ActivedQueryset(self.model)
    
    def active(self):
        return self.get_queryset().active()