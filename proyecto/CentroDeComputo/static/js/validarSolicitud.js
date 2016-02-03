 var K=0;
 var Dario=0;

 // JavaScript Document
 $(document).on("ready", function(){

 		//Maquetado de Matriz
 		//pintarMatriz("Horarios_Lcomp");
 		//pintarMatriz(2,"Horarios_Lcomp_2");
 		
 		//bloquearOcupados("lcomp1",0,"6:20 AM - 8:05 AM");

 		$(':checkbox[readonly=readonly]').click(function(){
			return false;         
		});
 		
 });


//Recibe numero de lcomp, nombre lcomp
function pintarMatriz(cadLab){

		var form = document.getElementById('TodosHorarios'); //Busca el formulario
		var matriz = document.createElement("section"); //Crea el Section
		matriz.setAttribute("id", cadLab);
		matriz.setAttribute("class", cadLab);

		//Titulo de Matriz
		var h4 = document.createElement("h4");
		var titulo = document.createTextNode(cadLab);
		h4.appendChild(titulo);

		matriz.appendChild(h4);

		form.appendChild(matriz);

		//Crear Tabla
 		var tabla = document.createElement("table");
 		tabla.setAttribute("class", "table table-bordered table-striped bs-table");
 		var tblBody = document.createElement("tbody");


 		//Crear thead Cabecera de la Matriz
 		var thead = document.createElement("thead");
 		var tr = document.createElement("tr");
 			//Nada
 			var th = document.createElement("th");
 			var textoCelda = document.createTextNode("");
 			th.appendChild(textoCelda);
 			tr.appendChild(th);

 			//LUNES
 			var th = document.createElement("th");
 			var textoCelda = document.createTextNode("LUNES");
 			th.appendChild(textoCelda);
 			tr.appendChild(th);


 			//MARTES
 			var th = document.createElement("th");
 			var textoCelda = document.createTextNode("MARTES");
 			th.appendChild(textoCelda);
 			tr.appendChild(th);

 			//MIERCOLES
 			var th = document.createElement("th");
 			var textoCelda = document.createTextNode("MIERCOLES");
 			th.appendChild(textoCelda);
 			tr.appendChild(th);

 			//JUEVES
 			var th = document.createElement("th");
 			var textoCelda = document.createTextNode("JUEVES");
 			th.appendChild(textoCelda);
 			tr.appendChild(th);

 			//VIERNES
 			var th = document.createElement("th");
 			var textoCelda = document.createTextNode("VIERNES");
 			th.appendChild(textoCelda);
 			tr.appendChild(th);

 			//SABADO
 			var th = document.createElement("th");
 			var textoCelda = document.createTextNode("SABADO");
 			th.appendChild(textoCelda);
 			tr.appendChild(th);

 		thead.appendChild(tr);
 		tabla.appendChild(thead);

 		//Crear tbody Cuerpo de la Matriz
 		for(var i=0; i<8; i++){ //#Filas
 			var fila = document.createElement("tr");
 			var th = document.createElement("th");
 			var textoCelda;

 			//if loco
 			if(i==0){textoCelda=document.createTextNode("6:20 AM - 8:00 AM");}
 			if(i==1){textoCelda=document.createTextNode("8:05 AM - 9:45 AM");}
 			if(i==2){textoCelda=document.createTextNode("9:50 AM - 11:30 AM");}
 			if(i==3){textoCelda=document.createTextNode("11:35 AM - 1:15 PM");}
 			if(i==4){textoCelda=document.createTextNode("1:20 PM - 3:00 PM");}
 			if(i==5){textoCelda=document.createTextNode("3:05 PM - 4:45 PM");}
 			if(i==6){textoCelda=document.createTextNode("4:50 PM - 6:30 PM");}
 			if(i==7){textoCelda=document.createTextNode("6:35 PM - 8:15 PM");}
 			

 			th.appendChild(textoCelda);
 			fila.appendChild(th);


 			for (var j = 0; j < 6; j++) { //#Columnas
 					var a = String(i);
					var b = String(j);
					
					var celda = document.createElement("td");
 					var label = document.createElement("label");
 					
 					var input1 = document.createElement("input");
					
					//Atributos del input checkbox
 					input1.setAttribute("type", "checkbox");
 					input1.setAttribute("name", 1+","+String(i)+","+String(j));
 					input1.setAttribute("id", 1+","+String(i)+","+String(j));

 					label.appendChild(input1);



 					var input2 = document.createElement("input");
					
					//Atributos del input checkbox
 					input2.setAttribute("type", "checkbox");
 					input2.setAttribute("name", 2+","+String(i)+","+String(j));
 					input2.setAttribute("id", 2+","+String(i)+","+String(j));

 					label.appendChild(input2);

 					
 					var input3 = document.createElement("input");
					
					//Atributos del input checkbox
 					input3.setAttribute("type", "checkbox");
 					input3.setAttribute("name", 3+","+String(i)+","+String(j));
 					input3.setAttribute("id", 3+","+String(i)+","+String(j));
 					
 					label.appendChild(input3);


 					var input4 = document.createElement("input");
					
					//Atributos del input checkbox
 					input4.setAttribute("type", "checkbox");
 					input4.setAttribute("name", 4+","+String(i)+","+String(j));
 					input4.setAttribute("id", 4+","+String(i)+","+String(j));
 					
					
					label.appendChild(input4);
 					var textoCelda = document.createTextNode(
 							"Aqui deberia ir el codigo del checkbutom"
 						);

 					//label.appendChild(input);
 					
 					
 					//label.appendChild(textoCelda);
 					celda.appendChild(label);
 					fila.appendChild(celda);
 			}

 			tblBody.appendChild(fila);
 		}

 		tabla.appendChild(tblBody);
 		matriz.appendChild(tabla);

}


function bloquearOcupados(){
	/*
	usado.hora //hora  6 - 8
    usado.dia // dia 0- 5 //lun - sab
    usado.fechaUso.laboratorio.codigo  //lcomp1 , .... lcomp4
	*/
	//alert(hora +dia +Codlab);
	/*
	global++;
	Codlab.setAttribute('id','A'+String(global));
	hora.setAttribute('id','B'+String(global));
	dia.setAttribute('id','C'+String(global));
	*/
	K= K+1;

	var Codlab = document.getElementById('A').value;
	var hora = document.getElementById('B').value;
	var dia = document.getElementById('C').value;


	document.getElementById('A').id = 'X'+String(K);
	document.getElementById('B').id = 'Y'+String(K);
	document.getElementById('C').id = 'Z'+String(K);

	var H;
	var D;
	var L;
	var chbx;

	switch(hora){
		case "6:20 AM - 8:00 AM":
			H = 0;
		break;
		case "8:05 AM - 9:45 AM":
			H = 1;
		break;
		case "9:50 AM - 11:30 AM":
			H = 2;
		break;
		case "11:35 AM - 1:15 PM":
			H = 3;
		break;
		case "1:20 PM - 3:00 PM":
			H = 4;
		break;
		case "3:05 PM - 4:45 PM":
			H = 5;
		break;
		case "4:50 PM - 6:30 PM":
			H = 6;
		break;
		case "6:35 PM - 8:15 PM":
			H = 7;
		break;
	}

	switch(Codlab){
		case "lcomp1":
			L = 1;
		break;
		case "lcomp2":
			L = 2;
		break;
		case "lcomp3":
			L = 3;
		break;
		case "lcomp4":
			L = 4;
		break;
	}

	D = dia ;
	/*
	L = String(L);
	D = String(D);
	H = String(H);
	*/


	bloqueo(L,H,D,0);

}


function NoUsado(){

	Dario= Dario+1;

	var Nolab = document.getElementById('Motto').value;
	document.getElementById('Motto').id = 'M'+String(Dario);

	switch(Nolab){
		case "lcomp1":
			L = 1;
		break;
		case "lcomp2":
			L = 2;
		break;
		case "lcomp3":
			L = 3;
		break;
		case "lcomp4":
			L = 4;
		break;
	}

	for(var i=0; i<8; i++){ //#Filas
		for (var j = 0; j < 6; j++) { //#Columnas
			bloqueo(L,i,j,1);

		}
	}
}


function bloqueo(Lab,Hora,Dia,tipo){
	invento = String(Lab)+","+String(Hora)+","+String(Dia);
	//alert(invento);

	chbx = document.getElementById(invento);

	chbx.setAttribute('readonly', 'readonly');
	chbx.setAttribute('onclick', 'javascript: return false;');
	if(tipo == 0){
		chbx.setAttribute('style','box-shadow: 0px 0px 7px #FF0000;');	//Bloqueado

	}else{
		chbx.setAttribute('style','box-shadow: 0px 0px 7px #286090;');	//Lcomp no seleccionado
	}
	
}