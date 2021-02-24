from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import Group

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password = None):
        if not email:
            raise ValueError('Пользователь должен иметь почту')
        if not username:
            raise ValueError('Пользователь должен ввести логин')
        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )
        user.set_password(password)
        user.save(using= self._db)
        return user
    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password = password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=30, unique= True)
    date_joined = models.DateTimeField(verbose_name= 'date joined', auto_now_add= True)
    last_login = models.DateTimeField(verbose_name= 'last login', auto_now_add= True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyAccountManager()

    date_of_birth = models.DateField(null= True, blank= True)
    first_name = models.CharField(max_length=30, verbose_name= 'Имя', blank=True)
    last_name = models.CharField(max_length=30, verbose_name='Фамилия', blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj= None):
        return  self.is_admin

    def has_module_perms(self, app_label):
        return True

    def get_absolute_url(self):  # добавим абсолютный путь чтобы после создания нас перебрасывало на страницу с новостью
        return f'/mypage/'

#MyUser.objects.get(username='Alex').email
