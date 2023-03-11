# Generated by Django 4.1.7 on 2023-03-11 19:44

from django.db import migrations, models
import genie_backend.utils.models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SocialAccount",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="created at model"
                    ),
                ),
                (
                    "created_by",
                    models.IntegerField(
                        blank=True,
                        help_text="user creates model",
                        null=True,
                        verbose_name="user creates model",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="updated at model"
                    ),
                ),
                (
                    "updated_by",
                    models.IntegerField(
                        blank=True,
                        help_text="user updates model",
                        null=True,
                        verbose_name="user updates model",
                    ),
                ),
                (
                    "is_deleted",
                    models.BooleanField(
                        default=False,
                        help_text="just flag, not delete data actually",
                        verbose_name="Whether model is deleted",
                    ),
                ),
                (
                    "nickname",
                    models.CharField(
                        help_text="nickname used in genie service",
                        max_length=50,
                        verbose_name="nickname",
                    ),
                ),
                (
                    "pub_key",
                    models.CharField(
                        help_text="public key",
                        max_length=100,
                        unique=True,
                        verbose_name="public key",
                    ),
                ),
                (
                    "secret_key",
                    models.CharField(
                        help_text="secret key",
                        max_length=100,
                        verbose_name="secret key",
                    ),
                ),
            ],
            options={
                "verbose_name": "Genie user",
                "verbose_name_plural": "Genie users",
            },
            bases=(models.Model, genie_backend.utils.models.PrintableMixin),
        ),
    ]