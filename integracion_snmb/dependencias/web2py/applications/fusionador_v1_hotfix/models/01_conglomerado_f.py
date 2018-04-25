# coding: utf8

## En esta sección se definen las tablas correspondientes a la pestaña de Conglomerado, es decir: Conglomerado_muestra, Sitio_muestra y Reference_image_site:
## El campo de ID es automático en Web2py, por lo que no se incluye:

###Se eliminó el requisito de que algunos campos sean requeridos para mayor flexibilidad en el fusionador.

########################
#Conglomerado_muestra
########################

Campos_Conglomerado_muestra = [

	Field('nombre','string'),
	Field('fecha_visita','date'),
	Field('predio','string'),
	Field('compania','string'),
	#Se insertarán a partir de un catálogo
	Field('tipo','string'),
    Field('estado','string'),
    Field('municipio','string'),
    Field('tenencia','string'),
    Field('uso_suelo_tipo', 'string'),

    #Campo oculto identificador SAR-MOD, SAC-MOD
    Field('monitoreo_tipo','string',),    

    #Los dos siguientes campos sólo se eligen si uso_suelo_tipo="Vegetación"

    #Se insertará a partir de un catálogo
	Field('vegetacion_tipo','string'),
    Field('perturbado','boolean'),

	Field('comentario','text')
	]

db.define_table('Conglomerado_muestra', *Campos_Conglomerado_muestra, 
	singular='Conglomerado', plural='Conglomerados')

########################
#Sitio_muestra
########################

Campos_Sitio_muestra = [

	Field('conglomerado_muestra_id','reference Conglomerado_muestra'),
	Field('sitio_numero','string'),
	Field('existe', 'boolean'),

	Field('lat_grado','integer'),
	Field('lat_min','integer'),
	Field('lat_seg','double'),
	Field('lon_grado','integer'),
	Field('lon_min','integer'),
	Field('lon_seg','double'),
    Field('altitud','double'),
    Field('gps_error','double'),

    #Se insertará a partir de un catálogo
	Field('elipsoide','string'), 
	
    Field('hay_evidencia','boolean')
    ] 

db.define_table('Sitio_muestra',*Campos_Sitio_muestra,singular='Sitio', 
	plural='Sitios')

########################
#Imagen_referencia_sitio
########################

Campos_Imagen_referencia_sitio = [

	Field('sitio_muestra_id','reference Sitio_muestra'),
    Field('archivo_nombre_original'),
    Field('archivo','upload',autodelete=True)
    ]
    
db.define_table('Imagen_referencia_sitio',*Campos_Imagen_referencia_sitio, 
	singular='Imagen sitio',plural='Imágenes sitios')

########################################################################
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more opcions, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################
