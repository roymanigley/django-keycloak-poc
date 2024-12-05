from django.db import models

from apps.core.models.abstracts import AuditableModel


class _QuerySet(models.QuerySet):

    def search(self, search) -> '_QuerySet[Dummy]':
        if search is not None:
            return self.filter(name__icontains=search)
        return self


class _Manager(models.Manager):

    def get_queryset(self) -> _QuerySet['Dummy']:
        return _QuerySet(model=self.model, using=self._db)

    def search(self, search) -> _QuerySet['Dummy']:
        return self.get_queryset().search(search)


class Dummy(AuditableModel):
    name = models.TextField(null=False)
    
    objects = _Manager()

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']

        # additional permissions
        # permissions = [
        #     ("can_import_dummy", "Can import Dummy"),
        #     ("can_export_dummy", "Can export Dummy"),
        #]
