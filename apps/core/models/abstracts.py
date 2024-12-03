from django.db import models

from config.middlewares import get_current_user


class AuditableModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(
        max_length=255, null=True, editable=False, auto_created=True
    )
    updated_by = models.CharField(
        max_length=255, null=True, editable=False
    )

    class Meta:
        abstract = True

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None
    ):
        current_user = get_current_user()
        if current_user is None or current_user.username is None:
            username = 'unknown user'
        else:
            username = current_user.username

        if self.id is None or force_insert:
            self.created_by = username
        self.updated_by = username
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields
        )

    def __str__(self):
        return f'{self.__class__.__name__}: {self.id}'
