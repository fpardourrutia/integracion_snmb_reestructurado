# Ruta donde se encuentran las dependencias de las funciones especificadas
# en "funciones_integracion.R". Esta ruta debe ser relativa a dicho archivo
ruta_dependencias <- "dependencias"

### Pasarlo a YAML para que se pueda leer tanto de R como de python.

#######################
# revisar_esquemas()
#######################

# Ruta hacia la carpeta en LUSTRE que contiene las bases de datos a fusionar
# (con temrinación .sqlite)
ruta_carpeta_entrada <- "ESPECIFICAR"

# Ruta hacia la carpeta que contendrá todos los productos del proceso de migración
# de dichas bases de datos
ruta_carpeta_salida <- "ESPECIFICAR"

# Nombre de la carpeta donde se almacenarán las bases de datos agrupadas
nombre_carpeta_bd_agrupadas = "1_bases_agrupadas"

# Nombre (sin terminación) del archivo con la información del esquema
# correspondiente a cada base. Se almacenará en la carpeta "nombre_carpeta_bd_agrupadas"
nombre_archivo_revision_bd = "archivo_revision_bd"

# Ruta al archivo de excel donde se especifican el cliente y el fusionador correspondiente
# a cada tipo de base de datos SQLite
ruta_archivo_esquemas_clientes_fusionadores <-
  paste0(ruta_dependencias, "/fusionar_bases/relacion_esquemas_clientes_fusionadores.xlsx")

#######################
# fusionar_bases()
#######################

# Ruta a la carpeta que contiene la aplicación de Web2py que contiene los clientes y
# fusionadores nombrados como en el archivo anterior.
ruta_web2py <- paste0(ruta_dependencias, "/web2py")

# Nombre de la carpeta donde se almacenarán las bases de datos fusionadas (tanto
# en formato csv como sqlite)
nombre_carpeta_bd_fusionadas = "2_bases_fusionadas"


