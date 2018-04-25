# coding: utf8

## En esta sección se definen las tablas correspondientes a la pestaña de 
## Especies Invasoras, es decir: Transecto_especies_invasoras_muestra, 
## Especie_invasora, Archivo_especie_invasora 

##########################################################################
## Transecto_especies_invasoras_muestra
########################################################################

Campos_Punto_conteo_aves =[

	Field('sitio_muestra_id','reference Sitio_muestra'),
	Field('tecnico','string'),
	Field('fecha','date'),
    Field('hora_inicio','time'),
	Field('hora_termino','time'),
	Field('condiciones_ambientales','string'),
    Field('comentario','text')
]

db.define_table('Punto_conteo_aves',*Campos_Punto_conteo_aves, 
	singular='Punto de conteo de aves',plural='Puntos de conteo de aves')

##########################################################################
## Conteo_ave
########################################################################

Campos_Conteo_ave =[

	Field('punto_conteo_aves_id','reference Punto_conteo_aves'),
	Field('nombre_en_lista','boolean'),
	Field('nombre_comun','string'),
    Field('nombre_cientifico','string'),
    Field('es_visual','boolean'),
    Field('es_sonora','boolean'),
    Field('numero_individuos','integer'),
    Field('distancia_aproximada','double')
]

db.define_table('Conteo_ave',*Campos_Conteo_ave,
	singular='Conteo de aves',plural='Conteos de aves')

##########################################################################
## Archivo_conteo_ave
########################################################################

Campos_Archivo_conteo_ave = [

	Field('conteo_ave_id','reference Conteo_ave'),
    Field('archivo_nombre_original'),
    Field('archivo','upload',autodelete=True)
]

db.define_table('Archivo_conteo_ave',*Campos_Archivo_conteo_ave,
	singular='Archivo conteo de aves',plural='Archivos conteo de aves')
