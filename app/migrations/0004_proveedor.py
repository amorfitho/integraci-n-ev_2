# Generated by Django 5.2 on 2025-05-10 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_local_stock'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id_proveedor', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_proveedor', models.CharField(max_length=80)),
                ('descripcion', models.TextField(blank=True)),
                ('telefono_proveedor', models.CharField(max_length=80)),
                ('direccion_proveedor', models.CharField(max_length=120)),
            ],
        ),
    ]
