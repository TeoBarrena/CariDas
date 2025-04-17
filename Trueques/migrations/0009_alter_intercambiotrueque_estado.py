# Generated by Django 5.0.4 on 2024-06-11 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Trueques', '0008_remove_intercambiotrueque_trueque_2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='intercambiotrueque',
            name='estado',
            field=models.CharField(choices=[('Pendiente', 'Pendiente'), ('Aceptado', 'Aceptado'), ('Completado', 'Completado'), ('Rechazado', 'Rechazado'), ('Espera de confirmacion', 'Espera de confirmacion'), ('Eliminado', 'Eliminado')], default='Espera de confirmacion', max_length=30),
        ),
    ]
