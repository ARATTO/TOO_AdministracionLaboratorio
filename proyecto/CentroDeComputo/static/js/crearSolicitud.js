// JavaScript Document
/*jQuery(function($){
	$.datepicker.regional['es'] = {
		closeText: 'Cerrar',
		prevText: '&#x3c;Ant',
		nextText: 'Sig&#x3e;',
		currentText: 'Hoy',
		monthNames: ['Enero','Febrero','Marzo','Abril','Mayo','Junio',
		'Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'],
		monthNamesShort: ['Ene','Feb','Mar','Abr','May','Jun',
		'Jul','Ago','Sep','Oct','Nov','Dic'],
		dayNames: ['Domingo','Lunes','Martes','Mi&eacute;rcoles','Jueves','Viernes','S&aacute;bado'],
		dayNamesShort: ['Dom','Lun','Mar','Mi&eacute;','Juv','Vie','S&aacute;b'],
		dayNamesMin: ['Do','Lu','Ma','Mi','Ju','Vi','S&aacute;'],
		weekHeader: 'Sm',
		dateFormat: 'dd/mm/yy',
		firstDay: 1,
		isRTL: false,
		showMonthAfterYear: false,
		yearSuffix: ''};
	$.datepicker.setDefaults($.datepicker.regional['es']);
});    */
		function validarFechasInicioFinal(date1, date2){
			  var x=new Date();
			  var fecha = date1.split("/");
			  x.setFullYear(fecha[2],fecha[0]-1,fecha[1]);
			  
			  var y=new Date();
			  var fecha = date2.split("/");
			  y.setFullYear(fecha[2],fecha[0]-1,fecha[1]);
		 		
				
			  if (x > y){
			  	alert("Fecha NO valida. Es menor que la Fecha Inicial");
			  }
		}
		
		function validarFechaMenorActual(date){
			  var x=new Date();
			  var fecha = date.split("/");
			  //alert(fecha);
			  x.setFullYear(fecha[2],fecha[0]-1,fecha[1]);
			  //alert(x);
			  var today = new Date();
		 	//alert(today);
				
			  if (x < today){
			  	alert("Fecha NO valida. Es menor que la Fecha Actual");
			  }
		}
		
		function validarForm(){

			//var x = document.forms["formCrear"]["lab1"].checked;
			if( document.forms["formCrear"]["lab1"].checked || document.forms["formCrear"]["lab2"].checked || document.forms["formCrear"]["lab3"].checked || document.forms["formCrear"]["lab4"].checked ){
					if( !(document.forms["formCrear"]["fechaInicio"].value == null || document.forms["formCrear"]["fechaInicio"].value == "")){
						if( !(document.forms["formCrear"]["fechaFinal"].value == null || document.forms["formCrear"]["fechaFinal"].value == "")){
							if( document.forms["formCrear"]["razonSolicitud"].value == "Otro"){
								if(  !(document.forms["formCrear"]["descripcionRazon"].value == null || document.forms["formCrear"]["descripcionRazon"].value == "") ){
									return true;
								}
								else{
									alert("Debe escribir una Descripcion de la razon de su solicitud");
									return false;
								}
							}
							else{
								return true;
							}
						}
						else{
							alert("Debe asignar una Fecha Final Valida");
							return false;
						}
					}
					else{
						alert("Debe asignar una Fecha Inicio Valida");
						return false;
					}
			}
			else{
				alert("Debe seleccionar almenos un LCOMP");
				return false;
			}
			
		}
		
        $(document).ready(function() {
           $("#fechaInicio").datepicker();
		   $("#fechaFinal").datepicker();

		   $("#fechaInicio").change(function(){				
							validarFechaMenorActual(document.getElementById('fechaInicio').value);			
		   });
		   $("#fechaFinal").change(function(){
			   				validarFechaMenorActual(document.getElementById('fechaFinal').value);
							validarFechasInicioFinal(document.getElementById('fechaInicio').value, document.getElementById('fechaFinal').value)
							
		   });

        });


		
		
		
		
		
		