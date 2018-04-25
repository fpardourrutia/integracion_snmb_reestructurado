# coding: utf8

# En esta sección se definen las tablas correspondientes a la pestaña de 
# Carbono, es decir: Carbono_mantillo, Ramas_transecto y Rama_caida_1000h

##########################################################################
## Transecto_ramas
##########################################################################

Campos_Transecto_ramas = [

    Field('sitio_muestra_id','reference Sitio_muestra'),
    Field('direccion','string'),
    Field('pendiente','integer'),
    Field('abundancia_1h','integer'),
    Field('abundancia_10h','integer'),
    Field('abundancia_100h','integer')
    ]

db.define_table('Transecto_ramas',*Campos_Transecto_ramas,
    singular='Ramas en transecto',plural='Ramas en transectos')


##########################################################################
## Rama_1000h
##########################################################################

Campos_Rama_1000h = [    
    Field('transecto_ramas_id','reference Transecto_ramas'),
    Field('diametro','double'),
    
    #Se insertará a partir de un catálogo
    Field('grado','integer')
]

db.define_table('Rama_1000h',*Campos_Rama_1000h,
    singular='Rama 1000h',plural='Ramas 1000h')


##########################################################################
## Punto_carbono
##########################################################################

Campos_Punto_carbono = [

    Field('sitio_muestra_id','reference Sitio_muestra'),
    Field('transecto_direccion','string'),
    Field('transecto_distancia','integer'),

    #Se insertará a partir de un catálogo
    Field('material_tipo','string'),

    Field('grosor','integer'),

    Field('peso_humedo','double'),
    Field('peso_humedo_muestra','double'),
    Field('peso_seco_muestra','double')
    ]

db.define_table('Punto_carbono',*Campos_Punto_carbono,
    singular='Carbono en el mantillo',plural='Carbono en el mantillo')


##########################################################################
## Arbol_transecto: arboles pequeños y arbustos
##########################################################################

Campos_Arbol_transecto = [

    Field('sitio_muestra_id','reference Sitio_muestra'),
    #Se insertará a partir de un catálogo
    Field('transecto','string'),
    Field('individuo_numero','integer'),
    Field('nombre_comun','string'),
    Field('nombre_cientifico','string'),
    Field('forma_vida','string'),
    Field('distancia_copa','double'),
    Field('altura','double'),
    
    ]

db.define_table('Arbol_transecto',*Campos_Arbol_transecto,
    singular='Árbol transecto',plural='Árboles transectos')


##########################################################################
## Arbol_cuadrante
##########################################################################

Campos_Arbol_cuadrante = [

    Field('sitio_muestra_id','reference Sitio_muestra'),
    #Se insertará a partir de un catálogo
    # Field('cuadrante','string'),
    Field('individuo_numero','integer'),
    Field('existe', 'boolean'),

    Field('distancia','double'),
    Field('azimut','double'),
    Field('nombre_comun','string'),
    Field('nombre_cientifico','string'),
    Field('altura','double'),
    Field('diametro_normal','double'),
    Field('diametro_copa','double')
    ]

db.define_table('Arbol_cuadrante',*Campos_Arbol_cuadrante,
    singular='Árbol cuadrante',plural='Árboles cuadrante')