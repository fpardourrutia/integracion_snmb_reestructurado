#!/usr/bin/env Rscript

# En este script se van llamado, en orden, las funciones definidas en
# "funciones_integracion.R", con el fin de llevar a cabo el proceso de integración,

args = commandArgs(trailingOnly=TRUE)
ruta_carpeta_entrada <- args[1]
ruta_carpeta_salida <- args[2]

revisar_esquemas(ruta_carpeta_entrada, ruta_carpeta_salida)
