from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    """
    Manager customizado para o modelo User.
    """
    def create_user(self, username, email, password=None, **extra_fields):
        """
        Cria e salva um User com o username, email e senha fornecidos.
        """
        if not email:
            raise ValueError(_('O Email deve ser definido'))
        if not username:
            raise ValueError(_('O Username deve ser definido'))
            
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Cria e salva um Superuser com o username, email e senha fornecidos.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    """
    Modelo de Usuário customizado para o Voz do Povo.
    """
    class TipoUsuario(models.TextChoices):
        CIDADAO = 'CIDADAO', _('Cidadão')
        GESTOR_PUBLICO = 'GESTOR_PUBLICO', _('Gestor Público')

    # O campo username é herdado de AbstractUser
    # O campo email é herdado, mas vamos torná-lo obrigatório
    email = models.EmailField(_('endereço de e-mail'), blank=False)
    
    # Adiciona o campo para diferenciar os tipos de usuário
    tipo_usuario = models.CharField(
        max_length=20,
        choices=TipoUsuario.choices,
        default=TipoUsuario.CIDADAO,
        verbose_name=_('tipo de usuário')
    )

    # Campos para verificação de e-mail e reset de senha
    is_email_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=5, blank=True, null=True)
    code_expires_at = models.DateTimeField(null=True, blank=True)

    # Torna o primeiro nome um campo obrigatório
    first_name = models.CharField(_('first name'), max_length=150, blank=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name']

    objects = UserManager()

    def __str__(self):
        return self.username