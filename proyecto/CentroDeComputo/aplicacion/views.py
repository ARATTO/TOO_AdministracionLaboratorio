from django.shortcuts import render
from django.shortcuts import render,redirect
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from aplicacion.models import Coordinador, Solicitud, FechaUso, Laboratorio, Materia, HoraUso

from django.views.generic import TemplateView
from django.views.generic import CreateView
from django.core.urlresolvers import reverse_lazy
from django.core.urlresolvers import reverse
#from .forms import FlujoForms, ComponenteForms
from django.core import serializers
#librerias para reporlab
from io import BytesIO
from django.views.generic import ListView
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
#login
from django.contrib.auth.models import User, Permission
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.mail import EmailMessage
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.contenttypes.models import ContentType
from datetime import datetime
import time

gestion = 0


def inicio(request):
	if request.method =="GET":
		
		return render(request, 'aplicacion/inicio.html')

def nuevousuario(request):
	if request.method=='POST':
		formulario =  UserCreationForm(request.POST)
		if formulario.is_valid():
			formulario.save()
			return render(request, 'aplicacion/inicio.html')
		else:
			formulario = UserCreationForm()
			return render_to_response('aplicacion/newuser.html',{'formulario':formulario}, context_instance=RequestContext(request))
	else:
		formulario = UserCreationForm()
		return render_to_response('aplicacion/newuser.html',{'formulario':formulario}, context_instance=RequestContext(request))

def iniciarsesion(request):
	encontrado = 0
	message = None
	if not request.user.is_anonymous():
		return render(request, 'aplicacion/inicio.html')
	if request.method == 'POST':
		formulario = AuthenticationForm(request.POST)
		if formulario.is_valid:
			username = request.POST['username']			
			clave = request.POST['password']			
			acceso = authenticate(username = username,password =clave)
			#next = request.POST["next"]
			#print(next)

			coor = Coordinador.objects.all()
			for i in coor:
				if i.nombre == username:
					encontrado = 1
				

			if encontrado == 0:
				C = Coordinador()
				C.nombre = username
				C.permisos = 2
				C.save()

			if acceso is not None:
				if acceso.is_active:
					login(request,acceso)
					
					#return HttpResponseRedirect(next)
					return redirect('/')
				else:
					message = "Tu usuario es inactivo"
			else:
					message = "Nombre de usuario y/o password es incorrecto"
	else:
		formulario = AuthenticationForm()
		#next = request.REQUEST.get('next','')
		#next = 'http://127.0.0.1:8000/'
	#return render_to_response('aplicacion/login.html',{'message':message, 'formulario':formulario, 'next':next},context_instance=RequestContext(request))
	return render_to_response('aplicacion/login.html',{'message':message, 'formulario':formulario},context_instance=RequestContext(request))

@login_required(login_url = '/login/')
def cerrarsesion(request):
	logout(request)
	return redirect('http://127.0.0.1:8000/')
	#return render(request, 'aplicacion/inicio.html')



@login_required(login_url = '/login/')
def solicitud(request):
	if request.method =="GET":
		return render(request, 'aplicacion/crearSolicitud.html')  
	elif request.method=="POST":
		us = request.user.username

		NL=0.0
		fechas = []
		horas = []
		nombreLab = []
		codigoLab = []
		capacidadLab = []
		
		#crea los datos de los lcomp
		nombreLab.append("Laboratorio 1")
		codigoLab.append("lcomp1")
		capacidadLab.append(30)

		
		nombreLab.append("Laboratorio 2")
		codigoLab.append("lcomp2")
		capacidadLab.append(35)

		
		nombreLab.append("Laboratorio 3")
		codigoLab.append("lcomp3")
		capacidadLab.append(28)


		nombreLab.append("Laboratorio 4")
		codigoLab.append("lcomp4")
		capacidadLab.append(20)
				
		#obtine cuales son los lcomp seleccionados
		laboratorios = []
		laboratorios.append(request.POST.get("lab1",0))
		laboratorios.append(request.POST.get("lab2",0))
		laboratorios.append(request.POST.get("lab3",0))
		laboratorios.append(request.POST.get("lab4",0))

		#hora = time.strftime("%c")
		hora = datetime.now()

		#obtiene el usuario en linea

		coor = Coordinador.objects.all()
		for i in coor:
				if i.nombre == us:
					coordi = i

		s = Solicitud()
		s.coordinador = coordi
		s.tipo = request.POST["razonSolicitud"]
		s.estado = "pendiente"
		s.Descripcion = request.POST["descripcionRazon"]
		s.fechaDeCreacion = hora.strftime("%d/%m/%Y/  %H:%M:%S")

		#obtiene el numero de lcomp solicitados
		for j in range(4):
			if (laboratorios[j]):
				NL+=1

		s.numeroLaboratorios = NL
		s.save()

		
		#crea los datos necesarios para la solicitud
		for j in range(4):
			if (laboratorios[j]):
				l = Laboratorio()
				l.solicitud = s
				l.nombreLaboratorio = nombreLab[j]
				l.codigo = codigoLab[j]
				l.capacidad = capacidadLab[j]	
				l.save()
	
				f= FechaUso()
				f.solicitud = s
				f.laboratorio = l
				f.fechaInicio = request.POST["fechaInicio"]
				f.fechaFinal = request.POST["fechaFinal"]
				f.save()

				fechas.append(f)
	
				m= Materia()
				m.laboratorio = l
				m.nombreMateria = request.POST["codMateria"]
				m.codigo = request.POST["codMateria"]
	
				m.save()

		fechaI = ''
		fechaF = ''
		for i in fechas:
			fechaI = i.fechaInicio
			fechaF = i.fechaFinal
			print 'pruebas:',i.id


		return HttpResponseRedirect('/validarSolicitud')
		


@login_required(login_url = '/login/')
def matriz(request):
	if request.method =="GET":

		control = 0
		labUsados = []
		labNoUsados = []
		lc1 = 0
		lc2 = 0
		lc3 = 0
		lc4 = 0

		FE = FechaUso.objects.all()
		for x in FE:
			FECH = x

		F = FechaUso.objects.filter(fechaInicio__range=(FECH.fechaInicio,FECH.fechaFinal))
		H = HoraUso.objects.all()


		usado = []


		for x in H:
			for y in F:
				if(x.fechaUso.id == y.id):
					if(x.fechaUso.solicitud.estado == "aprobado"):
						control +=1
						usado.append(x)
						

		fecha =[]

		soli = Solicitud.objects.all()
		for x in soli:
			solici = x

		numeroLab = solici.numeroLaboratorios

		print 'solicitud',solici.id

		Y = FechaUso.objects.all().order_by('-id')

		for z in Y:
			if(numeroLab>0):
				fecha.append(z)
				numeroLab -=1

		contador = 0
		for P in fecha:
			if(fecha[contador] != None):
				labUsados.append(fecha[contador].laboratorio.codigo)
				contador +=1

		for No in labUsados:
			if(No == "lcomp1"):
				lc1 +=1
			elif(No == "lcomp2"):
				lc2 +=1
			elif(No == "lcomp3"):
				lc3 +=1
			elif(No == "lcomp4"):
				lc4 +=1

		if(lc1==0):
			labNoUsados.append("lcomp1")

		if(lc2==0):
			labNoUsados.append("lcomp2")

		if(lc3==0):
			labNoUsados.append("lcomp3")

		if(lc4==0):
			labNoUsados.append("lcomp4")


		for x in usado:
			print '\nhora',x.id

		for x in labNoUsados:
			print '\nno usado',x
			

		print '\nnumero horarios',control
		
		return render(request,'aplicacion/validarSolicitud.html',{'usado':usado, 'labNoUsados':labNoUsados}) 
	elif request.method=="POST":
	
		fecha =[]

		soli = Solicitud.objects.all()
		for x in soli:
			solici = x

		numeroLab = solici.numeroLaboratorios

		Y = FechaUso.objects.all().order_by('-id')

		for z in Y:
			if(numeroLab>0):
				fecha.append(z)
				numeroLab -=1

		contador = 0
		for P in fecha:
			if(fecha[contador] != None):
				print 'pruebas2:',fecha[contador].laboratorio.codigo
				contador +=1


		lunesL1 = []
		lunesL2 = []
		lunesL3 = []
		lunesL4 = []

		martesL1 = []
		martesL2 = []
		martesL3 = []
		martesL4 = []

		miercolesL1 = []
		miercolesL2 = []
		miercolesL3 = []
		miercolesL4 = []

		juevesL1 = []
		juevesL2 = []
		juevesL3 = []
		juevesL4 = []

		viernesL1 = []
		viernesL2 = []
		viernesL3 = []
		viernesL4 = []

		sabadoL1 = []
		sabadoL2 = []
		sabadoL3 = []
		sabadoL4 = []

		horarios = []
		horarios.append("6:20 AM - 8:00 AM")
		horarios.append("8:05 AM - 9:45 AM")
		horarios.append("9:50 AM - 11:30 AM")
		horarios.append("11:35 AM - 1:15 PM")
		horarios.append("1:20 PM - 3:00 PM")
		horarios.append("3:05 PM - 4:45 PM")
		horarios.append("4:50 PM - 6:30 PM")
		horarios.append("6:35 PM - 8:15 PM")

		#lunes lab 1 
		lunesL1.append(request.POST.get("1,0,0",0))
		lunesL1.append(request.POST.get("1,1,0",0))
		lunesL1.append(request.POST.get("1,2,0",0))
		lunesL1.append(request.POST.get("1,3,0",0))
		lunesL1.append(request.POST.get("1,4,0",0))
		lunesL1.append(request.POST.get("1,5,0",0))
		lunesL1.append(request.POST.get("1,6,0",0))
		lunesL1.append(request.POST.get("1,7,0",0))
		
		#lunes lab 2
		lunesL2.append(request.POST.get("2,0,0",0))
		lunesL2.append(request.POST.get("2,1,0",0))
		lunesL2.append(request.POST.get("2,2,0",0))
		lunesL2.append(request.POST.get("2,3,0",0))
		lunesL2.append(request.POST.get("2,4,0",0))
		lunesL2.append(request.POST.get("2,5,0",0))
		lunesL2.append(request.POST.get("2,6,0",0))
		lunesL2.append(request.POST.get("2,7,0",0))

		#lunes lab 3
		lunesL3.append(request.POST.get("3,0,0",0))
		lunesL3.append(request.POST.get("3,1,0",0))
		lunesL3.append(request.POST.get("3,2,0",0))
		lunesL3.append(request.POST.get("3,3,0",0))
		lunesL3.append(request.POST.get("3,4,0",0))
		lunesL3.append(request.POST.get("3,5,0",0))
		lunesL3.append(request.POST.get("3,6,0",0))
		lunesL3.append(request.POST.get("3,7,0",0))

		#lunes lab 4
		lunesL4.append(request.POST.get("4,0,0",0))
		lunesL4.append(request.POST.get("4,1,0",0))
		lunesL4.append(request.POST.get("4,2,0",0))
		lunesL4.append(request.POST.get("4,3,0",0))
		lunesL4.append(request.POST.get("4,4,0",0))
		lunesL4.append(request.POST.get("4,5,0",0))
		lunesL4.append(request.POST.get("4,6,0",0))
		lunesL4.append(request.POST.get("4,7,0",0))

		#martes lab 1 
		martesL1.append(request.POST.get("1,0,1",0))
		martesL1.append(request.POST.get("1,1,1",0))
		martesL1.append(request.POST.get("1,2,1",0))
		martesL1.append(request.POST.get("1,3,1",0))
		martesL1.append(request.POST.get("1,4,1",0))
		martesL1.append(request.POST.get("1,5,1",0))
		martesL1.append(request.POST.get("1,6,1",0))
		martesL1.append(request.POST.get("1,7,1",0))
		
		#martes lab 2
		martesL2.append(request.POST.get("2,0,1",0))
		martesL2.append(request.POST.get("2,1,1",0))
		martesL2.append(request.POST.get("2,2,1",0))
		martesL2.append(request.POST.get("2,3,1",0))
		martesL2.append(request.POST.get("2,4,1",0))
		martesL2.append(request.POST.get("2,5,1",0))
		martesL2.append(request.POST.get("2,6,1",0))
		martesL2.append(request.POST.get("2,7,1",0))

		#martes lab 3
		martesL3.append(request.POST.get("3,0,1",0))
		martesL3.append(request.POST.get("3,1,1",0))
		martesL3.append(request.POST.get("3,2,1",0))
		martesL3.append(request.POST.get("3,3,1",0))
		martesL3.append(request.POST.get("3,4,1",0))
		martesL3.append(request.POST.get("3,5,1",0))
		martesL3.append(request.POST.get("3,6,1",0))
		martesL3.append(request.POST.get("3,7,1",0))

		#martes lab 4
		martesL4.append(request.POST.get("4,0,1",0))
		martesL4.append(request.POST.get("4,1,1",0))
		martesL4.append(request.POST.get("4,2,1",0))
		martesL4.append(request.POST.get("4,3,1",0))
		martesL4.append(request.POST.get("4,4,1",0))
		martesL4.append(request.POST.get("4,5,1",0))
		martesL4.append(request.POST.get("4,6,1",0))
		martesL4.append(request.POST.get("4,7,1",0))

		#miercoles lab 1 
		miercolesL1.append(request.POST.get("1,0,2",0))
		miercolesL1.append(request.POST.get("1,1,2",0))
		miercolesL1.append(request.POST.get("1,2,2",0))
		miercolesL1.append(request.POST.get("1,3,2",0))
		miercolesL1.append(request.POST.get("1,4,2",0))
		miercolesL1.append(request.POST.get("1,5,2",0))
		miercolesL1.append(request.POST.get("1,6,2",0))
		miercolesL1.append(request.POST.get("1,7,2",0))
		
		#miercoles lab 2
		miercolesL2.append(request.POST.get("2,0,2",0))
		miercolesL2.append(request.POST.get("2,1,2",0))
		miercolesL2.append(request.POST.get("2,2,2",0))
		miercolesL2.append(request.POST.get("2,3,2",0))
		miercolesL2.append(request.POST.get("2,4,2",0))
		miercolesL2.append(request.POST.get("2,5,2",0))
		miercolesL2.append(request.POST.get("2,6,2",0))
		miercolesL2.append(request.POST.get("2,7,2",0))

		#miercoles lab 3
		miercolesL3.append(request.POST.get("3,0,2",0))
		miercolesL3.append(request.POST.get("3,1,2",0))
		miercolesL3.append(request.POST.get("3,2,2",0))
		miercolesL3.append(request.POST.get("3,3,2",0))
		miercolesL3.append(request.POST.get("3,4,2",0))
		miercolesL3.append(request.POST.get("3,5,2",0))
		miercolesL3.append(request.POST.get("3,6,2",0))
		miercolesL3.append(request.POST.get("3,7,2",0))

		#miercoles lab 4
		miercolesL4.append(request.POST.get("4,0,2",0))
		miercolesL4.append(request.POST.get("4,1,2",0))
		miercolesL4.append(request.POST.get("4,2,2",0))
		miercolesL4.append(request.POST.get("4,3,2",0))
		miercolesL4.append(request.POST.get("4,4,2",0))
		miercolesL4.append(request.POST.get("4,5,2",0))
		miercolesL4.append(request.POST.get("4,6,2",0))
		miercolesL4.append(request.POST.get("4,7,2",0))

		#jueves lab 1 
		juevesL1.append(request.POST.get("1,0,3",0))
		juevesL1.append(request.POST.get("1,1,3",0))
		juevesL1.append(request.POST.get("1,2,3",0))
		juevesL1.append(request.POST.get("1,3,3",0))
		juevesL1.append(request.POST.get("1,4,3",0))
		juevesL1.append(request.POST.get("1,5,3",0))
		juevesL1.append(request.POST.get("1,6,3",0))
		juevesL1.append(request.POST.get("1,7,3",0))
		
		#jueves lab 2
		juevesL2.append(request.POST.get("2,0,3",0))
		juevesL2.append(request.POST.get("2,1,3",0))
		juevesL2.append(request.POST.get("2,2,3",0))
		juevesL2.append(request.POST.get("2,3,3",0))
		juevesL2.append(request.POST.get("2,4,3",0))
		juevesL2.append(request.POST.get("2,5,3",0))
		juevesL2.append(request.POST.get("2,6,3",0))
		juevesL2.append(request.POST.get("2,7,3",0))

		#jueves lab 3
		juevesL3.append(request.POST.get("3,0,3",0))
		juevesL3.append(request.POST.get("3,1,3",0))
		juevesL3.append(request.POST.get("3,2,3",0))
		juevesL3.append(request.POST.get("3,3,3",0))
		juevesL3.append(request.POST.get("3,4,3",0))
		juevesL3.append(request.POST.get("3,5,3",0))
		juevesL3.append(request.POST.get("3,6,3",0))
		juevesL3.append(request.POST.get("3,7,3",0))

		#jueveslab 4
		juevesL4.append(request.POST.get("4,0,3",0))
		juevesL4.append(request.POST.get("4,1,3",0))
		juevesL4.append(request.POST.get("4,2,3",0))
		juevesL4.append(request.POST.get("4,3,3",0))
		juevesL4.append(request.POST.get("4,4,3",0))
		juevesL4.append(request.POST.get("4,5,3",0))
		juevesL4.append(request.POST.get("4,6,3",0))
		juevesL4.append(request.POST.get("4,7,3",0))

		#viernes lab 1 
		viernesL1.append(request.POST.get("1,0,4",0))
		viernesL1.append(request.POST.get("1,1,4",0))
		viernesL1.append(request.POST.get("1,2,4",0))
		viernesL1.append(request.POST.get("1,3,4",0))
		viernesL1.append(request.POST.get("1,4,4",0))
		viernesL1.append(request.POST.get("1,5,4",0))
		viernesL1.append(request.POST.get("1,6,4",0))
		viernesL1.append(request.POST.get("1,7,4",0))
		
		#viernes lab 2
		viernesL2.append(request.POST.get("2,0,4",0))
		viernesL2.append(request.POST.get("2,1,4",0))
		viernesL2.append(request.POST.get("2,2,4",0))
		viernesL2.append(request.POST.get("2,3,4",0))
		viernesL2.append(request.POST.get("2,4,4",0))
		viernesL2.append(request.POST.get("2,5,4",0))
		viernesL2.append(request.POST.get("2,6,4",0))
		viernesL2.append(request.POST.get("2,7,4",0))

		#viernes lab 3
		viernesL3.append(request.POST.get("3,0,4",0))
		viernesL3.append(request.POST.get("3,1,4",0))
		viernesL3.append(request.POST.get("3,2,4",0))
		viernesL3.append(request.POST.get("3,3,4",0))
		viernesL3.append(request.POST.get("3,4,4",0))
		viernesL3.append(request.POST.get("3,5,4",0))
		viernesL3.append(request.POST.get("3,6,4",0))
		viernesL3.append(request.POST.get("3,7,4",0))

		#viernes lab 4
		viernesL4.append(request.POST.get("4,0,4",0))
		viernesL4.append(request.POST.get("4,1,4",0))
		viernesL4.append(request.POST.get("4,2,4",0))
		viernesL4.append(request.POST.get("4,3,4",0))
		viernesL4.append(request.POST.get("4,4,4",0))
		viernesL4.append(request.POST.get("4,5,4",0))
		viernesL4.append(request.POST.get("4,6,4",0))
		viernesL4.append(request.POST.get("4,7,4",0))

		#sabado lab 1 
		sabadoL1.append(request.POST.get("1,0,5",0))
		sabadoL1.append(request.POST.get("1,1,5",0))
		sabadoL1.append(request.POST.get("1,2,5",0))
		sabadoL1.append(request.POST.get("1,3,5",0))
		sabadoL1.append(request.POST.get("1,4,5",0))
		sabadoL1.append(request.POST.get("1,5,5",0))
		sabadoL1.append(request.POST.get("1,6,5",0))
		sabadoL1.append(request.POST.get("1,7,5",0))
		
		#sabado lab 2
		sabadoL2.append(request.POST.get("2,0,5",0))
		sabadoL2.append(request.POST.get("2,1,5",0))
		sabadoL2.append(request.POST.get("2,2,5",0))
		sabadoL2.append(request.POST.get("2,3,5",0))
		sabadoL2.append(request.POST.get("2,4,5",0))
		sabadoL2.append(request.POST.get("2,5,5",0))
		sabadoL2.append(request.POST.get("2,6,5",0))
		sabadoL2.append(request.POST.get("2,7,5",0))

		#sabado lab 3
		sabadoL3.append(request.POST.get("3,0,5",0))
		sabadoL3.append(request.POST.get("3,1,5",0))
		sabadoL3.append(request.POST.get("3,2,5",0))
		sabadoL3.append(request.POST.get("3,3,5",0))
		sabadoL3.append(request.POST.get("3,4,5",0))
		sabadoL3.append(request.POST.get("3,5,5",0))
		sabadoL3.append(request.POST.get("3,6,5",0))
		sabadoL3.append(request.POST.get("3,7,5",0))

		#sabado lab 4
		sabadoL4.append(request.POST.get("4,0,5",0))
		sabadoL4.append(request.POST.get("4,1,5",0))
		sabadoL4.append(request.POST.get("4,2,5",0))
		sabadoL4.append(request.POST.get("4,3,5",0))
		sabadoL4.append(request.POST.get("4,4,5",0))
		sabadoL4.append(request.POST.get("4,5,5",0))
		sabadoL4.append(request.POST.get("4,6,5",0))
		sabadoL4.append(request.POST.get("4,7,5",0))


		for R in fecha:
			if(R != None):
				if(R.laboratorio.codigo == "lcomp1"):		#LCOMP 1
					for j in range(8):
						if (lunesL1[j]):
							h = HoraUso()
							h.hora = horarios[j]
							h.fechaUso = R
							h.dia = 0
							h.save()

					for j in range(8):
						if (martesL1[j]):
							h = HoraUso()
							h.hora = horarios[j]
							h.fechaUso = R
							h.dia = 1
							h.save()

					for j in range(8):
						if (miercolesL1[j]):
							h = HoraUso()
							h.hora = horarios[j]
							h.fechaUso = R
							h.dia = 2
							h.save()

					for j in range(8):
						if (juevesL1[j]):
							h = HoraUso()
							h.hora = horarios[j]
							h.fechaUso = R
							h.dia = 3
							h.save()

					for j in range(8):
						if (viernesL1[j]):
							h = HoraUso()
							h.hora = horarios[j]
							h.fechaUso = R
							h.dia = 4
							h.save()


					for j in range(8):
						if (sabadoL1[j]):
							h = HoraUso()
							h.hora = horarios[j]
							h.fechaUso = R
							h.dia = 5
							h.save()


				elif(R.laboratorio.codigo == "lcomp2"):
					for j in range(8):
						if (lunesL2[j]):
							h = HoraUso()
							h.hora = horarios[j]
							h.fechaUso = R
							h.dia = 0
							h.save()


					for j in range(8):
						if (martesL2[j]):
							h = HoraUso()
							h.hora = horarios[j]
							h.fechaUso = R
							h.dia = 1
							h.save()

					for j in range(8):
						if (miercolesL2[j]):
							h = HoraUso()
							h.hora = horarios[j]
							h.fechaUso = R
							h.dia = 2
							h.save()

					for j in range(8):
						if (juevesL2[j]):
							h = HoraUso()
							h.hora = horarios[j]
							h.fechaUso = R
							h.dia = 3
							h.save()


					for j in range(8):
						if (viernesL2[j]):
							h = HoraUso()
							h.hora = horarios[j]
							h.fechaUso = R
							h.dia = 4
							h.save()

					for j in range(8):
						if (sabadoL2[j]):
							h = HoraUso()
							h.hora = horarios[j]
							h.fechaUso = R
							h.dia = 5
							h.save()


				elif(R.laboratorio.codigo == "lcomp3"):


					for j in range(8):
						if (lunesL3[j]):
							h = HoraUso()
							h.hora = horarios[j]
							h.fechaUso = R
							h.dia = 0
							h.save()

					for j in range(8):
						if (martesL3[j]):
							h = HoraUso()
							h.hora = horarios[j]
							h.fechaUso = R
							h.dia = 1
							h.save()		

					for j in range(8):
						if (miercolesL3[j]):
							h = HoraUso()
							h.hora = horarios[j]
							h.fechaUso = R
							h.dia = 2
							h.save()

					for j in range(8):
						if (juevesL3[j]):
							h = HoraUso()
							h.hora = horarios[j]
							h.fechaUso = R
							h.dia = 3
							h.save()

					for j in range(8):
						if (viernesL3[j]):
							h = HoraUso()
							h.hora = horarios[j]
							h.fechaUso = R
							h.dia = 4
							h.save()

					for j in range(8):
						if (sabadoL3[j]):
							h = HoraUso()
							h.hora = horarios[j]
							h.fechaUso = R
							h.dia = 5
							h.save()

				elif(R.laboratorio.codigo == "lcomp4"):

					for j in range(8):
						if (lunesL4[j]):
							h = HoraUso()
							h.hora = horarios[j]
							h.fechaUso = R
							h.dia = 0
							h.save()
	
					for j in range(8):
						if (martesL4[j]):
							h = HoraUso()
							h.hora = horarios[j]
							h.fechaUso = R
							h.dia = 1
							h.save()

					for j in range(8):
						if (miercolesL4[j]):
							h = HoraUso()
							h.hora = horarios[j]
							h.fechaUso = R
							h.dia = 2
							h.save()	

					for j in range(8):
						if (juevesL4[j]):
							h = HoraUso()
							h.hora = horarios[j]
							h.fechaUso = R
							h.dia = 3
							h.save()


					for j in range(8):
						if (viernesL4[j]):
							h = HoraUso()
							h.hora = horarios[j]
							h.fechaUso = R
							h.dia = 4
							h.save()

					for j in range(8):
						if (sabadoL4[j]):
							h = HoraUso()
							h.hora = horarios[j]
							h.fechaUso = R
							h.dia = 5
							h.save()

		
		
		return HttpResponseRedirect('/')



@login_required(login_url = '/login/')
def generar_pdf(request):
    	print "Generar el PDF"
    	response = HttpResponse(content_type='application/pdf')
    	pdf_name = "solicitudes.pdf" 
    	buff = BytesIO()
    	doc = SimpleDocTemplate(buff,
        	                    pagesize=letter,
            	                rightMargin=40,
                	            leftMargin=40,
                    	        topMargin=60,
                        	    bottomMargin=18,
                            	)
    	solicitud = []
    	styles = getSampleStyleSheet()
    	header = Paragraph("Listado de solicitudes", styles['Heading1'])
    	solicitud.append(header)
  
    	headings = ( 'hora', 'Dia', 'fechaInicio', 'fechaFinal', 'laboratorio')
    	
    	allsolicitudes = []
    	datos = HoraUso.objects.all().order_by('dia')
    	for p in datos:
    		if(p.fechaUso.solicitud.estado == "aprobado"):
    			if(p.dia == 0):
    				allsolicitudes += [(p.hora, 'lunes', p.fechaUso.fechaInicio	, p.fechaUso.fechaFinal, p.fechaUso.laboratorio.codigo)]
    			elif(p.dia == 1):
	    			allsolicitudes += [(p.hora, 'martes' , p.fechaUso.fechaInicio	, p.fechaUso.fechaFinal,p.fechaUso.laboratorio.codigo)]
    			elif(p.dia == 2):
    				allsolicitudes += [(p.hora, 'miercoles' , p.fechaUso.fechaInicio	, p.fechaUso.fechaFinal, p.fechaUso.laboratorio.codigo)]
	    		elif(p.dia == 3):
    				allsolicitudes += [(p.hora, 'jueves' , p.fechaUso.fechaInicio	, p.fechaUso.fechaFinal, p.fechaUso.laboratorio.codigo)]
    			elif(p.dia == 4):
    				allsolicitudes += [(p.hora, 'viernes' , p.fechaUso.fechaInicio	, p.fechaUso.fechaFinal, p.fechaUso.laboratorio.codigo)]
    			elif(p.dia == 5):
	    			allsolicitudes += [(p.hora, 'sabado' , p.fechaUso.fechaInicio	, p.fechaUso.fechaFinal, p.fechaUso.laboratorio.codigo)]

    	
    	print allsolicitudes

    	t = Table([headings] + allsolicitudes)
    	t.setStyle(TableStyle(
	        [
            	('GRID', (0, 0), (3, -1), 1, colors.dodgerblue),
            	('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            	('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        	]
    	))
    	solicitud.append(t)
    	doc.build(solicitud)
    	response.write(buff.getvalue())
    	buff.close()
    	return response
  
@login_required(login_url = '/login/')
#@permission_required('aplicacion.administrador',login_url = '/login/')
def gestionarSolicitud(request):
	if request.method =="GET":
		solicitud = []

		sol = Solicitud.objects.all().order_by('fechaDeCreacion')

		for x in sol:
			if(x.estado == "pendiente"):
				solicitud.append(x)

		return render(request,'aplicacion/gestionarSolicitud.html',{'solicitud':solicitud})
	elif request.method=="POST":

		global gestion 	

		gestion = request.POST.get("actual",0)

		if (gestion == 0):
			solicitud = []

			sol = Solicitud.objects.all().order_by('fechaDeCreacion')

			for x in sol:
				if(x.estado == "pendiente"):
					solicitud.append(x)

			return render(request,'aplicacion/gestionarSolicitud.html',{'solicitud':solicitud})
		else:
			return HttpResponseRedirect('/choqueSolicitud')



@login_required(login_url = '/login/')
def choqueSolicitud(request):
	if request.method =="GET":


		SolActual = Solicitud.objects.filter(id=gestion)
		

		FE = FechaUso.objects.filter(solicitud=SolActual)
		

		F = FechaUso.objects.filter(fechaInicio__range=(FE[0].fechaInicio,FE[0].fechaFinal))
		S = Solicitud.objects.all().order_by('fechaDeCreacion')


		solicitudT = []
		solicitud = []

		for x in S:
			for y in F:
				if(x.id == y.solicitud.id):
					if(x.estado == "aprobado" or x.estado == "pendiente"):
						solicitudT.append(x)

		control = 0
		for x in solicitudT:
			if(control>0):
				if(x.id == solicitudT[control-1].id):
					print ''
				else:
					solicitud.append(x)
				
		 	control+=1

		return render(request,'aplicacion/choqueSolicitud.html',{'SolActual':SolActual, 'solicitud':solicitud}) 

	elif request.method=="POST":
		global gestion

		r = request.POST.get("form1",0)

		if(r == "1"):

			actulizar = request.POST.get("sentencia",0)
			descripcion = request.POST.get("descripcionRazon",'-')
			
			if(actulizar == "Aprobar"):
				solic = Solicitud.objects.filter(id=gestion)

				soli = solic[0]

				soli.estado = "aprobado"
				soli.observacionAdministrador = descripcion
				soli.save()

			elif(actulizar == "Negar"):
				solic = Solicitud.objects.filter(id=gestion)
				
				soli = solic[0]
				soli.estado = "negado"
				soli.observacionAdministrador = descripcion
				soli.save()

			else:
				print ''

			return HttpResponseRedirect('/gestionarSolicitud')

		else:
			
			global gestion

			gestion1 = request.POST.get("nuevo",0)

			if (gestion1 != 0):
				gestion = gestion1

			
			SolActual = Solicitud.objects.filter(id=gestion)

			FE = FechaUso.objects.filter(solicitud=SolActual)
				

			F = FechaUso.objects.filter(fechaInicio__range=(FE[0].fechaInicio,FE[0].fechaFinal))
			S = Solicitud.objects.all().order_by('fechaDeCreacion')
			


			solicitudT = []
			solicitud = []

			for x in S:
				for y in F:
					if(x.id == y.solicitud.id):		
						if(x.estado == "aprobado" or x.estado == "pendiente"):
							solicitudT.append(x)

			control = 0
			for x in solicitudT:
				if(control>0):
					if(x.id == solicitudT[control-1].id):
						print ''
					else:
						solicitud.append(x)
						
				control+=1
			return render(request,'aplicacion/choqueSolicitud.html',{'SolActual':SolActual, 'solicitud':solicitud}) 
		


@login_required(login_url = '/login/')
def consultar(request):
	us = request.user.username	

	if request.method =="GET":
		
		#solicitud = Solicitud.objects.all()
		coordinador = Coordinador.objects.filter(nombre=us)
		solicitud = Solicitud.objects.filter(coordinador=coordinador).order_by("fechaDeCreacion")

		return render(request,'aplicacion/consultar.html',{'solicitudes':solicitud})
	elif request.method=="POST":

		elim = request.POST.get("eliminar",0)

		
		Solicitud.objects.filter(id=elim).delete()

		elim = 0
		coordinador = Coordinador.objects.filter(nombre=us)
		solicitud = Solicitud.objects.filter(coordinador=coordinador).order_by("fechaDeCreacion")

		return render(request,'aplicacion/consultar.html',{'solicitudes':solicitud})
		#return HttpResponseRedirect('/')

	
@login_required(login_url = '/login/')
def permisos(request):
	us = request.user
	ct = ContentType.objects.get_for_model(Solicitud)
	permiso = Permission.objects.create(codename = 'administrador', name = 'puede accesar como  administrador', content_type = ct)
	us.user_permissions.add(permiso)

	if request.method =="GET":
		return render(request, 'aplicacion/inicio.html')


