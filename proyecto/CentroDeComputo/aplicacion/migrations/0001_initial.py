# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coordinador',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=15)),
                ('permisos', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FechaUso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fechaInicio', models.CharField(max_length=15)),
                ('fechaFinal', models.CharField(max_length=15)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HoraUso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hora', models.CharField(max_length=30)),
                ('dia', models.IntegerField()),
                ('fechaUso', models.ForeignKey(to='aplicacion.FechaUso')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Laboratorio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombreLaboratorio', models.CharField(max_length=15)),
                ('codigo', models.CharField(max_length=15)),
                ('capacidad', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Materia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombreMateria', models.CharField(max_length=15)),
                ('codigo', models.CharField(max_length=15)),
                ('laboratorio', models.ForeignKey(to='aplicacion.Laboratorio')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo', models.CharField(max_length=17)),
                ('estado', models.CharField(max_length=17)),
                ('Descripcion', models.CharField(max_length=150)),
                ('fechaDeCreacion', models.CharField(max_length=30)),
                ('numeroLaboratorios', models.IntegerField()),
                ('observacionAdministrador', models.CharField(max_length=150)),
                ('coordinador', models.ForeignKey(to='aplicacion.Coordinador')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='laboratorio',
            name='solicitud',
            field=models.ForeignKey(to='aplicacion.Solicitud'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fechauso',
            name='laboratorio',
            field=models.ForeignKey(to='aplicacion.Laboratorio'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fechauso',
            name='solicitud',
            field=models.ForeignKey(to='aplicacion.Solicitud'),
            preserve_default=True,
        ),
    ]
