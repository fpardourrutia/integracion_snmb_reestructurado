##### Ruta crítica:

# 1. Copiar las bases de datos de una carpeta en LUSTRE a una externa, con el fin
# de poder acceder a ellas. De cada base copiada, revisar el esquema / versión del
# ncliente, etc... para saber qué versiones de las herramientas usar para el
# proceso de integración.
# 3. Crear manualmente carpetas de bases de datos que utilizarán las mismas
# herramientas. Esto es manual, puesto que otorga mayor flexibilidad en casos
# extremos (por ejemplo, no sabemos cómo vendrán los datos que entregará Belinda
# de CONAFOR).
# 4. Fusionar cada base de datos en la carpeta especificada, y enviar la base fusionada
# a una carpeta especificada (posiblemente una subcarpeta de la anterior).
# 5. Enviar una copia de la base de datos a una carpeta específica, y eliminar los
# duplicados de esta última.

################################################################################

library("RSQLite")
library("RPostgreSQL")
library("plyr")
library("dplyr")
library("readr")
library("readxl")

# Leyendo parámeteros de configuración
#source("config.R")

# Leyendo dependencias por medio de una búsqueda recursiva en la sección de
# "dependencias"

#list.files(ruta_dependencias, recursive = TRUE, full.names = TRUE, pattern = ".R$") %>%
#  l_ply(source)

################################################################################

# La siguiente función revisa la versión del cliente de captura y del esquema
# de una base de datos sqlite del SNMB.
# ruta_base: ruta de la base de datos sqlite de interés
# resultado de src_sqlite(ruta_base), src_postgres() o src_mysql()
# La función regresa un data frame  que contiene la ruta de la base de datos,
# y las versiones del cliente y del esquema correspondientes.

# Esta función no tiene dependencias externas, ya que para usar éstas se requiere
# de saber la versión del esquema de determinada base de datos.

revisar_esquema <- function(ruta_base){
  
  conexion_bd <- src_sqlite(ruta_base)
  tablas_bd <- src_tbls(conexion_bd)
  
  # Revisando si la base de datos contiene la tabla "Informacion_epifitas"
  if("Informacion_epifitas" %in% tablas_bd){
    columnas_tabla_informacion_epifitas <- colnames(tbl(conexion_bd, "Informacion_epifitas"))
  } else{
    columnas_tabla_informacion_epifitas <- NULL
  }

  if("Transecto_muestra" %in% tablas_bd){
    version_cliente <- 5
    if("Muestreo_plagas" %in% tablas_bd){
      version_esquema <- 13
      informacion_adicional <- NA
    } else{
      version_esquema <- 14
      informacion_adicional <- NA
    }
  } else if("conglomerado_muestra_id" %in% columnas_tabla_informacion_epifitas){
    version_cliente <- 4
    version_esquema <- 12
    informacion_adicional <- NA
  } else if("sitio_muestra_id" %in% columnas_tabla_informacion_epifitas){
    version_cliente <- 3
    version_esquema <- 10
    if("Cat_conabio_aves" %in% tablas_bd){
      informacion_adicional <- "SAR-MOD"
    } else{
      informacion_adicional <- "SAC-MOD"
    }
  } else{
    # no es una base de datos generada por el cliente de captura.
    version_cliente <- NA
    version_esquema <- NA
    informacion_adicional <- NA
  }

  return(
    data_frame(
      ruta = ruta_base,
      version_cliente = version_cliente,
      version_esquema = version_esquema,
      informacion_adicional = informacion_adicional
    )
  )
}

################################################################################

# La siguiente función sirve para revisar las versiones del cliente y del esquema
# para todas las bases con terminación ".sqlite" dentro de una carpeta:
# ruta_carpeta_entrada: la ruta hacia una carpeta que contiene archivos con
# terminación ".sqlite"
# ruta_carpeta_salida: la ruta hacia una carpeta donde se guardarán las bases
# con el fin de poder acceder a ellas (no en LUSTRE)

# La función:
# 1. Copia los archivos con terminación ".sqlite" que se encuentran en una carpeta
# de entrada (posiblemente dentro de subcarpetas) a una carpeta de salida.
# 2. Crea un CSV que contiene la siguiente información:
#   - ruta_entrada
#   - ruta_salida
#   - version_cliente
#   - version_esquema

# Dependencias:
# revisar_esquema()

# prueba:
#Rscript script.R "~/Desktop" "~/Desktop/conabio/revisar_bd_sqlite/prueba_mover_bd/"

revisar_esquemas <- function(ruta_carpeta_entrada, ruta_carpeta_salida){
  
  # Obteniendo las rutas de cada base en la carpeta de entrada
  rutas_bases_sqlite <- list.files(
    ruta_carpeta_entrada,
    pattern = ".sqlite$",
    recursive = TRUE,
    full.names = TRUE
  )
  
  # Creando data frame que expresa la relación entre "ruta_entrada" y "ruta_salida"
  mapeo_rutas_entrada_salida <- data_frame(
    ruta_entrada = rutas_bases_sqlite
  ) %>%
    mutate(
      ruta_salida = paste0(ruta_carpeta_salida, "/storage_", 1:nrow(.), ".sqlite")
    )
  
  # Creando el código de Bash para realizar la migración de bases
  codigo_bash <- mapeo_rutas_entrada_salida %>%
    mutate(
      codigo = paste0('cp ', ruta_entrada, ' ', ruta_salida, '')
    ) %>%
    '$'(codigo) 
  
  # Corriendo cada comando de Bash:
  l_ply(codigo_bash, system)
  
  # Corriendo la función "revisar_esquema()" para todas las "rutas_salida" para
  # ver el esquema de cada base en la carpeta de salida.
  revision_esquemas_carpeta_salida <-ldply(
    mapeo_rutas_entrada_salida$ruta_salida, function(ruta){
      revisar_esquema(ruta)
    })
  
  # Generando el data frame resumen:
  df_resumen <- mapeo_rutas_entrada_salida %>%
    inner_join(revision_esquemas_carpeta_salida, by = c("ruta_salida" = "ruta"))
  
  # Guardando el data frame resumen en un CSV
  write_csv(df_resumen, paste0(ruta_carpeta_salida, "/resumen_migracion.csv"))
}

################################################################################

# La siguiente función toma todas las bases de datos en una misma carpeta, revisa
# que tengan exactamente las mismas especificaciones y en caso afirmativo, procede
# a fusionarlas utilizando el cliente y fusionador correspondientes.

# Entradas:
# ruta_carpeta_entrada: ruta a la carpeta de entrada que contiene las bases de
# datos a fusionar.
# ruta_base_salida: nombre y ruta del archivo que contendrá la base de datos
# fusionada.
# ruta_archivo_excel: nombre y ruta del archivo de Excel que contiene la información
# de clientes y fusionadores asociada a cada tipo de base de datos (por default se
# utiliza el valor en "config.R")
# ruta_web2py: nombre y ruta hacia la carpeta de Web2py que contiene las aplicaciones
# instaladas (por default se utiliza el valor en "config.R")

# Salidas:
# Base SQLite fusionada, con el nombre y ruta como especificadas en
# "ruta_base_fusionada"

# Dependencias:
# - "fusionar_bases/conglomerados_fototrampa.xlsx". Este archivo especifica qué
# cliente de captura y fusionador corresponden a qué base de datos.

# - "fusionar_bases/web2py". Web2py (modo desarrollador) que tiene
# instaladas todas las aplicaciones de cliente y fusionador enlistadas en el
# archivo: "fusionar_bases/conglomerados_fototrampa.xlsx" (con nombres idénticos)

fusionar_bases <- function(ruta_carpeta_entrada, ruta_base_salida,
  ruta_archivo_excel = ruta_archivo_esquemas_clientes_fusionadores,
  ruta_web2py = ruta_web2py){

  # Leyendo información de clientes y fusionadores del archivo de excel:
  informacion_clientes_fusionadores <- read_excel(ruta_archivo_excel)
  
  # Obteniendo las rutas de cada base en la carpeta de entrada
  rutas_bases_sqlite <- list.files(
    ruta_carpeta_entrada,
    pattern = ".sqlite$",
    full.names = TRUE
  )
  
  if(length(rutas_bases_sqlite) == 0){
    stop("La carpeta especificada no contiene archivos con terminación .sqlite")
  }
  
  # Revisando que todas las bases en dicha carpeta correspondan al mismo cliente
  # y fusionador. Si este no es el caso, enviar un mensaje de error.
  revision_esquemas <- ldply(rutas_bases_sqlite, function(ruta){
      conexion_bd <- src_sqlite(ruta)
      informacion_esquema_bd <- revisar_esquema(conexion_bd)
      informacion_cliente_fusionador_bd <- informacion_esquema_bd %>%
        inner_join(informacion_clientes_fusionadores,
          by = c("version_cliente", "version_esquema", "informacion_adicional")
        ) %>%
        select(
          cliente_captura_correspondiente,
          fusionador_correspondiente
        )
      
      return(informacion_cliente_fusionador_bd)
    }) %>%
    # Quedándonos sólo con las distintas combinaciones de cliente de captura y 
    distinct()
  
  if(nrow(revision_esquemas) > 1){
    stop("Las bases de datos son de distintos tipos, por lo que no pueden ser fusionadas")
  }
  
  ### Finalmente, fusionando utilizando el (único) fusionador y cliente de captura
  ### correspondiente para dichas bases:
  
  # Creando ruta al cliente de captura y fusionador adecuados:
  ruta_cliente <- paste0(
    ruta_web2py,
    "/applications/",
    revision_esquemas$cliente_captura_correspondiente)
  
  ruta_fusionador <- paste0(
    ruta_web2py,
    "/applications/",
    revision_esquemas$fusionador_correspondiente)
  
  #
  
  
  
  
    
    
    
    
  
  
  
  
  
}

################################################################################

# La siguiente función duplica una base de datos SQLite (correspondiente a la
# base fusionada de una entrega) y elimina muestras de conglomerado repetidas
# (mismo nombre y fecha de visita). Los repetidos pueden ser de dos tipos:
#
# 1. Muestras repetidas en la misma base de datos SQLite
# 2. Muestras que ya fueron integrados a la base de datos PostgreSQL con
# anterioridad

# Los criterios para decidir entre dos muestras de conglomerado repetidas están
# especificados en la carpeta de "dependencias/eliminar_muestras_duplicadas",
# dependen de la versión del esquema de la base de datos SQLite, y por lo general
# tienen que ver con cantidad de registros de cámara, grabadora, imágenes de
# especies invasoras y huellas/excretas.

# Entradas:
# ruta_base_sqlite: ruta a la base SQLite que se duplicará y de la que se
# eliminarán repetidos.
# ruta_carpeta_destino: ruta de la carpeta en la que se guardará la copia de la
# base SQLite, así como el archivo con las id's de los renglones eliminados.
# nombre_base_destino: nombre del archivo correspondiente a la base de datos
# duplicada.
# Parámetros de conexión a la base de datos PostgreSQL:
# nombre_base_postgres, servidor, puerto, usuario, contrasena.

# Salidas:
# Además de la base de datos SQLite de interés copiada en "ruta_carpeta_destino",
# nombrada "nombre_base_destino" y sin duplicados, un archivo que enlista los id's
# de los conglomerados duplicados en dicha base.

# Dependencias:
# 1. revisar_esquema()
# 2. Cualquier función en "dependencias/eliminar_muestras_duplicadas", las cuáles
# deben ser invocadas en el cuerpo de "eliminar_muestras_duplicadas()"
# Cada una de estas funciones deben aceptar el objeto de conexion de la base de
# datos SQLite y el objeto de conexión de la base de datos PostgreSQL.
# Estas funciones deben regresar un vector con los id's de los conglomerados a
# eliminar.

eliminar_muestras_duplicadas <- function(ruta_base_sqlite, ruta_carpeta_destino,
  nombre_base_destino, nombre_base_postgres, servidor, puerto, usuario, contrasena){
  
  ruta_base_destino <- paste0(ruta_carpeta_destino, "/", nombre_base_destino)
  
  # Copiando la base de datos SQLite a la nueva carpeta.
  file.copy(ruta_base_sqlite, ruta_base_destino)
  
  # Conectándonos a la copia de la base de datos para hacerle las modificaciones
  # necesarias:
  conexion_sqlite <- src_sqlite(ruta_base_destino)
  
  # Y a la Postgres:
  conexion_postgres <- src_postgres(
    dbname = nombre_base_postgres,
    host = servidor,
    port = puerto,
    user = usuario,
    password = contrasena)
  
  # Encontrando el esquema de la base de datos SQLite de interés, con el fin de
  # saber cómo se revisarán los datos
  version_esquema <- revisar_esquema(conexion_sqlite)$version_esquema
  
  # Obteniendo las listas de registros a eliminar de la base SQLite duplicada:
  
  ####################################################################################
  # En esta sección  se inserta el código que depende del esquema de la base utilizado
  ####################################################################################
  
  if(!is.na(version_esquema)){
    
    if(version_esquema <= 12){
      
      lista_ids_conglomerado_muestra_eliminar <-
        encontrar_duplicados_v10_v12(conexion_sqlite, conexion_postgres)
      
    } else if(version_esquema == 13 | version_esquema == 14){
      
      lista_ids_conglomerado_muestra_eliminar <-
        encontrar_duplicados_v13_v14(conexion_sqlite, conexion_postgres)
    } else{
      stop("La base de datos no cuenta con un esquema soportado")
    }
    
    # Activando llaves foráneas para eliminación en cascada de registros en la SQLite
    dbSendQuery(conexion_sqlite, "PRAGMA foreign_keys = ON;")
    
    # Si hay registros para eliminar, eliminarlos:
    if(length(lista_ids_conglomerado_muestra_eliminar > 0)){
      
      query <- paste0("DELETE FROM Conglomerado_muestra WHERE id IN (",
        paste0(lista_ids_conglomerado_muestra_eliminar, collapse = ", "), ");")
      dbSendQuery(conexion_sqlite, query)
    }
    
    # Generando archivo de renglones eliminados:
    ruta_archivo_resumen <- paste0(ruta_carpeta_destino, "/ids_eliminados.txt")
    write.table(x = ids_eliminar, file = ruta_archivo_resumen, quote = FALSE, 
      row.names = FALSE, col.names = FALSE)
  } else{
    stop("La base de datos no cuenta con un esquema soportado")
  }
}