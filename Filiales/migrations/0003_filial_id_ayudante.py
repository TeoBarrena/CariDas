# Generated by Django 5.0.6 on 2024-05-21 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Filiales', '0002_alter_filial_direccion'),
    ]

    operations = [
        migrations.AddField(
            model_name='filial',
            name='id_ayudante',
            field=models.IntegerField(default=1, unique=True),
            preserve_default=False,
        ),
    ]
