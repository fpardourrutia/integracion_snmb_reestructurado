# coding: utf8

## En esta sección se definen las tablas correspondientes a la pestaña de 
## Grabadora, es decir: Grabadora, Imagen_referencia_grabadora, 
## Archivo_referencia_grabadora, Imagen_referencia_microfonos,
## Archivo_grabadora
## El campo de ID es automático en Web2py, por lo que no se incluye:

##########################################################################
## Grabadora
########################################################################

Campos_Grabadora = [

    Field('sitio_muestra_id','reference Sitio_muestra'),         

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

    Field('microfonos_mojados','boolean'),
    Field('comentario', 'text')
    ]

db.define_table('Grabadora',*Campos_Grabadora)

########################
#Imagen_referencia_grabadora
########################

Campos_Imagen_referencia_grabadora = [
    Field('grabadora_id','reference Grabadora'),
    Field('archivo_nombre_original'),
    Field('archivo','upload',autodelete=True)
    ]

db.define_table('Imagen_referencia_grabadora',*Campos_Imagen_referencia_grabadora,
    singular='Imagen grabadora', plural='Imágenes gradadoras')

########################
#Imagen_referencia_microfonos
########################

Campos_Imagen_referencia_microfonos = [
    Field('grabadora_id','reference Grabadora'),
    Field('archivo_nombre_original'),
    Field('archivo','upload',autodelete=True)
    ]

db.define_table('Imagen_referencia_microfonos',*Campos_Imagen_referencia_microfonos,
    singular='Imágen micrófonos', plural='Imágenes micrófonos')

########################
#Archivo_referencia_grabadora (metadatos)
########################

Campos_Archivo_referencia_grabadora = [
    Field('grabadora_id','reference Grabadora'),
    Field('archivo_nombre_original'),
    Field('archivo','upload', autodelete=True)
    ]

db.define_table('Archivo_referencia_grabadora',*Campos_Archivo_referencia_grabadora, 
    singular='Archivo metadatos', plural='Archivos metadatos')

########################
#Archivo_grabadora
########################

Campos_Archivo_grabadora = [
    Field('grabadora_id','reference Grabadora'),
    Field('archivo_nombre_original'),
    Field('archivo','upload', autodelete=True),
    Field('es_audible','boolean')
    ]

db.define_table('Archivo_grabadora',*Campos_Archivo_grabadora, 
    singular='Archivo grabadora', plurals='Archivos grabadoras')