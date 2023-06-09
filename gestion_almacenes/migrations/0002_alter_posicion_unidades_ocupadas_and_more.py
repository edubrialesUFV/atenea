# Generated by Django 4.1.7 on 2023-04-19 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_almacenes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posicion',
            name='unidades_ocupadas',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='producto',
            name='cantidad_stock',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='producto',
            name='peso_por_unidad',
            field=models.FloatField(default=200),
        ),
    ]
