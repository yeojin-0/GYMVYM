from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils import timezone
from django.conf import settings

class CustomUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid e-mail address")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_user(self, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('usertype', 2) # 일반유저 usertype : member로 기본설정
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('usertype', 0) # 관리자 usertype : owner로 기본설정
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(username, email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = [
    ('0', 'Man'),
    ('1', 'Woman'),
    ]

    USERTYPE_CHOICES = [
    (0, 'Owner'),
    (1, 'Trainer'),
    (2, 'Member'),
    ]

    user = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # UUID 사용 : 중복 방지, 난수 기반으로 보안 상승, 식별자 생성시 충돌방지
    nfc_uid = models.UUIDField(unique=True, null=True, blank=True, editable=False)
    username = models.CharField(max_length=100, unique=True, blank=False)
    password = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255)
    detail_address = models.CharField(max_length=255, null=False)
    nickname = models.CharField(max_length=100, null=False, default='', unique=True)
    user_image = models.ImageField(upload_to='static/', null=True, default='static/default.png')
    birth = models.DateField(null=False)
    usertype = models.IntegerField(default=2)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_userimage(self):
        return settings.WEBSITE_URL + self.user_image.url