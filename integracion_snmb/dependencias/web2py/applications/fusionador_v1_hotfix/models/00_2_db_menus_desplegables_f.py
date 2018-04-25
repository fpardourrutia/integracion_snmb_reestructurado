# coding: utf8

## En esta sección se definen las tablas de los menus desplegables 
## correspondientes a CONANP

############################################################################
# Pestaña Conteo de aves
############################################################################

db.define_table('Cat_conabio_aves', Field('nombre', 'string', required='TRUE'))

############################################################################

##########################################################################
## Pestaña Carbono
########################################################################

db.define_table('Cat_material_carbono',Field('nombre','string',
	required='TRUE'))

#########################################################################

db.define_table('Cat_grado_carbono',Field('nombre','integer',
	required='TRUE'))

#########################################################################

db.define_table('Cat_transecto_direccion',Field('nombre','string',
	required='TRUE'))

#########################################################################

db.define_table('Cat_forma_vida',Field('nombre','string',
	required='TRUE'))

#########################################################################

db.define_table('Cat_condiciones_ambientales',Field('nombre','string',
	required='TRUE'))

##########################################################################
## Pestaña Impactos ambientales
########################################################################

db.define_table('Cat_tipo_impacto',Field('nombre','string',
	required='TRUE'))

#########################################################################

db.define_table('Cat_severidad_impactos',Field('nombre','string',
	required='TRUE'))

#########################################################################

db.define_table('Cat_agente_impactos',Field('nombre','string',
	required='TRUE'))

#########################################################################

db.define_table('Cat_estatus_impactos',Field('nombre','string',
	required='TRUE'))

#########################################################################

db.define_table('Cat_prop_afectacion',Field('nombre','string',required='TRUE'))

#########################################################################

db.define_table('Cat_incendio',Field('nombre','string',required='TRUE'))

#########################################################################
