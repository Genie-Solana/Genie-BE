from django.db import models
from django.db.models import Q
from django.contrib import admin


class BaseModelManager(models.Manager):
    use_for_related_fields = True

    def __init__(self, *args, **kwargs):
        self.with_deleted = kwargs.pop("deleted", False)
        super().__init__(*args, **kwargs)

    def _base_queryset(self):
        return super().get_queryset().filter(Q(is_deleted=True) | Q(is_deleted=False))

    def get_queryset(self):
        qs = self._base_queryset()
        if self.with_deleted:
            return qs

        return qs.filter(is_deleted=False)


class PrintableMixin:
    def __repr__(self):
        return str(self.to_dict())

    def to_dict(self):
        opts = self._meta
        data = {}
        for f in chain(opts.concrete_fields, opts.private_fields):
            data[f.name] = f.value_from_object(self)
            if isinstance(
                f,
                (
                    models.DateTimeField,
                    models.DateField,
                    models.ImageField,
                    models.FileField,
                ),
            ):
                if f.value_from_object(self) is not None:
                    data[f.name] = str(f.value_from_object(self))
        for f in opts.many_to_many:
            data[f.name] = [i.id for i in f.value_from_object(self)]
        return data


class BaseModel(models.Model, PrintableMixin):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        verbose_name="created at model", auto_now_add=True, null=True
    )

    created_by = models.IntegerField(
        verbose_name="user creates model", help_text="user creates model", null=True, blank=True
    )

    updated_at = models.DateTimeField(verbose_name="updated at model", auto_now=True)

    updated_by = models.IntegerField(
        verbose_name="user updates model", help_text="user updates model", null=True, blank=True
    )

    is_deleted = models.BooleanField(
        verbose_name="Whether model is deleted",
        default=False,
        help_text="just flag, not delete data actually",
    )

    objects = BaseModelManager()
    objects_with_deleted = BaseModelManager(deleted=True)
    objects_for_admin = models.Manager()

    def save(self, *args, **kwargs):  # pylint:disable=signature-differs
        user_id = kwargs.pop("user_id", None)
        if user_id:
            if self.id:
                self.updated_by = user_id
            else:
                self.created_by = user_id

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):  # pylint:disable=signature-differs
        self.is_deleted = True
        self.save(*args, **kwargs)

    def restore(self, *args, **kwargs):
        self.is_deleted = False
        self.save(*args, **kwargs)

    def hard_delete(self):
        super().delete()


class BaseModelAdmin(admin.ModelAdmin):
    list_filter = ("is_deleted",)
    readonly_fields = (
        "created_at",
        "created_by",
        "updated_at",
        "updated_by",
        "is_deleted",
    )

    def get_queryset(self, request):
        return self.model.objects_for_admin.all()

    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user.id
        else:
            obj.created_by = request.user.id
            obj.updated_by = request.user.id

        super().save_model(request, obj, form, change)
