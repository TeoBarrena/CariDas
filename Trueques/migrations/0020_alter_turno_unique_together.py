# Generated by Django 4.2.11 on 2024-07-03 03:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Trueques', '0019_alter_intercambiotrueque_estado_alter_turno_filial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='turno',
            unique_together=set(),
        ),
    ]
