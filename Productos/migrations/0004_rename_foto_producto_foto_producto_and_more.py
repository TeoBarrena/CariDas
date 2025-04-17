# Generated by Django 4.2.11 on 2024-05-09 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Productos', '0003_rename_titulo_categoria_nombre'),
    ]

    operations = [
        migrations.RenameField(
            model_name='producto',
            old_name='foto',
            new_name='foto_producto',
        ),
        migrations.AlterField(
            model_name='producto',
            name='estado',
            field=models.CharField(choices=[('nuevo', 'Nuevo'), ('usado', 'Usado')], default='Usado', max_length=5),
        ),
    ]
