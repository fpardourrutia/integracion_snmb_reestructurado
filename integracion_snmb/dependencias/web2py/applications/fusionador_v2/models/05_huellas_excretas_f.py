# coding: utf8

## En esta sección se definen las tablas correspondientes a la pestaña de 
## Huellas y Excretas, es decir: Transecto_huellas_excretas_muestra, 
## Huella_excreta, Archivo_huella_excreta

##########################################################################
## Transecto_huellas_excretas_muestra
########################################################################

Campos_Transecto_huellas_excretas_muestra = [

    Field('conglomerado_muestra_id','reference Conglomerado_muestra'),
    Field('fecha','date'),

    #Se insertará a partir de un catálogo
    Field('transecto_numero','string'),
    
    Field('tecnico','string'),
    Field('hora_inicio','time'),
    Field('hora_termino','time'),
    Field('comentario','text')
    ]

db.define_table('Transecto_huellas_excretas_muestra',
    *Campos_Transecto_huellas_excretas_muestra,
    singular='Transecto huellas y excretas',
    plural='Transectos huellas y excretas')

##########################################################################
## Huella_excreta
########################################################################


Campos_Huella_excreta = [

    Field('transecto_huellas_excretas_id','reference Transecto_huellas_excretas_muestra'),
    Field('es_huella','boolean'),
    Field('nombre_comun','string'),
    Field('nombre_cientifico','string'),
    Field('largo','double'),
    Field('ancho','double')
    ]

db.define_table('Huella_excreta',*Campos_Huella_excreta,
    singular='Huellas/excretas',plural='Huellas/excretas')

##########################################################################
## Archivo_huella_excreta
########################################################################

Campos_Archivo_huella_excreta = [

    Field('huella_excreta_id','reference Huella_excreta'),
    Field('archivo_nombre_original'),
    Field('archivo', 'upload', autodelete=True)
    ]

db.define_table('Archivo_huella_excreta',*Campos_Archivo_huella_excreta,
    singular='Archivo huellas/excretas',plural='Archivos huellas/excretas')
