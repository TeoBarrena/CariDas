# Generated by Django 5.0.4 on 2024-06-10 21:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Productos', '0009_categoria_puntos'),
        ('Trueques', '0007_alter_intercambiotrueque_estado_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='intercambiotrueque',
            name='trueque_2',
        ),
        migrations.AddField(
            model_name='intercambiotrueque',
            name='producto_2',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, related_name='producto_2', to='Productos.producto'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='intercambiotrueque',
            name='estado',
            field=models.CharField(choices=[('Pendiente', 'Pendiente'), ('Aceptado', 'Aceptado'), ('Completado', 'Completado'), ('Rechazado', 'Rechazado'), ('Espera de confirmacion', 'Espera de confirmacion'), ('Eliminado', 'Eliminado')], default='Pendiente', max_length=30),
        ),
    ]
