# Generated by Django 4.2.11 on 2024-05-09 02:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=15)),
                ('descripcion', models.CharField(max_length=100)),
                ('estado', models.CharField(choices=[('nuevo', 'Nuevo'), ('usado', 'Usado')], default='nuevo', max_length=5)),
                ('foto', models.ImageField(blank=True, null=True, upload_to='media/')),
                ('categoria', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Productos.categoria')),
            ],
        ),
    ]
