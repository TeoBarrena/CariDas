# Generated by Django 4.2.11 on 2024-06-25 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0028_usuario_cant_resenias_usuario_estrellas_totales'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='cant_resenias',
            field=models.IntegerField(default=1),
        ),
    ]
