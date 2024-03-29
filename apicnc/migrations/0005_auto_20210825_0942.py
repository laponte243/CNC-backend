# Generated by Django 3.1.7 on 2021-08-25 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apicnc', '0004_auto_20210823_1231'),
    ]

    operations = [
        migrations.AddField(
            model_name='examen',
            name='observaciones',
            field=models.TextField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='examen',
            name='resultado',
            field=models.TextField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='examen',
            name='unidad',
            field=models.TextField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='examen',
            name='valor_referencia',
            field=models.TextField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='examen_detalle',
            name='descripcion',
            field=models.TextField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='examen_detalle',
            name='resultado',
            field=models.TextField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='examen_detalle',
            name='unidad',
            field=models.TextField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='examen_detalle',
            name='valor_referencia',
            field=models.TextField(max_length=50, null=True),
        ),
    ]
