# Generated by Django 4.0.6 on 2022-09-04 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mensajeria', '0005_alter_mensaje_privado_mensaje'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mensaje_privado',
            name='destinatario',
            field=models.CharField(default='', max_length=150),
        ),
    ]
