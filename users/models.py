from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, AbstractUser, User, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

class CustomUserManager(UserManager):
    def create_user(self, type, codigo, first_name, last_name, sex, email, password=None):
        if not email:
            raise ValueError("Campo e-mail é obrigatório!")
        if not codigo:
            raise ValueError("Campo código é obrigatório!")
        if not type:
            raise ValueError("Campo tipo de usuário é obrigatório!")
        if not first_name:
            raise ValueError("Campo nome de usuário é obrigatório!")
        if not last_name:
            raise ValueError("Campo sobrenome de usuário é obrigatório!")
        if not sex:
            raise ValueError("Campo sexo é obrigatório!")

        user = self.model(
            type=type,
            sex=sex,
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            codigo=codigo,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, type, first_name, last_name, sex, email, codigo, password=None):
        user = self.create_user(
            type=type,
            sex=sex,
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            codigo=codigo,
        )
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def update_Check_pass(self, has_pass):
        User.objects.get(id=has_pass).update(has_pass=True)


class CustomUser(AbstractUser, PermissionsMixin):

    username = None

    class Types(models.TextChoices):
        developer = "developer", "Developer"
        assessor = "assessor", "Assessor"
        admin = "admin", "Admin"

    class Sex(models.TextChoices):
        masculino = "M", "Masculino"
        feminino = "F", "Feminino"

    type = models.CharField('Tipo de Usuário', max_length=50, choices=Types.choices, default=Types.admin)
    codigo = models.CharField("Codigo", max_length=20, unique=True, blank=True, null=True)
    last_name = models.CharField("Sobrenome", max_length=100, blank=True, null=True)
    first_name = models.CharField("Nome", max_length=100, blank=True, null=True)
    sex = models.CharField("Sexo", max_length=10, choices=Sex.choices, default=Sex.feminino)
    telefone = models.CharField("Telefone", max_length=25, blank=True, null=True)
    email = models.EmailField("E-mail", max_length=150, unique=True, blank=True, null=True)
    nascimento = models.DateField("Nascimento", blank=True, null=True)
    last_login = models.DateTimeField('Último Login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    has_pass = models.BooleanField(default=False)


    USERNAME_FIELD = 'codigo'
    REQUIRED_FIELDS = ['type','first_name','last_name', 'email', 'sex']

    objects = CustomUserManager()

    def __str__(self):
        return str(self.id)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Developer(CustomUser):
    class Meta:
        proxy = True

class Assessores(CustomUser):
    class Meta:
        proxy = True

class Admin(CustomUser):
    class Meta:
        proxy = True

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(default='profile/default_profile.jpg', upload_to='profile')
    google_sheets = models.CharField("Telefone", max_length=255, blank=True, null=True)



    def __str__(self):
        return '{} - {} {}'.format(self.user.codigo, self.user.first_name, self.user.last_name)



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_save_user_profile(sender, created, instance, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()



