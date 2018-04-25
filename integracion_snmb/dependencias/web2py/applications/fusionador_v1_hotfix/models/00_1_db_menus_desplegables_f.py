# coding: utf8

## En esta sección se definen las tablas de los menus desplegables

##########################################################################
## Pestaña Conglomerado
########################################################################

db.define_table('Cat_tipo_conglomerado', Field('nombre', 'string', required='TRUE'))

#########################################################################

db.define_table('Cat_estado_conglomerado', 
    Field('clave_ent','integer',required='TRUE'),
    Field('nombre','string',required='TRUE'))

#########################################################################

db.define_table('Cat_tenencia_conglomerado', Field('nombre', 'string', required='TRUE'))

#########################################################################

db.define_table('Cat_suelo_conglomerado', Field('nombre', 'string'), required='TRUE')

#########################################################################

db.define_table('Cat_vegetacion_conglomerado', Field('nombre', 'string', required='TRUE'))

#########################################################################

db.define_table('Cat_numero_sitio', Field('nombre', 'string', required='TRUE'))

#########################################################################

db.define_table('Cat_elipsoide', Field('nombre', 'string', required='TRUE'))

##########################################################################
## Pestaña Camara
########################################################################

db.define_table('Cat_nombre_camara', Field('nombre', 'string', required='TRUE'))

#########################################################################

db.define_table('Cat_resolucion_camara', Field('nombre', 'string', required='TRUE'))

#########################################################################

db.define_table('Cat_sensibilidad_camara', Field('nombre', 'string', required='TRUE'))

##########################################################################
## Pestaña Grabadora
########################################################################

db.define_table('Cat_nombre_grabadora', Field('nombre', 'string', required='TRUE'))

##########################################################################
## Pestaña Especies Invasoras / Pestaña Huellas y excretas
######################################################################## 

db.define_table('Cat_numero_transecto', Field('nombre', 'string', required='TRUE'))

##########################################################################
## Pestaña Especies Invasoras
######################################################################## 

db.define_table('Cat_numero_individuos', Field('nombre', 'string', required='TRUE'))

##########################################################################
## Lista CONABIO de especies invasoras
######################################################################## 

db.define_table('Cat_conabio_invasoras', Field('nombre', 'string', required='TRUE'))

#########################################################################

db.define_table('Cat_municipio_conglomerado', 
    Field('clave_ent','integer',required='TRUE'),
    Field('clave_mun','integer',required='TRUE'),
    Field('nombre','string',required='TRUE'))
