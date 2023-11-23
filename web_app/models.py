from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify

DASHBOARD_TYPE_CHOICES = (
    ("PowerBI", "PowerBI"),
    ("Tableau", "Tableau"),
    ("Otro", "Otro"),
    
    )

class DigitalSolution(models.Model):
    """
    Digital solution model.
    """

    name = models.CharField(max_length=100, verbose_name="Nombre")
    description = models.TextField(verbose_name="Descripción")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")
    image = models.ImageField(
        verbose_name="Imagen",
        upload_to="digital_solutions",
        default="digital_solutions/default.png",
    )

    def dasboards_count(self):
        return self.dashboard_set.count()

    def save(self, *args, **kwargs):
        super(DigitalSolution, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Solución digital"
        verbose_name_plural = "Soluciones digitales"

    def __str__(self):
        return self.name


class Client(models.Model):
    """
    Client model.

    """

    name = models.CharField(max_length=100, verbose_name="Nombre", unique=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return self.name


class ClientUser(AbstractUser):
    """
    Client user model.

    """

    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, verbose_name="Cliente", null=True, blank=True
    )

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def saveffffffffff(self, *args, **kwargs):  
        user = ClientUser.objects.get(pk=self.pk)
        if user.password != self.password:
            self.set_password(self.password)
        super(ClientUser, self).save(*args, **kwargs)

    def get_digital_solutions(self):
        return DigitalSolution.objects.filter(dashboard__users=self).distinct()


    def __str__(self):
        return self.email


class DashboardTag(models.Model):
    """
    Dashboard tag model.

    """

    name = models.CharField(max_length=100, verbose_name="Nombre", unique=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")
    slug = models.SlugField(
        max_length=100,
        verbose_name="Slug",
        unique=True,
        blank=True,
        null=True,
        editable=False,
    )

    def get_slug(self):
        return slugify(self.name)

    class Meta:
        verbose_name = "Etiqueta"
        verbose_name_plural = "Etiquetas"

    def __str__(self):
        return self.name


class Dashboard(models.Model):
    """
    Dashboard model.

    """

    name = models.CharField(max_length=100, verbose_name="Nombre")
    description = models.TextField(verbose_name="Descripción")
    url = models.URLField(verbose_name="URL")
    tags = models.ManyToManyField(DashboardTag, verbose_name="Etiquetas")
    digital_solution = models.ForeignKey(
        DigitalSolution, on_delete=models.CASCADE, verbose_name="Solución digital"
    )
    clients = models.ManyToManyField(Client, verbose_name="Clientes")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")
    type = models.CharField(
        max_length=100,
        verbose_name="Tipo",
        choices=DASHBOARD_TYPE_CHOICES,
        default="PowerBI",
    )


    def get_description(self):
        if len(self.description) > 100:
            return self.description[:98] + "..."
        else:
            return self.description
        
    class Meta:
        verbose_name = "Tablero"
        verbose_name_plural = "Tableros"

    def __str__(self):
        return self.name


class HelpSection(models.Model):
    """
    Help section model.

    """

    name = models.CharField(max_length=100, verbose_name="Nombre")

    class Meta:
        verbose_name = "Ayuda - Sección"
        verbose_name_plural = "Ayuda - Secciones"

    def __str__(self):
        return self.name


class HelpContent(models.Model):
    """
    Help content model.

    """

    tittle = models.CharField(max_length=100, verbose_name="Nombre")
    description = models.TextField(verbose_name="Descripción")
    section = models.ForeignKey(
        HelpSection, on_delete=models.CASCADE, verbose_name="Sección"
    )

    class Meta:
        verbose_name = "Ayuda - Contenido"
        verbose_name_plural = "Ayuda - Contenidos"

    def __str__(self):
        return self.tittle


class DasboardLog(models.Model):
    """
    Dashboard log model.

    """

    dashboard = models.ForeignKey(
        Dashboard, on_delete=models.CASCADE, verbose_name="Tablero"
    )
    user = models.ForeignKey(
        ClientUser, on_delete=models.CASCADE, verbose_name="Usuario"
    )
    date = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de acceso")
    device = models.CharField(
        max_length=100, verbose_name="Dispositivo", null=True, blank=True
    )
    browser = models.CharField(max_length=100, verbose_name="Navegador", null=True, blank=True)
    ip = models.CharField(max_length=100, verbose_name="IP", null=True, blank=True)

    class Meta:
        verbose_name = "Log"
        verbose_name_plural = "Logs"

    def __str__(self):
        return self.dashboard.name + " - " + self.user.email
