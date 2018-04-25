# coding: utf8

# En esta sección se definen las tablas correspondientes a la pestaña de 
# epífitas, es decir: Informacion_epifitas

##########################################################################
## Informacion_epifitas
##########################################################################

Campos_Informacion_epifitas = [

    Field('sitio_muestra_id','reference Sitio_muestra'),
    Field('helechos_observados','boolean'),
    Field('orquideas_observadas','boolean'),
    Field('musgos_observados','boolean'),
    Field('liquenes_observados','boolean'),
    Field('cactaceas_observadas','boolean'),
    Field('bromeliaceas_observadas','boolean'),
    Field('otras_observadas','boolean'),
    Field('nombre_otras','string')
    ]

db.define_table('Informacion_epifitas',*Campos_Informacion_epifitas,
    singular='Epífita',plural='Epífitas')