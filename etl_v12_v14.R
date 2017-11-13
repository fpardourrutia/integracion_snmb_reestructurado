library("plyr")
library("dplyr")
library("tidyr")
library("forcats")
library("RPostgreSQL")
library("stringi")

# Este script leerá una base en la v12 y la migrará a la v14. Esto es útil puesto
# que la base final PostgreSQL tendrá que pasar por ese proceso.

conexion_entrada <- src_postgres(
  dbname = "snmb_development",
  host = "coati",
  port = "5432",
  user = "postgres",
  password = "000999000."
)

# Enlistando las tablas de la base v12, y eliminando tablas no requeridas.
# Cabe destacar que los catálogos no son requeridos puesto que se insertaron
# cuando se creó la base de datos con el esquema v14 (en Web2py), y sólo se
# agregaron catálogos y a los existentes campos; no hubo modificaciones
lista_nombres_tablas <- src_tbls(conexion_entrada) %>%
  data_frame(nombres_tablas = .) %>%
  filter(!(nombres_tablas %in% c(
    "spatial_ref_sys",
    "conglomerado_anp_cop13",
    "anp_agosto12gw",
    "dest_2012gw",
    "muni_2012gw",
    "metadata_raster",
    "metadata_vector",
    "taxonomia"
  ))) %>%
  filter(stri_detect_regex(nombres_tablas, "^cat_", negate = TRUE)) %>%
  filter(stri_detect_regex(nombres_tablas, "^auth_", negate = TRUE)) %>%
  '$'(nombres_tablas)

names(lista_nombres_tablas) <- lista_nombres_tablas

# Leyendo las tablas de interésy asignándolas a una lista nombrada:

lista_tablas <- llply(lista_nombres_tablas, function(nombre_tabla){
  tabla <- tbl(conexion_entrada, nombre_tabla) %>%
    collect(n = Inf)
  return(tabla)
})

################################################################################
# "Transecto_especies_invasoras_muestra" y "Transecto_huellas_excretas_muestra"
# -> "Transecto_muestra"
################################################################################

# En este paso los transectos de especies invasoras y huellas y excretas asociados
# al mismo muestreo de conglomerado, y con el mismo número, se pensarán como el
# mismo registro.

### Creando la tabla de "transecto_muestra"
# Pero preservando id's (y tablas de los que provienen) antiguos para reasignar
# id's de las tablas que apuntan a ellas (Especie_invasora y "Huella_excreta")
transecto_muestra_auxiliar <- lista_tablas$transecto_especies_invasoras_muestra %>%
  mutate(
    tabla_origen = "transecto_especies_invasoras_muestra",
    fecha = as.character(fecha)
  ) %>%
  rbind(
    lista_tablas$transecto_huellas_excretas_muestra %>%
      mutate(
        tabla_origen = "transecto_huellas_excretas_muestra",
        fecha = as.character(fecha)
      )
  ) %>%
  arrange(conglomerado_muestra_id, transecto_numero) %>%
  
  # Definiendo un único registro de "Transecto_muestra" para cada muestreo de
  # conglomerado, y preservo todas las id's de los transectos que lo originaron
  # (con la información de la tabla correspondiente)
  group_by(conglomerado_muestra_id, transecto_numero) %>%
  
  do(
    data_frame(
      
      # Creando columnas con las id's anteriores (y su tabla correspondiente) para
      # cada valor de "transecto_numero" en "conglomerado_muestra_id"
      
      tabla_origen = .$tabla_origen,
      id_anterior = .$id,
      
      # Calculando un valor único de los siguientes campos para cada combinación
      # de "conglomerado_muestra_id" y "transecto_numero":
      
      # Si encontré la combinación "conglomerado_muestra", "transecto_numero" en
      # la tabla, quiere decir que si hicieron el recorrido, y por tanto, que si
      # existe el transecto
      existe = "T",
      
      # Ordeno por fecha para que los NA's queden al final, y me quedo con el primero.
      # No funcionan los pipes dentro de un do.
      fecha = as.character(slice(select(arrange(., fecha), fecha), 1)),
      
      # Ordeno por fecha para que me queden los valores correspondientes al anterior
      hora_inicio = as.character(slice(select(arrange(., fecha), hora_inicio), 1)),
      
      hora_termino = as.character(slice(select(arrange(., fecha), hora_termino), 1)),
      
      tecnico = as.character(slice(select(arrange(., fecha), tecnico), 1)),
      
      comentario = as.character(slice(select(arrange(., fecha), comentario), 1))
    )
  ) %>%
  
  # No se agregaron los registros no encontrados como que no existen, porque no
  # tenemos la certeza de si existen y no se encontraron registros o en realidad
  # no existen.
  ungroup() %>%
  
  mutate(
    # Reasignando ID's
    id_nuevo = paste0(conglomerado_muestra_id, "_", transecto_numero) %>%
      # Para que los id's se asignen en el orden en que aparecen
      as_factor() %>%
      as.numeric()
  )


# transecto_muestra_auxiliar %>%
#   distinct(conglomerado_muestra_id, transecto_numero) %>%
#   nrow()
# 
# transecto_muestra_auxiliar %>%
#   distinct(existe, fecha, hora_inicio, hora_termino, tecnico, comentario) %>%
#   nrow()

# Perfecto: asigné exitosamente un único valor de existe, ..., comentario para
# cada combinación de conglomerado_muestra_id, transecto_numero

### Reasignando llaves foráneas de las tablas de "Especie_invasora" y "Huella_excreta":

# transecto_muestra_auxiliar %>%
#   filter(tabla_origen == "transecto_especies_invasoras_muestra") %>%
#   select(id_anterior) %>%
#   nrow()
# transecto_muestra_auxiliar %>%
#   filter(tabla_origen == "transecto_especies_invasoras_muestra") %>%
#   select(id_anterior) %>%
#   unique() %>%
#   nrow()

# transecto_muestra_auxiliar %>%
#   filter(tabla_origen == "transecto_huellas_excretas_muestra") %>%
#   select(id_anterior) %>%
#   nrow()
# transecto_muestra_auxiliar %>%
#   filter(tabla_origen == "transecto_huellas_excretas_muestra") %>%
#   select(id_anterior) %>%
#   unique() %>%
#   nrow()
# Perfecto: para cada "tabla_origen" las "id's_anteriores" son únicas:

especie_invasora_nueva <- lista_tablas$especie_invasora %>%
  inner_join(
    transecto_muestra_auxiliar %>%
      filter(tabla_origen == "transecto_especies_invasoras_muestra") %>%
      select(
        id_anterior,
        id_nuevo
      ),
    by = c("transecto_especies_invasoras_id" = "id_anterior")
  ) %>%
  rename(
    transecto_muestra_id = id_nuevo
  ) %>%
  select(-transecto_especies_invasoras_id)

huella_excreta_nueva <- lista_tablas$huella_excreta %>%
  inner_join(
    transecto_muestra_auxiliar %>%
      filter(tabla_origen == "transecto_huellas_excretas_muestra") %>%
      select(
        id_anterior,
        id_nuevo
      ),
    by = c("transecto_huellas_excretas_id" = "id_anterior")
  ) %>%
  rename(
    transecto_muestra_id = id_nuevo
  ) %>%
  select(-transecto_huellas_excretas_id)

# Finalmente, creando la tabla "Transecto_muestra":
transecto_muestra <- transecto_muestra_auxiliar %>%
  select(
    -tabla_origen,
    -id_anterior,
    id = id_nuevo
  ) %>%
  group_by(id) %>%
  summarise_all(first)

###################################################################################
# Archivo_conteo_ave -> Archivo_avistamiento_aves
###################################################################################

archivo_avistamiento_aves <- lista_tablas$archivo_conteo_ave %>%
  rename(
    avistamiento_aves_id = conteo_ave_id
  )

###################################################################################
# Arbol_cuadrante
###################################################################################

# Los árboles que tienen algún valor en el campo "Existe", fueron tomados con el
# protocolo de 8 árboles por sitio. Los demás, fueron censos por sitio.
arbol_cuadrante_nuevo <- lista_tablas$arbol_cuadrante %>%
  mutate(
    diametro_normal = as.character(diametro_normal),
    cambios = "",
    forma_vida = ""
  )

###########################################################################################
# Actualizando la lista de tablas a insertar
###########################################################################################

lista_tablas_insertar <- lista_tablas

# "Transecto_muestra" y asociados
lista_tablas_insertar$transecto_especies_invasoras_muestra <- NULL
lista_tablas_insertar$transecto_huellas_excretas_muestra <- NULL
lista_tablas_insertar$transecto_muestra <- transecto_muestra
lista_tablas_insertar$especie_invasora <- especie_invasora_nueva
lista_tablas_insertar$huella_excreta <- huella_excreta_nueva

# "Avistamiento_aves" y asociados:
lista_tablas_insertar$conteo_ave <- NULL
lista_tablas_insertar$archivo_conteo_ave <- NULL
lista_tablas_insertar$avistamiento_aves <- lista_tablas$conteo_ave
lista_tablas_insertar$archivo_avistamiento_aves <- archivo_avistamiento_aves

# "Arbol_cuadrante"
lista_tablas_insertar$arbol_cuadrante <- arbol_cuadrante_nuevo

# Especificando el nuevo orden de la lista (para insertar las tablas en orden
# y que no se violen restricciones de llaves foráneas)

orden_nuevo_tablas <- c(
  "conglomerado_muestra",
  "sitio_muestra",
  "imagen_referencia_sitio",
  
  "camara",
  "archivo_camara",
  "imagen_referencia_camara",
  
  "grabadora",
  "archivo_grabadora",
  "archivo_grabadora_info",
  "archivo_referencia_grabadora",
  "imagen_referencia_grabadora",
  "imagen_referencia_microfonos",
  
  "transecto_muestra",
  "especie_invasora",
  "archivo_especie_invasora",
  "huella_excreta",
  "archivo_huella_excreta",
  
  "especie_invasora_extra",
  "archivo_especie_invasora_extra",
  
  "huella_excreta_extra",
  "archivo_huella_excreta_extra",
  
  "especimen_restos_extra",
  "archivo_especimen_restos_extra",
  
  "punto_conteo_aves",
  "avistamiento_aves",
  "archivo_avistamiento_aves",
  
  "arbol_cuadrante",
  "transecto_ramas",
  "rama_1000h",
  "arbol_transecto",
  
  "informacion_epifitas",
  "punto_carbono",
  
  "incendio",
  "archivo_incendio",
  "plaga",
  "archivo_plaga",
  "impacto_actual"
  
  #"archivo_csv"
)

lista_tablas_insertar_ordenada <- lista_tablas_insertar[orden_nuevo_tablas]

###########################################################################################
# Introduciendo las nuevas tablas a la base PostgreSQL (con el esquema v14 ya implementado)
###########################################################################################

driver <- dbDriver("PostgreSQL")
base_output <- dbConnect(
  drv = driver,
  dbname = "snmb_testing_v14",
  port = 5432,
  host = "buho", 
  user = "postgres",
  password = "000999000")

# Insertando tablas en el esquema v14

l_ply(1:length(lista_tablas_insertar_ordenada), function(i){
  dbWriteTable(
    base_output,
    names(lista_tablas_insertar_ordenada)[i],
    as.data.frame(lista_tablas_insertar_ordenada[[i]]),
    overwrite = FALSE, append = TRUE, row.names = 0)
  print(names(lista_tablas_insertar_ordenada)[i])
})

# Actualizando secuencias de llaves autogeneradas:
l_ply(1:length(lista_tablas_insertar_ordenada), function(i){
  # Creando el query
  
  nombre_tabla <- names(lista_tablas_insertar_ordenada)[i]
  query <- paste0("SELECT setval('", nombre_tabla,
    "_id_seq', (SELECT MAX(id) FROM ",
    nombre_tabla,
    "));"
    )
  
  # Enviando el query a la base de datos PostgreSQL
  dbGetQuery(base_output, query)
  print(nombre_tabla)
})

dbDisconnect(base_output)






