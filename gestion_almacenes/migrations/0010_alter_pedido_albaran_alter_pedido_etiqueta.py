# Generated by Django 4.1.7 on 2023-04-26 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_almacenes', '0009_pedido_albaran_pedido_etiqueta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='albaran',
            field=models.FileField(blank=True, null=True, upload_to='media/albaranes/'),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='etiqueta',
            field=models.ImageField(blank=True, null=True, upload_to='media/etiquetas/'),
        ),
    ]
