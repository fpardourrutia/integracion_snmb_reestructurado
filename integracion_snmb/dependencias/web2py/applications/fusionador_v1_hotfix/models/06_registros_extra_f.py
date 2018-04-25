# coding: utf8

# En esta sección se definen las tablas correspondientes a la pestaña de Registros Extras,
# es decir: Especie_invasora_extra, Archivo_especie_invasora_extra,
# Huella_excreta_extra, Archivo_huella_excreta_extra,
# Especimen_restos_extra, Archivo_especimen_restos_extra.

##########################################################################
## Especie_invasora_extra
##########################################################################

Campos_Especie_invasora_extra = [

    Field('conglomerado_muestra_id','reference Conglomerado_muestra'),
    Field('esta_dentro_conglomerado','boolean'),
    Field('tecnico','string'),
    Field('fecha','date'),
    Field('hora','time'),

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

    Field('nombre_en_lista','boolean'),
    Field('nombre_comun','string'),
    Field('nombre_cientifico','string'),

    #Se insertará a partir de un catálogo
    Field('numero_individuos', 'string'),

    Field('comentario', 'text')
    ]

db.define_table('Especie_invasora_extra',*Campos_Especie_invasora_extra,
    singular='Especie invasora extra',plural='Especies invasoras extra')

##########################################################################
## Archivo_especie_invasora_extra
########################################################################

Campos_Archivo_especie_invasora_extra =[

    Field('especie_invasora_extra_id','reference Especie_invasora_extra'),
    Field('archivo_nombre_original'),
    Field('archivo','upload', autodelete=True)
]

db.define_table('Archivo_especie_invasora_extra',
    *Campos_Archivo_especie_invasora_extra,
    singular='Archivo especie invasora extra',
    plural='Archivo especies invasoras extra')

##########################################################################
## Huella_excreta_extra
##########################################################################

Campos_Huella_excreta_extra = [

    Field('conglomerado_muestra_id','reference Conglomerado_muestra'),
    Field('esta_dentro_conglomerado','boolean'),
    Field('tecnico','string'),
    Field('fecha','date'),
    Field('hora','time'),

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

    Field('es_huella','boolean'),
    Field('nombre_comun','string'),
    Field('nombre_cientifico','string'),
    Field('largo','double'),
    Field('ancho','double'),
    Field('comentario','text')
    ]

db.define_table('Huella_excreta_extra', *Campos_Huella_excreta_extra)

##########################################################################
## Archivo_huella_excreta_extra
########################################################################

Campos_Archivo_huella_excreta_extra = [

    Field('huella_excreta_extra_id','reference Huella_excreta_extra'),
    Field('archivo_nombre_original'),
    Field('archivo','upload',autodelete=True)
    ]

db.define_table('Archivo_huella_excreta_extra',
    *Campos_Archivo_huella_excreta_extra,
    singular='Huella/excreta extra',plural='Huellas/excretas extra')

##########################################################################
## Especimen_restos_extra
##########################################################################

Campos_Especimen_restos_extra = [

    Field('conglomerado_muestra_id','reference Conglomerado_muestra'),
    Field('esta_dentro_conglomerado','boolean'),
    Field('tecnico','string'),
    Field('fecha','date'),
    Field('hora','time'),

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

	Field('es_especimen','boolean'),
    Field('nombre_comun','string'),
    Field('nombre_cientifico','string'),

    #Se insertará a partir de un catálogo
    Field('numero_individuos','string'),
    Field('comentario','text')
    ]

db.define_table('Especimen_restos_extra',*Campos_Especimen_restos_extra,
    singular='Espécimen/restos', plural='Especímenes/restos')

##########################################################################
## Archivo_Especimen_restos_extra
########################################################################

Campos_Archivo_especimen_restos_extra = [

    Field('especimen_restos_extra_id','reference Especimen_restos_extra'),
    Field('archivo_nombre_original'),
    Field('archivo','upload', autodelete=True)
    ]

db.define_table('Archivo_especimen_restos_extra',
	*Campos_Archivo_especimen_restos_extra,
    singular='Archivo espécimen/restos',
    plural='Archivos especímenes/restos')

