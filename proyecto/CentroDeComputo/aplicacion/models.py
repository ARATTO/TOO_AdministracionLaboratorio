from django.db import models
from django.contrib import admin

class Coordinador(models.Model):
	nombre = models.CharField(max_length=15)
	permisos =  models.IntegerField()


class Solicitud(models.Model):
	tipo =  models.CharField(max_length=17)
	estado = models.CharField(max_length=17)
	Descripcion = models.CharField(max_length=150)
	fechaDeCreacion = models.CharField(max_length=30)
	numeroLaboratorios = models.IntegerField()
	observacionAdministrador = models.CharField(max_length=150)	
	coordinador = models.ForeignKey(Coordinador)

	
class Laboratorio(models.Model):
	nombreLaboratorio =  models.CharField(max_length=15)
	codigo =  models.CharField(max_length=15)
	capacidad =  models.IntegerField()	
	solicitud = models.ForeignKey(Solicitud)


class FechaUso(models.Model):
	fechaInicio =  models.CharField(max_length=15)
	fechaFinal =  models.CharField(max_length=15)
	solicitud = models.ForeignKey(Solicitud)
	laboratorio = models.ForeignKey(Laboratorio)

class Materia(models.Model):
	nombreMateria =  models.CharField(max_length=15)
	codigo =  models.CharField(max_length=15)
	laboratorio = models.ForeignKey(Laboratorio)

class HoraUso(models.Model):
	hora = 	models.CharField(max_length=30)
	dia = models.IntegerField()
	fechaUso = models.ForeignKey(FechaUso)
