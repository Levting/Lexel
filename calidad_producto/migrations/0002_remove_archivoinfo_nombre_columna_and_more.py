# Generated by Django 5.0.7 on 2024-07-23 14:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calidad_producto', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='archivoinfo',
            name='nombre_columna',
        ),
        migrations.RemoveField(
            model_name='archivoinfo',
            name='valor',
        ),
        migrations.AddField(
            model_name='archivoinfo',
            name='data',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='archivoinfo',
            name='archivo',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='info', to='calidad_producto.archivo'),
        ),
    ]
