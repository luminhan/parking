from uuid import uuid4

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from apps.shared.models import DatedModel


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("account_status", AccountStatus.UNCONFIRMED)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("account_status", AccountStatus.CONFIRMED)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class AccountStatus(models.TextChoices):
    UNCONFIRMED = "UNCONFIRMED", _("Unconfirmed")
    CONFIRMED = "CONFIRMED", _("Confirmed")


class User(AbstractUser):
    """User model."""

    id = models.UUIDField(primary_key=True, default=uuid4)

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=False,
        default="",
        blank=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and " "@/./+/-/_ only."
        ),
        validators=[AbstractUser.username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_("email address"), unique=True)
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    account_status = models.CharField(
        choices=AccountStatus.choices, default=AccountStatus.UNCONFIRMED, max_length=64
    )

    created = models.DateTimeField(db_index=True, auto_now_add=True)
    last_updated = models.DateTimeField(db_index=True, auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def is_confirmed(self):
        return self.account_status == AccountStatus.CONFIRMED

    class Meta:
        permissions = [("list_users", "Can view a list of users")]

    def __str__(self) -> str:
        return self.email


@receiver(pre_save, sender=User)
def set_username(sender, instance: User, **kwargs):
    """
    Set the username of the username to the email address.
    """
    instance.username = instance.email
