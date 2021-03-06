Impactos ambientales
====================

Cada archivo de vista está dividido en tres secciones: CSS, HTML y JavaScript. 

Index1
------
A continuación describimos las clases utilizadas en el archivo *index1.html*, así como los identificadores asociados al código JavaScript. Éste corresponde a la vista *Impactos actuales*.

Clases
^^^^^^

* **Tabla**, **TablaCONANP** y **Centrar** se utilizan para dar distinto estilo a las celdas de las tablas.

* **obligatorio** sirve para indicar campos obligatorios, mismos que serán validados al enviar la forma.

Identificadores
^^^^^^^^^^^^^^^

A continuación se describen los identificadores con funcionalidades ligadas a AJAX.

* **tabla_conglomerado_muestra_id** corresponde al campo *Conglomerado*, se utiliza para validar si el conglomerado que se escribió ya está registrado en la base de datos. 

Validaciones
^^^^^^^^^^^^

Hay dos tipos de validación, la primera (validación al momento) se lleva a cabo conforme el usuario captura la información y la segunda se lleva a cabo cuando se envía la forma.

1. Al momento. 
	+ Conglomerado (id *tabla_conglomerado_muestra_id*), se utiliza para validar si el número conglomerado que se seleccionó ya está registrado en la base de datos. Para lograr estó se utiliza AJAX, sin embargo, no es posible utilizar el AJAX de Web2py ya que el objetivo es validación.

2. Al enviar. 
	+ La clase *obligatorio*, todos los campos con esta clase deben tener información.


Index2
------
A continuación describimos las clases utilizadas en el archivo *index2.html*, así como los identificadores asociados al código JavaScript. Éste corresponde a la vista *Plagas*.

Clases
^^^^^^

* **Tabla**, **FlotaIzquierda** y **CentrarV** se utilizan para dar distinto estilo a las celdas de las tablas.

* **obligatorio** sirve para indicar campos obligatorios, mismos que serán validados al enviar la forma.

Identificadores
^^^^^^^^^^^^^^^

A continuación se describen los identificadores con funcionalidades ligadas a AJAX.

* **tabla_conglomerado_muestra_id** corresponde al campo *Conglomerado*, se utiliza para validar si el conglomerado que se escribió ya está registrado en la base de datos. 

Adicionalmente hay identificadores para la función de desvanecer campos (fade-in/fade-out).

* **tabla_hay_nombre_comun**, **tabla_hay_nombre_cientifico**, **tabla_nombre_comun** y **tabla_nombre_cientifico**,  la funcionalidad consiste en desvanecer los campos *Nombre común* y *Nombre científico* cuando no se selecciona la casilla correspondiente a existe. Adicionalmente son identificadores que se utilizan en la validación.


Validaciones
^^^^^^^^^^^^

La validación se lleva a cabo cuando se envía la forma.

	+ La clase *obligatorio*, todos los campos con esta clase deben tener información.

	+ Los identificadores *tabla_hay_nombre_comun*, *tabla_hay_nombre_cientifico*, *tabla_nombre_comun* y *tabla_nombre_cientifico* se utilizan para validar, primero que 
	al menos una de las casillas a la izquierda del campo *Nombre común* y *Nombre científico* este seleccionada. También se valida que si la casilla está seleccionada, el campo de Nombre no esté vacío.


Index3
------
A continuación describimos las clases utilizadas en el archivo *index3.html*, así como los identificadores asociados al código JavaScript. Éste corresponde a la vista *Incendios*.

Clases
^^^^^^

* **Tabla**, **FlotaIzquierda**, **Centrar** y **CentrarV** se utilizan para dar distinto estilo a las celdas de las tablas.

* **obligatorio** e **incendio_info* sirven para indicar campos obligatorios, mismos que serán validados al enviar la forma.

Identificadores
^^^^^^^^^^^^^^^

A continuación se describen los identificadores con funcionalidades ligadas a AJAX.

* **tabla_conglomerado_muestra_id** corresponde al campo *Conglomerado*, se utiliza para validar si el conglomerado que se escribió ya está registrado en la base de datos. 

Adicionalmente hay identificadores para la función de desvanecer campos (fade-in/fade-out).

* **tabla_hay_evidencia**, tiene la funcionalidad de aparecer/desvanecer los campos de la vista cuando se selecciona la casilla de *Evidencia*.

Validaciones
^^^^^^^^^^^^

Hay dos tipos de validación, la primera (validación al momento) se lleva a cabo conforme el usuario captura la información y la segunda se lleva a cabo cuando se envía la forma.

1. Al momento. 
	+ Conglomerado (id *tabla_conglomerado_muestra_id*), se utiliza para validar si el número conglomerado que se seleccionó ya está registrado en la base de datos. Para lograr estó se utiliza AJAX, sin embargo, no es posible utilizar el AJAX de Web2py ya que el objetivo es validación.

2. Al enviar. 
	+ La clase *obligatorio* todos los campos con esta clase deben tener información.

	+ La clase *incendio_info* si seleccionó la casilla de evidencia se debm llenar los campos con la clase *incendio_info*.


