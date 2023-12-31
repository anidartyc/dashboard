# Generated by Django 4.2 on 2023-11-06 21:50

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Nombre')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
            },
        ),
        migrations.CreateModel(
            name='DashboardTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Nombre')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('slug', models.SlugField(blank=True, editable=False, max_length=100, null=True, unique=True, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'Etiqueta',
                'verbose_name_plural': 'Etiquetas',
            },
        ),
        migrations.CreateModel(
            name='DigitalSolution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('description', models.TextField(verbose_name='Descripción')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('image', models.ImageField(default='digital_solutions/default.png', upload_to='digital_solutions', verbose_name='Imagen')),
            ],
            options={
                'verbose_name': 'Solución digital',
                'verbose_name_plural': 'Soluciones digitales',
            },
        ),
        migrations.CreateModel(
            name='HelpSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'Ayuda - Sección',
                'verbose_name_plural': 'Ayuda - Secciones',
            },
        ),
        migrations.CreateModel(
            name='HelpContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tittle', models.CharField(max_length=100, verbose_name='Nombre')),
                ('description', models.TextField(verbose_name='Descripción')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web_app.helpsection', verbose_name='Sección')),
            ],
            options={
                'verbose_name': 'Ayuda - Contenido',
                'verbose_name_plural': 'Ayuda - Contenidos',
            },
        ),
        migrations.CreateModel(
            name='Dashboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('description', models.TextField(verbose_name='Descripción')),
                ('url', models.URLField(verbose_name='URL')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('type', models.CharField(choices=[('PowerBI', 'PowerBI'), ('Tableau', 'Tableau'), ('Otro', 'Otro')], default='PowerBI', max_length=100, verbose_name='Tipo')),
                ('digital_solution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web_app.digitalsolution', verbose_name='Solución digital')),
                ('tags', models.ManyToManyField(to='web_app.dashboardtag', verbose_name='Etiquetas')),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Usuarios')),
            ],
            options={
                'verbose_name': 'Tablero',
                'verbose_name_plural': 'Tableros',
            },
        ),
        migrations.CreateModel(
            name='DasboardLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de acceso')),
                ('device', models.CharField(blank=True, max_length=100, null=True, verbose_name='Dispositivo')),
                ('browser', models.CharField(blank=True, max_length=100, null=True, verbose_name='Navegador')),
                ('ip', models.CharField(blank=True, max_length=100, null=True, verbose_name='IP')),
                ('dashboard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web_app.dashboard', verbose_name='Tablero')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Log',
                'verbose_name_plural': 'Logs',
            },
        ),
        migrations.AddField(
            model_name='clientuser',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web_app.client', verbose_name='Cliente'),
        ),
        migrations.AddField(
            model_name='clientuser',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='clientuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
