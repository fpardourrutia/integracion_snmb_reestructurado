# Ruta donde se encuentran las dependencias de las funciones especificadas
# en "funciones_integracion.R":
ruta_dependencias <- "/dependencias"

# Ruta al archivo de excel donde se especifican el cliente y el fusionador correspondiente
# a cada tipo de base de datos SQLite
ruta_archivo_esquemas_clientes_fusionadores <-
  paste0(ruta_dependencias, "/fusionar_bases/relacion_esquemas_clientes_fusionadores.xlsx")

# Ruta a la carpeta que contiene la aplicación de Web2py que contiene los clientes y
# fusionadores nombrados como en el archivo anterior.
ruta_web2py <- paste0(ruta_dependencias, "/fusionar_bases/web2py")

### Pasarlo a YAML para que se pueda leer tanto de R como de python.


