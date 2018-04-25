# coding: utf8

## En esta sección se definen una tabla auxiliar, que sirve para guardar los archivos csv
## subidos, antes de ser exportados a la base de datos.

########################
#Conglomerado_muestra
########################

Campos_Archivo_csv = [

    Field('archivo_nombre_original',required=True),
    Field('archivo','upload',autodelete=True,required=True)
    ]

db.define_table('Archivo_csv',*Campos_Archivo_csv)
