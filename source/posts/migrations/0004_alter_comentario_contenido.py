# Generated by Django 4.0.6 on 2022-09-03 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_remove_comentario_f_modificacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='contenido',
            field=models.CharField(max_length=150),
        ),
    ]
