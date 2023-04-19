# Generated by Django 4.1.7 on 2023-04-19 11:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('nombre_cliente', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('direccion_cliente', models.CharField(max_length=150)),
                ('codigo_postal', models.CharField(max_length=10)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_hora_pedido', models.DateTimeField()),
                ('tipo_envio', models.CharField(choices=[('EST', 'Estándar'), ('URG', 'Urgente')], max_length=3)),
                ('agencia_transporte', models.CharField(choices=[('COR', 'Correos'), ('SEU', 'Seur'), ('DHL', 'DHL')], max_length=3)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Posicion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_posicion', models.CharField(choices=[('PIC', 'Picking'), ('STO', 'Stock')], max_length=3)),
                ('capacidad', models.PositiveIntegerField()),
                ('unidades_ocupadas', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referencia', models.CharField(max_length=20)),
                ('cantidad_stock', models.PositiveIntegerField(blank=True, null=True)),
                ('cantidad_minima_reaprovisionamiento', models.PositiveIntegerField()),
                ('peso_por_unidad', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_proveedor', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ProductoPosicion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_almacenada', models.PositiveIntegerField()),
                ('posicion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_almacenes.posicion')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_almacenes.producto')),
            ],
        ),
        migrations.AddField(
            model_name='producto',
            name='proveedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_almacenes.proveedor'),
        ),
        migrations.CreateModel(
            name='PedidoProducto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_almacenes.pedido')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_almacenes.producto')),
            ],
        ),
    ]
