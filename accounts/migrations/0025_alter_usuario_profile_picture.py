# Generated by Django 4.2.11 on 2024-06-10 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0024_alter_usuario_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
    ]
