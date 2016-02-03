from django.conf.urls import patterns, url
from aplicacion import views
from .views import inicio,solicitud,matriz,generar_pdf, nuevousuario, iniciarsesion, cerrarsesion, choqueSolicitud, gestionarSolicitud, consultar, permisos
from django.views.generic import RedirectView


urlpatterns = patterns('',
                      # url(r'^$', views.first_view, name='first-view'),

		url(r'^$', 'aplicacion.views.inicio'),
		url(r'^newuser/$', 'aplicacion.views.nuevousuario',name="nuevousuario"),
		url(r'^login/$', 'aplicacion.views.iniciarsesion',name="iniciarsesion"),
		url(r'^logout/$', 'aplicacion.views.cerrarsesion',name="cerrarsesion"),
		url(r'^permisos/$', 'aplicacion.views.permisos',name="permisos"),
		url(r'^crearSolicitud/$', 'aplicacion.views.solicitud',name="solicitud"),
		url(r'^validarSolicitud/$', 'aplicacion.views.matriz',name="matriz"),
		url(r'^consultar/$', 'aplicacion.views.consultar',name="consultar"),
		url(r'^gestionarSolicitud/$', 'aplicacion.views.gestionarSolicitud',name="gestionarSolicitud"),
		url(r'^choqueSolicitud/$', 'aplicacion.views.choqueSolicitud',name="choqueSolicitud"),
		url(r'^generar_pdf/$', 'aplicacion.views.generar_pdf', name='pdf')
		            )
