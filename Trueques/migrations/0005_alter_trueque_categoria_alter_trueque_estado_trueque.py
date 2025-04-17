# Generated by Django 5.0.6 on 2024-06-04 23:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Productos', '0009_categoria_puntos'),
        ('Trueques', '0004_merge_20240604_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trueque',
            name='categoria',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Productos.categoria'),
        ),
        migrations.AlterField(
            model_name='trueque',
            name='estado_trueque',
            field=models.CharField(choices=[('Pendiente', 'Pendiente'), ('Aceptado', 'Aceptado'), ('Rechazado', 'Rechazado'), ('Eliminado', 'Eliminado')], default='Pendiente', max_length=20),
        ),
    ]
