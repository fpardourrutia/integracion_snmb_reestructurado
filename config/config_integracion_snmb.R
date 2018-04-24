# Ruta donde se encuentran las dependencias de las funciones especificadas
# en "funciones_integracion.R". Esta ruta debe ser relativa a dicho archivo
ruta_dependencias <- "dependencias"

# Ruta a la carpeta que contiene la aplicación de Web2py que contiene los clientes y
# fusionadores nombrados como en el archivo anterior.
ruta_web2py <- paste0(ruta_dependencias, "/web2py")

### Pasarlo a YAML para que se pueda leer tanto de R como de python.

#######################
# revisar_esquemas()
#######################

# Nombre de la carpeta donde se almacenarán las bases de datos agrupadas
nombre_carpeta_bd_agrupadas = "1_bases_agrupadas"
# Nombre del archivo con la información del esquema correspondiente a cada BD,
# sin terminación. Se almacenará en la carpeta "nombre_carpeta_bd_agrupadas"
nombre_archivo_revision_bd = "archivo_revision_bd"

#######################
# clasificar_bases()
#######################

# Nombre de la carpeta que contendrá las bases clasificadas en subcarpetas. Cada
# subcarpeta corresponde a un fusionador distinto.
nombre_carpeta_bd_clasificadas = "2_bases_clasificadas"
# Ruta al archivo de excel donde se especifican el cliente y el fusionador correspondiente
# a cada tipo de base de datos SQLite
ruta_archivo_esquemas_clientes_fusionadores <-
  paste0(ruta_dependencias, "/fusionar_bases/relacion_esquemas_clientes_fusionadores.xlsx")



