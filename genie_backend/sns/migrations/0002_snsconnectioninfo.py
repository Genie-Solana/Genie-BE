# Generated by Django 4.1.7 on 2023-03-12 03:08

from django.db import migrations, models
import django.db.models.deletion
import genie_backend.utils.models
import imagekit.models.fields


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
        ("sns", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="SNSConnectionInfo",
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
                    "handle",
                    models.CharField(
                        help_text="SNS handle", max_length=50, verbose_name="SNS handle"
                    ),
                ),
                (
                    "profile_img",
                    imagekit.models.fields.ProcessedImageField(
                        blank=True,
                        help_text="user Profile img",
                        null=True,
                        upload_to="user_profile_imgs",
                        verbose_name="user profile img",
                    ),
                ),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sns_info",
                        to="accounts.socialaccount",
                    ),
                ),
                (
                    "sns",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="users_info",
                        to="sns.sns",
                    ),
                ),
            ],
            options={
                "verbose_name": "SNS-SocialAccount info",
                "verbose_name_plural": "SNS-SocialAccount info",
            },
            bases=(models.Model, genie_backend.utils.models.PrintableMixin),
        ),
    ]