# Generated by Django 5.0.4 on 2024-06-03 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Trueques', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trueque',
            name='estado_trueque',
            field=models.CharField(choices=[('Pendiente', 'Pendiente'), ('Aceptado', 'Aceptado'), ('Rechazado', 'Rechazado')], default='Pendiente', max_length=20),
        ),
    ]
