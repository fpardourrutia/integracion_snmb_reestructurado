# La siguiente función genera la lista de id's de muestras de conglomerado a
# eliminar de una base de datos SQLite para los esquemas v13-v14
# (es decir, para el cliente de captura v5).

# Los requerimientos para estas funciones se pueden ver en los comentarios a
# "funciones_integracion::eliminar_muestras_duplicadas()"

# Esta función considerará que si hay duplicados, las muestras de conglomerado a
# eliminar son las que tienen menos registros asociados en las tablas:
# - "Archivo_camara"
# - "Archivo_grabadora"
# - "Archivo_huella_excreta"
# - "Archivo_especie_invasora"

# También eliminará los muestreos de conglomerado que ya fueron insertados
# con anterioridad a la base Postgres (revisando la llave (nombre, fecha_visita)).

# La función regresa una lista con los id's de los conglomerados a eliminar
# (en la base SQLite).

encontrar_duplicados_v13_14 <- function(conexion_sqlite, conexion_postgres){
  
  ################################
  # Obteniendo tablas de interés:
  ################################
  
  Conglomerado_muestra <- tbl(conexion_sqlite, "Conglomerado_muestra")
  Sitio_muestra <- tbl(conexion_sqlite, "Sitio_muestra")
  Camara <- tbl(conexion_sqlite, "Camara")
  Grabadora <- tbl(conexion_sqlite, "Grabadora")
  Archivo_camara <- tbl(conexion_sqlite, "Archivo_camara")
  Archivo_grabadora <- tbl(conexion_sqlite, "Archivo_grabadora")
  Transecto_muestra <- tbl(conexion_sqlite, "Transecto_muestra")
  Especie_invasora <- tbl(conexion_sqlite, "Especie_invasora")
  Huella_excreta <- tbl(conexion_sqlite, "Huella_excreta")
  Archivo_especie_invasora <- tbl(conexion_sqlite, "Archivo_especie_invasora")
  Archivo_huella_excreta <- tbl(conexion_sqlite, "Archivo_huella_excreta")
  
  Conglomerado_muestra_postgres <- tbl(conexion_postgres, "Conglomerado_muestra")
  
  #############################################################################
  # Calculando cantidad de archivos por muestreo registrado en la base SQLite:
  #############################################################################
  
  ### Archivos camara

  cantidad_archivos_camara_muestra <- Conglomerado_muestra %>%
    select(
      conglomerado_muestra_id = id,
      nombre,
      fecha_visita
    ) %>%
    inner_join(Sitio_muestra %>%
        select(
          sitio_muestra_id = id,
          conglomerado_muestra_id
        ), by = "conglomerado_muestra_id") %>%
    inner_join(Camara %>%
        select(
          camara_id = id,
          sitio_muestra_id
        ), by = "sitio_muestra_id") %>%
    inner_join(Archivo_camara %>%
        select(
          archivo_camara_id = id,
          camara_id
        ), by = "camara_id"
    ) %>%
    group_by(conglomerado_muestra_id) %>%
    tally() %>%
    rbind(
      # Agregando registros no tomados en cuenta porque no tienen
      # archivos asociados: notar que si un registros de muestra de conglomerado
      # no tiene registros asociados en cualquier tabla considerada en el join
      # anterior, se elimina por el funcionamiento del inner_join
      Conglomerado_muestra %>%
        select(conglomerado_muestra_id = id) %>%
        anti_join(., by = "conglomerado_muestra_id") %>%
        mutate(
          n = 0
        )
    )
  
  ### Archivos grabadora

  cantidad_archivos_grabadora_muestra <- Conglomerado_muestra %>%
    select(
      conglomerado_muestra_id = id,
      nombre,
      fecha_visita
    ) %>%
    inner_join(Sitio_muestra %>%
        select(
          sitio_muestra_id = id,
          conglomerado_muestra_id
        ), by = "conglomerado_muestra_id") %>%
    inner_join(Grabadora %>%
        select(
          grabadora_id = id,
          sitio_muestra_id
        ), by = "sitio_muestra_id") %>%
    inner_join(Archivo_grabadora %>%
        select(
          archivo_grabadora_id = id,
          grabadora_id
        ), by = "grabadora_id"
    ) %>%
    group_by(conglomerado_muestra_id) %>%
    tally() %>%
    rbind(
      # Agregando registros no tomados en cuenta porque no tienen
      # archivos asociados
      Conglomerado_muestra %>%
        select(conglomerado_muestra_id = id) %>%
        anti_join(., by = "conglomerado_muestra_id") %>%
        mutate(
          n = 0
        )
    )
  
  ### Archivos especies invasoras

  cantidad_archivos_especies_invasoras_muestra <- Conglomerado_muestra %>%
    select(
      conglomerado_muestra_id = id,
      nombre,
      fecha_visita
    ) %>%
    inner_join(Transecto_muestra %>%
        select(
          transecto_muestra_id = id,
          conglomerado_muestra_id
        ), by = "conglomerado_muestra_id") %>%
    inner_join(Especie_invasora %>%
        select(
          especie_invasora_id = id,
          transecto_muestra_id
        ), by = "transecto_muestra_id") %>%
    inner_join(Archivo_especie_invasora %>%
        select(
          archivo_especie_invasora_id = id,
          especie_invasora_id
        ), by = "especie_invasora_id"
    ) %>%
    group_by(conglomerado_muestra_id) %>%
    tally() %>%
    rbind(
      # Agregando registros no tomados en cuenta porque no tienen
      # archivos asociados
      Conglomerado_muestra %>%
        select(conglomerado_muestra_id = id) %>%
        anti_join(., by = "conglomerado_muestra_id") %>%
        mutate(
          n = 0
        )
    )
  
  ### Archivos Huellas Excretas

  cantidad_archivos_huellas_excretas_muestra <- Conglomerado_muestra %>%
    select(
      conglomerado_muestra_id = id,
      nombre,
      fecha_visita
    ) %>%
    inner_join(Transecto_muestra %>%
        select(
          transecto_muestra_id = id,
          conglomerado_muestra_id
        ), by = "conglomerado_muestra_id") %>%
    inner_join(Huella_excreta %>%
        select(
          huella_excreta_id = id,
          transecto_muestra_id
        ), by = "transecto_muestra_id") %>%
    inner_join(Archivo_huella_excreta %>%
        select(
          archivo_huella_excreta_id = id,
          huella_excreta_id
        ), by = "huella_excreta_id"
    ) %>%
    group_by(conglomerado_muestra_id) %>%
    tally() %>%
    rbind(
      # Agregando registros no tomados en cuenta porque no tienen
      # archivos asociados
      Conglomerado_muestra %>%
        select(conglomerado_muestra_id = id) %>%
        anti_join(., by = "conglomerado_muestra_id") %>%
        mutate(
          n = 0
        )
    )
  
  #############################################################################################
  # Formando tabla con muestras de conglomerado que se preservarán en la base duplicada SQLite
  #############################################################################################
  
  seleccion_registros_muestras_conglomerado_sqlite <- rbind(
    cantidad_archivos_camara_muestra,
    cantidad_archivos_grabadora_muestra,
    cantidad_archivos_especies_invasoras_muestra,
    cantidad_archivos_huellas_excretas_muestrea
    ) %>%
    # Sumando cantidad de archivos por muestra de conglomerado registrada en la base SQLite:
    group_by(conglomerado_muestra_id) %>%
    summarise(
      total_archivos = sum(n)
    ) %>%
    # Agregando el nombre y la fecha de visita de la muestra de conglomerado a
    # la tabla anterior. Notar que la tabla anterior ya tiene uno y sólo un
    # registro correspondiente a cada id distinta.
    inner_join(
      Conglomerado_muestra %>%
        select(
          conglomerado_muestra_id = id,
          nombre,
          fecha_visita
        ), by = "conglomerado_muestra_id"
    ) %>%
    # Ordeno de manera descendente por total de archivos
    arrange(nombre, fecha_visita, desc(total_archivos)) %>%
    group_by(nombre, fecha_visita) %>%
    summarise(
      # Para cada muestreo de conglomerado, me quedo con la id del registro que
      # tuvo la mayor cantidad de registros asociados
      conglomerado_muestra_id = first(conglomerado_muestra_id)
    ) %>%
    
    # Eliminando las muestras de conglomerado que ya fueron registradas con
    # anterioridad en la base PostgreSQL:
    anti_join(Conglomerado_muestra_postgres, by = c("nombre", "fecha_visita"))
  
  #######################################################################
  # Creando vector con las id's de los registros a eliminar de la sqlite
  #######################################################################
  
  registros_eliminar_sqlite <- Conglomerado_muestra %>%
    anti_join(
      seleccion_registros_muestras_conglomerado_sqlite,
      by = c("id" = "conglomerado_muestra_id")
    ) %>%
    '$'(id)
  
  return(registros_eliminar_sqlite)
}

