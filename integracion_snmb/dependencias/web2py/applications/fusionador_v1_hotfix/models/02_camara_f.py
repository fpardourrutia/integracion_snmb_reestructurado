#coding: utf8

# En esta sección se definen las tablas correspondientes a la pestaña de 
# Camara, es decir: Camara, File_camera, Reference_image_camera
# El campo de ID es automático en Web2py, por lo que no se incluye:

##########################################################################
## Cámara
########################################################################


Campos_Camara = [

	Field('sitio_muestra_id','reference Sitio_muestra'), 

 	#Se insertará a partir de un catálogo
	Field('nombre','string'),

	Field('fecha_inicio','date'),
	Field('fecha_termino','date'),
	Field('hora_inicio','time'),
	Field('hora_termino','time'),

	Field('lat_grado','integer'),
	Field('lat_min','integer'),
	Field('lat_seg','double'),
	Field('lon_grado','integer'),
	Field('lon_min','integer'),
	Field('lon_seg','double'),
	Field('altitud','double'),
	Field('gps_error','double'),

	#Se insertarán a partir de un catálogo
	Field('elipsoide','string'),
	Field('condiciones_ambientales','string'),

	Field('distancia_centro','double'),
	Field('azimut','double'),

	#Se insertarán a partir de un catálogo
	Field('resolucion','string'),
	Field('sensibilidad','string'),

    Field('comentario', 'text')
    ]

db.define_table('Camara',*Campos_Camara,singular='Trampa cámara',plural=
	'Trampas cámara')

########################
#Imagen_referencia_camara
########################

Campos_Imagen_referencia_camara = [

	Field('camara_id','reference Camara'),
    Field('archivo_nombre_original'),
    Field('archivo','upload',autodelete=True)
    ]

db.define_table('Imagen_referencia_camara',*Campos_Imagen_referencia_camara, 
	singular='Imagen cámara',plural='Imágenes cámaras')

########################
#Archivo_camara
########################

Campos_Archivo_camara = [
	Field('camara_id','reference Camara'),
    Field('archivo_nombre_original'),
    Field('archivo','upload',autodelete=True),
# uploadfolder='static/pictures'),      pensar estructura de carpetas
    Field('presencia','boolean'),
    Field('nombre_comun','string'),
    Field('nombre_cientifico','string'),
    Field('numero_individuos','integer')
    ]

db.define_table('Archivo_camara',*Campos_Archivo_camara, 
	singular='Archivo cámara',plural='Archivos cámara')
