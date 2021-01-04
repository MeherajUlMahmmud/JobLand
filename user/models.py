from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Must have an email address')

        if not name:
            raise ValueError('Must have a name')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    # def create_staffuser(self, email, name, password):
    #     """
    #     Creates and saves a staff user with the given email and password.
    #     """
    #     user = self.create_user(
    #         email=self.normalize_email(email),
    #         name=name,
    #         password=password,
    #     )
    #     user.staff = True
    #     user.save(using=self._db)
    #     return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            name=name,
            password=password,
        )
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_applicant = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']  # Email & Password are required by default.

    objects = MyUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class ApplicantProfileModel(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    bio = RichTextField(null=True, blank=True)
    address = models.TextField(max_length=255, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES, null=True, blank=True)
    interest = RichTextField(null=True, blank=True)
    linkedin = models.CharField(max_length=255, null=True, blank=True)
    github = models.CharField(max_length=255, null=True, blank=True)
    twitter = models.CharField(max_length=255, null=True, blank=True)
    facebook = models.CharField(max_length=255, null=True, blank=True)
    resume = models.FileField(null=True, blank=True)
    totalViewCount = models.IntegerField(null=True, blank=True, default=0)


class CompanyProfileModel(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    about = RichTextField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    logo = models.ImageField(null=True, blank=True)
    totalViewCount = models.IntegerField(null=True, blank=True)


class WorkExperienceModel(models.Model):
    JOB_TYPE_CHOICES = [
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
        ('Intern', 'Intern'),
    ]

    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255, null=True, blank=True)
    job_type = models.CharField(max_length=30, choices=JOB_TYPE_CHOICES, null=True, blank=True)
    job_desc = RichTextField(null=True, blank=True)
    company = models.CharField(max_length=255, default="nazia")
    location = models.CharField(max_length=255, null=True, blank=True)
    started = models.DateField(null=True, blank=True)
    left = models.DateField(null=True, blank=True)


class EducationModel(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    school = models.CharField(max_length=255, null=True, blank=True)
    degree = models.CharField(max_length=255, null=True, blank=True)
    department = models.CharField(max_length=255, null=True, blank=True)
    started = models.DateField(null=True, blank=True)
    end = models.DateField(null=True, blank=True)
    cgpa = models.FloatField(max_length=255, null=True, blank=True)


class SkillSetModel(models.Model):
    SKILL_PROFICIENCY = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
        ('Pro', 'Pro'),
    ]

    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    skill_title = models.CharField(max_length=255, null=True, blank=True)
    proficiency = models.CharField(max_length=255, choices=SKILL_PROFICIENCY, null=True, blank=True)


class ReferenceModel(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    note = models.CharField(max_length=255, null=True, blank=True)
    designation = models.CharField(max_length=255, null=True, blank=True)
    workplace = models.CharField(max_length=255, null=True, blank=True)


class LanguageModel(models.Model):
    SKILL_PROFICIENCY = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
        ('Native', 'Native'),
    ]

    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    language = models.CharField(max_length=255, null=True, blank=True)
    proficiency = models.CharField(max_length=30, choices=SKILL_PROFICIENCY, null=True, blank=True)


class AwardModel(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    detail = models.CharField(max_length=255, null=True, blank=True)


class PreferredJobModel(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    details = models.CharField(max_length=255, null=True, blank=True)


class RatingModel(models.Model):
    company = models.ForeignKey(CompanyProfileModel, null=True, blank=True, on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    comments = models.CharField(max_length=255, default="")
    extra = models.CharField(max_length=255, default=0)
    rate = models.IntegerField(default=0,
                               validators=[
                                   MaxValueValidator(5),
                                   MinValueValidator(0),
                               ], )


class ProfileViewDetails(models.Model):
    viewedBy = models.ForeignKey(User, related_name='viewedBy', on_delete=models.CASCADE)
    viewed = models.ForeignKey(User, related_name='viewed', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class EmployeeSearchKeywordModel(models.Model):
    searched_by = models.ForeignKey(User, on_delete=models.CASCADE)
    searched_for = models.CharField(max_length=200, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class JobSearchKeywordModel(models.Model):
    searched_by = models.ForeignKey(User, on_delete=models.CASCADE)
    searched_for = models.CharField(max_length=200, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
