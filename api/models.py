from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, BaseUserManager
from . import utils
from . import upload_dirs as upload_to


class CustomUserManager(BaseUserManager):
    """
    Define a model manager for User model with no username field
    """

    def _create_user(self, email, password=None, **extra_fields):
        """
        Create and save a User with the given email and password
        """

        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given email and password
        """

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Custom user model representing an individual user.
    """

    username = None

    gender_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others')
    ]


    id = models.CharField(primary_key=True, default=utils.generate_random_ids, editable=False)

    gender = models.CharField(choices=gender_choices, default='M')
    dob = models.DateField(blank=False, null=False)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


class User_Name(models.Model):
    id = models.CharField(primary_key=True, default=utils.generate_random_ids, editable=False)
    user_id = models.ForeignKey("CustomUser", on_delete=models.CASCADE, related_name='user_name')

    first_name = models.CharField(max_length=30, blank=False, null=False)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=False, null=False)


class User_Address(models.Model):
    id = models.CharField(primary_key=True, default=utils.generate_random_ids, editable=False)
    user_id = models.ForeignKey("CustomUser", on_delete=models.CASCADE, related_name='user_address')

    address_line1 = models.CharField(max_length=50, blank=False, null=False)
    address_line2 = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=False, null=False)
    state = models.CharField(max_length=50, blank=False, null=False)
    country = models.CharField(max_length=50, blank=False, null=False)


class User_Contact(models.Model):
    status_choices = [
        ('INA', 'inactive'),
        ('A', 'active')
    ]

    id = models.CharField(primary_key=True, default=utils.generate_random_ids, editable=False)
    user_id = models.ForeignKey("CustomUser", on_delete=models.CASCADE, related_name='user_contact')

    phone_number = models.CharField(max_length=20, blank=False, null=False)
    status = models.CharField(choices=status_choices, default='A')


class User_Profile_Images(models.Model):
    file_choices = [
        ('CPP', 'Current Profile Pic'),
        ('PPP', 'Previous Profile Pic')
    ]

    id = models.CharField(primary_key=True, default=utils.generate_random_ids, editable=False)
    user_id = models.ForeignKey("CustomUser", on_delete=models.CASCADE, related_name='user_profiles')

    image = models.FileField(upload_to=upload_to.user_profile_path)
    status = models.CharField(choices=file_choices, default='CPP')


class User_Documents(models.Model):
    file_choices = [
        ('CD', 'Current Document'),
        ('PD', 'Previous Document')
    ]

    id = models.CharField(primary_key=True, default=utils.generate_random_ids, editable=False)
    user_id = models.ForeignKey("CustomUser", on_delete=models.CASCADE, related_name='user_documents')

    title = models.CharField(max_length=50, blank=False, null=False)
    file = models.FileField(upload_to=upload_to.user_documents_path)
    status = models.CharField(choices=file_choices, default='CD')


class User_Applications(models.Model):
    application_status = [
        ('PD', 'Pending'),
        ('SH', 'ShortListed'),
        ('RJ', 'Rejected'),
        ('ACPT', 'Accepted')
    ]

    id = models.CharField(primary_key=True, default=utils.generate_random_ids, editable=False)
    user_id = models.ForeignKey("CustomUser", on_delete=models.CASCADE, related_name='users')
    job_id = models.ForeignKey("Jobs", on_delete=models.CASCADE, related_name='user_applications')

    status = models.CharField(choices=application_status, default='PD')
    cover_letter = models.FileField(upload_to=upload_to.application_uploads)
    resume = models.FileField(upload_to=upload_to.application_uploads)
    applied_at = models.DateTimeField(auto_now_add=True)


class Recruiter(models.Model):
    id = models.CharField(primary_key=True, default=utils.generate_random_ids, editable=False)
    user_id = models.OneToOneField("CustomUser", on_delete=models.CASCADE)

    company_name = models.CharField(max_length=50, blank=False, null=False)
    designation = models.CharField(max_length=50, blank=False, null=False)


class Jobs(models.Model):
    job_status = [
        ('OP', 'Open'),
        ('CL', 'Closed')
    ]

    id = models.CharField(primary_key=True, default=utils.generate_random_ids, editable=False)
    recruiter_id = models.ForeignKey("Recruiter", on_delete=models.CASCADE, related_name='Recruiter')

    title = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    requirements = models.TextField(blank=False, null=False)
    salary = models.CharField(max_length=30, blank=False, null=False)
    location = models.CharField(max_length=50, blank=False, null=False)
    deadline = models.DateField(blank=False, null=False)
    status = models.CharField(choices=job_status, default='OP')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
