# Generated by Django 5.0.6 on 2024-06-03 06:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Productos', '0008_alter_producto_foto_producto'),
        ('Trueques', '0002_categoria_alter_trueque_categoria'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trueque',
            name='categoria',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Productos.categoria'),
        ),
        migrations.DeleteModel(
            name='Categoria',
        ),
    ]
