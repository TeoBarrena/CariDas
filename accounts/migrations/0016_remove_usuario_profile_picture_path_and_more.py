# Generated by Django 4.2.11 on 2024-05-30 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_usuario_profile_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='profile_picture_path',
        ),
        migrations.AlterField(
            model_name='usuario',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='accounts/static/media'),
        ),
    ]
