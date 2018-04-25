# -*- coding: utf-8 -*-
import os

def index():

	# Creando una forma para que se suban los archivos CSV múltiples,
	# que contienen la información de cada base de datos enviada a CONAFOR

	Campos_forma = [
		INPUT(_name='archivos_csv', _type='file', requires=IS_NOT_EMPTY(), multiple=True),
	]
	
	forma = FORM(*Campos_forma)
	
	if forma.accepts(request.vars, formname='formaHTML'):
		
################Procesando los archivos múltiples###############################
		
		archivos = forma.vars['archivos_csv']
		if not isinstance(archivos, list):
			
			archivos = [archivos]
			
		for aux in archivos:
			
			# Guardando el archivo en la carpeta adecuada
			archivoCSV = db.Archivo_csv.archivo.store(aux, aux.filename)
			
			datosArchivoCSV = {}
			datosArchivoCSV['archivo'] = archivoCSV
			datosArchivoCSV['archivo_nombre_original'] = aux.filename
		
			# Insertando el registro en la base de datos:
			
			db.Archivo_csv.insert(**datosArchivoCSV)
			
			# Definiendo el nombre del archivo
			nombre_archivo = os.path.join(request.folder,'uploads',archivoCSV)

			# Abriéndolo en modo de lectura
			archivo = open(nombre_archivo,'r')
			# Leyendo el archivo como una lista de renglones
			contenido_archivo_original = archivo.readlines()
			# Cerrando el archivo
			archivo.close()

			# Sustituyendo en la lista anterior los nombres de las tablas
			# inutilizadas en el cliente v5 del SAC-MOD a su versión más reciente
			# en el SAR-MOD, ya que tanto "map_tablenames" como "ignore_missing_tables"
			# no sirven en "import_from_csv_file()"

			# Abriendo el archivo en modo de escritura con reemplazo:
			archivo = open(nombre_archivo,'w')

			dic_sust = {
				"TABLE Transecto_arboles\r\r\n": "TABLE Cat_forma_vida_arboles_grandes\r\r\n",
				"TABLE Muestreo_plagas\r\r\n": "TABLE Cat_cambios_arboles_grandes\r\r\n",
				"TABLE Transecto_arboles\r\n": "TABLE Cat_forma_vida_arboles_grandes\r\n",
				"TABLE Muestreo_plagas\r\n": "TABLE Cat_cambios_arboles_grandes\r\n"
			}

			contenido_archivo_nuevo = [dic_sust[n] if n in dic_sust else n for n in contenido_archivo_original]

			# Guardando el contenido  nuevo en el archivo para poder trabajar con él.
			for renglon in contenido_archivo_nuevo:
				archivo.write(renglon)

			# Cerrando el archivo y abriéndolo en modo de lectura de nuevo.
			archivo.close()
			archivo = open(nombre_archivo,'r')

			# Importando el contenido del archivo en la BD
			db.import_from_csv_file(archivo)

			# Cerrando archivo
			archivo.close()


		# Borrando los catálogos al terminar de insertar, ya que se replican con
		# cada inserción.

		db(db.Version_cliente).delete()
		db(db.Cat_tipo_conglomerado).delete()
		db(db.Cat_estado_conglomerado).delete()
		db(db.Cat_tenencia_conglomerado).delete()
		db(db.Cat_suelo_conglomerado).delete()
		db(db.Cat_vegetacion_conglomerado).delete()
		db(db.Cat_numero_sitio).delete()
		db(db.Cat_elipsoide).delete()
		db(db.Cat_resolucion_camara).delete()
		db(db.Cat_sensibilidad_camara).delete()
		db(db.Cat_condiciones_ambientales).delete()
		db(db.Cat_numero_transecto).delete()
		db(db.Cat_numero_individuos).delete()
		db(db.Cat_conabio_invasoras).delete()
		db(db.Cat_municipio_conglomerado).delete()

		######Exclusivos de CONANP
		db(db.Cat_material_carbono).delete()
		db(db.Cat_grado_carbono).delete()
		db(db.Cat_transecto_direccion).delete()
		db(db.Cat_forma_vida).delete()
		db(db.Cat_forma_vida_arboles_grandes).delete()
		db(db.Cat_cambios_arboles_grandes).delete()
		db(db.Cat_tipo_impacto).delete()
		db(db.Cat_severidad_impactos).delete()
		db(db.Cat_agente_impactos).delete()
		db(db.Cat_estatus_impactos).delete()
		db(db.Cat_prop_afectacion).delete()
		db(db.Cat_incendio).delete()
		db(db.Cat_conabio_aves).delete()

		# Llenando los catálogos después de borrarlos

		##########################################################################
		## Versión del cliente
		########################################################################

		if db(db.Version_cliente.id>0).count() == 0:
			db.Version_cliente.insert(v='5')

		##########################################################################
		## Pestaña Conglomerado
		########################################################################

		if db(db.Cat_tipo_conglomerado.id>0).count() == 0:
			db.Cat_tipo_conglomerado.insert(nombre='1 Inicial')
			db.Cat_tipo_conglomerado.insert(nombre='2 Reemplazo')
			db.Cat_tipo_conglomerado.insert(nombre='3 Inaccesible terreno/clima')
			db.Cat_tipo_conglomerado.insert(nombre='4 Inaccesible social')
			db.Cat_tipo_conglomerado.insert(nombre='5 Inaccesible gabinete')
			db.Cat_tipo_conglomerado.insert(nombre='6 Supervisión interna')
			db.Cat_tipo_conglomerado.insert(nombre='7 Biodiversidad')
			db.Cat_tipo_conglomerado.insert(nombre='7 Biodiversidad (remuestreo)')

		#########################################################################

		if db(db.Cat_estado_conglomerado.id>0).count() == 0:
			db.Cat_estado_conglomerado.insert(clave_ent='1', nombre='Aguascalientes')
			db.Cat_estado_conglomerado.insert(clave_ent='2', nombre='Baja California')
			db.Cat_estado_conglomerado.insert(clave_ent='3', nombre='Baja California Sur')
			db.Cat_estado_conglomerado.insert(clave_ent='4', nombre='Campeche')
			db.Cat_estado_conglomerado.insert(clave_ent='5', nombre='Coahuila')
			db.Cat_estado_conglomerado.insert(clave_ent='6', nombre='Colima')
			db.Cat_estado_conglomerado.insert(clave_ent='7', nombre='Chiapas')
			db.Cat_estado_conglomerado.insert(clave_ent='8', nombre='Chihuahua')
			db.Cat_estado_conglomerado.insert(clave_ent='9', nombre='Distrito Federal')
			db.Cat_estado_conglomerado.insert(clave_ent='10', nombre='Durango')
			db.Cat_estado_conglomerado.insert(clave_ent='11', nombre='Guanajuato')
			db.Cat_estado_conglomerado.insert(clave_ent='12', nombre='Guerrero')
			db.Cat_estado_conglomerado.insert(clave_ent='13', nombre='Hidalgo')
			db.Cat_estado_conglomerado.insert(clave_ent='14', nombre='Jalisco')
			db.Cat_estado_conglomerado.insert(clave_ent='15', nombre='México')
			db.Cat_estado_conglomerado.insert(clave_ent='16', nombre='Michoacán')
			db.Cat_estado_conglomerado.insert(clave_ent='17', nombre='Morelos')
			db.Cat_estado_conglomerado.insert(clave_ent='18', nombre='Nayarit')
			db.Cat_estado_conglomerado.insert(clave_ent='19', nombre='Nuevo León')
			db.Cat_estado_conglomerado.insert(clave_ent='20', nombre='Oaxaca')
			db.Cat_estado_conglomerado.insert(clave_ent='21', nombre='Puebla')
			db.Cat_estado_conglomerado.insert(clave_ent='22', nombre='Querétaro')
			db.Cat_estado_conglomerado.insert(clave_ent='23', nombre='Quintana Roo')
			db.Cat_estado_conglomerado.insert(clave_ent='24', nombre='San Luis Potosí')
			db.Cat_estado_conglomerado.insert(clave_ent='25', nombre='Sinaloa')
			db.Cat_estado_conglomerado.insert(clave_ent='26', nombre='Sonora')
			db.Cat_estado_conglomerado.insert(clave_ent='27', nombre='Tabasco')
			db.Cat_estado_conglomerado.insert(clave_ent='28', nombre='Tamaulipas')
			db.Cat_estado_conglomerado.insert(clave_ent='29', nombre='Tlaxcala')
			db.Cat_estado_conglomerado.insert(clave_ent='30', nombre='Veracruz')
			db.Cat_estado_conglomerado.insert(clave_ent='31', nombre='Yucatán')
			db.Cat_estado_conglomerado.insert(clave_ent='32', nombre='Zacatecas') 

		#########################################################################

		if db(db.Cat_tenencia_conglomerado.id>0).count() == 0:
			db.Cat_tenencia_conglomerado.insert(nombre='1 Ejidal')
			db.Cat_tenencia_conglomerado.insert(nombre='2 Comunal')
			db.Cat_tenencia_conglomerado.insert(nombre='3 Propiedad particular')
			db.Cat_tenencia_conglomerado.insert(nombre='4 Propiedad federal')


		#########################################################################

		if db(db.Cat_suelo_conglomerado.id>0).count() == 0:
			db.Cat_suelo_conglomerado.insert(nombre='ACUI - Acuicola')
			db.Cat_suelo_conglomerado.insert(nombre='H - Agricultura de humedad')
			db.Cat_suelo_conglomerado.insert(nombre='R - Agricultura de riego')
			db.Cat_suelo_conglomerado.insert(nombre='T - Agricultura de temporal')
			db.Cat_suelo_conglomerado.insert(nombre='AH - Asentamiento humano')
			db.Cat_suelo_conglomerado.insert(nombre='H2O - Cuerpo de agua')
			db.Cat_suelo_conglomerado.insert(nombre='ADV - Desprovisto de vegetación')
			db.Cat_suelo_conglomerado.insert(nombre='PC - Pastizal cultivado')
			db.Cat_suelo_conglomerado.insert(nombre='PI - Pastizal inducido')
			db.Cat_suelo_conglomerado.insert(nombre='DV - Sin vegetación aparente')
			db.Cat_suelo_conglomerado.insert(nombre='ZU - Zona urbana')

			db.Cat_suelo_conglomerado.insert(nombre='Vegetación')
			db.Cat_suelo_conglomerado.insert(nombre='Otros')


		#########################################################################

		if db(db.Cat_vegetacion_conglomerado.id>0).count() == 0:
			db.Cat_vegetacion_conglomerado.insert(nombre='BC - Bosque Cultivado')
			db.Cat_vegetacion_conglomerado.insert(nombre='BS - Bosque de Ayarín')
			db.Cat_vegetacion_conglomerado.insert(nombre='BB - Bosque de Cedro')
			db.Cat_vegetacion_conglomerado.insert(nombre='BQ - Bosque de Encino')
			db.Cat_vegetacion_conglomerado.insert(nombre='BQP - Bosque de Encino-Pino')
			db.Cat_vegetacion_conglomerado.insert(nombre='BPQ - Bosque de Pino-Encino')
			db.Cat_vegetacion_conglomerado.insert(nombre='BG - Bosque de Galería')
			db.Cat_vegetacion_conglomerado.insert(nombre='MK - Bosque de Mezquite')
			db.Cat_vegetacion_conglomerado.insert(nombre='BA - Bosque de Oyamel')
			db.Cat_vegetacion_conglomerado.insert(nombre='BP - Bosque de Pino')
			db.Cat_vegetacion_conglomerado.insert(nombre='BJ - Bosque de Tascate')
			db.Cat_vegetacion_conglomerado.insert(nombre='BI - Bosque Inducido')
			db.Cat_vegetacion_conglomerado.insert(nombre='BM - Bosque Mesófilo de Montaña')
			db.Cat_vegetacion_conglomerado.insert(nombre='ML - Chaparral')
			db.Cat_vegetacion_conglomerado.insert(nombre='VM - Manglar')
			db.Cat_vegetacion_conglomerado.insert(nombre='MC - Matorral Crasicaule')
			db.Cat_vegetacion_conglomerado.insert(nombre='MJ - Matorral de Coníferas')
			db.Cat_vegetacion_conglomerado.insert(nombre='MDM - Matorral Desértico Micrófilo')
			db.Cat_vegetacion_conglomerado.insert(nombre='MDR - Matorral Desértico Rosetófilo')
			db.Cat_vegetacion_conglomerado.insert(nombre='MRC - Matorral Rosetófilo Costero')
			db.Cat_vegetacion_conglomerado.insert(nombre='MET - Matorral Espinoso Tamaulipeco')
			db.Cat_vegetacion_conglomerado.insert(nombre='MSCC - Matorral Sarco-cracicaule')
			db.Cat_vegetacion_conglomerado.insert(nombre='MSC - Matorral Sarcocaule')
			db.Cat_vegetacion_conglomerado.insert(nombre='MSN - Matorral Sarcocracicaule de Neblina')
			db.Cat_vegetacion_conglomerado.insert(nombre='MSM - Matorral Submontano')
			db.Cat_vegetacion_conglomerado.insert(nombre='MST - Matorral Subtropical')
			db.Cat_vegetacion_conglomerado.insert(nombre='MKX - Mezquital Desértico')
			db.Cat_vegetacion_conglomerado.insert(nombre='MKE - Mezquital Tropical')
			db.Cat_vegetacion_conglomerado.insert(nombre='VPN - Palmar Natural')
			db.Cat_vegetacion_conglomerado.insert(nombre='VPI - Palmar Inducido')
			db.Cat_vegetacion_conglomerado.insert(nombre='PY - Pastizal Gypsófilo')
			db.Cat_vegetacion_conglomerado.insert(nombre='PH - Pastizal Halófilo')
			db.Cat_vegetacion_conglomerado.insert(nombre='PN - Pastizal Natural')
			db.Cat_vegetacion_conglomerado.insert(nombre='VA - Popal')
			db.Cat_vegetacion_conglomerado.insert(nombre='VW - Pradera de Alta Montaña')
			db.Cat_vegetacion_conglomerado.insert(nombre='VS - Sabana')
			db.Cat_vegetacion_conglomerado.insert(nombre='VSI - Sabanoide')
			db.Cat_vegetacion_conglomerado.insert(nombre='SAP - Selva alta perennifolia')
			db.Cat_vegetacion_conglomerado.insert(nombre='SAQ - Selva alta subperennifolia')
			db.Cat_vegetacion_conglomerado.insert(nombre='SBC - Selva baja caducifolia')
			db.Cat_vegetacion_conglomerado.insert(nombre='SBK - Selva baja espinosa caducifolia')
			db.Cat_vegetacion_conglomerado.insert(nombre='SBQ - Selva baja espinosa subperennifolia')
			db.Cat_vegetacion_conglomerado.insert(nombre='SBP - Selva baja perennifolia')
			db.Cat_vegetacion_conglomerado.insert(nombre='SBS - Selva baja subcaducifolia')
			db.Cat_vegetacion_conglomerado.insert(nombre='SBQP - Selva baja subperennifolia')
			db.Cat_vegetacion_conglomerado.insert(nombre='SG - Selva de Galería')
			db.Cat_vegetacion_conglomerado.insert(nombre='SMC - Selva mediana caducifolia')
			db.Cat_vegetacion_conglomerado.insert(nombre='SMP - Selva mediana perennifolia')
			db.Cat_vegetacion_conglomerado.insert(nombre='SMS - Selva mediana subcaducifolia')
			db.Cat_vegetacion_conglomerado.insert(nombre='SMQ - Selva mediana subperennifolia')
			db.Cat_vegetacion_conglomerado.insert(nombre='VT - Tular')
			db.Cat_vegetacion_conglomerado.insert(nombre='VD - Vegetación de Desiertos Arenosos')
			db.Cat_vegetacion_conglomerado.insert(nombre='VU - Vegetación de Dunas Costeras')
			db.Cat_vegetacion_conglomerado.insert(nombre='VG - Vegetación de Galería')
			db.Cat_vegetacion_conglomerado.insert(nombre='PT - Vegetación de Petén')
			db.Cat_vegetacion_conglomerado.insert(nombre='VY - Vegetación Gypsófila')
			db.Cat_vegetacion_conglomerado.insert(nombre='VHH - Vegetación Halófila Hidrófila')
			db.Cat_vegetacion_conglomerado.insert(nombre='VH - Vegetación Halófila Xerófila')

		#########################################################################

		if db(db.Cat_numero_sitio.id>0).count() == 0:
			db.Cat_numero_sitio.insert(nombre='Centro')
			db.Cat_numero_sitio.insert(nombre='Sitio 2')
			db.Cat_numero_sitio.insert(nombre='Sitio 3')
			db.Cat_numero_sitio.insert(nombre='Sitio 4')
			db.Cat_numero_sitio.insert(nombre='Punto de control')

		#########################################################################

		if db(db.Cat_elipsoide.id>0).count() == 0:
			db.Cat_elipsoide.insert(nombre='WGS84')

		##########################################################################
		## Pestaña Camara
		########################################################################

		if db(db.Cat_resolucion_camara.id>0).count() == 0:
			db.Cat_resolucion_camara.insert(nombre='5MP')
			db.Cat_resolucion_camara.insert(nombre='12MP')
			db.Cat_resolucion_camara.insert(nombre='2MP')

		#########################################################################

		if db(db.Cat_sensibilidad_camara.id>0).count() == 0:
			db.Cat_sensibilidad_camara.insert(nombre='Normal')
			db.Cat_sensibilidad_camara.insert(nombre='High')
			db.Cat_sensibilidad_camara.insert(nombre='Low')

		#########################################################################

		if db(db.Cat_condiciones_ambientales.id>0).count() == 0:
			db.Cat_condiciones_ambientales.insert(nombre='Ninguna')
			db.Cat_condiciones_ambientales.insert(nombre='Lluvia')
			db.Cat_condiciones_ambientales.insert(nombre='Viento')
			db.Cat_condiciones_ambientales.insert(nombre='Nieve')
			db.Cat_condiciones_ambientales.insert(nombre='Neblina')

		##########################################################################
		## Pestaña Especies Invasoras / Pestaña Huellas y excretas
		######################################################################## 

		if db(db.Cat_numero_transecto.id>0).count() == 0:
			db.Cat_numero_transecto.insert(nombre='Transecto 2')
			db.Cat_numero_transecto.insert(nombre='Transecto 3')
			db.Cat_numero_transecto.insert(nombre='Transecto 4')


		##########################################################################
		## Pestaña Especies Invasoras
		######################################################################## 

		if db(db.Cat_numero_individuos.id>0).count() == 0:
			#db.Cat_numero_individuos.insert(nombre='No aplica')
			db.Cat_numero_individuos.insert(nombre='1 a 5')
			db.Cat_numero_individuos.insert(nombre='6 a 10')
			db.Cat_numero_individuos.insert(nombre='más de 10')

		##########################################################################
		## Lista CONABIO de especies invasoras
		######################################################################## 

		if db(db.Cat_conabio_invasoras.id>0).count() == 0:
			db.Cat_conabio_invasoras.insert(nombre='Arundo donax - Carrizo gigante')
			db.Cat_conabio_invasoras.insert(nombre='Axis axis - Venado axis')
			db.Cat_conabio_invasoras.insert(nombre='Bassia scoparia - Rodadora')
			db.Cat_conabio_invasoras.insert(nombre='Bromus madritensis - Bromo')
			db.Cat_conabio_invasoras.insert(nombre='Cactoblastis cactorum - Palomilla de nopal')
			db.Cat_conabio_invasoras.insert(nombre='Carpobrotus sp (C. edulis) - Higo marino')
			db.Cat_conabio_invasoras.insert(nombre='Cyperus papyrus (ANP) - Papiro')
			db.Cat_conabio_invasoras.insert(nombre='Eichhornia crassipes - Lirio acuático')
			db.Cat_conabio_invasoras.insert(nombre='Hedera helix - Hiedra')
			db.Cat_conabio_invasoras.insert(nombre='Lepidium draba /Cardaria draba - Flor bábol, capellanes')
			db.Cat_conabio_invasoras.insert(nombre='Melinis minutiflora - Paja rosada, pasto morado, zacate colorado')
			db.Cat_conabio_invasoras.insert(nombre='Melinis repens - Paja rosada, pasto morado, zacate colorado')
			db.Cat_conabio_invasoras.insert(nombre='Mesembryanthemum crystallinum - Vidrillo')
			db.Cat_conabio_invasoras.insert(nombre='Myiopsitta monachus - Perico monje')
			db.Cat_conabio_invasoras.insert(nombre='Myocastor coypus - Coipu')
			db.Cat_conabio_invasoras.insert(nombre='Oeceoclades maculata - Orquídea monje')
			db.Cat_conabio_invasoras.insert(nombre='Pennisetum clandestinum - Kikuyo, kuyuyú, tapete, colchoncillo')
			db.Cat_conabio_invasoras.insert(nombre='Pueraria sp. (montana lobata o phaseoloides - Kudzu')
			db.Cat_conabio_invasoras.insert(nombre='Rottboellia cochinchinensis - Caminadora')
			db.Cat_conabio_invasoras.insert(nombre='Salsola sp. (vermiculata o tragus) - Rodadora')
			db.Cat_conabio_invasoras.insert(nombre='Stizlobium prurienes - Picapica')
			db.Cat_conabio_invasoras.insert(nombre='Sus scrofa - Cerdo europeo')
			db.Cat_conabio_invasoras.insert(nombre='Tamarix sp. - Pino salado, cedro salado, tamarisco')
			db.Cat_conabio_invasoras.insert(nombre='Otros')

		#########################################################################

		if db(db.Cat_municipio_conglomerado.id>0).count() == 0:
			db.Cat_municipio_conglomerado.insert(clave_ent='1',clave_mun='1',nombre='Aguascalientes')
			db.Cat_municipio_conglomerado.insert(clave_ent='1',clave_mun='2',nombre='Asientos')
			db.Cat_municipio_conglomerado.insert(clave_ent='1',clave_mun='3',nombre='Calvillo')
			db.Cat_municipio_conglomerado.insert(clave_ent='1',clave_mun='4',nombre='Cosío')
			db.Cat_municipio_conglomerado.insert(clave_ent='1',clave_mun='10',nombre='El Llano')
			db.Cat_municipio_conglomerado.insert(clave_ent='1',clave_mun='5',nombre='Jesús María')
			db.Cat_municipio_conglomerado.insert(clave_ent='1',clave_mun='6',nombre='Pabellón de Arteaga')
			db.Cat_municipio_conglomerado.insert(clave_ent='1',clave_mun='7',nombre='Rincón de Romos')
			db.Cat_municipio_conglomerado.insert(clave_ent='1',clave_mun='11',nombre='San Francisco de los Romo')
			db.Cat_municipio_conglomerado.insert(clave_ent='1',clave_mun='8',nombre='San José de Gracia')
			db.Cat_municipio_conglomerado.insert(clave_ent='1',clave_mun='9',nombre='Tepezalá')
			db.Cat_municipio_conglomerado.insert(clave_ent='2',clave_mun='1',nombre='Ensenada')
			db.Cat_municipio_conglomerado.insert(clave_ent='2',clave_mun='2',nombre='Mexicali')
			db.Cat_municipio_conglomerado.insert(clave_ent='2',clave_mun='5',nombre='Playas de Rosarito')
			db.Cat_municipio_conglomerado.insert(clave_ent='2',clave_mun='3',nombre='Tecate')
			db.Cat_municipio_conglomerado.insert(clave_ent='2',clave_mun='4',nombre='Tijuana')
			db.Cat_municipio_conglomerado.insert(clave_ent='3',clave_mun='1',nombre='Comondú')
			db.Cat_municipio_conglomerado.insert(clave_ent='3',clave_mun='3',nombre='La Paz')
			db.Cat_municipio_conglomerado.insert(clave_ent='3',clave_mun='9',nombre='Loreto')
			db.Cat_municipio_conglomerado.insert(clave_ent='3',clave_mun='8',nombre='Los Cabos')
			db.Cat_municipio_conglomerado.insert(clave_ent='3',clave_mun='2',nombre='Mulegé')
			db.Cat_municipio_conglomerado.insert(clave_ent='4',clave_mun='10',nombre='Calakmul')
			db.Cat_municipio_conglomerado.insert(clave_ent='4',clave_mun='1',nombre='Calkiní')
			db.Cat_municipio_conglomerado.insert(clave_ent='4',clave_mun='2',nombre='Campeche')
			db.Cat_municipio_conglomerado.insert(clave_ent='4',clave_mun='11',nombre='Candelaria')
			db.Cat_municipio_conglomerado.insert(clave_ent='4',clave_mun='3',nombre='Carmen')
			db.Cat_municipio_conglomerado.insert(clave_ent='4',clave_mun='4',nombre='Champotón')
			db.Cat_municipio_conglomerado.insert(clave_ent='4',clave_mun='9',nombre='Escárcega')
			db.Cat_municipio_conglomerado.insert(clave_ent='4',clave_mun='5',nombre='Hecelchakán')
			db.Cat_municipio_conglomerado.insert(clave_ent='4',clave_mun='6',nombre='Hopelchén')
			db.Cat_municipio_conglomerado.insert(clave_ent='4',clave_mun='7',nombre='Palizada')
			db.Cat_municipio_conglomerado.insert(clave_ent='4',clave_mun='8',nombre='Tenabo')
			db.Cat_municipio_conglomerado.insert(clave_ent='5',clave_mun='1',nombre='Abasolo')
			db.Cat_municipio_conglomerado.insert(clave_ent='5',clave_mun='2',nombre='Acuña')
			db.Cat_municipio_conglomerado.insert(clave_ent='5',clave_mun='3',nombre='Allende')
			db.Cat_municipio_conglomerado.insert(clave_ent='5',clave_mun='4',nombre='Arteaga')
			db.Cat_municipio_conglomerado.insert(clave_ent='5',clave_mun='5',nombre='Candela')
			db.Cat_municipio_conglomerado.insert(clave_ent='5',clave_mun='6',nombre='Castaños')
			db.Cat_municipio_conglomerado.insert(clave_ent='5',clave_mun='7',nombre='Cuatro Ciénegas')
			db.Cat_municipio_conglomerado.insert(clave_ent='5',clave_mun='8',nombre='Escobedo')
			db.Cat_municipio_conglomerado.insert(clave_ent='5',clave_mun='9',nombre='Francisco I. Madero')
			db.Cat_municipio_conglomerado.insert(clave_ent='5',clave_mun='10',nombre='Frontera')
			db.Cat_municipio_conglomerado.insert(clave_ent='5',clave_mun='11',nombre='General Cepeda')
			db.Cat_municipio_conglomerado.insert(clave_ent='5',clave_mun='12',nombre='Guerrero')
			db.Cat_municipio_conglomerado.insert(clave_ent='5',clave_mun='13',nombre='Hidalgo')
			db.Cat_municipio_conglomerado.insert(clave_ent='5',clave_mun='14',nombre='Jiménez')
			db.Cat_municipio_conglomerado.insert(clave_ent='5',clave_mun='15',nombre='Juárez')
			db.Cat_municipio_conglomerado.insert(clave_ent='5',clave_mun='16',nombre='Lamadrid')
			db.Cat_municipio_conglomerado.insert(clave_ent='5',clave_mun='17',nombre='Matamoros')
			db.Cat_municipio_conglomerado.insert(clave_ent='5',clave_mun='18',nombre='Monclova')
			db.Cat_municipio_conglomerado.insert(clave_ent='5',clave_mun='19',nombre='Morelos')
			db.Cat_municipio_conglomerado.insert(clave_ent='5',clave_mun='20',nombre='Múzquiz')
			db.Cat_municipio_conglomerado.insert(clave_ent='5',clave_mun='21',nombre='Nadadores')
			db.Cat_municipio_conglomerado.insert(clave_ent='5',clave_mun='22',nombre='Nava')
			db.Cat_municipio_conglomerado.insert(clave_ent='5',clave_mun='23',nombre='Ocampo')
			db.Cat_municipio_conglomerado.insert(clave_ent='5',clave_mun='24',nombre='Parras')
			db.Cat_municipio_conglomerado.insert(clave_ent='5',clave_mun='25',nombre='Piedras Negras')
			db.Cat_municipio_conglomerado.insert(clave_ent='5',clave_mun='26',nombre='Progreso')
			db.Cat_municipio_conglomerado.insert(clave_ent='5',clave_mun='27',nombre='Ramos Arizpe')
			db.Cat_municipio_conglomerado.insert(clave_ent='5',clave_mun='28',nombre='Sabinas')
			db.Cat_municipio_conglomerado.insert(clave_ent='5',clave_mun='29',nombre='Sacramento')
			db.Cat_municipio_conglomerado.insert(clave_ent='5',clave_mun='30',nombre='Saltillo')
			db.Cat_municipio_conglomerado.insert(clave_ent='5',clave_mun='31',nombre='San Buenaventura')
			db.Cat_municipio_conglomerado.insert(clave_ent='5',clave_mun='32',nombre='San Juan de Sabinas')
			db.Cat_municipio_conglomerado.insert(clave_ent='5',clave_mun='33',nombre='San Pedro')
			db.Cat_municipio_conglomerado.insert(clave_ent='5',clave_mun='34',nombre='Sierra Mojada')
			db.Cat_municipio_conglomerado.insert(clave_ent='5',clave_mun='35',nombre='Torreón')
			db.Cat_municipio_conglomerado.insert(clave_ent='5',clave_mun='36',nombre='Viesca')
			db.Cat_municipio_conglomerado.insert(clave_ent='5',clave_mun='37',nombre='Villa Unión')
			db.Cat_municipio_conglomerado.insert(clave_ent='5',clave_mun='38',nombre='Zaragoza')
			db.Cat_municipio_conglomerado.insert(clave_ent='6',clave_mun='1',nombre='Armería')
			db.Cat_municipio_conglomerado.insert(clave_ent='6',clave_mun='2',nombre='Colima')
			db.Cat_municipio_conglomerado.insert(clave_ent='6',clave_mun='3',nombre='Comala')
			db.Cat_municipio_conglomerado.insert(clave_ent='6',clave_mun='4',nombre='Coquimatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='6',clave_mun='5',nombre='Cuauhtémoc')
			db.Cat_municipio_conglomerado.insert(clave_ent='6',clave_mun='6',nombre='Ixtlahuacán')
			db.Cat_municipio_conglomerado.insert(clave_ent='6',clave_mun='7',nombre='Manzanillo')
			db.Cat_municipio_conglomerado.insert(clave_ent='6',clave_mun='8',nombre='Minatitlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='6',clave_mun='9',nombre='Tecomán')
			db.Cat_municipio_conglomerado.insert(clave_ent='6',clave_mun='10',nombre='Villa de Álvarez')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='1',nombre='Acacoyagua')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='2',nombre='Acala')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='3',nombre='Acapetahua')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='113',nombre='Aldama')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='4',nombre='Altamirano')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='5',nombre='Amatán')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='6',nombre='Amatenango de la Frontera')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='7',nombre='Amatenango del Valle')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='8',nombre='Angel Albino Corzo')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='9',nombre='Arriaga')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='10',nombre='Bejucal de Ocampo')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='11',nombre='Bella Vista')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='114',nombre='Benemérito de las Américas')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='12',nombre='Berriozábal')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='13',nombre='Bochil')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='15',nombre='Cacahoatán')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='16',nombre='Catazajá')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='22',nombre='Chalchihuitán')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='23',nombre='Chamula')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='24',nombre='Chanal')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='25',nombre='Chapultenango')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='26',nombre='Chenalhó')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='27',nombre='Chiapa de Corzo')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='28',nombre='Chiapilla')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='29',nombre='Chicoasén')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='30',nombre='Chicomuselo')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='31',nombre='Chilón')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='17',nombre='Cintalapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='18',nombre='Coapilla')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='19',nombre='Comitán de Domínguez')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='21',nombre='Copainalá')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='14',nombre='El Bosque')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='70',nombre='El Porvenir')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='32',nombre='Escuintla')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='33',nombre='Francisco León')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='34',nombre='Frontera Comalapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='35',nombre='Frontera Hidalgo')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='37',nombre='Huehuetán')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='39',nombre='Huitiupán')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='38',nombre='Huixtán')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='40',nombre='Huixtla')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='42',nombre='Ixhuatán')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='43',nombre='Ixtacomitán')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='44',nombre='Ixtapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='45',nombre='Ixtapangajoya')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='46',nombre='Jiquipilas')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='47',nombre='Jitotol')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='48',nombre='Juárez')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='20',nombre='La Concordia')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='36',nombre='La Grandeza')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='41',nombre='La Independencia')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='50',nombre='La Libertad')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='99',nombre='La Trinitaria')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='49',nombre='Larráinzar')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='52',nombre='Las Margaritas')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='75',nombre='Las Rosas')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='51',nombre='Mapastepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='115',nombre='Maravilla Tenejapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='116',nombre='Marqués de Comillas')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='53',nombre='Mazapa de Madero')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='54',nombre='Mazatán')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='55',nombre='Metapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='56',nombre='Mitontic')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='117',nombre='Montecristo de Guerrero')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='57',nombre='Motozintla')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='58',nombre='Nicolás Ruíz')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='59',nombre='Ocosingo')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='60',nombre='Ocotepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='61',nombre='Ocozocoautla de Espinosa')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='62',nombre='Ostuacán')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='63',nombre='Osumacinta')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='64',nombre='Oxchuc')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='65',nombre='Palenque')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='66',nombre='Pantelhó')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='67',nombre='Pantepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='68',nombre='Pichucalco')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='69',nombre='Pijijiapan')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='72',nombre='Pueblo Nuevo Solistahuacán')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='73',nombre='Rayón')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='74',nombre='Reforma')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='76',nombre='Sabanilla')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='77',nombre='Salto de Agua')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='118',nombre='San Andrés Duraznal')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='78',nombre='San Cristóbal de las Casas')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='79',nombre='San Fernando')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='112',nombre='San Juan Cancuc')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='110',nombre='San Lucas')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='119',nombre='Santiago el Pinar')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='80',nombre='Siltepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='81',nombre='Simojovel')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='82',nombre='Sitalá')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='83',nombre='Socoltenango')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='84',nombre='Solosuchiapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='85',nombre='Soyaló')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='86',nombre='Suchiapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='87',nombre='Suchiate')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='88',nombre='Sunuapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='89',nombre='Tapachula')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='90',nombre='Tapalapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='91',nombre='Tapilula')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='92',nombre='Tecpatán')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='93',nombre='Tenejapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='94',nombre='Teopisca')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='96',nombre='Tila')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='97',nombre='Tonalá')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='98',nombre='Totolapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='100',nombre='Tumbalá')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='102',nombre='Tuxtla Chico')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='101',nombre='Tuxtla Gutiérrez')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='103',nombre='Tuzantán')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='104',nombre='Tzimol')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='105',nombre='Unión Juárez')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='106',nombre='Venustiano Carranza')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='71',nombre='Villa Comaltitlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='107',nombre='Villa Corzo')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='108',nombre='Villaflores')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='109',nombre='Yajalón')
			db.Cat_municipio_conglomerado.insert(clave_ent='7',clave_mun='111',nombre='Zinacantán')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='1',nombre='Ahumada')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='2',nombre='Aldama')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='3',nombre='Allende')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='4',nombre='Aquiles Serdán')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='5',nombre='Ascensión')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='6',nombre='Bachíniva')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='7',nombre='Balleza')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='8',nombre='Batopilas')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='9',nombre='Bocoyna')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='10',nombre='Buenaventura')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='11',nombre='Camargo')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='12',nombre='Carichí')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='13',nombre='Casas Grandes')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='19',nombre='Chihuahua')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='20',nombre='Chínipas')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='14',nombre='Coronado')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='15',nombre='Coyame del Sotol')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='17',nombre='Cuauhtémoc')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='18',nombre='Cusihuiriachi')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='21',nombre='Delicias')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='22',nombre='Dr. Belisario Domínguez')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='64',nombre='El Tule')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='23',nombre='Galeana')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='25',nombre='Gómez Farías')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='26',nombre='Gran Morelos')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='27',nombre='Guachochi')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='28',nombre='Guadalupe')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='29',nombre='Guadalupe y Calvo')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='30',nombre='Guazapares')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='31',nombre='Guerrero')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='32',nombre='Hidalgo del Parral')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='33',nombre='Huejotitán')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='34',nombre='Ignacio Zaragoza')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='35',nombre='Janos')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='36',nombre='Jiménez')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='37',nombre='Juárez')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='38',nombre='Julimes')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='16',nombre='La Cruz')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='39',nombre='López')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='40',nombre='Madera')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='41',nombre='Maguarichi')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='42',nombre='Manuel Benavides')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='43',nombre='Matachí')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='44',nombre='Matamoros')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='45',nombre='Meoqui')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='46',nombre='Morelos')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='47',nombre='Moris')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='48',nombre='Namiquipa')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='49',nombre='Nonoava')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='50',nombre='Nuevo Casas Grandes')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='51',nombre='Ocampo')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='52',nombre='Ojinaga')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='53',nombre='Praxedis G. Guerrero')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='54',nombre='Riva Palacio')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='55',nombre='Rosales')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='56',nombre='Rosario')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='57',nombre='San Francisco de Borja')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='58',nombre='San Francisco de Conchos')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='59',nombre='San Francisco del Oro')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='60',nombre='Santa Bárbara')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='24',nombre='Santa Isabel')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='61',nombre='Satevó')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='62',nombre='Saucillo')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='63',nombre='Temósachic')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='65',nombre='Urique')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='66',nombre='Uruachi')
			db.Cat_municipio_conglomerado.insert(clave_ent='8',clave_mun='67',nombre='Valle de Zaragoza')
			db.Cat_municipio_conglomerado.insert(clave_ent='9',clave_mun='10',nombre='Álvaro Obregón')
			db.Cat_municipio_conglomerado.insert(clave_ent='9',clave_mun='2',nombre='Azcapotzalco')
			db.Cat_municipio_conglomerado.insert(clave_ent='9',clave_mun='14',nombre='Benito Juárez')
			db.Cat_municipio_conglomerado.insert(clave_ent='9',clave_mun='3',nombre='Coyoacán')
			db.Cat_municipio_conglomerado.insert(clave_ent='9',clave_mun='4',nombre='Cuajimalpa de Morelos')
			db.Cat_municipio_conglomerado.insert(clave_ent='9',clave_mun='15',nombre='Cuauhtémoc')
			db.Cat_municipio_conglomerado.insert(clave_ent='9',clave_mun='5',nombre='Gustavo A. Madero')
			db.Cat_municipio_conglomerado.insert(clave_ent='9',clave_mun='6',nombre='Iztacalco')
			db.Cat_municipio_conglomerado.insert(clave_ent='9',clave_mun='7',nombre='Iztapalapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='9',clave_mun='8',nombre='La Magdalena Contreras')
			db.Cat_municipio_conglomerado.insert(clave_ent='9',clave_mun='16',nombre='Miguel Hidalgo')
			db.Cat_municipio_conglomerado.insert(clave_ent='9',clave_mun='9',nombre='Milpa Alta')
			db.Cat_municipio_conglomerado.insert(clave_ent='9',clave_mun='11',nombre='Tláhuac')
			db.Cat_municipio_conglomerado.insert(clave_ent='9',clave_mun='12',nombre='Tlalpan')
			db.Cat_municipio_conglomerado.insert(clave_ent='9',clave_mun='17',nombre='Venustiano Carranza')
			db.Cat_municipio_conglomerado.insert(clave_ent='9',clave_mun='13',nombre='Xochimilco')
			db.Cat_municipio_conglomerado.insert(clave_ent='10',clave_mun='1',nombre='Canatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='10',clave_mun='2',nombre='Canelas')
			db.Cat_municipio_conglomerado.insert(clave_ent='10',clave_mun='3',nombre='Coneto de Comonfort')
			db.Cat_municipio_conglomerado.insert(clave_ent='10',clave_mun='4',nombre='Cuencamé')
			db.Cat_municipio_conglomerado.insert(clave_ent='10',clave_mun='5',nombre='Durango')
			db.Cat_municipio_conglomerado.insert(clave_ent='10',clave_mun='18',nombre='El Oro')
			db.Cat_municipio_conglomerado.insert(clave_ent='10',clave_mun='6',nombre='General Simón Bolívar')
			db.Cat_municipio_conglomerado.insert(clave_ent='10',clave_mun='7',nombre='Gómez Palacio')
			db.Cat_municipio_conglomerado.insert(clave_ent='10',clave_mun='8',nombre='Guadalupe Victoria')
			db.Cat_municipio_conglomerado.insert(clave_ent='10',clave_mun='9',nombre='Guanaceví')
			db.Cat_municipio_conglomerado.insert(clave_ent='10',clave_mun='10',nombre='Hidalgo')
			db.Cat_municipio_conglomerado.insert(clave_ent='10',clave_mun='11',nombre='Indé')
			db.Cat_municipio_conglomerado.insert(clave_ent='10',clave_mun='12',nombre='Lerdo')
			db.Cat_municipio_conglomerado.insert(clave_ent='10',clave_mun='13',nombre='Mapimí')
			db.Cat_municipio_conglomerado.insert(clave_ent='10',clave_mun='14',nombre='Mezquital')
			db.Cat_municipio_conglomerado.insert(clave_ent='10',clave_mun='15',nombre='Nazas')
			db.Cat_municipio_conglomerado.insert(clave_ent='10',clave_mun='16',nombre='Nombre de Dios')
			db.Cat_municipio_conglomerado.insert(clave_ent='10',clave_mun='39',nombre='Nuevo Ideal')
			db.Cat_municipio_conglomerado.insert(clave_ent='10',clave_mun='17',nombre='Ocampo')
			db.Cat_municipio_conglomerado.insert(clave_ent='10',clave_mun='19',nombre='Otáez')
			db.Cat_municipio_conglomerado.insert(clave_ent='10',clave_mun='20',nombre='Pánuco de Coronado')
			db.Cat_municipio_conglomerado.insert(clave_ent='10',clave_mun='21',nombre='Peñón Blanco')
			db.Cat_municipio_conglomerado.insert(clave_ent='10',clave_mun='22',nombre='Poanas')
			db.Cat_municipio_conglomerado.insert(clave_ent='10',clave_mun='23',nombre='Pueblo Nuevo')
			db.Cat_municipio_conglomerado.insert(clave_ent='10',clave_mun='24',nombre='Rodeo')
			db.Cat_municipio_conglomerado.insert(clave_ent='10',clave_mun='25',nombre='San Bernardo')
			db.Cat_municipio_conglomerado.insert(clave_ent='10',clave_mun='26',nombre='San Dimas')
			db.Cat_municipio_conglomerado.insert(clave_ent='10',clave_mun='27',nombre='San Juan de Guadalupe')
			db.Cat_municipio_conglomerado.insert(clave_ent='10',clave_mun='28',nombre='San Juan del Río')
			db.Cat_municipio_conglomerado.insert(clave_ent='10',clave_mun='29',nombre='San Luis del Cordero')
			db.Cat_municipio_conglomerado.insert(clave_ent='10',clave_mun='30',nombre='San Pedro del Gallo')
			db.Cat_municipio_conglomerado.insert(clave_ent='10',clave_mun='31',nombre='Santa Clara')
			db.Cat_municipio_conglomerado.insert(clave_ent='10',clave_mun='32',nombre='Santiago Papasquiaro')
			db.Cat_municipio_conglomerado.insert(clave_ent='10',clave_mun='33',nombre='Súchil')
			db.Cat_municipio_conglomerado.insert(clave_ent='10',clave_mun='34',nombre='Tamazula')
			db.Cat_municipio_conglomerado.insert(clave_ent='10',clave_mun='35',nombre='Tepehuanes')
			db.Cat_municipio_conglomerado.insert(clave_ent='10',clave_mun='36',nombre='Tlahualilo')
			db.Cat_municipio_conglomerado.insert(clave_ent='10',clave_mun='37',nombre='Topia')
			db.Cat_municipio_conglomerado.insert(clave_ent='10',clave_mun='38',nombre='Vicente Guerrero')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='1',nombre='Abasolo')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='2',nombre='Acámbaro')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='4',nombre='Apaseo el Alto')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='5',nombre='Apaseo el Grande')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='6',nombre='Atarjea')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='7',nombre='Celaya')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='9',nombre='Comonfort')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='10',nombre='Coroneo')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='11',nombre='Cortazar')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='12',nombre='Cuerámaro')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='13',nombre='Doctor Mora')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='14',nombre='Dolores Hidalgo Cuna de la Independencia Nacional')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='15',nombre='Guanajuato')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='16',nombre='Huanímaro')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='17',nombre='Irapuato')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='18',nombre='Jaral del Progreso')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='19',nombre='Jerécuaro')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='20',nombre='León')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='8',nombre='Manuel Doblado')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='21',nombre='Moroleón')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='22',nombre='Ocampo')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='23',nombre='Pénjamo')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='24',nombre='Pueblo Nuevo')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='25',nombre='Purísima del Rincón')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='26',nombre='Romita')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='27',nombre='Salamanca')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='28',nombre='Salvatierra')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='29',nombre='San Diego de la Unión')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='30',nombre='San Felipe')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='31',nombre='San Francisco del Rincón')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='32',nombre='San José Iturbide')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='33',nombre='San Luis de la Paz')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='3',nombre='San Miguel de Allende')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='34',nombre='Santa Catarina')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='35',nombre='Santa Cruz de Juventino Rosas')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='36',nombre='Santiago Maravatío')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='37',nombre='Silao de la Victoria')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='38',nombre='Tarandacuao')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='39',nombre='Tarimoro')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='40',nombre='Tierra Blanca')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='41',nombre='Uriangato')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='42',nombre='Valle de Santiago')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='43',nombre='Victoria')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='44',nombre='Villagrán')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='45',nombre='Xichú')
			db.Cat_municipio_conglomerado.insert(clave_ent='11',clave_mun='46',nombre='Yuriria')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='1',nombre='Acapulco de Juárez')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='76',nombre='Acatepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='2',nombre='Ahuacuotzingo')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='3',nombre='Ajuchitlán del Progreso')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='4',nombre='Alcozauca de Guerrero')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='5',nombre='Alpoyeca')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='6',nombre='Apaxtla')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='7',nombre='Arcelia')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='8',nombre='Atenango del Río')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='9',nombre='Atlamajalcingo del Monte')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='10',nombre='Atlixtac')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='11',nombre='Atoyac de Álvarez')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='12',nombre='Ayutla de los Libres')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='13',nombre='Azoyú')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='14',nombre='Benito Juárez')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='15',nombre='Buenavista de Cuéllar')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='28',nombre='Chilapa de Álvarez')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='29',nombre='Chilpancingo de los Bravo')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='16',nombre='Coahuayutla de José María Izazaga')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='78',nombre='Cochoapa el Grande')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='17',nombre='Cocula')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='18',nombre='Copala')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='19',nombre='Copalillo')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='20',nombre='Copanatoyac')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='21',nombre='Coyuca de Benítez')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='22',nombre='Coyuca de Catalán')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='23',nombre='Cuajinicuilapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='24',nombre='Cualác')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='25',nombre='Cuautepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='26',nombre='Cuetzala del Progreso')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='27',nombre='Cutzamala de Pinzón')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='75',nombre='Eduardo Neri')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='30',nombre='Florencio Villarreal')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='31',nombre='General Canuto A. Neri')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='32',nombre='General Heliodoro Castillo')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='33',nombre='Huamuxtitlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='34',nombre='Huitzuco de los Figueroa')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='35',nombre='Iguala de la Independencia')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='36',nombre='Igualapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='81',nombre='Iliatenco')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='37',nombre='Ixcateopan de Cuauhtémoc')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='79',nombre='José Joaquín de Herrera')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='39',nombre='Juan R. Escudero')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='80',nombre='Juchitán')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='68',nombre='La Unión de Isidoro Montes de Oca')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='40',nombre='Leonardo Bravo')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='41',nombre='Malinaltepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='77',nombre='Marquelia')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='42',nombre='Mártir de Cuilapan')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='43',nombre='Metlatónoc')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='44',nombre='Mochitlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='45',nombre='Olinalá')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='46',nombre='Ometepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='47',nombre='Pedro Ascencio Alquisiras')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='48',nombre='Petatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='49',nombre='Pilcaya')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='50',nombre='Pungarabato')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='51',nombre='Quechultenango')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='52',nombre='San Luis Acatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='53',nombre='San Marcos')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='54',nombre='San Miguel Totolapan')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='55',nombre='Taxco de Alarcón')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='56',nombre='Tecoanapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='57',nombre='Técpan de Galeana')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='58',nombre='Teloloapan')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='59',nombre='Tepecoacuilco de Trujano')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='60',nombre='Tetipac')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='61',nombre='Tixtla de Guerrero')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='62',nombre='Tlacoachistlahuaca')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='63',nombre='Tlacoapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='64',nombre='Tlalchapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='65',nombre='Tlalixtaquilla de Maldonado')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='66',nombre='Tlapa de Comonfort')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='67',nombre='Tlapehuala')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='69',nombre='Xalpatláhuac')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='70',nombre='Xochihuehuetlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='71',nombre='Xochistlahuaca')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='72',nombre='Zapotitlán Tablas')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='38',nombre='Zihuatanejo de Azueta')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='73',nombre='Zirándaro')
			db.Cat_municipio_conglomerado.insert(clave_ent='12',clave_mun='74',nombre='Zitlala')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='1',nombre='Acatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='2',nombre='Acaxochitlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='3',nombre='Actopan')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='4',nombre='Agua Blanca de Iturbide')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='5',nombre='Ajacuba')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='6',nombre='Alfajayucan')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='7',nombre='Almoloya')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='8',nombre='Apan')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='10',nombre='Atitalaquia')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='11',nombre='Atlapexco')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='13',nombre='Atotonilco de Tula')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='12',nombre='Atotonilco el Grande')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='14',nombre='Calnali')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='15',nombre='Cardonal')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='17',nombre='Chapantongo')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='18',nombre='Chapulhuacán')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='19',nombre='Chilcuautla')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='16',nombre='Cuautepec de Hinojosa')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='9',nombre='El Arenal')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='20',nombre='Eloxochitlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='21',nombre='Emiliano Zapata')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='22',nombre='Epazoyucan')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='23',nombre='Francisco I. Madero')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='24',nombre='Huasca de Ocampo')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='25',nombre='Huautla')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='26',nombre='Huazalingo')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='27',nombre='Huehuetla')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='28',nombre='Huejutla de Reyes')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='29',nombre='Huichapan')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='30',nombre='Ixmiquilpan')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='31',nombre='Jacala de Ledezma')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='32',nombre='Jaltocán')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='33',nombre='Juárez Hidalgo')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='40',nombre='La Misión')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='34',nombre='Lolotla')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='35',nombre='Metepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='37',nombre='Metztitlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='51',nombre='Mineral de la Reforma')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='38',nombre='Mineral del Chico')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='39',nombre='Mineral del Monte')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='41',nombre='Mixquiahuala de Juárez')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='42',nombre='Molango de Escamilla')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='43',nombre='Nicolás Flores')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='44',nombre='Nopala de Villagrán')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='45',nombre='Omitlán de Juárez')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='48',nombre='Pachuca de Soto')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='47',nombre='Pacula')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='49',nombre='Pisaflores')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='50',nombre='Progreso de Obregón')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='36',nombre='San Agustín Metzquititlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='52',nombre='San Agustín Tlaxiaca')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='53',nombre='San Bartolo Tutotepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='46',nombre='San Felipe Orizatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='54',nombre='San Salvador')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='55',nombre='Santiago de Anaya')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='56',nombre='Santiago Tulantepec de Lugo Guerrero')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='57',nombre='Singuilucan')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='58',nombre='Tasquillo')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='59',nombre='Tecozautla')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='60',nombre='Tenango de Doria')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='61',nombre='Tepeapulco')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='62',nombre='Tepehuacán de Guerrero')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='63',nombre='Tepeji del Río de Ocampo')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='64',nombre='Tepetitlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='65',nombre='Tetepango')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='67',nombre='Tezontepec de Aldama')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='68',nombre='Tianguistengo')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='69',nombre='Tizayuca')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='70',nombre='Tlahuelilpan')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='71',nombre='Tlahuiltepa')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='72',nombre='Tlanalapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='73',nombre='Tlanchinol')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='74',nombre='Tlaxcoapan')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='75',nombre='Tolcayuca')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='76',nombre='Tula de Allende')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='77',nombre='Tulancingo de Bravo')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='66',nombre='Villa de Tezontepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='78',nombre='Xochiatipan')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='79',nombre='Xochicoatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='80',nombre='Yahualica')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='81',nombre='Zacualtipán de Ángeles')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='82',nombre='Zapotlán de Juárez')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='83',nombre='Zempoala')
			db.Cat_municipio_conglomerado.insert(clave_ent='13',clave_mun='84',nombre='Zimapán')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='1',nombre='Acatic')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='2',nombre='Acatlán de Juárez')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='3',nombre='Ahualulco de Mercado')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='4',nombre='Amacueca')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='5',nombre='Amatitán')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='6',nombre='Ameca')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='8',nombre='Arandas')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='10',nombre='Atemajac de Brizuela')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='11',nombre='Atengo')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='12',nombre='Atenguillo')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='13',nombre='Atotonilco el Alto')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='14',nombre='Atoyac')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='15',nombre='Autlán de Navarro')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='16',nombre='Ayotlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='17',nombre='Ayutla')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='19',nombre='Bolaños')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='20',nombre='Cabo Corrientes')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='117',nombre='Cañadas de Obregón')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='21',nombre='Casimiro Castillo')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='30',nombre='Chapala')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='31',nombre='Chimaltitán')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='32',nombre='Chiquilistlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='22',nombre='Cihuatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='24',nombre='Cocula')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='25',nombre='Colotlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='26',nombre='Concepción de Buenos Aires')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='27',nombre='Cuautitlán de García Barragán')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='28',nombre='Cuautla')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='29',nombre='Cuquío')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='33',nombre='Degollado')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='34',nombre='Ejutla')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='9',nombre='El Arenal')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='37',nombre='El Grullo')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='54',nombre='El Limón')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='70',nombre='El Salto')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='35',nombre='Encarnación de Díaz')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='36',nombre='Etzatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='79',nombre='Gómez Farías')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='38',nombre='Guachinango')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='39',nombre='Guadalajara')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='40',nombre='Hostotipaquillo')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='41',nombre='Huejúcar')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='42',nombre='Huejuquilla el Alto')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='44',nombre='Ixtlahuacán de los Membrillos')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='45',nombre='Ixtlahuacán del Río')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='46',nombre='Jalostotitlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='47',nombre='Jamay')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='48',nombre='Jesús María')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='49',nombre='Jilotlán de los Dolores')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='50',nombre='Jocotepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='51',nombre='Juanacatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='52',nombre='Juchitlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='18',nombre='La Barca')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='43',nombre='La Huerta')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='57',nombre='La Manzanilla de la Paz')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='53',nombre='Lagos de Moreno')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='55',nombre='Magdalena')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='58',nombre='Mascota')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='59',nombre='Mazamitla')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='60',nombre='Mexticacán')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='61',nombre='Mezquitic')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='62',nombre='Mixtlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='63',nombre='Ocotlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='64',nombre='Ojuelos de Jalisco')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='65',nombre='Pihuamo')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='66',nombre='Poncitlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='67',nombre='Puerto Vallarta')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='69',nombre='Quitupan')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='71',nombre='San Cristóbal de la Barranca')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='72',nombre='San Diego de Alejandría')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='113',nombre='San Gabriel')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='125',nombre='San Ignacio Cerro Gordo')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='73',nombre='San Juan de los Lagos')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='7',nombre='San Juanito de Escobedo')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='74',nombre='San Julián')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='75',nombre='San Marcos')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='76',nombre='San Martín de Bolaños')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='77',nombre='San Martín Hidalgo')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='78',nombre='San Miguel el Alto')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='98',nombre='San Pedro Tlaquepaque')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='80',nombre='San Sebastián del Oeste')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='81',nombre='Santa María de los Ángeles')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='56',nombre='Santa María del Oro')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='82',nombre='Sayula')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='83',nombre='Tala')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='84',nombre='Talpa de Allende')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='85',nombre='Tamazula de Gordiano')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='86',nombre='Tapalpa')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='87',nombre='Tecalitlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='89',nombre='Techaluta de Montenegro')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='88',nombre='Tecolotlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='90',nombre='Tenamaxtlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='91',nombre='Teocaltiche')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='92',nombre='Teocuitatlán de Corona')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='93',nombre='Tepatitlán de Morelos')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='94',nombre='Tequila')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='95',nombre='Teuchitlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='96',nombre='Tizapán el Alto')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='97',nombre='Tlajomulco de Zúñiga')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='99',nombre='Tolimán')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='100',nombre='Tomatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='101',nombre='Tonalá')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='102',nombre='Tonaya')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='103',nombre='Tonila')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='104',nombre='Totatiche')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='105',nombre='Tototlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='106',nombre='Tuxcacuesco')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='107',nombre='Tuxcueca')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='108',nombre='Tuxpan')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='109',nombre='Unión de San Antonio')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='110',nombre='Unión de Tula')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='111',nombre='Valle de Guadalupe')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='112',nombre='Valle de Juárez')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='114',nombre='Villa Corona')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='115',nombre='Villa Guerrero')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='116',nombre='Villa Hidalgo')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='68',nombre='Villa Purificación')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='118',nombre='Yahualica de González Gallo')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='119',nombre='Zacoalco de Torres')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='120',nombre='Zapopan')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='121',nombre='Zapotiltic')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='122',nombre='Zapotitlán de Vadillo')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='123',nombre='Zapotlán del Rey')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='23',nombre='Zapotlán el Grande')
			db.Cat_municipio_conglomerado.insert(clave_ent='14',clave_mun='124',nombre='Zapotlanejo')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='1',nombre='Acambay de Ruíz Castañeda')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='2',nombre='Acolman')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='3',nombre='Aculco')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='4',nombre='Almoloya de Alquisiras')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='5',nombre='Almoloya de Juárez')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='6',nombre='Almoloya del Río')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='7',nombre='Amanalco')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='8',nombre='Amatepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='9',nombre='Amecameca')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='10',nombre='Apaxco')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='11',nombre='Atenco')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='12',nombre='Atizapán')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='13',nombre='Atizapán de Zaragoza')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='14',nombre='Atlacomulco')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='15',nombre='Atlautla')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='16',nombre='Axapusco')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='17',nombre='Ayapango')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='18',nombre='Calimaya')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='19',nombre='Capulhuac')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='25',nombre='Chalco')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='26',nombre='Chapa de Mota')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='27',nombre='Chapultepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='28',nombre='Chiautla')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='29',nombre='Chicoloapan')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='30',nombre='Chiconcuac')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='31',nombre='Chimalhuacán')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='20',nombre='Coacalco de Berriozábal')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='21',nombre='Coatepec Harinas')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='22',nombre='Cocotitlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='23',nombre='Coyotepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='24',nombre='Cuautitlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='121',nombre='Cuautitlán Izcalli')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='32',nombre='Donato Guerra')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='33',nombre='Ecatepec de Morelos')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='34',nombre='Ecatzingo')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='64',nombre='El Oro')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='35',nombre='Huehuetoca')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='36',nombre='Hueypoxtla')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='37',nombre='Huixquilucan')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='38',nombre='Isidro Fabela')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='39',nombre='Ixtapaluca')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='40',nombre='Ixtapan de la Sal')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='41',nombre='Ixtapan del Oro')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='42',nombre='Ixtlahuaca')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='44',nombre='Jaltenco')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='45',nombre='Jilotepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='46',nombre='Jilotzingo')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='47',nombre='Jiquipilco')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='48',nombre='Jocotitlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='49',nombre='Joquicingo')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='50',nombre='Juchitepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='70',nombre='La Paz')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='51',nombre='Lerma')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='123',nombre='Luvianos')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='52',nombre='Malinalco')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='53',nombre='Melchor Ocampo')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='54',nombre='Metepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='55',nombre='Mexicaltzingo')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='56',nombre='Morelos')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='57',nombre='Naucalpan de Juárez')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='59',nombre='Nextlalpan')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='58',nombre='Nezahualcóyotl')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='60',nombre='Nicolás Romero')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='61',nombre='Nopaltepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='62',nombre='Ocoyoacac')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='63',nombre='Ocuilan')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='65',nombre='Otumba')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='66',nombre='Otzoloapan')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='67',nombre='Otzolotepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='68',nombre='Ozumba')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='69',nombre='Papalotla')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='71',nombre='Polotitlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='72',nombre='Rayón')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='73',nombre='San Antonio la Isla')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='74',nombre='San Felipe del Progreso')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='124',nombre='San José del Rincón')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='75',nombre='San Martín de las Pirámides')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='76',nombre='San Mateo Atenco')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='77',nombre='San Simón de Guerrero')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='78',nombre='Santo Tomás')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='79',nombre='Soyaniquilpan de Juárez')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='80',nombre='Sultepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='81',nombre='Tecámac')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='82',nombre='Tejupilco')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='83',nombre='Temamatla')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='84',nombre='Temascalapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='85',nombre='Temascalcingo')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='86',nombre='Temascaltepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='87',nombre='Temoaya')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='88',nombre='Tenancingo')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='89',nombre='Tenango del Aire')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='90',nombre='Tenango del Valle')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='91',nombre='Teoloyucan')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='92',nombre='Teotihuacán')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='93',nombre='Tepetlaoxtoc')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='94',nombre='Tepetlixpa')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='95',nombre='Tepotzotlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='96',nombre='Tequixquiac')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='97',nombre='Texcaltitlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='98',nombre='Texcalyacac')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='99',nombre='Texcoco')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='100',nombre='Tezoyuca')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='101',nombre='Tianguistenco')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='102',nombre='Timilpan')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='103',nombre='Tlalmanalco')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='104',nombre='Tlalnepantla de Baz')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='105',nombre='Tlatlaya')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='106',nombre='Toluca')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='125',nombre='Tonanitla')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='107',nombre='Tonatico')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='108',nombre='Tultepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='109',nombre='Tultitlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='110',nombre='Valle de Bravo')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='122',nombre='Valle de Chalco Solidaridad')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='111',nombre='Villa de Allende')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='112',nombre='Villa del Carbón')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='113',nombre='Villa Guerrero')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='114',nombre='Villa Victoria')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='43',nombre='Xalatlaco')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='115',nombre='Xonacatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='116',nombre='Zacazonapan')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='117',nombre='Zacualpan')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='118',nombre='Zinacantepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='119',nombre='Zumpahuacán')
			db.Cat_municipio_conglomerado.insert(clave_ent='15',clave_mun='120',nombre='Zumpango')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='1',nombre='Acuitzio')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='2',nombre='Aguililla')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='3',nombre='Álvaro Obregón')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='4',nombre='Angamacutiro')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='5',nombre='Angangueo')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='6',nombre='Apatzingán')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='7',nombre='Aporo')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='8',nombre='Aquila')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='9',nombre='Ario')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='10',nombre='Arteaga')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='11',nombre='Briseñas')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='12',nombre='Buenavista')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='13',nombre='Carácuaro')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='21',nombre='Charapan')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='22',nombre='Charo')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='23',nombre='Chavinda')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='24',nombre='Cherán')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='25',nombre='Chilchota')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='26',nombre='Chinicuila')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='27',nombre='Chucándiro')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='28',nombre='Churintzio')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='29',nombre='Churumuco')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='14',nombre='Coahuayana')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='15',nombre='Coalcomán de Vázquez Pallares')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='16',nombre='Coeneo')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='74',nombre='Cojumatlán de Régules')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='17',nombre='Contepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='18',nombre='Copándaro')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='19',nombre='Cotija')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='20',nombre='Cuitzeo')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='30',nombre='Ecuandureo')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='31',nombre='Epitacio Huerta')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='32',nombre='Erongarícuaro')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='33',nombre='Gabriel Zamora')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='34',nombre='Hidalgo')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='36',nombre='Huandacareo')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='37',nombre='Huaniqueo')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='38',nombre='Huetamo')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='39',nombre='Huiramba')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='40',nombre='Indaparapeo')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='41',nombre='Irimbo')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='42',nombre='Ixtlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='43',nombre='Jacona')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='44',nombre='Jiménez')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='45',nombre='Jiquilpan')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='113',nombre='José Sixto Verduzco')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='46',nombre='Juárez')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='47',nombre='Jungapeo')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='35',nombre='La Huacana')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='69',nombre='La Piedad')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='48',nombre='Lagunillas')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='52',nombre='Lázaro Cárdenas')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='75',nombre='Los Reyes')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='49',nombre='Madero')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='50',nombre='Maravatío')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='51',nombre='Marcos Castellanos')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='53',nombre='Morelia')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='54',nombre='Morelos')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='55',nombre='Múgica')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='56',nombre='Nahuatzen')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='57',nombre='Nocupétaro')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='58',nombre='Nuevo Parangaricutiro')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='59',nombre='Nuevo Urecho')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='60',nombre='Numarán')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='61',nombre='Ocampo')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='62',nombre='Pajacuarán')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='63',nombre='Panindícuaro')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='65',nombre='Paracho')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='64',nombre='Parácuaro')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='66',nombre='Pátzcuaro')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='67',nombre='Penjamillo')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='68',nombre='Peribán')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='70',nombre='Purépero')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='71',nombre='Puruándiro')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='72',nombre='Queréndaro')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='73',nombre='Quiroga')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='76',nombre='Sahuayo')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='79',nombre='Salvador Escalante')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='77',nombre='San Lucas')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='78',nombre='Santa Ana Maya')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='80',nombre='Senguio')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='81',nombre='Susupuato')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='82',nombre='Tacámbaro')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='83',nombre='Tancítaro')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='84',nombre='Tangamandapio')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='85',nombre='Tangancícuaro')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='86',nombre='Tanhuato')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='87',nombre='Taretan')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='88',nombre='Tarímbaro')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='89',nombre='Tepalcatepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='90',nombre='Tingambato')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='91',nombre='Tingüindín')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='92',nombre='Tiquicheo de Nicolás Romero')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='93',nombre='Tlalpujahua')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='94',nombre='Tlazazalca')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='95',nombre='Tocumbo')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='96',nombre='Tumbiscatío')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='97',nombre='Turicato')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='98',nombre='Tuxpan')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='99',nombre='Tuzantla')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='100',nombre='Tzintzuntzan')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='101',nombre='Tzitzio')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='102',nombre='Uruapan')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='103',nombre='Venustiano Carranza')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='104',nombre='Villamar')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='105',nombre='Vista Hermosa')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='106',nombre='Yurécuaro')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='107',nombre='Zacapu')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='108',nombre='Zamora')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='109',nombre='Zináparo')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='110',nombre='Zinapécuaro')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='111',nombre='Ziracuaretiro')
			db.Cat_municipio_conglomerado.insert(clave_ent='16',clave_mun='112',nombre='Zitácuaro')
			db.Cat_municipio_conglomerado.insert(clave_ent='17',clave_mun='1',nombre='Amacuzac')
			db.Cat_municipio_conglomerado.insert(clave_ent='17',clave_mun='2',nombre='Atlatlahucan')
			db.Cat_municipio_conglomerado.insert(clave_ent='17',clave_mun='3',nombre='Axochiapan')
			db.Cat_municipio_conglomerado.insert(clave_ent='17',clave_mun='4',nombre='Ayala')
			db.Cat_municipio_conglomerado.insert(clave_ent='17',clave_mun='5',nombre='Coatlán del Río')
			db.Cat_municipio_conglomerado.insert(clave_ent='17',clave_mun='6',nombre='Cuautla')
			db.Cat_municipio_conglomerado.insert(clave_ent='17',clave_mun='7',nombre='Cuernavaca')
			db.Cat_municipio_conglomerado.insert(clave_ent='17',clave_mun='8',nombre='Emiliano Zapata')
			db.Cat_municipio_conglomerado.insert(clave_ent='17',clave_mun='9',nombre='Huitzilac')
			db.Cat_municipio_conglomerado.insert(clave_ent='17',clave_mun='10',nombre='Jantetelco')
			db.Cat_municipio_conglomerado.insert(clave_ent='17',clave_mun='11',nombre='Jiutepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='17',clave_mun='12',nombre='Jojutla')
			db.Cat_municipio_conglomerado.insert(clave_ent='17',clave_mun='13',nombre='Jonacatepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='17',clave_mun='14',nombre='Mazatepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='17',clave_mun='15',nombre='Miacatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='17',clave_mun='16',nombre='Ocuituco')
			db.Cat_municipio_conglomerado.insert(clave_ent='17',clave_mun='17',nombre='Puente de Ixtla')
			db.Cat_municipio_conglomerado.insert(clave_ent='17',clave_mun='18',nombre='Temixco')
			db.Cat_municipio_conglomerado.insert(clave_ent='17',clave_mun='33',nombre='Temoac')
			db.Cat_municipio_conglomerado.insert(clave_ent='17',clave_mun='19',nombre='Tepalcingo')
			db.Cat_municipio_conglomerado.insert(clave_ent='17',clave_mun='20',nombre='Tepoztlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='17',clave_mun='21',nombre='Tetecala')
			db.Cat_municipio_conglomerado.insert(clave_ent='17',clave_mun='22',nombre='Tetela del Volcán')
			db.Cat_municipio_conglomerado.insert(clave_ent='17',clave_mun='23',nombre='Tlalnepantla')
			db.Cat_municipio_conglomerado.insert(clave_ent='17',clave_mun='24',nombre='Tlaltizapán de Zapata')
			db.Cat_municipio_conglomerado.insert(clave_ent='17',clave_mun='25',nombre='Tlaquiltenango')
			db.Cat_municipio_conglomerado.insert(clave_ent='17',clave_mun='26',nombre='Tlayacapan')
			db.Cat_municipio_conglomerado.insert(clave_ent='17',clave_mun='27',nombre='Totolapan')
			db.Cat_municipio_conglomerado.insert(clave_ent='17',clave_mun='28',nombre='Xochitepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='17',clave_mun='29',nombre='Yautepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='17',clave_mun='30',nombre='Yecapixtla')
			db.Cat_municipio_conglomerado.insert(clave_ent='17',clave_mun='31',nombre='Zacatepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='17',clave_mun='32',nombre='Zacualpan')
			db.Cat_municipio_conglomerado.insert(clave_ent='18',clave_mun='1',nombre='Acaponeta')
			db.Cat_municipio_conglomerado.insert(clave_ent='18',clave_mun='2',nombre='Ahuacatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='18',clave_mun='3',nombre='Amatlán de Cañas')
			db.Cat_municipio_conglomerado.insert(clave_ent='18',clave_mun='20',nombre='Bahía de Banderas')
			db.Cat_municipio_conglomerado.insert(clave_ent='18',clave_mun='4',nombre='Compostela')
			db.Cat_municipio_conglomerado.insert(clave_ent='18',clave_mun='9',nombre='Del Nayar')
			db.Cat_municipio_conglomerado.insert(clave_ent='18',clave_mun='5',nombre='Huajicori')
			db.Cat_municipio_conglomerado.insert(clave_ent='18',clave_mun='6',nombre='Ixtlán del Río')
			db.Cat_municipio_conglomerado.insert(clave_ent='18',clave_mun='7',nombre='Jala')
			db.Cat_municipio_conglomerado.insert(clave_ent='18',clave_mun='19',nombre='La Yesca')
			db.Cat_municipio_conglomerado.insert(clave_ent='18',clave_mun='10',nombre='Rosamorada')
			db.Cat_municipio_conglomerado.insert(clave_ent='18',clave_mun='11',nombre='Ruíz')
			db.Cat_municipio_conglomerado.insert(clave_ent='18',clave_mun='12',nombre='San Blas')
			db.Cat_municipio_conglomerado.insert(clave_ent='18',clave_mun='13',nombre='San Pedro Lagunillas')
			db.Cat_municipio_conglomerado.insert(clave_ent='18',clave_mun='14',nombre='Santa María del Oro')
			db.Cat_municipio_conglomerado.insert(clave_ent='18',clave_mun='15',nombre='Santiago Ixcuintla')
			db.Cat_municipio_conglomerado.insert(clave_ent='18',clave_mun='16',nombre='Tecuala')
			db.Cat_municipio_conglomerado.insert(clave_ent='18',clave_mun='17',nombre='Tepic')
			db.Cat_municipio_conglomerado.insert(clave_ent='18',clave_mun='18',nombre='Tuxpan')
			db.Cat_municipio_conglomerado.insert(clave_ent='18',clave_mun='8',nombre='Xalisco')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='1',nombre='Abasolo')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='2',nombre='Agualeguas')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='4',nombre='Allende')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='5',nombre='Anáhuac')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='6',nombre='Apodaca')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='7',nombre='Aramberri')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='8',nombre='Bustamante')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='9',nombre='Cadereyta Jiménez')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='11',nombre='Cerralvo')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='13',nombre='China')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='12',nombre='Ciénega de Flores')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='14',nombre='Doctor Arroyo')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='15',nombre='Doctor Coss')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='16',nombre='Doctor González')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='10',nombre='El Carmen')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='17',nombre='Galeana')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='18',nombre='García')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='20',nombre='General Bravo')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='21',nombre='General Escobedo')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='22',nombre='General Terán')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='23',nombre='General Treviño')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='24',nombre='General Zaragoza')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='25',nombre='General Zuazua')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='26',nombre='Guadalupe')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='47',nombre='Hidalgo')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='28',nombre='Higueras')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='29',nombre='Hualahuises')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='30',nombre='Iturbide')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='31',nombre='Juárez')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='32',nombre='Lampazos de Naranjo')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='33',nombre='Linares')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='3',nombre='Los Aldamas')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='27',nombre='Los Herreras')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='42',nombre='Los Ramones')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='34',nombre='Marín')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='35',nombre='Melchor Ocampo')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='36',nombre='Mier y Noriega')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='37',nombre='Mina')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='38',nombre='Montemorelos')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='39',nombre='Monterrey')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='40',nombre='Parás')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='41',nombre='Pesquería')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='43',nombre='Rayones')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='44',nombre='Sabinas Hidalgo')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='45',nombre='Salinas Victoria')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='46',nombre='San Nicolás de los Garza')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='19',nombre='San Pedro Garza García')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='48',nombre='Santa Catarina')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='49',nombre='Santiago')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='50',nombre='Vallecillo')
			db.Cat_municipio_conglomerado.insert(clave_ent='19',clave_mun='51',nombre='Villaldama')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='1',nombre='Abejones')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='2',nombre='Acatlán de Pérez Figueroa')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='174',nombre='Ánimas Trujano')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='3',nombre='Asunción Cacalotepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='4',nombre='Asunción Cuyotepeji')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='5',nombre='Asunción Ixtaltepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='6',nombre='Asunción Nochixtlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='7',nombre='Asunción Ocotlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='8',nombre='Asunción Tlacolulita')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='398',nombre='Ayoquezco de Aldama')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='9',nombre='Ayotzintepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='11',nombre='Calihualá')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='12',nombre='Candelaria Loxicha')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='247',nombre='Capulálpam de Méndez')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='25',nombre='Chahuites')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='26',nombre='Chalcatongo de Hidalgo')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='27',nombre='Chiquihuitlán de Benito Juárez')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='13',nombre='Ciénega de Zimatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='14',nombre='Ciudad Ixtepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='15',nombre='Coatecas Altas')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='16',nombre='Coicoyán de las Flores')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='18',nombre='Concepción Buenavista')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='19',nombre='Concepción Pápalo')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='20',nombre='Constancia del Rosario')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='21',nombre='Cosolapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='22',nombre='Cosoltepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='23',nombre='Cuilápam de Guerrero')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='24',nombre='Cuyamecalco Villa de Zaragoza')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='10',nombre='El Barrio de la Soledad')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='30',nombre='El Espinal')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='29',nombre='Eloxochitlán de Flores Magón')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='32',nombre='Fresnillo de Trujano')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='34',nombre='Guadalupe de Ramírez')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='33',nombre='Guadalupe Etla')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='35',nombre='Guelatao de Juárez')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='36',nombre='Guevea de Humboldt')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='28',nombre='Heroica Ciudad de Ejutla de Crespo')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='39',nombre='Heroica Ciudad de Huajuapan de León')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='43',nombre='Heroica Ciudad de Juchitán de Zaragoza')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='397',nombre='Heroica Ciudad de Tlaxiaco')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='549',nombre='Heroica Villa Tezoatlán de Segura y Luna, Cuna de la Independencia de Oaxaca')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='40',nombre='Huautepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='41',nombre='Huautla de Jiménez')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='65',nombre='Ixpantepec Nieves')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='42',nombre='Ixtlán de Juárez')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='17',nombre='La Compañía')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='69',nombre='La Pe')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='76',nombre='La Reforma')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='556',nombre='La Trinidad Vista Hermosa')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='44',nombre='Loma Bonita')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='45',nombre='Magdalena Apasco')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='46',nombre='Magdalena Jaltepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='48',nombre='Magdalena Mixtepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='49',nombre='Magdalena Ocotlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='50',nombre='Magdalena Peñasco')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='51',nombre='Magdalena Teitipac')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='52',nombre='Magdalena Tequisistlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='53',nombre='Magdalena Tlacotepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='562',nombre='Magdalena Yodocono de Porfirio Díaz')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='54',nombre='Magdalena Zahuatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='55',nombre='Mariscala de Juárez')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='56',nombre='Mártires de Tacubaya')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='57',nombre='Matías Romero Avendaño')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='58',nombre='Mazatlán Villa de Flores')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='37',nombre='Mesones Hidalgo')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='59',nombre='Miahuatlán de Porfirio Díaz')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='60',nombre='Mixistlán de la Reforma')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='61',nombre='Monjas')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='62',nombre='Natividad')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='63',nombre='Nazareno Etla')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='64',nombre='Nejapa de Madero')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='504',nombre='Nuevo Zoquiápam')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='67',nombre='Oaxaca de Juárez')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='68',nombre='Ocotlán de Morelos')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='70',nombre='Pinotepa de Don Luis')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='71',nombre='Pluma Hidalgo')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='73',nombre='Putla Villa de Guerrero')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='75',nombre='Reforma de Pineda')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='77',nombre='Reyes Etla')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='78',nombre='Rojas de Cuauhtémoc')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='79',nombre='Salina Cruz')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='80',nombre='San Agustín Amatengo')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='81',nombre='San Agustín Atenango')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='82',nombre='San Agustín Chayuco')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='83',nombre='San Agustín de las Juntas')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='84',nombre='San Agustín Etla')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='85',nombre='San Agustín Loxicha')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='86',nombre='San Agustín Tlacotepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='87',nombre='San Agustín Yatareni')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='88',nombre='San Andrés Cabecera Nueva')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='89',nombre='San Andrés Dinicuiti')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='90',nombre='San Andrés Huaxpaltepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='91',nombre='San Andrés Huayápam')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='92',nombre='San Andrés Ixtlahuaca')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='93',nombre='San Andrés Lagunas')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='94',nombre='San Andrés Nuxiño')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='95',nombre='San Andrés Paxtlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='96',nombre='San Andrés Sinaxtla')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='97',nombre='San Andrés Solaga')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='98',nombre='San Andrés Teotilálpam')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='99',nombre='San Andrés Tepetlapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='100',nombre='San Andrés Yaá')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='101',nombre='San Andrés Zabache')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='102',nombre='San Andrés Zautla')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='103',nombre='San Antonino Castillo Velasco')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='104',nombre='San Antonino el Alto')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='105',nombre='San Antonino Monte Verde')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='106',nombre='San Antonio Acutla')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='107',nombre='San Antonio de la Cal')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='108',nombre='San Antonio Huitepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='109',nombre='San Antonio Nanahuatípam')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='110',nombre='San Antonio Sinicahua')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='111',nombre='San Antonio Tepetlapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='112',nombre='San Baltazar Chichicápam')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='113',nombre='San Baltazar Loxicha')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='114',nombre='San Baltazar Yatzachi el Bajo')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='115',nombre='San Bartolo Coyotepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='121',nombre='San Bartolo Soyaltepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='122',nombre='San Bartolo Yautepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='116',nombre='San Bartolomé Ayautla')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='117',nombre='San Bartolomé Loxicha')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='118',nombre='San Bartolomé Quialana')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='119',nombre='San Bartolomé Yucuañe')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='120',nombre='San Bartolomé Zoogocho')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='123',nombre='San Bernardo Mixtepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='124',nombre='San Blas Atempa')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='125',nombre='San Carlos Yautepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='126',nombre='San Cristóbal Amatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='127',nombre='San Cristóbal Amoltepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='128',nombre='San Cristóbal Lachirioag')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='129',nombre='San Cristóbal Suchixtlahuaca')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='130',nombre='San Dionisio del Mar')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='131',nombre='San Dionisio Ocotepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='132',nombre='San Dionisio Ocotlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='133',nombre='San Esteban Atatlahuca')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='134',nombre='San Felipe Jalapa de Díaz')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='135',nombre='San Felipe Tejalápam')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='136',nombre='San Felipe Usila')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='137',nombre='San Francisco Cahuacuá')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='138',nombre='San Francisco Cajonos')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='139',nombre='San Francisco Chapulapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='140',nombre='San Francisco Chindúa')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='141',nombre='San Francisco del Mar')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='142',nombre='San Francisco Huehuetlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='143',nombre='San Francisco Ixhuatán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='144',nombre='San Francisco Jaltepetongo')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='145',nombre='San Francisco Lachigoló')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='146',nombre='San Francisco Logueche')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='147',nombre='San Francisco Nuxaño')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='148',nombre='San Francisco Ozolotepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='149',nombre='San Francisco Sola')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='150',nombre='San Francisco Telixtlahuaca')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='151',nombre='San Francisco Teopan')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='152',nombre='San Francisco Tlapancingo')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='153',nombre='San Gabriel Mixtepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='154',nombre='San Ildefonso Amatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='155',nombre='San Ildefonso Sola')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='156',nombre='San Ildefonso Villa Alta')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='157',nombre='San Jacinto Amilpas')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='158',nombre='San Jacinto Tlacotepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='159',nombre='San Jerónimo Coatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='160',nombre='San Jerónimo Silacayoapilla')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='161',nombre='San Jerónimo Sosola')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='162',nombre='San Jerónimo Taviche')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='163',nombre='San Jerónimo Tecóatl')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='550',nombre='San Jerónimo Tlacochahuaya')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='164',nombre='San Jorge Nuchita')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='165',nombre='San José Ayuquila')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='166',nombre='San José Chiltepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='167',nombre='San José del Peñasco')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='72',nombre='San José del Progreso')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='168',nombre='San José Estancia Grande')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='169',nombre='San José Independencia')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='170',nombre='San José Lachiguiri')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='171',nombre='San José Tenango')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='172',nombre='San Juan Achiutla')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='173',nombre='San Juan Atepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='175',nombre='San Juan Bautista Atatlahuca')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='176',nombre='San Juan Bautista Coixtlahuaca')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='177',nombre='San Juan Bautista Cuicatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='178',nombre='San Juan Bautista Guelache')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='179',nombre='San Juan Bautista Jayacatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='180',nombre='San Juan Bautista Lo de Soto')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='181',nombre='San Juan Bautista Suchitepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='183',nombre='San Juan Bautista Tlachichilco')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='182',nombre='San Juan Bautista Tlacoatzintepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='184',nombre='San Juan Bautista Tuxtepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='559',nombre='San Juan Bautista Valle Nacional')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='185',nombre='San Juan Cacahuatepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='191',nombre='San Juan Chicomezúchil')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='192',nombre='San Juan Chilateca')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='186',nombre='San Juan Cieneguilla')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='187',nombre='San Juan Coatzóspam')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='188',nombre='San Juan Colorado')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='189',nombre='San Juan Comaltepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='190',nombre='San Juan Cotzocón')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='206',nombre='San Juan de los Cués')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='193',nombre='San Juan del Estado')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='194',nombre='San Juan del Río')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='195',nombre='San Juan Diuxi')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='196',nombre='San Juan Evangelista Analco')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='197',nombre='San Juan Guelavía')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='198',nombre='San Juan Guichicovi')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='199',nombre='San Juan Ihualtepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='200',nombre='San Juan Juquila Mixes')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='201',nombre='San Juan Juquila Vijanos')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='202',nombre='San Juan Lachao')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='203',nombre='San Juan Lachigalla')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='204',nombre='San Juan Lajarcia')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='205',nombre='San Juan Lalana')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='207',nombre='San Juan Mazatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='208',nombre='San Juan Mixtepec (208)')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='209',nombre='San Juan Mixtepec (209)')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='210',nombre='San Juan Ñumí')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='211',nombre='San Juan Ozolotepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='212',nombre='San Juan Petlapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='213',nombre='San Juan Quiahije')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='214',nombre='San Juan Quiotepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='215',nombre='San Juan Sayultepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='216',nombre='San Juan Tabaá')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='217',nombre='San Juan Tamazola')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='218',nombre='San Juan Teita')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='219',nombre='San Juan Teitipac')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='220',nombre='San Juan Tepeuxila')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='221',nombre='San Juan Teposcolula')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='222',nombre='San Juan Yaeé')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='223',nombre='San Juan Yatzona')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='224',nombre='San Juan Yucuita')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='225',nombre='San Lorenzo')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='226',nombre='San Lorenzo Albarradas')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='227',nombre='San Lorenzo Cacaotepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='228',nombre='San Lorenzo Cuaunecuiltitla')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='229',nombre='San Lorenzo Texmelúcan')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='230',nombre='San Lorenzo Victoria')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='231',nombre='San Lucas Camotlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='232',nombre='San Lucas Ojitlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='233',nombre='San Lucas Quiaviní')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='234',nombre='San Lucas Zoquiápam')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='235',nombre='San Luis Amatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='236',nombre='San Marcial Ozolotepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='237',nombre='San Marcos Arteaga')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='238',nombre='San Martín de los Cansecos')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='239',nombre='San Martín Huamelúlpam')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='240',nombre='San Martín Itunyoso')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='241',nombre='San Martín Lachilá')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='242',nombre='San Martín Peras')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='243',nombre='San Martín Tilcajete')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='244',nombre='San Martín Toxpalan')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='245',nombre='San Martín Zacatepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='246',nombre='San Mateo Cajonos')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='248',nombre='San Mateo del Mar')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='250',nombre='San Mateo Etlatongo')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='251',nombre='San Mateo Nejápam')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='252',nombre='San Mateo Peñasco')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='253',nombre='San Mateo Piñas')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='254',nombre='San Mateo Río Hondo')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='255',nombre='San Mateo Sindihui')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='256',nombre='San Mateo Tlapiltepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='249',nombre='San Mateo Yoloxochitlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='566',nombre='San Mateo Yucutindoo')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='257',nombre='San Melchor Betaza')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='258',nombre='San Miguel Achiutla')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='259',nombre='San Miguel Ahuehuetitlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='260',nombre='San Miguel Aloápam')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='261',nombre='San Miguel Amatitlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='262',nombre='San Miguel Amatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='264',nombre='San Miguel Chicahua')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='265',nombre='San Miguel Chimalapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='263',nombre='San Miguel Coatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='266',nombre='San Miguel del Puerto')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='267',nombre='San Miguel del Río')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='268',nombre='San Miguel Ejutla')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='269',nombre='San Miguel el Grande')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='270',nombre='San Miguel Huautla')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='271',nombre='San Miguel Mixtepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='272',nombre='San Miguel Panixtlahuaca')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='273',nombre='San Miguel Peras')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='274',nombre='San Miguel Piedras')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='275',nombre='San Miguel Quetzaltepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='276',nombre='San Miguel Santa Flor')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='278',nombre='San Miguel Soyaltepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='279',nombre='San Miguel Suchixtepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='281',nombre='San Miguel Tecomatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='282',nombre='San Miguel Tenango')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='283',nombre='San Miguel Tequixtepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='284',nombre='San Miguel Tilquiápam')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='285',nombre='San Miguel Tlacamama')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='286',nombre='San Miguel Tlacotepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='287',nombre='San Miguel Tulancingo')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='288',nombre='San Miguel Yotao')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='289',nombre='San Nicolás')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='290',nombre='San Nicolás Hidalgo')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='291',nombre='San Pablo Coatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='292',nombre='San Pablo Cuatro Venados')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='293',nombre='San Pablo Etla')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='294',nombre='San Pablo Huitzo')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='295',nombre='San Pablo Huixtepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='296',nombre='San Pablo Macuiltianguis')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='297',nombre='San Pablo Tijaltepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='298',nombre='San Pablo Villa de Mitla')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='299',nombre='San Pablo Yaganiza')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='300',nombre='San Pedro Amuzgos')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='301',nombre='San Pedro Apóstol')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='302',nombre='San Pedro Atoyac')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='303',nombre='San Pedro Cajonos')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='305',nombre='San Pedro Comitancillo')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='304',nombre='San Pedro Coxcaltepec Cántaros')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='306',nombre='San Pedro el Alto')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='307',nombre='San Pedro Huamelula')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='308',nombre='San Pedro Huilotepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='309',nombre='San Pedro Ixcatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='310',nombre='San Pedro Ixtlahuaca')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='311',nombre='San Pedro Jaltepetongo')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='312',nombre='San Pedro Jicayán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='313',nombre='San Pedro Jocotipac')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='314',nombre='San Pedro Juchatengo')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='315',nombre='San Pedro Mártir')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='316',nombre='San Pedro Mártir Quiechapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='317',nombre='San Pedro Mártir Yucuxaco')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='318',nombre='San Pedro Mixtepec (318)')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='319',nombre='San Pedro Mixtepec (319)')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='320',nombre='San Pedro Molinos')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='321',nombre='San Pedro Nopala')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='322',nombre='San Pedro Ocopetatillo')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='323',nombre='San Pedro Ocotepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='324',nombre='San Pedro Pochutla')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='325',nombre='San Pedro Quiatoni')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='326',nombre='San Pedro Sochiápam')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='327',nombre='San Pedro Tapanatepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='328',nombre='San Pedro Taviche')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='329',nombre='San Pedro Teozacoalco')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='330',nombre='San Pedro Teutila')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='331',nombre='San Pedro Tidaá')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='332',nombre='San Pedro Topiltepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='333',nombre='San Pedro Totolápam')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='337',nombre='San Pedro y San Pablo Ayutla')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='339',nombre='San Pedro y San Pablo Teposcolula')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='340',nombre='San Pedro y San Pablo Tequixtepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='335',nombre='San Pedro Yaneri')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='336',nombre='San Pedro Yólox')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='341',nombre='San Pedro Yucunama')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='342',nombre='San Raymundo Jalpan')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='343',nombre='San Sebastián Abasolo')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='344',nombre='San Sebastián Coatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='345',nombre='San Sebastián Ixcapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='346',nombre='San Sebastián Nicananduta')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='347',nombre='San Sebastián Río Hondo')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='348',nombre='San Sebastián Tecomaxtlahuaca')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='349',nombre='San Sebastián Teitipac')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='350',nombre='San Sebastián Tutla')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='351',nombre='San Simón Almolongas')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='352',nombre='San Simón Zahuatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='534',nombre='San Vicente Coatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='535',nombre='San Vicente Lachixío')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='536',nombre='San Vicente Nuñú')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='353',nombre='Santa Ana')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='354',nombre='Santa Ana Ateixtlahuaca')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='355',nombre='Santa Ana Cuauhtémoc')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='356',nombre='Santa Ana del Valle')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='357',nombre='Santa Ana Tavela')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='358',nombre='Santa Ana Tlapacoyan')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='359',nombre='Santa Ana Yareni')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='360',nombre='Santa Ana Zegache')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='361',nombre='Santa Catalina Quierí')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='362',nombre='Santa Catarina Cuixtla')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='363',nombre='Santa Catarina Ixtepeji')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='364',nombre='Santa Catarina Juquila')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='365',nombre='Santa Catarina Lachatao')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='366',nombre='Santa Catarina Loxicha')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='367',nombre='Santa Catarina Mechoacán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='368',nombre='Santa Catarina Minas')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='369',nombre='Santa Catarina Quiané')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='74',nombre='Santa Catarina Quioquitani')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='370',nombre='Santa Catarina Tayata')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='371',nombre='Santa Catarina Ticuá')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='372',nombre='Santa Catarina Yosonotú')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='373',nombre='Santa Catarina Zapoquila')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='374',nombre='Santa Cruz Acatepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='375',nombre='Santa Cruz Amilpas')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='376',nombre='Santa Cruz de Bravo')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='377',nombre='Santa Cruz Itundujia')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='378',nombre='Santa Cruz Mixtepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='379',nombre='Santa Cruz Nundaco')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='380',nombre='Santa Cruz Papalutla')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='381',nombre='Santa Cruz Tacache de Mina')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='382',nombre='Santa Cruz Tacahua')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='383',nombre='Santa Cruz Tayata')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='384',nombre='Santa Cruz Xitla')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='385',nombre='Santa Cruz Xoxocotlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='386',nombre='Santa Cruz Zenzontepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='387',nombre='Santa Gertrudis')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='569',nombre='Santa Inés de Zaragoza')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='388',nombre='Santa Inés del Monte')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='389',nombre='Santa Inés Yatzeche')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='390',nombre='Santa Lucía del Camino')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='391',nombre='Santa Lucía Miahuatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='392',nombre='Santa Lucía Monteverde')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='393',nombre='Santa Lucía Ocotlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='47',nombre='Santa Magdalena Jicotlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='394',nombre='Santa María Alotepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='395',nombre='Santa María Apazco')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='399',nombre='Santa María Atzompa')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='400',nombre='Santa María Camotlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='404',nombre='Santa María Chachoápam')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='406',nombre='Santa María Chilchotla')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='407',nombre='Santa María Chimalapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='401',nombre='Santa María Colotepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='402',nombre='Santa María Cortijo')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='403',nombre='Santa María Coyotepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='408',nombre='Santa María del Rosario')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='409',nombre='Santa María del Tule')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='410',nombre='Santa María Ecatepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='411',nombre='Santa María Guelacé')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='412',nombre='Santa María Guienagati')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='413',nombre='Santa María Huatulco')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='414',nombre='Santa María Huazolotitlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='415',nombre='Santa María Ipalapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='416',nombre='Santa María Ixcatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='417',nombre='Santa María Jacatepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='418',nombre='Santa María Jalapa del Marqués')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='419',nombre='Santa María Jaltianguis')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='396',nombre='Santa María la Asunción')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='420',nombre='Santa María Lachixío')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='421',nombre='Santa María Mixtequilla')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='422',nombre='Santa María Nativitas')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='423',nombre='Santa María Nduayaco')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='424',nombre='Santa María Ozolotepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='425',nombre='Santa María Pápalo')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='426',nombre='Santa María Peñoles')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='427',nombre='Santa María Petapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='428',nombre='Santa María Quiegolani')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='429',nombre='Santa María Sola')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='430',nombre='Santa María Tataltepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='431',nombre='Santa María Tecomavaca')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='432',nombre='Santa María Temaxcalapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='433',nombre='Santa María Temaxcaltepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='434',nombre='Santa María Teopoxco')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='435',nombre='Santa María Tepantlali')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='436',nombre='Santa María Texcatitlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='437',nombre='Santa María Tlahuitoltepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='438',nombre='Santa María Tlalixtac')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='439',nombre='Santa María Tonameca')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='440',nombre='Santa María Totolapilla')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='441',nombre='Santa María Xadani')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='442',nombre='Santa María Yalina')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='443',nombre='Santa María Yavesía')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='444',nombre='Santa María Yolotepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='445',nombre='Santa María Yosoyúa')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='446',nombre='Santa María Yucuhiti')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='447',nombre='Santa María Zacatepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='448',nombre='Santa María Zaniza')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='449',nombre='Santa María Zoquitlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='450',nombre='Santiago Amoltepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='451',nombre='Santiago Apoala')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='452',nombre='Santiago Apóstol')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='453',nombre='Santiago Astata')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='454',nombre='Santiago Atitlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='455',nombre='Santiago Ayuquililla')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='456',nombre='Santiago Cacaloxtepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='457',nombre='Santiago Camotlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='459',nombre='Santiago Chazumba')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='460',nombre='Santiago Choápam')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='458',nombre='Santiago Comaltepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='461',nombre='Santiago del Río')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='462',nombre='Santiago Huajolotitlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='463',nombre='Santiago Huauclilla')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='464',nombre='Santiago Ihuitlán Plumas')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='465',nombre='Santiago Ixcuintepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='466',nombre='Santiago Ixtayutla')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='467',nombre='Santiago Jamiltepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='468',nombre='Santiago Jocotepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='469',nombre='Santiago Juxtlahuaca')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='470',nombre='Santiago Lachiguiri')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='471',nombre='Santiago Lalopa')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='472',nombre='Santiago Laollaga')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='473',nombre='Santiago Laxopa')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='474',nombre='Santiago Llano Grande')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='475',nombre='Santiago Matatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='476',nombre='Santiago Miltepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='477',nombre='Santiago Minas')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='478',nombre='Santiago Nacaltepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='479',nombre='Santiago Nejapilla')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='66',nombre='Santiago Niltepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='480',nombre='Santiago Nundiche')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='481',nombre='Santiago Nuyoó')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='482',nombre='Santiago Pinotepa Nacional')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='483',nombre='Santiago Suchilquitongo')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='484',nombre='Santiago Tamazola')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='485',nombre='Santiago Tapextla')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='487',nombre='Santiago Tenango')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='488',nombre='Santiago Tepetlapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='489',nombre='Santiago Tetepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='490',nombre='Santiago Texcalcingo')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='491',nombre='Santiago Textitlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='492',nombre='Santiago Tilantongo')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='493',nombre='Santiago Tillo')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='494',nombre='Santiago Tlazoyaltepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='495',nombre='Santiago Xanica')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='496',nombre='Santiago Xiacuí')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='497',nombre='Santiago Yaitepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='498',nombre='Santiago Yaveo')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='499',nombre='Santiago Yolomécatl')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='500',nombre='Santiago Yosondúa')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='501',nombre='Santiago Yucuyachi')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='502',nombre='Santiago Zacatepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='503',nombre='Santiago Zoochila')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='506',nombre='Santo Domingo Albarradas')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='507',nombre='Santo Domingo Armenta')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='508',nombre='Santo Domingo Chihuitán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='509',nombre='Santo Domingo de Morelos')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='505',nombre='Santo Domingo Ingenio')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='510',nombre='Santo Domingo Ixcatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='511',nombre='Santo Domingo Nuxaá')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='512',nombre='Santo Domingo Ozolotepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='513',nombre='Santo Domingo Petapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='514',nombre='Santo Domingo Roayaga')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='515',nombre='Santo Domingo Tehuantepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='516',nombre='Santo Domingo Teojomulco')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='517',nombre='Santo Domingo Tepuxtepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='518',nombre='Santo Domingo Tlatayápam')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='519',nombre='Santo Domingo Tomaltepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='520',nombre='Santo Domingo Tonalá')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='521',nombre='Santo Domingo Tonaltepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='522',nombre='Santo Domingo Xagacía')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='523',nombre='Santo Domingo Yanhuitlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='524',nombre='Santo Domingo Yodohino')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='525',nombre='Santo Domingo Zanatepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='530',nombre='Santo Tomás Jalieza')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='531',nombre='Santo Tomás Mazaltepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='532',nombre='Santo Tomás Ocotepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='533',nombre='Santo Tomás Tamazulapan')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='526',nombre='Santos Reyes Nopala')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='527',nombre='Santos Reyes Pápalo')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='528',nombre='Santos Reyes Tepejillo')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='529',nombre='Santos Reyes Yucuná')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='537',nombre='Silacayoápam')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='538',nombre='Sitio de Xitlapehua')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='539',nombre='Soledad Etla')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='31',nombre='Tamazulápam del Espíritu Santo')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='541',nombre='Tanetze de Zaragoza')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='542',nombre='Taniche')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='543',nombre='Tataltepec de Valdés')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='544',nombre='Teococuilco de Marcos Pérez')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='545',nombre='Teotitlán de Flores Magón')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='546',nombre='Teotitlán del Valle')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='547',nombre='Teotongo')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='548',nombre='Tepelmeme Villa de Morelos')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='551',nombre='Tlacolula de Matamoros')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='552',nombre='Tlacotepec Plumas')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='553',nombre='Tlalixtac de Cabrera')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='554',nombre='Totontepec Villa de Morelos')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='555',nombre='Trinidad Zaachila')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='557',nombre='Unión Hidalgo')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='558',nombre='Valerio Trujano')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='405',nombre='Villa de Chilapa de Díaz')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='338',nombre='Villa de Etla')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='540',nombre='Villa de Tamazulápam del Progreso')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='334',nombre='Villa de Tututepec de Melchor Ocampo')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='565',nombre='Villa de Zaachila')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='560',nombre='Villa Díaz Ordaz')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='38',nombre='Villa Hidalgo')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='277',nombre='Villa Sola de Vega')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='280',nombre='Villa Talea de Castro')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='486',nombre='Villa Tejúpam de la Unión')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='561',nombre='Yaxe')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='563',nombre='Yogana')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='564',nombre='Yutanduchi de Guerrero')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='567',nombre='Zapotitlán Lagunas')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='568',nombre='Zapotitlán Palmas')
			db.Cat_municipio_conglomerado.insert(clave_ent='20',clave_mun='570',nombre='Zimatlán de Álvarez')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='1',nombre='Acajete')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='2',nombre='Acateno')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='3',nombre='Acatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='4',nombre='Acatzingo')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='5',nombre='Acteopan')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='6',nombre='Ahuacatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='7',nombre='Ahuatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='8',nombre='Ahuazotepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='9',nombre='Ahuehuetitla')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='10',nombre='Ajalpan')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='11',nombre='Albino Zertuche')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='12',nombre='Aljojuca')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='13',nombre='Altepexi')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='14',nombre='Amixtlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='15',nombre='Amozoc')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='16',nombre='Aquixtla')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='17',nombre='Atempan')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='18',nombre='Atexcal')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='80',nombre='Atlequizayan')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='19',nombre='Atlixco')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='20',nombre='Atoyatempan')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='21',nombre='Atzala')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='22',nombre='Atzitzihuacán')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='23',nombre='Atzitzintla')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='24',nombre='Axutla')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='25',nombre='Ayotoxco de Guerrero')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='26',nombre='Calpan')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='27',nombre='Caltepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='28',nombre='Camocuautla')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='99',nombre='Cañada Morelos')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='29',nombre='Caxhuacan')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='45',nombre='Chalchicomula de Sesma')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='46',nombre='Chapulco')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='47',nombre='Chiautla')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='48',nombre='Chiautzingo')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='50',nombre='Chichiquila')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='49',nombre='Chiconcuautla')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='51',nombre='Chietla')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='52',nombre='Chigmecatitlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='53',nombre='Chignahuapan')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='54',nombre='Chignautla')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='55',nombre='Chila')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='56',nombre='Chila de la Sal')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='58',nombre='Chilchotla')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='59',nombre='Chinantla')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='30',nombre='Coatepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='31',nombre='Coatzingo')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='32',nombre='Cohetzala')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='33',nombre='Cohuecan')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='34',nombre='Coronango')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='35',nombre='Coxcatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='36',nombre='Coyomeapan')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='37',nombre='Coyotepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='38',nombre='Cuapiaxtla de Madero')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='39',nombre='Cuautempan')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='40',nombre='Cuautinchán')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='41',nombre='Cuautlancingo')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='42',nombre='Cuayuca de Andrade')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='43',nombre='Cuetzalan del Progreso')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='44',nombre='Cuyoaco')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='60',nombre='Domingo Arenas')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='61',nombre='Eloxochitlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='62',nombre='Epatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='63',nombre='Esperanza')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='64',nombre='Francisco Z. Mena')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='65',nombre='General Felipe Ángeles')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='66',nombre='Guadalupe')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='67',nombre='Guadalupe Victoria')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='68',nombre='Hermenegildo Galeana')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='57',nombre='Honey')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='69',nombre='Huaquechula')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='70',nombre='Huatlatlauca')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='71',nombre='Huauchinango')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='72',nombre='Huehuetla')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='73',nombre='Huehuetlán el Chico')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='150',nombre='Huehuetlán el Grande')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='74',nombre='Huejotzingo')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='75',nombre='Hueyapan')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='76',nombre='Hueytamalco')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='77',nombre='Hueytlalpan')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='78',nombre='Huitzilan de Serdán')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='79',nombre='Huitziltepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='81',nombre='Ixcamilpa de Guerrero')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='82',nombre='Ixcaquixtla')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='83',nombre='Ixtacamaxtitlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='84',nombre='Ixtepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='85',nombre='Izúcar de Matamoros')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='86',nombre='Jalpan')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='87',nombre='Jolalpan')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='88',nombre='Jonotla')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='89',nombre='Jopala')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='90',nombre='Juan C. Bonilla')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='91',nombre='Juan Galindo')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='92',nombre='Juan N. Méndez')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='95',nombre='La Magdalena Tlatlauquitepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='93',nombre='Lafragua')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='94',nombre='Libres')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='118',nombre='Los Reyes de Juárez')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='96',nombre='Mazapiltepec de Juárez')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='97',nombre='Mixtla')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='98',nombre='Molcaxac')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='100',nombre='Naupan')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='101',nombre='Nauzontla')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='102',nombre='Nealtican')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='103',nombre='Nicolás Bravo')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='104',nombre='Nopalucan')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='105',nombre='Ocotepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='106',nombre='Ocoyucan')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='107',nombre='Olintla')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='108',nombre='Oriental')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='109',nombre='Pahuatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='110',nombre='Palmar de Bravo')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='111',nombre='Pantepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='112',nombre='Petlalcingo')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='113',nombre='Piaxtla')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='114',nombre='Puebla')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='115',nombre='Quecholac')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='116',nombre='Quimixtlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='117',nombre='Rafael Lara Grajales')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='119',nombre='San Andrés Cholula')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='120',nombre='San Antonio Cañada')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='121',nombre='San Diego la Mesa Tochimiltzingo')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='122',nombre='San Felipe Teotlalcingo')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='123',nombre='San Felipe Tepatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='124',nombre='San Gabriel Chilac')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='125',nombre='San Gregorio Atzompa')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='126',nombre='San Jerónimo Tecuanipan')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='127',nombre='San Jerónimo Xayacatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='128',nombre='San José Chiapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='129',nombre='San José Miahuatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='130',nombre='San Juan Atenco')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='131',nombre='San Juan Atzompa')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='132',nombre='San Martín Texmelucan')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='133',nombre='San Martín Totoltepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='134',nombre='San Matías Tlalancaleca')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='135',nombre='San Miguel Ixitlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='136',nombre='San Miguel Xoxtla')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='137',nombre='San Nicolás Buenos Aires')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='138',nombre='San Nicolás de los Ranchos')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='139',nombre='San Pablo Anicano')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='140',nombre='San Pedro Cholula')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='141',nombre='San Pedro Yeloixtlahuaca')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='142',nombre='San Salvador el Seco')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='143',nombre='San Salvador el Verde')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='144',nombre='San Salvador Huixcolotla')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='145',nombre='San Sebastián Tlacotepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='146',nombre='Santa Catarina Tlaltempan')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='147',nombre='Santa Inés Ahuatempan')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='148',nombre='Santa Isabel Cholula')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='149',nombre='Santiago Miahuatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='151',nombre='Santo Tomás Hueyotlipan')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='152',nombre='Soltepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='153',nombre='Tecali de Herrera')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='154',nombre='Tecamachalco')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='155',nombre='Tecomatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='156',nombre='Tehuacán')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='157',nombre='Tehuitzingo')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='158',nombre='Tenampulco')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='159',nombre='Teopantlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='160',nombre='Teotlalco')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='161',nombre='Tepanco de López')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='162',nombre='Tepango de Rodríguez')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='163',nombre='Tepatlaxco de Hidalgo')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='164',nombre='Tepeaca')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='165',nombre='Tepemaxalco')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='166',nombre='Tepeojuma')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='167',nombre='Tepetzintla')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='168',nombre='Tepexco')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='169',nombre='Tepexi de Rodríguez')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='170',nombre='Tepeyahualco')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='171',nombre='Tepeyahualco de Cuauhtémoc')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='172',nombre='Tetela de Ocampo')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='173',nombre='Teteles de Avila Castillo')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='174',nombre='Teziutlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='175',nombre='Tianguismanalco')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='176',nombre='Tilapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='179',nombre='Tlachichuca')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='177',nombre='Tlacotepec de Benito Juárez')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='178',nombre='Tlacuilotepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='180',nombre='Tlahuapan')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='181',nombre='Tlaltenango')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='182',nombre='Tlanepantla')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='183',nombre='Tlaola')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='184',nombre='Tlapacoya')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='185',nombre='Tlapanalá')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='186',nombre='Tlatlauquitepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='187',nombre='Tlaxco')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='188',nombre='Tochimilco')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='189',nombre='Tochtepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='190',nombre='Totoltepec de Guerrero')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='191',nombre='Tulcingo')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='192',nombre='Tuzamapan de Galeana')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='193',nombre='Tzicatlacoyan')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='194',nombre='Venustiano Carranza')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='195',nombre='Vicente Guerrero')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='196',nombre='Xayacatlán de Bravo')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='197',nombre='Xicotepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='198',nombre='Xicotlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='199',nombre='Xiutetelco')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='200',nombre='Xochiapulco')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='201',nombre='Xochiltepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='202',nombre='Xochitlán de Vicente Suárez')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='203',nombre='Xochitlán Todos Santos')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='204',nombre='Yaonáhuac')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='205',nombre='Yehualtepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='206',nombre='Zacapala')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='207',nombre='Zacapoaxtla')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='208',nombre='Zacatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='209',nombre='Zapotitlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='210',nombre='Zapotitlán de Méndez')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='211',nombre='Zaragoza')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='212',nombre='Zautla')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='213',nombre='Zihuateutla')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='214',nombre='Zinacatepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='215',nombre='Zongozotla')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='216',nombre='Zoquiapan')
			db.Cat_municipio_conglomerado.insert(clave_ent='21',clave_mun='217',nombre='Zoquitlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='22',clave_mun='1',nombre='Amealco de Bonfil')
			db.Cat_municipio_conglomerado.insert(clave_ent='22',clave_mun='3',nombre='Arroyo Seco')
			db.Cat_municipio_conglomerado.insert(clave_ent='22',clave_mun='4',nombre='Cadereyta de Montes')
			db.Cat_municipio_conglomerado.insert(clave_ent='22',clave_mun='5',nombre='Colón')
			db.Cat_municipio_conglomerado.insert(clave_ent='22',clave_mun='6',nombre='Corregidora')
			db.Cat_municipio_conglomerado.insert(clave_ent='22',clave_mun='11',nombre='El Marqués')
			db.Cat_municipio_conglomerado.insert(clave_ent='22',clave_mun='7',nombre='Ezequiel Montes')
			db.Cat_municipio_conglomerado.insert(clave_ent='22',clave_mun='8',nombre='Huimilpan')
			db.Cat_municipio_conglomerado.insert(clave_ent='22',clave_mun='9',nombre='Jalpan de Serra')
			db.Cat_municipio_conglomerado.insert(clave_ent='22',clave_mun='10',nombre='Landa de Matamoros')
			db.Cat_municipio_conglomerado.insert(clave_ent='22',clave_mun='12',nombre='Pedro Escobedo')
			db.Cat_municipio_conglomerado.insert(clave_ent='22',clave_mun='13',nombre='Peñamiller')
			db.Cat_municipio_conglomerado.insert(clave_ent='22',clave_mun='2',nombre='Pinal de Amoles')
			db.Cat_municipio_conglomerado.insert(clave_ent='22',clave_mun='14',nombre='Querétaro')
			db.Cat_municipio_conglomerado.insert(clave_ent='22',clave_mun='15',nombre='San Joaquín')
			db.Cat_municipio_conglomerado.insert(clave_ent='22',clave_mun='16',nombre='San Juan del Río')
			db.Cat_municipio_conglomerado.insert(clave_ent='22',clave_mun='17',nombre='Tequisquiapan')
			db.Cat_municipio_conglomerado.insert(clave_ent='22',clave_mun='18',nombre='Tolimán')
			db.Cat_municipio_conglomerado.insert(clave_ent='23',clave_mun='10',nombre='Bacalar')
			db.Cat_municipio_conglomerado.insert(clave_ent='23',clave_mun='5',nombre='Benito Juárez')
			db.Cat_municipio_conglomerado.insert(clave_ent='23',clave_mun='1',nombre='Cozumel')
			db.Cat_municipio_conglomerado.insert(clave_ent='23',clave_mun='2',nombre='Felipe Carrillo Puerto')
			db.Cat_municipio_conglomerado.insert(clave_ent='23',clave_mun='3',nombre='Isla Mujeres')
			db.Cat_municipio_conglomerado.insert(clave_ent='23',clave_mun='6',nombre='José María Morelos')
			db.Cat_municipio_conglomerado.insert(clave_ent='23',clave_mun='7',nombre='Lázaro Cárdenas')
			db.Cat_municipio_conglomerado.insert(clave_ent='23',clave_mun='4',nombre='Othón P. Blanco')
			db.Cat_municipio_conglomerado.insert(clave_ent='23',clave_mun='8',nombre='Solidaridad')
			db.Cat_municipio_conglomerado.insert(clave_ent='23',clave_mun='9',nombre='Tulum')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='1',nombre='Ahualulco')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='2',nombre='Alaquines')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='3',nombre='Aquismón')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='4',nombre='Armadillo de los Infante')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='53',nombre='Axtla de Terrazas')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='5',nombre='Cárdenas')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='6',nombre='Catorce')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='7',nombre='Cedral')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='8',nombre='Cerritos')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='9',nombre='Cerro de San Pedro')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='15',nombre='Charcas')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='10',nombre='Ciudad del Maíz')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='11',nombre='Ciudad Fernández')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='13',nombre='Ciudad Valles')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='14',nombre='Coxcatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='16',nombre='Ebano')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='58',nombre='El Naranjo')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='17',nombre='Guadalcázar')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='18',nombre='Huehuetlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='19',nombre='Lagunillas')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='20',nombre='Matehuala')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='57',nombre='Matlapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='21',nombre='Mexquitic de Carmona')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='22',nombre='Moctezuma')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='23',nombre='Rayón')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='24',nombre='Rioverde')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='25',nombre='Salinas')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='26',nombre='San Antonio')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='27',nombre='San Ciro de Acosta')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='28',nombre='San Luis Potosí')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='29',nombre='San Martín Chalchicuautla')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='30',nombre='San Nicolás Tolentino')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='34',nombre='San Vicente Tancuayalab')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='31',nombre='Santa Catarina')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='32',nombre='Santa María del Río')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='33',nombre='Santo Domingo')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='35',nombre='Soledad de Graciano Sánchez')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='36',nombre='Tamasopo')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='37',nombre='Tamazunchale')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='38',nombre='Tampacán')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='39',nombre='Tampamolón Corona')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='40',nombre='Tamuín')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='12',nombre='Tancanhuitz')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='41',nombre='Tanlajás')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='42',nombre='Tanquián de Escobedo')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='43',nombre='Tierra Nueva')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='44',nombre='Vanegas')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='45',nombre='Venado')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='56',nombre='Villa de Arista')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='46',nombre='Villa de Arriaga')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='47',nombre='Villa de Guadalupe')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='48',nombre='Villa de la Paz')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='49',nombre='Villa de Ramos')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='50',nombre='Villa de Reyes')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='51',nombre='Villa Hidalgo')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='52',nombre='Villa Juárez')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='54',nombre='Xilitla')
			db.Cat_municipio_conglomerado.insert(clave_ent='24',clave_mun='55',nombre='Zaragoza')
			db.Cat_municipio_conglomerado.insert(clave_ent='25',clave_mun='1',nombre='Ahome')
			db.Cat_municipio_conglomerado.insert(clave_ent='25',clave_mun='2',nombre='Angostura')
			db.Cat_municipio_conglomerado.insert(clave_ent='25',clave_mun='3',nombre='Badiraguato')
			db.Cat_municipio_conglomerado.insert(clave_ent='25',clave_mun='7',nombre='Choix')
			db.Cat_municipio_conglomerado.insert(clave_ent='25',clave_mun='4',nombre='Concordia')
			db.Cat_municipio_conglomerado.insert(clave_ent='25',clave_mun='5',nombre='Cosalá')
			db.Cat_municipio_conglomerado.insert(clave_ent='25',clave_mun='6',nombre='Culiacán')
			db.Cat_municipio_conglomerado.insert(clave_ent='25',clave_mun='10',nombre='El Fuerte')
			db.Cat_municipio_conglomerado.insert(clave_ent='25',clave_mun='8',nombre='Elota')
			db.Cat_municipio_conglomerado.insert(clave_ent='25',clave_mun='9',nombre='Escuinapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='25',clave_mun='11',nombre='Guasave')
			db.Cat_municipio_conglomerado.insert(clave_ent='25',clave_mun='12',nombre='Mazatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='25',clave_mun='13',nombre='Mocorito')
			db.Cat_municipio_conglomerado.insert(clave_ent='25',clave_mun='18',nombre='Navolato')
			db.Cat_municipio_conglomerado.insert(clave_ent='25',clave_mun='14',nombre='Rosario')
			db.Cat_municipio_conglomerado.insert(clave_ent='25',clave_mun='15',nombre='Salvador Alvarado')
			db.Cat_municipio_conglomerado.insert(clave_ent='25',clave_mun='16',nombre='San Ignacio')
			db.Cat_municipio_conglomerado.insert(clave_ent='25',clave_mun='17',nombre='Sinaloa')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='1',nombre='Aconchi')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='2',nombre='Agua Prieta')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='3',nombre='Alamos')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='4',nombre='Altar')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='5',nombre='Arivechi')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='6',nombre='Arizpe')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='7',nombre='Atil')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='8',nombre='Bacadéhuachi')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='9',nombre='Bacanora')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='10',nombre='Bacerac')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='11',nombre='Bacoachi')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='12',nombre='Bácum')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='13',nombre='Banámichi')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='14',nombre='Baviácora')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='15',nombre='Bavispe')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='71',nombre='Benito Juárez')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='16',nombre='Benjamín Hill')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='17',nombre='Caborca')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='18',nombre='Cajeme')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='19',nombre='Cananea')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='20',nombre='Carbó')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='22',nombre='Cucurpe')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='23',nombre='Cumpas')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='24',nombre='Divisaderos')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='25',nombre='Empalme')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='26',nombre='Etchojoa')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='27',nombre='Fronteras')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='70',nombre='General Plutarco Elías Calles')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='28',nombre='Granados')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='29',nombre='Guaymas')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='30',nombre='Hermosillo')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='31',nombre='Huachinera')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='32',nombre='Huásabas')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='33',nombre='Huatabampo')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='34',nombre='Huépac')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='35',nombre='Imuris')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='21',nombre='La Colorada')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='36',nombre='Magdalena')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='37',nombre='Mazatán')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='38',nombre='Moctezuma')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='39',nombre='Naco')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='40',nombre='Nácori Chico')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='41',nombre='Nacozari de García')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='42',nombre='Navojoa')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='43',nombre='Nogales')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='44',nombre='Onavas')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='45',nombre='Opodepe')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='46',nombre='Oquitoa')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='47',nombre='Pitiquito')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='48',nombre='Puerto Peñasco')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='49',nombre='Quiriego')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='50',nombre='Rayón')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='51',nombre='Rosario')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='52',nombre='Sahuaripa')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='53',nombre='San Felipe de Jesús')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='72',nombre='San Ignacio Río Muerto')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='54',nombre='San Javier')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='55',nombre='San Luis Río Colorado')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='56',nombre='San Miguel de Horcasitas')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='57',nombre='San Pedro de la Cueva')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='58',nombre='Santa Ana')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='59',nombre='Santa Cruz')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='60',nombre='Sáric')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='61',nombre='Soyopa')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='62',nombre='Suaqui Grande')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='63',nombre='Tepache')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='64',nombre='Trincheras')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='65',nombre='Tubutama')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='66',nombre='Ures')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='67',nombre='Villa Hidalgo')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='68',nombre='Villa Pesqueira')
			db.Cat_municipio_conglomerado.insert(clave_ent='26',clave_mun='69',nombre='Yécora')
			db.Cat_municipio_conglomerado.insert(clave_ent='27',clave_mun='1',nombre='Balancán')
			db.Cat_municipio_conglomerado.insert(clave_ent='27',clave_mun='2',nombre='Cárdenas')
			db.Cat_municipio_conglomerado.insert(clave_ent='27',clave_mun='3',nombre='Centla')
			db.Cat_municipio_conglomerado.insert(clave_ent='27',clave_mun='4',nombre='Centro')
			db.Cat_municipio_conglomerado.insert(clave_ent='27',clave_mun='5',nombre='Comalcalco')
			db.Cat_municipio_conglomerado.insert(clave_ent='27',clave_mun='6',nombre='Cunduacán')
			db.Cat_municipio_conglomerado.insert(clave_ent='27',clave_mun='7',nombre='Emiliano Zapata')
			db.Cat_municipio_conglomerado.insert(clave_ent='27',clave_mun='8',nombre='Huimanguillo')
			db.Cat_municipio_conglomerado.insert(clave_ent='27',clave_mun='9',nombre='Jalapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='27',clave_mun='10',nombre='Jalpa de Méndez')
			db.Cat_municipio_conglomerado.insert(clave_ent='27',clave_mun='11',nombre='Jonuta')
			db.Cat_municipio_conglomerado.insert(clave_ent='27',clave_mun='12',nombre='Macuspana')
			db.Cat_municipio_conglomerado.insert(clave_ent='27',clave_mun='13',nombre='Nacajuca')
			db.Cat_municipio_conglomerado.insert(clave_ent='27',clave_mun='14',nombre='Paraíso')
			db.Cat_municipio_conglomerado.insert(clave_ent='27',clave_mun='15',nombre='Tacotalpa')
			db.Cat_municipio_conglomerado.insert(clave_ent='27',clave_mun='16',nombre='Teapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='27',clave_mun='17',nombre='Tenosique')
			db.Cat_municipio_conglomerado.insert(clave_ent='28',clave_mun='1',nombre='Abasolo')
			db.Cat_municipio_conglomerado.insert(clave_ent='28',clave_mun='2',nombre='Aldama')
			db.Cat_municipio_conglomerado.insert(clave_ent='28',clave_mun='3',nombre='Altamira')
			db.Cat_municipio_conglomerado.insert(clave_ent='28',clave_mun='4',nombre='Antiguo Morelos')
			db.Cat_municipio_conglomerado.insert(clave_ent='28',clave_mun='5',nombre='Burgos')
			db.Cat_municipio_conglomerado.insert(clave_ent='28',clave_mun='6',nombre='Bustamante')
			db.Cat_municipio_conglomerado.insert(clave_ent='28',clave_mun='7',nombre='Camargo')
			db.Cat_municipio_conglomerado.insert(clave_ent='28',clave_mun='8',nombre='Casas')
			db.Cat_municipio_conglomerado.insert(clave_ent='28',clave_mun='9',nombre='Ciudad Madero')
			db.Cat_municipio_conglomerado.insert(clave_ent='28',clave_mun='10',nombre='Cruillas')
			db.Cat_municipio_conglomerado.insert(clave_ent='28',clave_mun='21',nombre='El Mante')
			db.Cat_municipio_conglomerado.insert(clave_ent='28',clave_mun='11',nombre='Gómez Farías')
			db.Cat_municipio_conglomerado.insert(clave_ent='28',clave_mun='12',nombre='González')
			db.Cat_municipio_conglomerado.insert(clave_ent='28',clave_mun='13',nombre='Güémez')
			db.Cat_municipio_conglomerado.insert(clave_ent='28',clave_mun='14',nombre='Guerrero')
			db.Cat_municipio_conglomerado.insert(clave_ent='28',clave_mun='15',nombre='Gustavo Díaz Ordaz')
			db.Cat_municipio_conglomerado.insert(clave_ent='28',clave_mun='16',nombre='Hidalgo')
			db.Cat_municipio_conglomerado.insert(clave_ent='28',clave_mun='17',nombre='Jaumave')
			db.Cat_municipio_conglomerado.insert(clave_ent='28',clave_mun='18',nombre='Jiménez')
			db.Cat_municipio_conglomerado.insert(clave_ent='28',clave_mun='19',nombre='Llera')
			db.Cat_municipio_conglomerado.insert(clave_ent='28',clave_mun='20',nombre='Mainero')
			db.Cat_municipio_conglomerado.insert(clave_ent='28',clave_mun='22',nombre='Matamoros')
			db.Cat_municipio_conglomerado.insert(clave_ent='28',clave_mun='23',nombre='Méndez')
			db.Cat_municipio_conglomerado.insert(clave_ent='28',clave_mun='24',nombre='Mier')
			db.Cat_municipio_conglomerado.insert(clave_ent='28',clave_mun='25',nombre='Miguel Alemán')
			db.Cat_municipio_conglomerado.insert(clave_ent='28',clave_mun='26',nombre='Miquihuana')
			db.Cat_municipio_conglomerado.insert(clave_ent='28',clave_mun='27',nombre='Nuevo Laredo')
			db.Cat_municipio_conglomerado.insert(clave_ent='28',clave_mun='28',nombre='Nuevo Morelos')
			db.Cat_municipio_conglomerado.insert(clave_ent='28',clave_mun='29',nombre='Ocampo')
			db.Cat_municipio_conglomerado.insert(clave_ent='28',clave_mun='30',nombre='Padilla')
			db.Cat_municipio_conglomerado.insert(clave_ent='28',clave_mun='31',nombre='Palmillas')
			db.Cat_municipio_conglomerado.insert(clave_ent='28',clave_mun='32',nombre='Reynosa')
			db.Cat_municipio_conglomerado.insert(clave_ent='28',clave_mun='33',nombre='Río Bravo')
			db.Cat_municipio_conglomerado.insert(clave_ent='28',clave_mun='34',nombre='San Carlos')
			db.Cat_municipio_conglomerado.insert(clave_ent='28',clave_mun='35',nombre='San Fernando')
			db.Cat_municipio_conglomerado.insert(clave_ent='28',clave_mun='36',nombre='San Nicolás')
			db.Cat_municipio_conglomerado.insert(clave_ent='28',clave_mun='37',nombre='Soto la Marina')
			db.Cat_municipio_conglomerado.insert(clave_ent='28',clave_mun='38',nombre='Tampico')
			db.Cat_municipio_conglomerado.insert(clave_ent='28',clave_mun='39',nombre='Tula')
			db.Cat_municipio_conglomerado.insert(clave_ent='28',clave_mun='40',nombre='Valle Hermoso')
			db.Cat_municipio_conglomerado.insert(clave_ent='28',clave_mun='41',nombre='Victoria')
			db.Cat_municipio_conglomerado.insert(clave_ent='28',clave_mun='42',nombre='Villagrán')
			db.Cat_municipio_conglomerado.insert(clave_ent='28',clave_mun='43',nombre='Xicoténcatl')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='22',nombre='Acuamanala de Miguel Hidalgo')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='1',nombre='Amaxac de Guerrero')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='2',nombre='Apetatitlán de Antonio Carvajal')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='5',nombre='Apizaco')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='3',nombre='Atlangatepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='4',nombre='Atltzayanca')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='45',nombre='Benito Juárez')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='6',nombre='Calpulalpan')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='10',nombre='Chiautempan')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='18',nombre='Contla de Juan Cuamatzi')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='8',nombre='Cuapiaxtla')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='9',nombre='Cuaxomulco')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='7',nombre='El Carmen Tequexquitla')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='46',nombre='Emiliano Zapata')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='12',nombre='Españita')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='13',nombre='Huamantla')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='14',nombre='Hueyotlipan')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='15',nombre='Ixtacuixtla de Mariano Matamoros')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='16',nombre='Ixtenco')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='48',nombre='La Magdalena Tlaltelulco')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='47',nombre='Lázaro Cárdenas')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='17',nombre='Mazatecochco de José María Morelos')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='11',nombre='Muñoz de Domingo Arenas')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='21',nombre='Nanacamilpa de Mariano Arista')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='23',nombre='Natívitas')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='24',nombre='Panotla')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='41',nombre='Papalotla de Xicohténcatl')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='49',nombre='San Damián Texóloc')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='50',nombre='San Francisco Tetlanohcan')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='51',nombre='San Jerónimo Zacualpan')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='52',nombre='San José Teacalco')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='53',nombre='San Juan Huactzinco')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='54',nombre='San Lorenzo Axocomanitla')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='55',nombre='San Lucas Tecopilco')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='25',nombre='San Pablo del Monte')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='20',nombre='Sanctórum de Lázaro Cárdenas')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='56',nombre='Santa Ana Nopalucan')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='57',nombre='Santa Apolonia Teacalco')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='58',nombre='Santa Catarina Ayometla')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='59',nombre='Santa Cruz Quilehtla')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='26',nombre='Santa Cruz Tlaxcala')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='60',nombre='Santa Isabel Xiloxoxtla')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='27',nombre='Tenancingo')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='28',nombre='Teolocholco')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='19',nombre='Tepetitla de Lardizábal')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='29',nombre='Tepeyanco')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='30',nombre='Terrenate')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='31',nombre='Tetla de la Solidaridad')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='32',nombre='Tetlatlahuca')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='33',nombre='Tlaxcala')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='34',nombre='Tlaxco')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='35',nombre='Tocatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='36',nombre='Totolac')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='38',nombre='Tzompantepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='39',nombre='Xaloztoc')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='40',nombre='Xaltocan')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='42',nombre='Xicohtzinco')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='43',nombre='Yauhquemehcan')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='44',nombre='Zacatelco')
			db.Cat_municipio_conglomerado.insert(clave_ent='29',clave_mun='37',nombre='Ziltlaltépec de Trinidad Sánchez Santos')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='1',nombre='Acajete')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='2',nombre='Acatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='3',nombre='Acayucan')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='4',nombre='Actopan')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='5',nombre='Acula')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='6',nombre='Acultzingo')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='204',nombre='Agua Dulce')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='160',nombre='Álamo Temapache')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='8',nombre='Alpatláhuac')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='9',nombre='Alto Lucero de Gutiérrez Barrios')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='10',nombre='Altotonga')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='11',nombre='Alvarado')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='12',nombre='Amatitlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='14',nombre='Amatlán de los Reyes')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='15',nombre='Angel R. Cabada')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='17',nombre='Apazapan')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='18',nombre='Aquila')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='19',nombre='Astacinga')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='20',nombre='Atlahuilco')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='21',nombre='Atoyac')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='22',nombre='Atzacan')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='23',nombre='Atzalan')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='25',nombre='Ayahualulco')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='26',nombre='Banderilla')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='27',nombre='Benito Juárez')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='28',nombre='Boca del Río')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='29',nombre='Calcahualco')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='7',nombre='Camarón de Tejeda')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='30',nombre='Camerino Z. Mendoza')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='208',nombre='Carlos A. Carrillo')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='31',nombre='Carrillo Puerto')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='157',nombre='Castillo de Teayo')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='32',nombre='Catemaco')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='33',nombre='Cazones de Herrera')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='34',nombre='Cerro Azul')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='54',nombre='Chacaltianguis')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='55',nombre='Chalma')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='56',nombre='Chiconamel')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='57',nombre='Chiconquiaco')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='58',nombre='Chicontepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='59',nombre='Chinameca')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='60',nombre='Chinampa de Gorostiza')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='62',nombre='Chocamán')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='63',nombre='Chontla')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='64',nombre='Chumatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='35',nombre='Citlaltépetl')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='36',nombre='Coacoatzintla')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='37',nombre='Coahuitlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='38',nombre='Coatepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='39',nombre='Coatzacoalcos')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='40',nombre='Coatzintla')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='41',nombre='Coetzala')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='42',nombre='Colipa')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='43',nombre='Comapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='44',nombre='Córdoba')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='45',nombre='Cosamaloapan de Carpio')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='46',nombre='Cosautlán de Carvajal')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='47',nombre='Coscomatepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='48',nombre='Cosoleacaque')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='49',nombre='Cotaxtla')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='50',nombre='Coxquihui')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='51',nombre='Coyutla')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='52',nombre='Cuichapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='53',nombre='Cuitláhuac')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='205',nombre='El Higo')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='65',nombre='Emiliano Zapata')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='66',nombre='Espinal')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='67',nombre='Filomeno Mata')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='68',nombre='Fortín')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='69',nombre='Gutiérrez Zamora')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='70',nombre='Hidalgotitlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='71',nombre='Huatusco')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='72',nombre='Huayacocotla')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='73',nombre='Hueyapan de Ocampo')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='74',nombre='Huiloapan de Cuauhtémoc')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='75',nombre='Ignacio de la Llave')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='76',nombre='Ilamatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='77',nombre='Isla')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='78',nombre='Ixcatepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='79',nombre='Ixhuacán de los Reyes')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='83',nombre='Ixhuatlán de Madero')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='80',nombre='Ixhuatlán del Café')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='82',nombre='Ixhuatlán del Sureste')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='81',nombre='Ixhuatlancillo')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='84',nombre='Ixmatlahuacan')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='85',nombre='Ixtaczoquitlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='86',nombre='Jalacingo')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='88',nombre='Jalcomulco')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='89',nombre='Jáltipan')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='90',nombre='Jamapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='91',nombre='Jesús Carranza')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='93',nombre='Jilotepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='169',nombre='José Azueta')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='94',nombre='Juan Rodríguez Clara')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='95',nombre='Juchique de Ferrer')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='16',nombre='La Antigua')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='127',nombre='La Perla')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='96',nombre='Landero y Coss')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='61',nombre='Las Choapas')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='107',nombre='Las Minas')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='132',nombre='Las Vigas de Ramírez')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='97',nombre='Lerdo de Tejada')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='137',nombre='Los Reyes')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='98',nombre='Magdalena')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='99',nombre='Maltrata')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='100',nombre='Manlio Fabio Altamirano')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='101',nombre='Mariano Escobedo')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='102',nombre='Martínez de la Torre')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='103',nombre='Mecatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='104',nombre='Mecayapan')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='105',nombre='Medellín')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='106',nombre='Miahuatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='108',nombre='Minatitlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='109',nombre='Misantla')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='110',nombre='Mixtla de Altamirano')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='111',nombre='Moloacán')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='206',nombre='Nanchital de Lázaro Cárdenas del Río')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='112',nombre='Naolinco')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='113',nombre='Naranjal')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='13',nombre='Naranjos Amatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='114',nombre='Nautla')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='115',nombre='Nogales')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='116',nombre='Oluta')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='117',nombre='Omealca')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='118',nombre='Orizaba')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='119',nombre='Otatitlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='120',nombre='Oteapan')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='121',nombre='Ozuluama de Mascareñas')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='122',nombre='Pajapan')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='123',nombre='Pánuco')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='124',nombre='Papantla')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='126',nombre='Paso de Ovejas')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='125',nombre='Paso del Macho')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='128',nombre='Perote')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='129',nombre='Platón Sánchez')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='130',nombre='Playa Vicente')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='131',nombre='Poza Rica de Hidalgo')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='133',nombre='Pueblo Viejo')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='134',nombre='Puente Nacional')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='135',nombre='Rafael Delgado')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='136',nombre='Rafael Lucio')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='138',nombre='Río Blanco')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='139',nombre='Saltabarranca')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='140',nombre='San Andrés Tenejapan')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='141',nombre='San Andrés Tuxtla')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='142',nombre='San Juan Evangelista')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='211',nombre='San Rafael')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='212',nombre='Santiago Sochiapan')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='143',nombre='Santiago Tuxtla')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='144',nombre='Sayula de Alemán')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='146',nombre='Sochiapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='145',nombre='Soconusco')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='147',nombre='Soledad Atzompa')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='148',nombre='Soledad de Doblado')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='149',nombre='Soteapan')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='150',nombre='Tamalín')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='151',nombre='Tamiahua')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='152',nombre='Tampico Alto')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='153',nombre='Tancoco')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='154',nombre='Tantima')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='155',nombre='Tantoyuca')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='209',nombre='Tatahuicapan de Juárez')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='156',nombre='Tatatila')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='158',nombre='Tecolutla')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='159',nombre='Tehuipango')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='161',nombre='Tempoal')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='162',nombre='Tenampa')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='163',nombre='Tenochtitlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='164',nombre='Teocelo')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='165',nombre='Tepatlaxco')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='166',nombre='Tepetlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='167',nombre='Tepetzintla')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='168',nombre='Tequila')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='170',nombre='Texcatepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='171',nombre='Texhuacán')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='172',nombre='Texistepec')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='173',nombre='Tezonapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='174',nombre='Tierra Blanca')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='175',nombre='Tihuatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='180',nombre='Tlachichilco')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='176',nombre='Tlacojalpan')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='177',nombre='Tlacolulan')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='178',nombre='Tlacotalpan')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='179',nombre='Tlacotepec de Mejía')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='181',nombre='Tlalixcoyan')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='182',nombre='Tlalnelhuayocan')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='24',nombre='Tlaltetela')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='183',nombre='Tlapacoyan')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='184',nombre='Tlaquilpa')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='185',nombre='Tlilapan')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='186',nombre='Tomatlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='187',nombre='Tonayán')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='188',nombre='Totutla')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='207',nombre='Tres Valles')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='189',nombre='Tuxpan')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='190',nombre='Tuxtilla')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='191',nombre='Ursulo Galván')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='210',nombre='Uxpanapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='192',nombre='Vega de Alatorre')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='193',nombre='Veracruz')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='194',nombre='Villa Aldama')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='87',nombre='Xalapa')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='92',nombre='Xico')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='195',nombre='Xoxocotla')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='196',nombre='Yanga')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='197',nombre='Yecuatla')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='198',nombre='Zacualpan')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='199',nombre='Zaragoza')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='200',nombre='Zentla')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='201',nombre='Zongolica')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='202',nombre='Zontecomatlán de López y Fuentes')
			db.Cat_municipio_conglomerado.insert(clave_ent='30',clave_mun='203',nombre='Zozocolco de Hidalgo')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='1',nombre='Abalá')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='2',nombre='Acanceh')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='3',nombre='Akil')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='4',nombre='Baca')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='5',nombre='Bokobá')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='6',nombre='Buctzotz')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='7',nombre='Cacalchén')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='8',nombre='Calotmul')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='9',nombre='Cansahcab')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='10',nombre='Cantamayec')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='11',nombre='Celestún')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='12',nombre='Cenotillo')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='16',nombre='Chacsinkín')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='17',nombre='Chankom')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='18',nombre='Chapab')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='19',nombre='Chemax')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='21',nombre='Chichimilá')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='20',nombre='Chicxulub Pueblo')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='22',nombre='Chikindzonot')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='23',nombre='Chocholá')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='24',nombre='Chumayel')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='13',nombre='Conkal')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='14',nombre='Cuncunul')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='15',nombre='Cuzamá')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='25',nombre='Dzán')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='26',nombre='Dzemul')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='27',nombre='Dzidzantún')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='28',nombre='Dzilam de Bravo')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='29',nombre='Dzilam González')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='30',nombre='Dzitás')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='31',nombre='Dzoncauich')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='32',nombre='Espita')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='33',nombre='Halachó')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='34',nombre='Hocabá')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='35',nombre='Hoctún')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='36',nombre='Homún')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='37',nombre='Huhí')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='38',nombre='Hunucmá')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='39',nombre='Ixil')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='40',nombre='Izamal')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='41',nombre='Kanasín')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='42',nombre='Kantunil')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='43',nombre='Kaua')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='44',nombre='Kinchil')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='45',nombre='Kopomá')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='46',nombre='Mama')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='47',nombre='Maní')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='48',nombre='Maxcanú')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='49',nombre='Mayapán')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='50',nombre='Mérida')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='51',nombre='Mocochá')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='52',nombre='Motul')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='53',nombre='Muna')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='54',nombre='Muxupip')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='55',nombre='Opichén')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='56',nombre='Oxkutzcab')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='57',nombre='Panabá')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='58',nombre='Peto')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='59',nombre='Progreso')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='60',nombre='Quintana Roo')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='61',nombre='Río Lagartos')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='62',nombre='Sacalum')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='63',nombre='Samahil')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='65',nombre='San Felipe')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='64',nombre='Sanahcat')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='66',nombre='Santa Elena')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='67',nombre='Seyé')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='68',nombre='Sinanché')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='69',nombre='Sotuta')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='70',nombre='Sucilá')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='71',nombre='Sudzal')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='72',nombre='Suma')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='73',nombre='Tahdziú')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='74',nombre='Tahmek')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='75',nombre='Teabo')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='76',nombre='Tecoh')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='77',nombre='Tekal de Venegas')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='78',nombre='Tekantó')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='79',nombre='Tekax')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='80',nombre='Tekit')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='81',nombre='Tekom')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='82',nombre='Telchac Pueblo')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='83',nombre='Telchac Puerto')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='84',nombre='Temax')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='85',nombre='Temozón')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='86',nombre='Tepakán')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='87',nombre='Tetiz')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='88',nombre='Teya')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='89',nombre='Ticul')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='90',nombre='Timucuy')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='91',nombre='Tinum')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='92',nombre='Tixcacalcupul')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='93',nombre='Tixkokob')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='94',nombre='Tixmehuac')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='95',nombre='Tixpéhual')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='96',nombre='Tizimín')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='97',nombre='Tunkás')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='98',nombre='Tzucacab')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='99',nombre='Uayma')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='100',nombre='Ucú')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='101',nombre='Umán')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='102',nombre='Valladolid')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='103',nombre='Xocchel')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='104',nombre='Yaxcabá')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='105',nombre='Yaxkukul')
			db.Cat_municipio_conglomerado.insert(clave_ent='31',clave_mun='106',nombre='Yobaín')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='1',nombre='Apozol')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='2',nombre='Apulco')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='3',nombre='Atolinga')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='4',nombre='Benito Juárez')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='5',nombre='Calera')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='6',nombre='Cañitas de Felipe Pescador')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='9',nombre='Chalchihuites')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='7',nombre='Concepción del Oro')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='8',nombre='Cuauhtémoc')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='15',nombre='El Plateado de Joaquín Amaro')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='41',nombre='El Salvador')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='10',nombre='Fresnillo')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='12',nombre='Genaro Codina')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='13',nombre='General Enrique Estrada')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='14',nombre='General Francisco R. Murguía')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='16',nombre='General Pánfilo Natera')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='17',nombre='Guadalupe')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='18',nombre='Huanusco')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='19',nombre='Jalpa')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='20',nombre='Jerez')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='21',nombre='Jiménez del Teul')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='22',nombre='Juan Aldama')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='23',nombre='Juchipila')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='24',nombre='Loreto')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='25',nombre='Luis Moya')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='26',nombre='Mazapil')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='27',nombre='Melchor Ocampo')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='28',nombre='Mezquital del Oro')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='29',nombre='Miguel Auza')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='30',nombre='Momax')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='31',nombre='Monte Escobedo')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='32',nombre='Morelos')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='33',nombre='Moyahua de Estrada')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='34',nombre='Nochistlán de Mejía')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='35',nombre='Noria de Ángeles')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='36',nombre='Ojocaliente')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='37',nombre='Pánuco')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='38',nombre='Pinos')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='39',nombre='Río Grande')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='40',nombre='Sain Alto')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='58',nombre='Santa María de la Paz')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='42',nombre='Sombrerete')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='43',nombre='Susticacán')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='44',nombre='Tabasco')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='45',nombre='Tepechitlán')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='46',nombre='Tepetongo')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='47',nombre='Teúl de González Ortega')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='48',nombre='Tlaltenango de Sánchez Román')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='57',nombre='Trancoso')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='11',nombre='Trinidad García de la Cadena')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='49',nombre='Valparaíso')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='50',nombre='Vetagrande')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='51',nombre='Villa de Cos')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='52',nombre='Villa García')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='53',nombre='Villa González Ortega')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='54',nombre='Villa Hidalgo')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='55',nombre='Villanueva')
			db.Cat_municipio_conglomerado.insert(clave_ent='32',clave_mun='56',nombre='Zacatecas')

		##########################################################################
		## Pestaña Vegetación y suelos
		########################################################################

		if db(db.Cat_material_carbono.id>0).count() == 0:
			db.Cat_material_carbono.insert(nombre='HP - De pino')
			db.Cat_material_carbono.insert(nombre='HL - De latifoliadas')
			db.Cat_material_carbono.insert(nombre='HA - De abies')
			db.Cat_material_carbono.insert(nombre='MP - Madera putrefacta')
			db.Cat_material_carbono.insert(nombre='CO - Corteza')
			db.Cat_material_carbono.insert(nombre='RD - Roca desnuda')
			db.Cat_material_carbono.insert(nombre='MU - Musgo')
			db.Cat_material_carbono.insert(nombre='OS - Otros')
			db.Cat_material_carbono.insert(nombre='NO - No contiene')

		#########################################################################

		if db(db.Cat_grado_carbono.id>0).count() == 0:
			db.Cat_grado_carbono.insert(nombre=1)
			db.Cat_grado_carbono.insert(nombre=2)
			db.Cat_grado_carbono.insert(nombre=3)
			db.Cat_grado_carbono.insert(nombre=4)
			db.Cat_grado_carbono.insert(nombre=5)

		#########################################################################

		if db(db.Cat_transecto_direccion.id>0).count() == 0:
			db.Cat_transecto_direccion.insert(nombre='Norte')
			db.Cat_transecto_direccion.insert(nombre='Este')
			db.Cat_transecto_direccion.insert(nombre='Sur')
			db.Cat_transecto_direccion.insert(nombre='Oeste')

		#########################################################################

		if db(db.Cat_forma_vida.id>0).count() == 0:
			db.Cat_forma_vida.insert(nombre='No existe')
			db.Cat_forma_vida.insert(nombre='Arbustiva')
			db.Cat_forma_vida.insert(nombre='Arbórea')

		#########################################################################

		if db(db.Cat_forma_vida_arboles_grandes.id>0).count() == 0:
			db.Cat_forma_vida_arboles_grandes.insert(nombre='No existe')
			db.Cat_forma_vida_arboles_grandes.insert(nombre='Árbol')
			db.Cat_forma_vida_arboles_grandes.insert(nombre='Arbustiva')
			db.Cat_forma_vida_arboles_grandes.insert(nombre='Arborescente')
			db.Cat_forma_vida_arboles_grandes.insert(nombre='Cañas')
			db.Cat_forma_vida_arboles_grandes.insert(nombre='Cactáceas arborescentes')
			db.Cat_forma_vida_arboles_grandes.insert(nombre='Manglares')

		#########################################################################

		if db(db.Cat_cambios_arboles_grandes.id>0).count() == 0:
			db.Cat_cambios_arboles_grandes.insert(nombre='Ninguno')
			db.Cat_cambios_arboles_grandes.insert(nombre='Árbol nuevo')
			db.Cat_cambios_arboles_grandes.insert(nombre='Árbol muerto nuevo')
			db.Cat_cambios_arboles_grandes.insert(nombre='Tocón nuevo')

		##########################################################################
		## Pestaña Impactos ambientales
		########################################################################

		if db(db.Cat_tipo_impacto.id>0).count() == 0:
			db.Cat_tipo_impacto.insert(nombre='Incendios')
			db.Cat_tipo_impacto.insert(nombre='Huracanes')
			db.Cat_tipo_impacto.insert(nombre='Inundaciones')
			db.Cat_tipo_impacto.insert(nombre='Apertura de caminos')
			db.Cat_tipo_impacto.insert(nombre='Aprovechamientos forestales')
			db.Cat_tipo_impacto.insert(nombre='Uso del suelo diferente al forestal')
			db.Cat_tipo_impacto.insert(nombre='Pastoreo')
			db.Cat_tipo_impacto.insert(nombre='Plagas y enfermedades')
			db.Cat_tipo_impacto.insert(nombre='Líneas eléctricas')
			db.Cat_tipo_impacto.insert(nombre='Actividades mineras')
			db.Cat_tipo_impacto.insert(nombre='Asentamientos humanos')

		#########################################################################

		if db(db.Cat_severidad_impactos.id>0).count() == 0:
			db.Cat_severidad_impactos.insert(nombre='1 No perceptible')
			db.Cat_severidad_impactos.insert(nombre='2 Menor')
			db.Cat_severidad_impactos.insert(nombre='3 Mediana')
			db.Cat_severidad_impactos.insert(nombre='4 Mayor')

		#########################################################################

		if db(db.Cat_agente_impactos.id>0).count() == 0:
			db.Cat_agente_impactos.insert(nombre='0 Sin plagas')
			db.Cat_agente_impactos.insert(nombre='1 Barrenador')
			db.Cat_agente_impactos.insert(nombre='2 Defoliador')
			db.Cat_agente_impactos.insert(nombre='3 Descortezador')
			db.Cat_agente_impactos.insert(nombre='4 Muérdagos')

		#########################################################################

		if db(db.Cat_estatus_impactos.id>0).count() == 0:
			db.Cat_estatus_impactos.insert(nombre='1 Activa')
			db.Cat_estatus_impactos.insert(nombre='2 Inactiva')

		#########################################################################

		if db(db.Cat_prop_afectacion.id>0).count() == 0:
			db.Cat_prop_afectacion.insert(nombre='Menor a 10%')
			db.Cat_prop_afectacion.insert(nombre='10 a 30%')
			db.Cat_prop_afectacion.insert(nombre='30 a 50%')
			db.Cat_prop_afectacion.insert(nombre='50 a 70%')
			db.Cat_prop_afectacion.insert(nombre='70 a 90%')
			db.Cat_prop_afectacion.insert(nombre='Más de 90%')

		#########################################################################

		if db(db.Cat_incendio.id>0).count() == 0:
			db.Cat_incendio.insert(nombre='Subterráneo')
			db.Cat_incendio.insert(nombre='Superficial')
			db.Cat_incendio.insert(nombre='Aéreo copa')

		#########################################################################


		##########################################################################
		## Pestaña Aves
		########################################################################
		# Por la cantidad de registros, en esta pestaña se separan el nombre común del
		# nombre científico

		if db(db.Cat_conabio_aves.id>0).count() == 0:
			db.Cat_conabio_aves.insert(
				nombre_comun='Achichilique Pico Amarillo',
				nombre_cientifico='Aechmophorus occidentalis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Achichilique Pico Naranja',
				nombre_cientifico='Aechmophorus clarkii')
			db.Cat_conabio_aves.insert(
				nombre_comun='Agachona Norteamericana',
				nombre_cientifico='Gallinago delicata')
			db.Cat_conabio_aves.insert(
				nombre_comun='Águila Albinegra',
				nombre_cientifico='Spizaetus melanoleucus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Águila Arpía',
				nombre_cientifico='Harpia harpyja')
			db.Cat_conabio_aves.insert(
				nombre_comun='Águila Cabeza Blanca',
				nombre_cientifico='Haliaeetus leucocephalus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Águila Crestada',
				nombre_cientifico='Morphnus guianensis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Águila Elegante',
				nombre_cientifico='Spizaetus ornatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Águila Pescadora',
				nombre_cientifico='Pandion haliaetus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Águila Real',
				nombre_cientifico='Aquila chrysaetos')
			db.Cat_conabio_aves.insert(
				nombre_comun='Águila Solitaria',
				nombre_cientifico='Buteogallus solitarius')
			db.Cat_conabio_aves.insert(
				nombre_comun='Águila Tirana',
				nombre_cientifico='Spizaetus tyrannus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Aguililla Alas Anchas',
				nombre_cientifico='Buteo platypterus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Aguililla Ártica',
				nombre_cientifico='Buteo lagopus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Aguililla Aura',
				nombre_cientifico='Buteo albonotatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Aguililla Blanca',
				nombre_cientifico='Pseudastur albicollis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Aguililla Caminera',
				nombre_cientifico='Buteo magnirostris')
			db.Cat_conabio_aves.insert(
				nombre_comun='Aguililla Canela',
				nombre_cientifico='Busarellus nigricollis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Aguililla Cola Blanca',
				nombre_cientifico='Buteo albicaudatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Aguililla Cola Corta',
				nombre_cientifico='Buteo brachyurus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Aguililla Cola Roja',
				nombre_cientifico='Buteo jamaicensis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Aguililla de Swainson',
				nombre_cientifico='Buteo swainsoni')
			db.Cat_conabio_aves.insert(
				nombre_comun='Aguililla Gris',
				nombre_cientifico='Buteo plagiatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Aguililla Negra Mayor',
				nombre_cientifico='Buteogallus urubitinga')
			db.Cat_conabio_aves.insert(
				nombre_comun='Aguililla Negra Menor',
				nombre_cientifico='Buteogallus anthracinus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Aguililla Pecho Rojo',
				nombre_cientifico='Buteo lineatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Aguililla Real',
				nombre_cientifico='Buteo regalis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Aguililla Rojinegra',
				nombre_cientifico='Parabuteo unicinctus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Albatros de Laysan',
				nombre_cientifico='Phoebastria immutabilis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Albatros Patas Negras',
				nombre_cientifico='Phoebastria nigripes')
			db.Cat_conabio_aves.insert(
				nombre_comun='Albatros Rabón',
				nombre_cientifico='Phoebastria albatrus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Alca Marmoleada',
				nombre_cientifico='Brachyramphus marmoratus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Alca Rinoceronte',
				nombre_cientifico='Cerorhinca monocerata')
			db.Cat_conabio_aves.insert(
				nombre_comun='Alcaraván Americano',
				nombre_cientifico='Burhinus bistriatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Alondra Cornuda',
				nombre_cientifico='Eremophila alpestris')
			db.Cat_conabio_aves.insert(
				nombre_comun='Alquita Crestada',
				nombre_cientifico='Aethia cristatella')
			db.Cat_conabio_aves.insert(
				nombre_comun='Alquita Oscura',
				nombre_cientifico='Ptychoramphus aleuticus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Alquita Perico',
				nombre_cientifico='Aethia psittacula')
			db.Cat_conabio_aves.insert(
				nombre_comun='Anhinga Americana',
				nombre_cientifico='Anhinga anhinga')
			db.Cat_conabio_aves.insert(
				nombre_comun='Arao Común',
				nombre_cientifico='Uria aalge')
			db.Cat_conabio_aves.insert(
				nombre_comun='Arao Pichón',
				nombre_cientifico='Cepphus columba')
			db.Cat_conabio_aves.insert(
				nombre_comun='Arrocero Americano',
				nombre_cientifico='Spiza americana')
			db.Cat_conabio_aves.insert(
				nombre_comun='Ave Sol',
				nombre_cientifico='Eurypyga helias')
			db.Cat_conabio_aves.insert(
				nombre_comun='Avefría Tero',
				nombre_cientifico='Vanellus chilensis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Avetoro Menor',
				nombre_cientifico='Ixobrychus exilis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Avetoro Neotropical',
				nombre_cientifico='Botaurus pinnatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Avetoro Norteño',
				nombre_cientifico='Botaurus lentiginosus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Avoceta Americana',
				nombre_cientifico='Recurvirostra americana')
			db.Cat_conabio_aves.insert(
				nombre_comun='Azulejo Garganta Azul',
				nombre_cientifico='Sialia mexicana')
			db.Cat_conabio_aves.insert(
				nombre_comun='Azulejo Garganta Canela',
				nombre_cientifico='Sialia sialis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Azulejo Pálido',
				nombre_cientifico='Sialia currucoides')
			db.Cat_conabio_aves.insert(
				nombre_comun='Bajapalos Enano',
				nombre_cientifico='Sitta pygmaea')
			db.Cat_conabio_aves.insert(
				nombre_comun='Bajapalos Pecho Blanco',
				nombre_cientifico='Sitta carolinensis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Bajapalos Pecho Canela',
				nombre_cientifico='Sitta canadensis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Baloncillo',
				nombre_cientifico='Auriparus flaviceps')
			db.Cat_conabio_aves.insert(
				nombre_comun='Batará Barrado',
				nombre_cientifico='Thamnophilus doliatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Batará Canelo',
				nombre_cientifico='Thamnistes anabatinus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Batará Mayor',
				nombre_cientifico='Taraba major')
			db.Cat_conabio_aves.insert(
				nombre_comun='Bisbita de Oriente',
				nombre_cientifico='Anthus hodgsoni')
			db.Cat_conabio_aves.insert(
				nombre_comun='Bisbita Garganta Roja',
				nombre_cientifico='Anthus cervinus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Bisbita Llanera',
				nombre_cientifico='Anthus spragueii')
			db.Cat_conabio_aves.insert(
				nombre_comun='Bisbita Norteamericana',
				nombre_cientifico='Anthus rubescens')
			db.Cat_conabio_aves.insert(
				nombre_comun='Bobo Café',
				nombre_cientifico='Sula leucogaster')
			db.Cat_conabio_aves.insert(
				nombre_comun='Bobo de Nazca',
				nombre_cientifico='Sula granti')
			db.Cat_conabio_aves.insert(
				nombre_comun='Bobo Enmascarado',
				nombre_cientifico='Sula dactylatra')
			db.Cat_conabio_aves.insert(
				nombre_comun='Bobo Norteño',
				nombre_cientifico='Morus bassanus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Bobo Patas Azules',
				nombre_cientifico='Sula nebouxii')
			db.Cat_conabio_aves.insert(
				nombre_comun='Bobo Patas Rojas',
				nombre_cientifico='Sula sula')
			db.Cat_conabio_aves.insert(
				nombre_comun='Buco Barbón',
				nombre_cientifico='Malacoptila panamensis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Buco de Collar',
				nombre_cientifico='Notharchus hyperrhynchus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Búho Barrado',
				nombre_cientifico='Strix varia')
			db.Cat_conabio_aves.insert(
				nombre_comun='Búho Barrado Albinegro',
				nombre_cientifico='Ciccaba nigrolineata')
			db.Cat_conabio_aves.insert(
				nombre_comun='Búho Café',
				nombre_cientifico='Ciccaba virgata')
			db.Cat_conabio_aves.insert(
				nombre_comun='Búho Cara Blanca',
				nombre_cientifico='Pseudoscops clamator')
			db.Cat_conabio_aves.insert(
				nombre_comun='Búho Cara Canela',
				nombre_cientifico='Asio otus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Búho Cara Oscura',
				nombre_cientifico='Asio stygius')
			db.Cat_conabio_aves.insert(
				nombre_comun='Búho Cornudo',
				nombre_cientifico='Bubo virginianus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Búho Cuernos Blancos',
				nombre_cientifico='Lophostrix cristata')
			db.Cat_conabio_aves.insert(
				nombre_comun='Búho de Anteojos',
				nombre_cientifico='Pulsatrix perspicillata')
			db.Cat_conabio_aves.insert(
				nombre_comun='Búho Leonado',
				nombre_cientifico='Strix fulvescens')
			db.Cat_conabio_aves.insert(
				nombre_comun='Búho Moteado',
				nombre_cientifico='Strix occidentalis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Búho Sabanero',
				nombre_cientifico='Asio flammeus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cabezón Alas Blancas',
				nombre_cientifico='Pachyramphus polychopterus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cabezón Canelo',
				nombre_cientifico='Pachyramphus cinnamomeus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cabezón Degollado',
				nombre_cientifico='Pachyramphus aglaiae')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cabezón Mexicano',
				nombre_cientifico='Pachyramphus major')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cacique Mexicano',
				nombre_cientifico='Cassiculus melanicterus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cacique Pico Claro',
				nombre_cientifico='Amblycercus holosericeus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Calandria Caperuza Negra',
				nombre_cientifico='Icterus prosthemelas')
			db.Cat_conabio_aves.insert(
				nombre_comun='Calandria Capucha Negra',
				nombre_cientifico='Icterus graduacauda')
			db.Cat_conabio_aves.insert(
				nombre_comun='Calandria Castaña',
				nombre_cientifico='Icterus spurius')
			db.Cat_conabio_aves.insert(
				nombre_comun='Calandria Cejas Naranjas',
				nombre_cientifico='Icterus bullockii')
			db.Cat_conabio_aves.insert(
				nombre_comun='Calandria Cola Amarilla',
				nombre_cientifico='Icterus mesomelas')
			db.Cat_conabio_aves.insert(
				nombre_comun='Calandria de Baltimore',
				nombre_cientifico='Icterus galbula')
			db.Cat_conabio_aves.insert(
				nombre_comun='Calandria de Wagler',
				nombre_cientifico='Icterus wagleri')
			db.Cat_conabio_aves.insert(
				nombre_comun='Calandria Dorso Amarillo',
				nombre_cientifico='Icterus chrysater')
			db.Cat_conabio_aves.insert(
				nombre_comun='Calandria Dorso Naranja',
				nombre_cientifico='Icterus auratus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Calandria Dorso Negro Mayor',
				nombre_cientifico='Icterus gularis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Calandria Dorso Negro Menor',
				nombre_cientifico='Icterus cucullatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Calandria Dorso Rayado',
				nombre_cientifico='Icterus pustulatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Calandria Flancos Negros',
				nombre_cientifico='Icterus abeillei')
			db.Cat_conabio_aves.insert(
				nombre_comun='Calandria Guatemalteca',
				nombre_cientifico='Icterus maculialatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Calandria Pecho Moteado',
				nombre_cientifico='Icterus pectoralis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Calandria Tunera',
				nombre_cientifico='Icterus parisorum')
			db.Cat_conabio_aves.insert(
				nombre_comun='Camea',
				nombre_cientifico='Chamaea fasciata')
			db.Cat_conabio_aves.insert(
				nombre_comun='Capuchino Pecho Escamoso',
				nombre_cientifico='Lonchura punctulata')
			db.Cat_conabio_aves.insert(
				nombre_comun='Capuchino Tricolor',
				nombre_cientifico='Lonchura malacca')
			db.Cat_conabio_aves.insert(
				nombre_comun='Capulinero Gris',
				nombre_cientifico='Ptiliogonys cinereus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Capulinero Negro',
				nombre_cientifico='Phainopepla nitens')
			db.Cat_conabio_aves.insert(
				nombre_comun='Caracara Comecacao',
				nombre_cientifico='Ibycter americanus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Caracara de Isla Guadalupe',
				nombre_cientifico='Caracara lutosa')
			db.Cat_conabio_aves.insert(
				nombre_comun='Caracara Quebrantahuesos',
				nombre_cientifico='Caracara cheriway')
			db.Cat_conabio_aves.insert(
				nombre_comun='Carbonero Cejas Blancas',
				nombre_cientifico='Poecile gambeli')
			db.Cat_conabio_aves.insert(
				nombre_comun='Carbonero Cresta Negra',
				nombre_cientifico='Baeolophus atricristatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Carbonero de Juníperos',
				nombre_cientifico='Baeolophus ridgwayi')
			db.Cat_conabio_aves.insert(
				nombre_comun='Carbonero Embridado',
				nombre_cientifico='Baeolophus wollweberi')
			db.Cat_conabio_aves.insert(
				nombre_comun='Carbonero Encinero',
				nombre_cientifico='Baeolophus inornatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Carbonero Mexicano',
				nombre_cientifico='Poecile sclateri')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cardenal Desértico',
				nombre_cientifico='Cardinalis sinuatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cardenal Rojo',
				nombre_cientifico='Cardinalis cardinalis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Carpintero Albinegro Mayor',
				nombre_cientifico='Picoides villosus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Carpintero Albinegro Menor',
				nombre_cientifico='Picoides pubescens')
			db.Cat_conabio_aves.insert(
				nombre_comun='Carpintero Bellotero',
				nombre_cientifico='Melanerpes formicivorus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Carpintero Café',
				nombre_cientifico='Picoides fumigatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Carpintero Californiano',
				nombre_cientifico='Picoides nuttallii')
			db.Cat_conabio_aves.insert(
				nombre_comun='Carpintero Cara Negra',
				nombre_cientifico='Melanerpes pucherani')
			db.Cat_conabio_aves.insert(
				nombre_comun='Carpintero Castaño',
				nombre_cientifico='Celeus castaneus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Carpintero Cheje',
				nombre_cientifico='Melanerpes aurifrons')
			db.Cat_conabio_aves.insert(
				nombre_comun='Carpintero Corona Gris',
				nombre_cientifico='Colaptes auricularis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Carpintero de Arizona',
				nombre_cientifico='Picoides arizonae')
			db.Cat_conabio_aves.insert(
				nombre_comun='Carpintero de Lewis',
				nombre_cientifico='Melanerpes lewis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Carpintero de Pechera Común',
				nombre_cientifico='Colaptes auratus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Carpintero de Pechera del Noroeste',
				nombre_cientifico='Colaptes chrysoides')
			db.Cat_conabio_aves.insert(
				nombre_comun='Carpintero del Balsas',
				nombre_cientifico='Melanerpes hypopolius')
			db.Cat_conabio_aves.insert(
				nombre_comun='Carpintero del Desierto',
				nombre_cientifico='Melanerpes uropygialis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Carpintero Elegante',
				nombre_cientifico='Sphyrapicus thyroideus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Carpintero Enmascarado',
				nombre_cientifico='Melanerpes chrysogenys')
			db.Cat_conabio_aves.insert(
				nombre_comun='Carpintero Imperial',
				nombre_cientifico='Campephilus imperialis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Carpintero Lineado',
				nombre_cientifico='Dryocopus lineatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Carpintero Mexicano',
				nombre_cientifico='Picoides scalaris')
			db.Cat_conabio_aves.insert(
				nombre_comun='Carpintero Moteado',
				nombre_cientifico='Sphyrapicus varius')
			db.Cat_conabio_aves.insert(
				nombre_comun='Carpintero Nuca Roja',
				nombre_cientifico='Sphyrapicus nuchalis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Carpintero Olivo',
				nombre_cientifico='Colaptes rubiginosus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Carpintero Pecho Rojo',
				nombre_cientifico='Sphyrapicus ruber')
			db.Cat_conabio_aves.insert(
				nombre_comun='Carpintero Pico Plateado',
				nombre_cientifico='Campephilus guatemalensis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Carpintero Transvolcánico',
				nombre_cientifico='Picoides stricklandi')
			db.Cat_conabio_aves.insert(
				nombre_comun='Carpintero Yucateco',
				nombre_cientifico='Melanerpes pygmaeus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Carrao',
				nombre_cientifico='Aramus guarauna')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cascanueces Americano',
				nombre_cientifico='Nucifraga columbiana')
			db.Cat_conabio_aves.insert(
				nombre_comun='Centzontle de Isla Socorro',
				nombre_cientifico='Mimus graysoni')
			db.Cat_conabio_aves.insert(
				nombre_comun='Centzontle Norteño',
				nombre_cientifico='Mimus polyglottos')
			db.Cat_conabio_aves.insert(
				nombre_comun='Centzontle Tropical',
				nombre_cientifico='Mimus gilvus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cerceta Alas Azules',
				nombre_cientifico='Anas discors')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cerceta Alas Verdes',
				nombre_cientifico='Anas crecca')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cerceta Canela',
				nombre_cientifico='Anas cyanoptera')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cerceta Cejas Blancas',
				nombre_cientifico='Anas querquedula')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cernícalo Americano',
				nombre_cientifico='Falco sparverius')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chachalaca Oriental',
				nombre_cientifico='Ortalis vetula')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chachalaca Pálida',
				nombre_cientifico='Ortalis poliocephala')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chachalaca Vientre Blanco',
				nombre_cientifico='Ortalis leucogastra')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chachalaca Vientre Castaño',
				nombre_cientifico='Ortalis wagleri')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chara Copetona',
				nombre_cientifico='Cyanocitta stelleri')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chara de Collar',
				nombre_cientifico='Aphelocoma californica')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chara de Niebla',
				nombre_cientifico='Cyanolyca pumilo')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chara de San Blas',
				nombre_cientifico='Cyanocorax sanblasianus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chara Enana',
				nombre_cientifico='Cyanolyca nana')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chara Garganta Blanca',
				nombre_cientifico='Cyanolyca mirabilis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chara Gorro Azul',
				nombre_cientifico='Cyanolyca cucullata')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chara Pea',
				nombre_cientifico='Psilorhinus morio')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chara Pecho Gris',
				nombre_cientifico='Aphelocoma wollweberi')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chara Piñonera',
				nombre_cientifico='Gymnorhinus cyanocephalus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chara Pinta',
				nombre_cientifico='Cyanocorax dickeyi')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chara Sinaloense',
				nombre_cientifico='Cyanocorax beecheii')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chara Transvolcánica',
				nombre_cientifico='Aphelocoma ultramarina')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chara Unicolor',
				nombre_cientifico='Aphelocoma unicolor')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chara Verde',
				nombre_cientifico='Cyanocorax yncas')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chara Yucateca',
				nombre_cientifico='Cyanocorax yucatanicus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Charrán Albinegro',
				nombre_cientifico='Onychoprion fuscatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Charrán Ártico',
				nombre_cientifico='Sterna paradisaea')
			db.Cat_conabio_aves.insert(
				nombre_comun='Charrán Blanco',
				nombre_cientifico='Gygis alba')
			db.Cat_conabio_aves.insert(
				nombre_comun='Charrán Café',
				nombre_cientifico='Anous stolidus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Charrán Común',
				nombre_cientifico='Sterna hirundo')
			db.Cat_conabio_aves.insert(
				nombre_comun='Charrán Corona Blanca',
				nombre_cientifico='Anous minutus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Charrán de Forster',
				nombre_cientifico='Sterna forsteri')
			db.Cat_conabio_aves.insert(
				nombre_comun='Charrán de Sandwich',
				nombre_cientifico='Thalasseus sandvicensis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Charrán del Caspio',
				nombre_cientifico='Hydroprogne caspia')
			db.Cat_conabio_aves.insert(
				nombre_comun='Charrán Elegante',
				nombre_cientifico='Thalasseus elegans')
			db.Cat_conabio_aves.insert(
				nombre_comun='Charrán Embridado',
				nombre_cientifico='Onychoprion anaethetus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Charrán Mínimo',
				nombre_cientifico='Sternula antillarum')
			db.Cat_conabio_aves.insert(
				nombre_comun='Charrán Negro',
				nombre_cientifico='Chlidonias niger')
			db.Cat_conabio_aves.insert(
				nombre_comun='Charrán Pico Grueso',
				nombre_cientifico='Gelochelidon nilotica')
			db.Cat_conabio_aves.insert(
				nombre_comun='Charrán Real',
				nombre_cientifico='Thalasseus maximus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Charrán Rosado',
				nombre_cientifico='Sterna dougallii')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chinchinero Común',
				nombre_cientifico='Chlorospingus flavopectus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chinito',
				nombre_cientifico='Bombycilla cedrorum')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe Alas Amarillas',
				nombre_cientifico='Vermivora chrysoptera')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe Alas Azules',
				nombre_cientifico='Vermivora cyanoptera')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe Amarillo',
				nombre_cientifico='Setophaga petechia')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe Arroyero',
				nombre_cientifico='Parkesia motacilla')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe Atigrado',
				nombre_cientifico='Setophaga tigrina')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe Azulnegro',
				nombre_cientifico='Setophaga caerulescens')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe Cabeza Amarilla',
				nombre_cientifico='Setophaga occidentalis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe Cabeza Gris',
				nombre_cientifico='Oreothlypis ruficapilla')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe Cabeza Negra',
				nombre_cientifico='Setophaga striata')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe Cachetes Amarillos',
				nombre_cientifico='Setophaga chrysoparia')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe Cara Roja',
				nombre_cientifico='Cardellina rubrifrons')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe Castaño',
				nombre_cientifico='Setophaga castanea')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe Cejas Amarillas',
				nombre_cientifico='Setophaga graciae')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe Cejas Blancas',
				nombre_cientifico='Oreothlypis superciliosa')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe Cejas Doradas',
				nombre_cientifico='Basileuterus belli')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe Cejas Negras',
				nombre_cientifico='Basileuterus culicivorus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe Celeste',
				nombre_cientifico='Setophaga cerulea')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe Charquero',
				nombre_cientifico='Parkesia noveboracensis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe Corona Café',
				nombre_cientifico='Limnothlypis swainsonii')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe Corona Negra',
				nombre_cientifico='Cardellina pusilla')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe de Colima',
				nombre_cientifico='Oreothlypis crissalis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe de Collar',
				nombre_cientifico='Cardellina canadensis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe de Connecticut',
				nombre_cientifico='Oporornis agilis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe de Magnolias',
				nombre_cientifico='Setophaga magnolia')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe de Pechera',
				nombre_cientifico='Geothlypis philadelphia')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe de Pradera',
				nombre_cientifico='Setophaga discolor')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe de Townsend',
				nombre_cientifico='Setophaga townsendi')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe de Virginia',
				nombre_cientifico='Oreothlypis virginiae')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe Dorado',
				nombre_cientifico='Protonotaria citrea')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe Dorso Verde',
				nombre_cientifico='Setophaga virens')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe Encapuchado',
				nombre_cientifico='Setophaga citrina')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe Flancos Castaños',
				nombre_cientifico='Setophaga pensylvanica')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe Garganta Amarilla',
				nombre_cientifico='Setophaga dominica')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe Garganta Naranja',
				nombre_cientifico='Setophaga fusca')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe Gorra Canela',
				nombre_cientifico='Basileuterus rufifrons')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe Grande',
				nombre_cientifico='Icteria virens')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe Gusanero',
				nombre_cientifico='Helmitheros vermivorum')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe Lores Negros',
				nombre_cientifico='Geothlypis tolmiei')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe Negrogris',
				nombre_cientifico='Setophaga nigrescens')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe Oliváceo',
				nombre_cientifico='Oreothlypis celata')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe Patilludo',
				nombre_cientifico='Geothlypis formosa')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe Pecho Manchado',
				nombre_cientifico='Setophaga americana')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe Peregrino',
				nombre_cientifico='Oreothlypis peregrina')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe Pinero',
				nombre_cientifico='Setophaga pinus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe Playero',
				nombre_cientifico='Setophaga palmarum')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe Rabadilla Amarilla',
				nombre_cientifico='Setophaga coronata')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe Rabadilla Castaña',
				nombre_cientifico='Oreothlypis luciae')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe Rojo',
				nombre_cientifico='Cardellina rubra')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe Rosado',
				nombre_cientifico='Cardellina versicolor')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe Suelero',
				nombre_cientifico='Seiurus aurocapilla')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe Trepador',
				nombre_cientifico='Mniotilta varia')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chipe Tropical',
				nombre_cientifico='Setophaga pitiayumi')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chocha del Este',
				nombre_cientifico='Scolopax minor')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chorlo Carambolo',
				nombre_cientifico='Charadrius morinellus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chorlo Chiflador',
				nombre_cientifico='Charadrius melodus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chorlo de Collar',
				nombre_cientifico='Charadrius collaris')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chorlo Dorado Americano',
				nombre_cientifico='Pluvialis dominica')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chorlo Dorado del Pacífico',
				nombre_cientifico='Pluvialis fulva')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chorlo Gris',
				nombre_cientifico='Pluvialis squatarola')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chorlo Llanero',
				nombre_cientifico='Charadrius montanus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chorlo Nevado',
				nombre_cientifico='Charadrius nivosus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chorlo Pico Grueso',
				nombre_cientifico='Charadrius wilsonia')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chorlo Semipalmeado',
				nombre_cientifico='Charadrius semipalmatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chorlo Tildío',
				nombre_cientifico='Charadrius vociferus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chotacabras Cola Corta',
				nombre_cientifico='Lurocalis semitorquatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chotacabras Menor',
				nombre_cientifico='Chordeiles acutipennis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chotacabras Pauraque',
				nombre_cientifico='Nyctidromus albicollis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Chotacabras Zumbón',
				nombre_cientifico='Chordeiles minor')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cigüeña Americana',
				nombre_cientifico='Mycteria americana')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cigüeña Jabirú',
				nombre_cientifico='Jabiru mycteria')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cisne de Tundra',
				nombre_cientifico='Cygnus columbianus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cisne Trompetero',
				nombre_cientifico='Cygnus buccinator')
			db.Cat_conabio_aves.insert(
				nombre_comun='Clarín Jilguero',
				nombre_cientifico='Myadestes occidentalis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Clarín Norteño',
				nombre_cientifico='Myadestes townsendi')
			db.Cat_conabio_aves.insert(
				nombre_comun='Clarín Unicolor',
				nombre_cientifico='Myadestes unicolor')
			db.Cat_conabio_aves.insert(
				nombre_comun='Clorofonia Corona Azul',
				nombre_cientifico='Chlorophonia occipitalis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Coa Cabeza Negra',
				nombre_cientifico='Trogon melanocephalus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Coa Citrina',
				nombre_cientifico='Trogon citreolus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Coa Cola Oscura',
				nombre_cientifico='Trogon massena')
			db.Cat_conabio_aves.insert(
				nombre_comun='Coa de Collar',
				nombre_cientifico='Trogon collaris')
			db.Cat_conabio_aves.insert(
				nombre_comun='Coa Elegante',
				nombre_cientifico='Trogon elegans')
			db.Cat_conabio_aves.insert(
				nombre_comun='Coa Mexicana',
				nombre_cientifico='Trogon mexicanus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Coa Violácea Norteña',
				nombre_cientifico='Trogon caligatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Codorniz Barrada',
				nombre_cientifico='Philortyx fasciatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Codorniz Bolonchaco',
				nombre_cientifico='Odontophorus guttatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Codorniz Californiana',
				nombre_cientifico='Callipepla californica')
			db.Cat_conabio_aves.insert(
				nombre_comun='Codorniz Coluda Centroamericana',
				nombre_cientifico='Dendrortyx leucophrys')
			db.Cat_conabio_aves.insert(
				nombre_comun='Codorniz Coluda Transvolcánica',
				nombre_cientifico='Dendrortyx macroura')
			db.Cat_conabio_aves.insert(
				nombre_comun='Codorniz Coluda Veracruzana',
				nombre_cientifico='Dendrortyx barbatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Codorniz Cotuí',
				nombre_cientifico='Colinus virginianus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Codorniz Cresta Dorada',
				nombre_cientifico='Callipepla douglasii')
			db.Cat_conabio_aves.insert(
				nombre_comun='Codorniz de Gambel',
				nombre_cientifico='Callipepla gambelii')
			db.Cat_conabio_aves.insert(
				nombre_comun='Codorniz de Moctezuma',
				nombre_cientifico='Cyrtonyx montezumae')
			db.Cat_conabio_aves.insert(
				nombre_comun='Codorniz de Montaña',
				nombre_cientifico='Oreortyx pictus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Codorniz Escamosa',
				nombre_cientifico='Callipepla squamata')
			db.Cat_conabio_aves.insert(
				nombre_comun='Codorniz Ocelada',
				nombre_cientifico='Cyrtonyx ocellatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Codorniz Silbadora',
				nombre_cientifico='Dactylortyx thoracicus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Codorniz Yucateca',
				nombre_cientifico='Colinus nigrogularis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colibrí Barba Negra',
				nombre_cientifico='Archilochus alexandri')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colibrí Berilo',
				nombre_cientifico='Amazilia beryllina')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colibrí Cabeza Roja',
				nombre_cientifico='Calypte anna')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colibrí Cabeza Violeta',
				nombre_cientifico='Calypte costae')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colibrí Cándido',
				nombre_cientifico='Amazilia candida')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colibrí Canelo',
				nombre_cientifico='Amazilia rutila')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colibrí Capucha Azul',
				nombre_cientifico='Florisuga mellivora')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colibrí Cola Azul',
				nombre_cientifico='Amazilia cyanura')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colibrí Cola Canela',
				nombre_cientifico='Amazilia tzacatl')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colibrí Cola Pinta',
				nombre_cientifico='Tilmatura dupontii')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colibrí Cola Rayada',
				nombre_cientifico='Eupherusa eximia')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colibrí Corona Azul',
				nombre_cientifico='Amazilia cyanocephala')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colibrí Corona Violeta',
				nombre_cientifico='Amazilia violiceps')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colibrí Ermitaño Enano',
				nombre_cientifico='Phaethornis striigularis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colibrí Ermitaño Mesoamericano',
				nombre_cientifico='Phaethornis longirostris')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colibrí Frente Verde',
				nombre_cientifico='Amazilia viridifrons')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colibrí Garganta Amatista',
				nombre_cientifico='Lampornis amethystinus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colibrí Garganta Azul',
				nombre_cientifico='Lampornis clemenciae')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colibrí Garganta Negra',
				nombre_cientifico='Anthracothorax prevostii')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colibrí Garganta Rubí',
				nombre_cientifico='Archilochus colubris')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colibrí Garganta Verde',
				nombre_cientifico='Lampornis viridipallens')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colibrí Guerrerense',
				nombre_cientifico='Eupherusa poliocerca')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colibrí Hada Enmascarada',
				nombre_cientifico='Heliothryx barroti')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colibrí Lucifer',
				nombre_cientifico='Calothorax lucifer')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colibrí Magnífico',
				nombre_cientifico='Eugenes fulgens')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colibrí Miahuatleco',
				nombre_cientifico='Eupherusa cyanophrys')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colibrí Mixteco',
				nombre_cientifico='Calothorax pulcher')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colibrí Multicolor',
				nombre_cientifico='Lamprolaima rhami')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colibrí Opaco',
				nombre_cientifico='Cynanthus sordidus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colibrí Orejas Violetas',
				nombre_cientifico='Colibri thalassinus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colibrí Pecho Escamoso',
				nombre_cientifico='Phaeochroa cuvierii')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colibrí Pico Ancho',
				nombre_cientifico='Cynanthus latirostris')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colibrí Pico Corto',
				nombre_cientifico='Abeillia abeillei')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colibrí Picudo Coroniazul',
				nombre_cientifico='Heliomaster longirostris')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colibrí Picudo Occidental',
				nombre_cientifico='Heliomaster constantii')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colibrí Tijereta Guatemalteco',
				nombre_cientifico='Doricha enicura')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colibrí Tijereta Mexicano',
				nombre_cientifico='Doricha eliza')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colibrí Vientre Canelo',
				nombre_cientifico='Amazilia yucatanensis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colimbo Ártico',
				nombre_cientifico='Gavia arctica')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colimbo Común',
				nombre_cientifico='Gavia immer')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colimbo del Pacífico',
				nombre_cientifico='Gavia pacifica')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colimbo Menor',
				nombre_cientifico='Gavia stellata')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colimbo Pico Amarillo',
				nombre_cientifico='Gavia adamsii')
			db.Cat_conabio_aves.insert(
				nombre_comun='Collalba Norteña',
				nombre_cientifico='Oenanthe oenanthe')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colorín Azul',
				nombre_cientifico='Passerina cyanea')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colorín Azulnegro',
				nombre_cientifico='Cyanocompsa parellina')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colorín Azulrosa',
				nombre_cientifico='Passerina rositae')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colorín Morado',
				nombre_cientifico='Passerina versicolor')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colorín Pecho Canela',
				nombre_cientifico='Passerina amoena')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colorín Pecho Naranja',
				nombre_cientifico='Passerina leclancherii')
			db.Cat_conabio_aves.insert(
				nombre_comun='Colorín Sietecolores',
				nombre_cientifico='Passerina ciris')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cóndor Californiano',
				nombre_cientifico='Gymnogyps californianus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Coqueta Cresta Negra',
				nombre_cientifico='Lophornis helenae')
			db.Cat_conabio_aves.insert(
				nombre_comun='Coqueta de Atoyac',
				nombre_cientifico='Lophornis brachylophus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cormorán de Brandt',
				nombre_cientifico='Phalacrocorax penicillatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cormorán Neotropical',
				nombre_cientifico='Phalacrocorax brasilianus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cormorán Orejón',
				nombre_cientifico='Phalacrocorax auritus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cormorán Pelágico',
				nombre_cientifico='Phalacrocorax pelagicus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Correcaminos Norteño',
				nombre_cientifico='Geococcyx californianus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Correcaminos Tropical',
				nombre_cientifico='Geococcyx velox')
			db.Cat_conabio_aves.insert(
				nombre_comun='Costurero Pico Corto',
				nombre_cientifico='Limnodromus griseus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Costurero Pico Largo',
				nombre_cientifico='Limnodromus scolopaceus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cotinga Azuleja',
				nombre_cientifico='Cotinga amabilis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cotorra Serrana Occidental',
				nombre_cientifico='Rhynchopsitta pachyrhyncha')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cotorra Serrana Oriental',
				nombre_cientifico='Rhynchopsitta terrisi')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cuclillo Canelo',
				nombre_cientifico='Piaya cayana')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cuclillo Faisán',
				nombre_cientifico='Dromococcyx phasianellus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cuclillo Manglero',
				nombre_cientifico='Coccyzus minor')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cuclillo Pico Amarillo',
				nombre_cientifico='Coccyzus americanus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cuclillo Pico Negro',
				nombre_cientifico='Coccyzus erythropthalmus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cuclillo Rayado',
				nombre_cientifico='Tapera naevia')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cuclillo Terrestre',
				nombre_cientifico='Morococcyx erythropygus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cuervo Común',
				nombre_cientifico='Corvus corax')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cuervo Llanero',
				nombre_cientifico='Corvus cryptoleucus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cuervo Norteamericano',
				nombre_cientifico='Corvus brachyrhynchos')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cuervo Sinaloense',
				nombre_cientifico='Corvus sinaloae')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cuervo Tamaulipeco',
				nombre_cientifico='Corvus imparatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cuevero de Nava',
				nombre_cientifico='Hylorchilus navai')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cuevero de Sumichrast',
				nombre_cientifico='Hylorchilus sumichrasti')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cuicacoche Bajacaliforniano',
				nombre_cientifico='Toxostoma cinereum')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cuicacoche Californiano',
				nombre_cientifico='Toxostoma redivivum')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cuicacoche Castaño',
				nombre_cientifico='Toxostoma rufum')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cuicacoche Chato',
				nombre_cientifico='Oreoscoptes montanus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cuicacoche Crisal',
				nombre_cientifico='Toxostoma crissale')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cuicacoche de Cozumel',
				nombre_cientifico='Toxostoma guttatum')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cuicacoche Moteado',
				nombre_cientifico='Toxostoma ocellatum')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cuicacoche Pálido',
				nombre_cientifico='Toxostoma lecontei')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cuicacoche Pico Corto',
				nombre_cientifico='Toxostoma bendirei')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cuicacoche Pico Curvo',
				nombre_cientifico='Toxostoma curvirostre')
			db.Cat_conabio_aves.insert(
				nombre_comun='Cuicacoche Pico Largo',
				nombre_cientifico='Toxostoma longirostre')
			db.Cat_conabio_aves.insert(
				nombre_comun='Escribano Ártico',
				nombre_cientifico='Calcarius lapponicus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Escribano Collar Castaño',
				nombre_cientifico='Calcarius ornatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Escribano de McCown',
				nombre_cientifico='Rhynchophanes mccownii')
			db.Cat_conabio_aves.insert(
				nombre_comun='Escribano Pigmeo',
				nombre_cientifico='Emberiza pusilla')
			db.Cat_conabio_aves.insert(
				nombre_comun='Esmeralda de Cozumel',
				nombre_cientifico='Chlorostilbon forficatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Esmeralda Occidental',
				nombre_cientifico='Chlorostilbon auriceps')
			db.Cat_conabio_aves.insert(
				nombre_comun='Esmeralda Oriental',
				nombre_cientifico='Chlorostilbon canivetii')
			db.Cat_conabio_aves.insert(
				nombre_comun='Espátula Rosada',
				nombre_cientifico='Platalea ajaja')
			db.Cat_conabio_aves.insert(
				nombre_comun='Estornino Pinto',
				nombre_cientifico='Sturnus vulgaris')
			db.Cat_conabio_aves.insert(
				nombre_comun='Eufonia Garganta Amarilla',
				nombre_cientifico='Euphonia hirundinacea')
			db.Cat_conabio_aves.insert(
				nombre_comun='Eufonia Garganta Negra',
				nombre_cientifico='Euphonia affinis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Eufonia Gorra Azul',
				nombre_cientifico='Euphonia elegantissima')
			db.Cat_conabio_aves.insert(
				nombre_comun='Eufonia Olivácea',
				nombre_cientifico='Euphonia gouldi')
			db.Cat_conabio_aves.insert(
				nombre_comun='Eufonia Vientre Blanco',
				nombre_cientifico='Euphonia minuta')
			db.Cat_conabio_aves.insert(
				nombre_comun='Faisán de Collar',
				nombre_cientifico='Phasianus colchicus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Falaropo Cuello Rojo',
				nombre_cientifico='Phalaropus lobatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Falaropo Pico Grueso',
				nombre_cientifico='Phalaropus fulicarius')
			db.Cat_conabio_aves.insert(
				nombre_comun='Falaropo Pico Largo',
				nombre_cientifico='Phalaropus tricolor')
			db.Cat_conabio_aves.insert(
				nombre_comun='Fandanguero Canelo',
				nombre_cientifico='Campylopterus rufus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Fandanguero Mexicano',
				nombre_cientifico='Campylopterus curvipennis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Fandanguero Morado',
				nombre_cientifico='Campylopterus hemileucurus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Fandanguero Tuxtleño',
				nombre_cientifico='Campylopterus excellens')
			db.Cat_conabio_aves.insert(
				nombre_comun='Flamenco Americano',
				nombre_cientifico='Phoenicopterus ruber')
			db.Cat_conabio_aves.insert(
				nombre_comun='Flautín Cabezón Mesoamericano',
				nombre_cientifico='Schiffornis veraepacis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Fragata Pelágica',
				nombre_cientifico='Fregata minor')
			db.Cat_conabio_aves.insert(
				nombre_comun='Fragata Tijereta',
				nombre_cientifico='Fregata magnificens')
			db.Cat_conabio_aves.insert(
				nombre_comun='Fulmar Norteño',
				nombre_cientifico='Fulmarus glacialis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gallareta Americana',
				nombre_cientifico='Fulica americana')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gallineta Frente Roja',
				nombre_cientifico='Gallinula galeata')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gallineta Morada',
				nombre_cientifico='Porphyrio martinicus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Ganso Blanco',
				nombre_cientifico='Chen caerulescens')
			db.Cat_conabio_aves.insert(
				nombre_comun='Ganso Canadiense Mayor',
				nombre_cientifico='Branta canadensis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Ganso Canadiense Menor',
				nombre_cientifico='Branta hutchinsii')
			db.Cat_conabio_aves.insert(
				nombre_comun='Ganso Careto Mayor',
				nombre_cientifico='Anser albifrons')
			db.Cat_conabio_aves.insert(
				nombre_comun='Ganso de Collar',
				nombre_cientifico='Branta bernicla')
			db.Cat_conabio_aves.insert(
				nombre_comun='Ganso de Ross',
				nombre_cientifico='Chen rossii')
			db.Cat_conabio_aves.insert(
				nombre_comun='Garcita Verde',
				nombre_cientifico='Butorides virescens')
			db.Cat_conabio_aves.insert(
				nombre_comun='Garrapatero Pico Liso',
				nombre_cientifico='Crotophaga ani')
			db.Cat_conabio_aves.insert(
				nombre_comun='Garrapatero Pijuy',
				nombre_cientifico='Crotophaga sulcirostris')
			db.Cat_conabio_aves.insert(
				nombre_comun='Garza Agami',
				nombre_cientifico='Agamia agami')
			db.Cat_conabio_aves.insert(
				nombre_comun='Garza Azul',
				nombre_cientifico='Egretta caerulea')
			db.Cat_conabio_aves.insert(
				nombre_comun='Garza Blanca',
				nombre_cientifico='Ardea alba')
			db.Cat_conabio_aves.insert(
				nombre_comun='Garza Cucharón',
				nombre_cientifico='Cochlearius cochlearius')
			db.Cat_conabio_aves.insert(
				nombre_comun='Garza Dedos Dorados',
				nombre_cientifico='Egretta thula')
			db.Cat_conabio_aves.insert(
				nombre_comun='Garza Ganadera',
				nombre_cientifico='Bubulcus ibis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Garza Morena',
				nombre_cientifico='Ardea herodias')
			db.Cat_conabio_aves.insert(
				nombre_comun='Garza Nocturna Corona Clara',
				nombre_cientifico='Nyctanassa violacea')
			db.Cat_conabio_aves.insert(
				nombre_comun='Garza Nocturna Corona Negra',
				nombre_cientifico='Nycticorax nycticorax')
			db.Cat_conabio_aves.insert(
				nombre_comun='Garza Rojiza',
				nombre_cientifico='Egretta rufescens')
			db.Cat_conabio_aves.insert(
				nombre_comun='Garza Tigre Mexicana',
				nombre_cientifico='Tigrisoma mexicanum')
			db.Cat_conabio_aves.insert(
				nombre_comun='Garza Tricolor',
				nombre_cientifico='Egretta tricolor')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gavilán Azor',
				nombre_cientifico='Accipiter gentilis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gavilán Bicolor',
				nombre_cientifico='Accipiter bicolor')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gavilán Bidentado',
				nombre_cientifico='Harpagus bidentatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gavilán Cabeza Gris',
				nombre_cientifico='Leptodon cayanensis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gavilán Caracolero',
				nombre_cientifico='Rostrhamus sociabilis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gavilán de Cooper',
				nombre_cientifico='Accipiter cooperii')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gavilán Pecho Canela',
				nombre_cientifico='Accipiter striatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gavilán Pico de Gancho',
				nombre_cientifico='Chondrohierax uncinatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gavilán Rastrero',
				nombre_cientifico='Circus cyaneus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gavilán Zancón',
				nombre_cientifico='Geranospiza caerulescens')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gaviota Alas Blancas',
				nombre_cientifico='Larus glaucescens')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gaviota Bajacaliforniana',
				nombre_cientifico='Larus livens')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gaviota Blanca',
				nombre_cientifico='Larus hyperboreus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gaviota Californiana',
				nombre_cientifico='Larus californicus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gaviota Cana',
				nombre_cientifico='Larus canus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gaviota Cola Hendida',
				nombre_cientifico='Xema sabini')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gaviota Cola Negra',
				nombre_cientifico='Larus crassirostris')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gaviota de Bonaparte',
				nombre_cientifico='Chroicocephalus philadelphia')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gaviota de Franklin',
				nombre_cientifico='Leucophaeus pipixcan')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gaviota de Thayer',
				nombre_cientifico='Larus thayeri')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gaviota Encapuchada',
				nombre_cientifico='Chroicocephalus ridibundus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gaviota Gris',
				nombre_cientifico='Leucophaeus modestus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gaviota Mayor',
				nombre_cientifico='Larus marinus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gaviota Menor',
				nombre_cientifico='Hydrocoloeus minutus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gaviota Meridional',
				nombre_cientifico='Larus dominicanus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gaviota Occidental',
				nombre_cientifico='Larus occidentalis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gaviota Patas Negras',
				nombre_cientifico='Rissa tridactyla')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gaviota Pico Anillado',
				nombre_cientifico='Larus delawarensis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gaviota Plateada',
				nombre_cientifico='Larus argentatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gaviota Plomiza',
				nombre_cientifico='Larus heermanni')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gaviota Reidora',
				nombre_cientifico='Leucophaeus atricilla')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gaviota Sombría',
				nombre_cientifico='Larus fuscus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Golondrina Alas Aserradas',
				nombre_cientifico='Stelgidopteryx serripennis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Golondrina Albiazul',
				nombre_cientifico='Pygochelidon cyanoleuca')
			db.Cat_conabio_aves.insert(
				nombre_comun='Golondrina Azulnegra',
				nombre_cientifico='Progne subis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Golondrina Bicolor',
				nombre_cientifico='Tachycineta bicolor')
			db.Cat_conabio_aves.insert(
				nombre_comun='Golondrina Gorra Negra',
				nombre_cientifico='Notiochelidon pileata')
			db.Cat_conabio_aves.insert(
				nombre_comun='Golondrina Manglera',
				nombre_cientifico='Tachycineta albilinea')
			db.Cat_conabio_aves.insert(
				nombre_comun='Golondrina Pecho Gris',
				nombre_cientifico='Progne chalybea')
			db.Cat_conabio_aves.insert(
				nombre_comun='Golondrina Pueblera',
				nombre_cientifico='Petrochelidon fulva')
			db.Cat_conabio_aves.insert(
				nombre_comun='Golondrina Ribereña',
				nombre_cientifico='Riparia riparia')
			db.Cat_conabio_aves.insert(
				nombre_comun='Golondrina Risquera',
				nombre_cientifico='Petrochelidon pyrrhonota')
			db.Cat_conabio_aves.insert(
				nombre_comun='Golondrina Sinaloense',
				nombre_cientifico='Progne sinaloae')
			db.Cat_conabio_aves.insert(
				nombre_comun='Golondrina Tijereta',
				nombre_cientifico='Hirundo rustica')
			db.Cat_conabio_aves.insert(
				nombre_comun='Golondrina Verdemar',
				nombre_cientifico='Tachycineta thalassina')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gorrión Alas Blancas',
				nombre_cientifico='Calamospiza melanocorys')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gorrión Arlequín',
				nombre_cientifico='Chondestes grammacus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gorrión Barba Negra',
				nombre_cientifico='Spizella atrogularis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gorrión Canario Sabanero',
				nombre_cientifico='Sicalis luteola')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gorrión Cantor',
				nombre_cientifico='Melospiza melodia')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gorrión Cejas Blancas',
				nombre_cientifico='Spizella passerina')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gorrión Chapulín',
				nombre_cientifico='Ammodramus savannarum')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gorrión Chingolo',
				nombre_cientifico='Zonotrichia capensis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gorrión Cola Blanca',
				nombre_cientifico='Pooecetes gramineus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gorrión Corona Amarilla',
				nombre_cientifico='Zonotrichia atricapilla')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gorrión Corona Blanca',
				nombre_cientifico='Zonotrichia leucophrys')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gorrión Costero',
				nombre_cientifico='Ammodramus maritimus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gorrión de Baird',
				nombre_cientifico='Ammodramus bairdii')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gorrión de Brewer',
				nombre_cientifico='Spizella breweri')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gorrión de Harris',
				nombre_cientifico='Zonotrichia querula')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gorrión de Le Conte',
				nombre_cientifico='Ammodramus leconteii')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gorrión de Lincoln',
				nombre_cientifico='Melospiza lincolnii')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gorrión de Nelson',
				nombre_cientifico='Ammodramus nelsoni')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gorrión de Worthen',
				nombre_cientifico='Spizella wortheni')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gorrión Doméstico',
				nombre_cientifico='Passer domesticus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gorrión Garganta Blanca',
				nombre_cientifico='Zonotrichia albicollis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gorrión Llanero',
				nombre_cientifico='Spizella pusilla')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gorrión Pálido',
				nombre_cientifico='Spizella pallida')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gorrión Pantanero',
				nombre_cientifico='Melospiza georgiana')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gorrión Rascador',
				nombre_cientifico='Passerella iliaca')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gorrión Sabanero',
				nombre_cientifico='Passerculus sandwichensis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Gorrión Serrano',
				nombre_cientifico='Xenospiza baileyi')
			db.Cat_conabio_aves.insert(
				nombre_comun='Granatelo Mexicano',
				nombre_cientifico='Granatellus venustus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Granatelo Yucateco',
				nombre_cientifico='Granatellus sallaei')
			db.Cat_conabio_aves.insert(
				nombre_comun='Grulla Blanca',
				nombre_cientifico='Grus americana')
			db.Cat_conabio_aves.insert(
				nombre_comun='Grulla Gris',
				nombre_cientifico='Grus canadensis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Guacamaya Roja',
				nombre_cientifico='Ara macao')
			db.Cat_conabio_aves.insert(
				nombre_comun='Guacamaya Verde',
				nombre_cientifico='Ara militaris')
			db.Cat_conabio_aves.insert(
				nombre_comun='Guajolote Norteño',
				nombre_cientifico='Meleagris gallopavo')
			db.Cat_conabio_aves.insert(
				nombre_comun='Guajolote Ocelado',
				nombre_cientifico='Meleagris ocellata')
			db.Cat_conabio_aves.insert(
				nombre_comun='Halcón Esmerejón',
				nombre_cientifico='Falco columbarius')
			db.Cat_conabio_aves.insert(
				nombre_comun='Halcón Fajado',
				nombre_cientifico='Falco femoralis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Halcón Guaco',
				nombre_cientifico='Herpetotheres cachinnans')
			db.Cat_conabio_aves.insert(
				nombre_comun='Halcón Mexicano',
				nombre_cientifico='Falco mexicanus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Halcón Murcielaguero',
				nombre_cientifico='Falco rufigularis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Halcón Pecho Canela',
				nombre_cientifico='Falco deiroleucus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Halcón Peregrino',
				nombre_cientifico='Falco peregrinus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Halcón Selvático Barrado',
				nombre_cientifico='Micrastur ruficollis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Halcón Selvático de Collar',
				nombre_cientifico='Micrastur semitorquatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Hocofaisán',
				nombre_cientifico='Crax rubra')
			db.Cat_conabio_aves.insert(
				nombre_comun='Hojarasquero Oscuro',
				nombre_cientifico='Sclerurus guatemalensis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Hojarasquero Pecho Canela',
				nombre_cientifico='Sclerurus mexicanus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Hormiguero Alas Punteadas',
				nombre_cientifico='Microrhopias quixensis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Hormiguero Cantor',
				nombre_cientifico='Cercomacra tyrannina')
			db.Cat_conabio_aves.insert(
				nombre_comun='Hormiguero Cholino Cara Negra',
				nombre_cientifico='Formicarius analis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Hormiguero Cholino Escamoso',
				nombre_cientifico='Grallaria guatimalensis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Hormiguero Pepito',
				nombre_cientifico='Synallaxis erythrothorax')
			db.Cat_conabio_aves.insert(
				nombre_comun='Hormiguero Plomizo',
				nombre_cientifico='Myrmotherula schisticolor')
			db.Cat_conabio_aves.insert(
				nombre_comun='Hormiguero Sencillo',
				nombre_cientifico='Dysithamnus mentalis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Huilota Caribeña',
				nombre_cientifico='Zenaida aurita')
			db.Cat_conabio_aves.insert(
				nombre_comun='Huilota Común',
				nombre_cientifico='Zenaida macroura')
			db.Cat_conabio_aves.insert(
				nombre_comun='Huilota de Socorro',
				nombre_cientifico='Zenaida graysoni')
			db.Cat_conabio_aves.insert(
				nombre_comun='Ibis Blanco',
				nombre_cientifico='Eudocimus albus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Ibis Cara Oscura',
				nombre_cientifico='Plegadis falcinellus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Ibis Ojos Rojos',
				nombre_cientifico='Plegadis chihi')
			db.Cat_conabio_aves.insert(
				nombre_comun='Jacamar Cola Canela',
				nombre_cientifico='Galbula ruficauda')
			db.Cat_conabio_aves.insert(
				nombre_comun='Jacana Norteña',
				nombre_cientifico='Jacana spinosa')
			db.Cat_conabio_aves.insert(
				nombre_comun='Jilguerito Canario',
				nombre_cientifico='Spinus tristis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Jilguerito Cara Negra',
				nombre_cientifico='Spinus lawrencei')
			db.Cat_conabio_aves.insert(
				nombre_comun='Jilguerito Corona Negra',
				nombre_cientifico='Spinus atriceps')
			db.Cat_conabio_aves.insert(
				nombre_comun='Jilguerito Dominico',
				nombre_cientifico='Spinus psaltria')
			db.Cat_conabio_aves.insert(
				nombre_comun='Jilguerito Encapuchado',
				nombre_cientifico='Spinus notatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Jilguerito Pinero',
				nombre_cientifico='Spinus pinus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Junco de Isla Guadalupe',
				nombre_cientifico='Junco insularis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Junco Ojos de Lumbre',
				nombre_cientifico='Junco phaeonotus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Junco Ojos Negros',
				nombre_cientifico='Junco hyemalis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Lavandera Amarilla',
				nombre_cientifico='Motacilla tschutschensis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Lavandera Blanca',
				nombre_cientifico='Motacilla alba')
			db.Cat_conabio_aves.insert(
				nombre_comun='Lechuza de Campanario',
				nombre_cientifico='Tyto alba')
			db.Cat_conabio_aves.insert(
				nombre_comun='Llorón Fioié',
				nombre_cientifico='Laniocera rufescens')
			db.Cat_conabio_aves.insert(
				nombre_comun='Loro Cabeza Amarilla',
				nombre_cientifico='Amazona oratrix')
			db.Cat_conabio_aves.insert(
				nombre_comun='Loro Cabeza Oscura',
				nombre_cientifico='Pyrilia haematotis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Loro Cachetes Amarillos',
				nombre_cientifico='Amazona autumnalis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Loro Corona Azul',
				nombre_cientifico='Amazona farinosa')
			db.Cat_conabio_aves.insert(
				nombre_comun='Loro Corona Blanca',
				nombre_cientifico='Pionus senilis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Loro Corona Lila',
				nombre_cientifico='Amazona finschi')
			db.Cat_conabio_aves.insert(
				nombre_comun='Loro Frente Blanca',
				nombre_cientifico='Amazona albifrons')
			db.Cat_conabio_aves.insert(
				nombre_comun='Loro Nuca Amarilla',
				nombre_cientifico='Amazona auropalliata')
			db.Cat_conabio_aves.insert(
				nombre_comun='Loro Tamaulipeco',
				nombre_cientifico='Amazona viridigenalis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Loro Yucateco',
				nombre_cientifico='Amazona xantholora')
			db.Cat_conabio_aves.insert(
				nombre_comun='Luis Bienteveo',
				nombre_cientifico='Pitangus sulphuratus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Luis Pico Grueso',
				nombre_cientifico='Megarynchus pitangua')
			db.Cat_conabio_aves.insert(
				nombre_comun='Luisito Común',
				nombre_cientifico='Myiozetetes similis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Martín Pescador Amazónico',
				nombre_cientifico='Chloroceryle amazona')
			db.Cat_conabio_aves.insert(
				nombre_comun='Martín Pescador de Collar',
				nombre_cientifico='Megaceryle torquata')
			db.Cat_conabio_aves.insert(
				nombre_comun='Martín Pescador Enano',
				nombre_cientifico='Chloroceryle aenea')
			db.Cat_conabio_aves.insert(
				nombre_comun='Martín Pescador Norteño',
				nombre_cientifico='Megaceryle alcyon')
			db.Cat_conabio_aves.insert(
				nombre_comun='Martín Pescador Verde',
				nombre_cientifico='Chloroceryle americana')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mascarita Bajacaliforniana',
				nombre_cientifico='Geothlypis beldingi')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mascarita Común',
				nombre_cientifico='Geothlypis trichas')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mascarita de Altamira',
				nombre_cientifico='Geothlypis flavovelata')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mascarita del Lerma',
				nombre_cientifico='Geothlypis speciosa')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mascarita Matorralera',
				nombre_cientifico='Geothlypis nelsoni')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mascarita Pico Grueso',
				nombre_cientifico='Geothlypis poliocephala')
			db.Cat_conabio_aves.insert(
				nombre_comun='Matraca Barrada',
				nombre_cientifico='Campylorhynchus megalopterus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Matraca Chiapaneca',
				nombre_cientifico='Campylorhynchus chiapensis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Matraca del Balsas',
				nombre_cientifico='Campylorhynchus jocosus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Matraca del Desierto',
				nombre_cientifico='Campylorhynchus brunneicapillus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Matraca Nuca Canela',
				nombre_cientifico='Campylorhynchus rufinucha')
			db.Cat_conabio_aves.insert(
				nombre_comun='Matraca Serrana',
				nombre_cientifico='Campylorhynchus gularis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Matraca Tropical',
				nombre_cientifico='Campylorhynchus zonatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Matraca Yucateca',
				nombre_cientifico='Campylorhynchus yucatanicus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Maullador Gris',
				nombre_cientifico='Dumetella carolinensis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Maullador Negro',
				nombre_cientifico='Melanoptila glabrirostris')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mergo Copetón',
				nombre_cientifico='Mergus serrator')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mergo Cresta Blanca',
				nombre_cientifico='Lophodytes cucullatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mergo Mayor',
				nombre_cientifico='Mergus merganser')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mérgulo Antiguo',
				nombre_cientifico='Synthliboramphus antiquus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mérgulo de Craveri',
				nombre_cientifico='Synthliboramphus craveri')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mérgulo de Scripps',
				nombre_cientifico='Synthliboramphus scrippsi')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mérgulo de Xantus',
				nombre_cientifico='Synthliboramphus hypoleucus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mielero Patas Amarillas',
				nombre_cientifico='Cyanerpes lucidus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mielero Patas Rojas',
				nombre_cientifico='Cyanerpes cyaneus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mielero Verde',
				nombre_cientifico='Chlorophanes spiza')
			db.Cat_conabio_aves.insert(
				nombre_comun='Milano Cola Blanca',
				nombre_cientifico='Elanus leucurus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Milano de Mississippi',
				nombre_cientifico='Ictinia mississippiensis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Milano Plomizo',
				nombre_cientifico='Ictinia plumbea')
			db.Cat_conabio_aves.insert(
				nombre_comun='Milano Tijereta',
				nombre_cientifico='Elanoides forficatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mirlo Acuático Norteamericano',
				nombre_cientifico='Cinclus mexicanus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mirlo Azteca',
				nombre_cientifico='Ridgwayia pinicola')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mirlo Café',
				nombre_cientifico='Turdus grayi')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mirlo Cinchado',
				nombre_cientifico='Ixoreus naevius')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mirlo Cuello Canela',
				nombre_cientifico='Turdus rufitorques')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mirlo Dorso Canela',
				nombre_cientifico='Turdus rufopalliatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mirlo Garganta Blanca',
				nombre_cientifico='Turdus assimilis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mirlo Negro',
				nombre_cientifico='Turdus infuscatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mirlo Primavera',
				nombre_cientifico='Turdus migratorius')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mirlo Serrano',
				nombre_cientifico='Turdus plebejus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Momoto Cejas Azules',
				nombre_cientifico='Eumomota superciliosa')
			db.Cat_conabio_aves.insert(
				nombre_comun='Momoto Corona Azul',
				nombre_cientifico='Momotus momota')
			db.Cat_conabio_aves.insert(
				nombre_comun='Momoto Corona Canela',
				nombre_cientifico='Momotus mexicanus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Momoto Enano',
				nombre_cientifico='Hylomanes momotula')
			db.Cat_conabio_aves.insert(
				nombre_comun='Momoto Garganta Azul',
				nombre_cientifico='Aspatha gularis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Momoto Pico Quillado',
				nombre_cientifico='Electron carinatum')
			db.Cat_conabio_aves.insert(
				nombre_comun='Monjita Americana',
				nombre_cientifico='Himantopus mexicanus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mosquerito Cejas Blancas',
				nombre_cientifico='Zimmerius vilissimus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mosquerito Chillón',
				nombre_cientifico='Camptostoma imberbe')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mosquerito Cola Castaña',
				nombre_cientifico='Terenotriccus erythrurus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mosquerito Enano',
				nombre_cientifico='Ornithion semiflavum')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mosquerito Espatulilla Común',
				nombre_cientifico='Todirostrum cinereum')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mosquerito Espatulilla Gris',
				nombre_cientifico='Poecilotriccus sylvia')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mosquerito Fajado',
				nombre_cientifico='Xenotriccus callizonus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mosquerito Gorra Café',
				nombre_cientifico='Leptopogon amaurocephalus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mosquerito Ocre',
				nombre_cientifico='Mionectes oleagineus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mosquerito Ojos Blancos',
				nombre_cientifico='Tolmomyias sulphurescens')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mosquerito Pico Chato',
				nombre_cientifico='Platyrinchus cancrominus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mosquerito Pico Curvo',
				nombre_cientifico='Oncostoma cinereigulare')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mosquerito Pico Plano',
				nombre_cientifico='Rhynchocyclus brevirostris')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mosquerito Rabadilla Amarilla',
				nombre_cientifico='Myiobius sulphureipygius')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mosquerito Verdoso',
				nombre_cientifico='Myiopagis viridicata')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mosquero Atila',
				nombre_cientifico='Attila spadiceus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mosquero Canelo',
				nombre_cientifico='Rhytipterna holerythra')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mosquero del Balsas',
				nombre_cientifico='Xenotriccus mexicanus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mosquero Elenia Caribeño',
				nombre_cientifico='Elaenia martinica')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mosquero Elenia Copetón',
				nombre_cientifico='Elaenia flavogaster')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mosquero Real',
				nombre_cientifico='Onychorhynchus coronatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mosquitero Ártico',
				nombre_cientifico='Phylloscopus borealis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mosquitero Cejas Amarillas',
				nombre_cientifico='Phylloscopus inornatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mosquitero Sombrío',
				nombre_cientifico='Phylloscopus fuscatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mulato Azul',
				nombre_cientifico='Melanotis caerulescens')
			db.Cat_conabio_aves.insert(
				nombre_comun='Mulato Pecho Blanco',
				nombre_cientifico='Melanotis hypoleucus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Musguero Castaño',
				nombre_cientifico='Clibanornis rubiginosus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Musguero Garganta Pálida',
				nombre_cientifico='Automolus ochrolaemus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Musguero Trepador',
				nombre_cientifico='Anabacerthia variegaticeps')
			db.Cat_conabio_aves.insert(
				nombre_comun='Negreta Alas Blancas',
				nombre_cientifico='Melanitta fusca')
			db.Cat_conabio_aves.insert(
				nombre_comun='Negreta Nuca Blanca',
				nombre_cientifico='Melanitta perspicillata')
			db.Cat_conabio_aves.insert(
				nombre_comun='Negreta Pico Amarillo',
				nombre_cientifico='Melanitta americana')
			db.Cat_conabio_aves.insert(
				nombre_comun='Ninfa Mexicana',
				nombre_cientifico='Thalurania ridgwayi')
			db.Cat_conabio_aves.insert(
				nombre_comun='Ocotero Enmascarado',
				nombre_cientifico='Peucedramus taeniatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Oropéndola Cabeza Castaña',
				nombre_cientifico='Psarocolius wagleri')
			db.Cat_conabio_aves.insert(
				nombre_comun='Oropéndola de Moctezuma',
				nombre_cientifico='Psarocolius montezuma')
			db.Cat_conabio_aves.insert(
				nombre_comun='Ostrero Americano',
				nombre_cientifico='Haematopus palliatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Ostrero Negro',
				nombre_cientifico='Haematopus bachmani')
			db.Cat_conabio_aves.insert(
				nombre_comun='Págalo Sureño',
				nombre_cientifico='Stercorarius maccormicki')
			db.Cat_conabio_aves.insert(
				nombre_comun='Paíño Cenizo',
				nombre_cientifico='Oceanodroma homochroa')
			db.Cat_conabio_aves.insert(
				nombre_comun='Paíño de Galápagos',
				nombre_cientifico='Oceanodroma tethys')
			db.Cat_conabio_aves.insert(
				nombre_comun='Paíño de Harcourt',
				nombre_cientifico='Oceanodroma castro')
			db.Cat_conabio_aves.insert(
				nombre_comun='Paíño de Isla Guadalupe',
				nombre_cientifico='Oceanodroma macrodactyla')
			db.Cat_conabio_aves.insert(
				nombre_comun='Paíño de Leach',
				nombre_cientifico='Oceanodroma leucorhoa')
			db.Cat_conabio_aves.insert(
				nombre_comun='Paíño de Wilson',
				nombre_cientifico='Oceanites oceanicus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Paíño Gris',
				nombre_cientifico='Oceanodroma furcata')
			db.Cat_conabio_aves.insert(
				nombre_comun='Paíño Mínimo',
				nombre_cientifico='Oceanodroma microsoma')
			db.Cat_conabio_aves.insert(
				nombre_comun='Paíño Negro',
				nombre_cientifico='Oceanodroma melania')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pájaro Cantil',
				nombre_cientifico='Heliornis fulica')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pájaro Estaca Mayor',
				nombre_cientifico='Nyctibius grandis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pájaro Estaca Norteño',
				nombre_cientifico='Nyctibius jamaicensis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pajuil',
				nombre_cientifico='Penelopina nigra')
			db.Cat_conabio_aves.insert(
				nombre_comun='Paloma Alas Blancas',
				nombre_cientifico='Zenaida asiatica')
			db.Cat_conabio_aves.insert(
				nombre_comun='Paloma Arroyera',
				nombre_cientifico='Leptotila verreauxi')
			db.Cat_conabio_aves.insert(
				nombre_comun='Paloma Cabeza Gris',
				nombre_cientifico='Leptotila plumbeiceps')
			db.Cat_conabio_aves.insert(
				nombre_comun='Paloma Canela',
				nombre_cientifico='Geotrygon montana')
			db.Cat_conabio_aves.insert(
				nombre_comun='Paloma Cara Blanca',
				nombre_cientifico='Zentrygon albifacies')
			db.Cat_conabio_aves.insert(
				nombre_comun='Paloma Caribeña',
				nombre_cientifico='Leptotila jamaicensis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Paloma Colorada',
				nombre_cientifico='Patagioenas cayennensis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Paloma Corona Blanca',
				nombre_cientifico='Patagioenas leucocephala')
			db.Cat_conabio_aves.insert(
				nombre_comun='Paloma de Collar Africana',
				nombre_cientifico='Streptopelia roseogrisea')
			db.Cat_conabio_aves.insert(
				nombre_comun='Paloma de Collar Turca',
				nombre_cientifico='Streptopelia decaocto')
			db.Cat_conabio_aves.insert(
				nombre_comun='Paloma de Oriente',
				nombre_cientifico='Streptopelia chinensis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Paloma Doméstica',
				nombre_cientifico='Columba livia')
			db.Cat_conabio_aves.insert(
				nombre_comun='Paloma Encinera',
				nombre_cientifico='Patagioenas fasciata')
			db.Cat_conabio_aves.insert(
				nombre_comun='Paloma Escamosa',
				nombre_cientifico='Patagioenas speciosa')
			db.Cat_conabio_aves.insert(
				nombre_comun='Paloma Migratoria',
				nombre_cientifico='Ectopistes migratorius')
			db.Cat_conabio_aves.insert(
				nombre_comun='Paloma Morada',
				nombre_cientifico='Patagioenas flavirostris')
			db.Cat_conabio_aves.insert(
				nombre_comun='Paloma Pecho Gris',
				nombre_cientifico='Leptotila cassini')
			db.Cat_conabio_aves.insert(
				nombre_comun='Paloma Triste',
				nombre_cientifico='Patagioenas nigrirostris')
			db.Cat_conabio_aves.insert(
				nombre_comun='Paloma Tuxtleña',
				nombre_cientifico='Zentrygon carrikeri')
			db.Cat_conabio_aves.insert(
				nombre_comun='Papamoscas Ailero',
				nombre_cientifico='Empidonax alnorum')
			db.Cat_conabio_aves.insert(
				nombre_comun='Papamoscas Amarillo Barranqueño',
				nombre_cientifico='Empidonax occidentalis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Papamoscas Amarillo del Pacífico',
				nombre_cientifico='Empidonax difficilis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Papamoscas Amarillo Sureño',
				nombre_cientifico='Empidonax flavescens')
			db.Cat_conabio_aves.insert(
				nombre_comun='Papamoscas Bajacolita',
				nombre_cientifico='Empidonax wrightii')
			db.Cat_conabio_aves.insert(
				nombre_comun='Papamoscas Boreal',
				nombre_cientifico='Contopus cooperi')
			db.Cat_conabio_aves.insert(
				nombre_comun='Papamoscas Cardenalito',
				nombre_cientifico='Pyrocephalus rubinus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Papamoscas Cenizo',
				nombre_cientifico='Myiarchus cinerascens')
			db.Cat_conabio_aves.insert(
				nombre_comun='Papamoscas Chico',
				nombre_cientifico='Empidonax minimus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Papamoscas Copetón',
				nombre_cientifico='Mitrephanes phaeocercus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Papamoscas de Hammond',
				nombre_cientifico='Empidonax hammondii')
			db.Cat_conabio_aves.insert(
				nombre_comun='Papamoscas del Este',
				nombre_cientifico='Contopus virens')
			db.Cat_conabio_aves.insert(
				nombre_comun='Papamoscas del Oeste',
				nombre_cientifico='Contopus sordidulus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Papamoscas Fibí',
				nombre_cientifico='Sayornis phoebe')
			db.Cat_conabio_aves.insert(
				nombre_comun='Papamoscas Garganta Blanca',
				nombre_cientifico='Empidonax albigularis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Papamoscas Gritón',
				nombre_cientifico='Myiarchus tyrannulus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Papamoscas Huí',
				nombre_cientifico='Myiarchus nuttingi')
			db.Cat_conabio_aves.insert(
				nombre_comun='Papamoscas José María',
				nombre_cientifico='Contopus pertinax')
			db.Cat_conabio_aves.insert(
				nombre_comun='Papamoscas Llanero',
				nombre_cientifico='Sayornis saya')
			db.Cat_conabio_aves.insert(
				nombre_comun='Papamoscas Matorralero',
				nombre_cientifico='Empidonax oberholseri')
			db.Cat_conabio_aves.insert(
				nombre_comun='Papamoscas Mexicano',
				nombre_cientifico='Deltarhynchus flammulatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Papamoscas Negro',
				nombre_cientifico='Sayornis nigricans')
			db.Cat_conabio_aves.insert(
				nombre_comun='Papamoscas Pecho Canela',
				nombre_cientifico='Empidonax fulvifrons')
			db.Cat_conabio_aves.insert(
				nombre_comun='Papamoscas Pinero',
				nombre_cientifico='Empidonax affinis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Papamoscas Rayado Cheje',
				nombre_cientifico='Myiodynastes maculatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Papamoscas Rayado Chico',
				nombre_cientifico='Legatus leucophaius')
			db.Cat_conabio_aves.insert(
				nombre_comun='Papamoscas Rayado Común',
				nombre_cientifico='Myiodynastes luteiventris')
			db.Cat_conabio_aves.insert(
				nombre_comun='Papamoscas Saucero',
				nombre_cientifico='Empidonax traillii')
			db.Cat_conabio_aves.insert(
				nombre_comun='Papamoscas Triste',
				nombre_cientifico='Myiarchus tuberculifer')
			db.Cat_conabio_aves.insert(
				nombre_comun='Papamoscas Tropical',
				nombre_cientifico='Contopus cinereus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Papamoscas Verdoso',
				nombre_cientifico='Empidonax virescens')
			db.Cat_conabio_aves.insert(
				nombre_comun='Papamoscas Viajero',
				nombre_cientifico='Myiarchus crinitus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Papamoscas Vientre Amarillo',
				nombre_cientifico='Empidonax flaviventris')
			db.Cat_conabio_aves.insert(
				nombre_comun='Papamoscas Yucateco',
				nombre_cientifico='Myiarchus yucatanensis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pardela Boreal',
				nombre_cientifico='Puffinus puffinus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pardela Cola Corta',
				nombre_cientifico='Puffinus tenuirostris')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pardela Cola Cuña',
				nombre_cientifico='Puffinus pacificus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pardela de Audubon',
				nombre_cientifico='Puffinus lherminieri')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pardela de Buller',
				nombre_cientifico='Puffinus bulleri')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pardela de Cory',
				nombre_cientifico='Calonectris diomedea')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pardela de Galápagos',
				nombre_cientifico='Puffinus subalaris')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pardela de Isla Navidad',
				nombre_cientifico='Puffinus nativitatis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pardela de Islas Revillagigedo',
				nombre_cientifico='Puffinus auricularis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pardela Gris',
				nombre_cientifico='Puffinus griseus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pardela Mayor',
				nombre_cientifico='Puffinus gravis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pardela Mexicana',
				nombre_cientifico='Puffinus opisthomelas')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pardela Patas Pálidas',
				nombre_cientifico='Puffinus carneipes')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pardela Patas Rosadas',
				nombre_cientifico='Puffinus creatopus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Patamarilla Euroasiática',
				nombre_cientifico='Tringa stagnatilis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Patamarilla Mayor',
				nombre_cientifico='Tringa melanoleuca')
			db.Cat_conabio_aves.insert(
				nombre_comun='Patamarilla Menor',
				nombre_cientifico='Tringa flavipes')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pato Arcoíris',
				nombre_cientifico='Aix sponsa')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pato Arlequín',
				nombre_cientifico='Histrionicus histrionicus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pato Boludo Mayor',
				nombre_cientifico='Aythya marila')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pato Boludo Menor',
				nombre_cientifico='Aythya affinis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pato Cabeza Roja',
				nombre_cientifico='Aythya americana')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pato Chalcuán',
				nombre_cientifico='Anas americana')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pato Chillón',
				nombre_cientifico='Bucephala clangula')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pato Coacoxtle',
				nombre_cientifico='Aythya valisineria')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pato Cola Larga',
				nombre_cientifico='Clangula hyemalis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pato Cucharón Norteño',
				nombre_cientifico='Anas clypeata')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pato de Collar',
				nombre_cientifico='Anas platyrhynchos')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pato Enmascarado',
				nombre_cientifico='Nomonyx dominicus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pato Friso',
				nombre_cientifico='Anas strepera')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pato Golondrino',
				nombre_cientifico='Anas acuta')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pato Islándico',
				nombre_cientifico='Bucephala islandica')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pato Monja',
				nombre_cientifico='Bucephala albeola')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pato Pico Anillado',
				nombre_cientifico='Aythya collaris')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pato Real',
				nombre_cientifico='Cairina moschata')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pato Silbón',
				nombre_cientifico='Anas penelope')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pato Tejano',
				nombre_cientifico='Anas fulvigula')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pato Tepalcate',
				nombre_cientifico='Oxyura jamaicensis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pava Cojolita',
				nombre_cientifico='Penelope purpurascens')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pavito Alas Blancas',
				nombre_cientifico='Myioborus pictus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pavito Alas Negras',
				nombre_cientifico='Myioborus miniatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pavito de Rocas',
				nombre_cientifico='Basileuterus lachrymosus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pavito Migratorio',
				nombre_cientifico='Setophaga ruticilla')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pavón Cornudo',
				nombre_cientifico='Oreophasis derbianus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pelícano Blanco Americano',
				nombre_cientifico='Pelecanus erythrorhynchos')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pelícano Café',
				nombre_cientifico='Pelecanus occidentalis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Perico Centroamericano',
				nombre_cientifico='Psittacara strenuus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Perico Frente Naranja',
				nombre_cientifico='Eupsittula canicularis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Perico Mexicano',
				nombre_cientifico='Psittacara holochlorus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Perico Monje Argentino',
				nombre_cientifico='Myiopsitta monachus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Perico Pecho Sucio',
				nombre_cientifico='Eupsittula nana')
			db.Cat_conabio_aves.insert(
				nombre_comun='Periquito Alas Amarillas',
				nombre_cientifico='Brotogeris jugularis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Periquito Barrado',
				nombre_cientifico='Bolborhynchus lineola')
			db.Cat_conabio_aves.insert(
				nombre_comun='Periquito Catarino',
				nombre_cientifico='Forpus cyanopygius')
			db.Cat_conabio_aves.insert(
				nombre_comun='Perlita Azulgris',
				nombre_cientifico='Polioptila caerulea')
			db.Cat_conabio_aves.insert(
				nombre_comun='Perlita Californiana',
				nombre_cientifico='Polioptila californica')
			db.Cat_conabio_aves.insert(
				nombre_comun='Perlita del Desierto',
				nombre_cientifico='Polioptila melanura')
			db.Cat_conabio_aves.insert(
				nombre_comun='Perlita Pispirria',
				nombre_cientifico='Polioptila albiloris')
			db.Cat_conabio_aves.insert(
				nombre_comun='Perlita Sinaloense',
				nombre_cientifico='Polioptila nigriceps')
			db.Cat_conabio_aves.insert(
				nombre_comun='Perlita Tropical',
				nombre_cientifico='Polioptila plumbea')
			db.Cat_conabio_aves.insert(
				nombre_comun='Petrel de Bulwer',
				nombre_cientifico='Bulweria bulwerii')
			db.Cat_conabio_aves.insert(
				nombre_comun='Petrel de Cook',
				nombre_cientifico='Pterodroma cookii')
			db.Cat_conabio_aves.insert(
				nombre_comun='Petrel de Galápagos',
				nombre_cientifico='Pterodroma phaeopygia')
			db.Cat_conabio_aves.insert(
				nombre_comun='Petrel de Isla Juan Fernández',
				nombre_cientifico='Pterodroma externa')
			db.Cat_conabio_aves.insert(
				nombre_comun='Petrel de Kermadec',
				nombre_cientifico='Pterodroma neglecta')
			db.Cat_conabio_aves.insert(
				nombre_comun='Petrel de Parkinson',
				nombre_cientifico='Procellaria parkinsoni')
			db.Cat_conabio_aves.insert(
				nombre_comun='Petrel Heráldico',
				nombre_cientifico='Pterodroma arminjoniana')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pía Guardabosques',
				nombre_cientifico='Lipaugus unirufus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Picochueco Vientre Canela',
				nombre_cientifico='Diglossa baritula')
			db.Cat_conabio_aves.insert(
				nombre_comun='Picogordo Amarillo',
				nombre_cientifico='Pheucticus chrysopeplus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Picogordo Azul',
				nombre_cientifico='Passerina caerulea')
			db.Cat_conabio_aves.insert(
				nombre_comun='Picogordo Azulnegro',
				nombre_cientifico='Cyanocompsa cyanoides')
			db.Cat_conabio_aves.insert(
				nombre_comun='Picogordo Cara Negra',
				nombre_cientifico='Caryothraustes poliogaster')
			db.Cat_conabio_aves.insert(
				nombre_comun='Picogordo Cuello Rojo',
				nombre_cientifico='Rhodothraupis celaeno')
			db.Cat_conabio_aves.insert(
				nombre_comun='Picogordo Degollado',
				nombre_cientifico='Pheucticus ludovicianus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Picogordo Tigrillo',
				nombre_cientifico='Pheucticus melanocephalus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Picogrueso Encapuchado',
				nombre_cientifico='Coccothraustes abeillei')
			db.Cat_conabio_aves.insert(
				nombre_comun='Picogrueso Norteño',
				nombre_cientifico='Coccothraustes vespertinus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Picolezna Común',
				nombre_cientifico='Xenops minutus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Picopando Canelo',
				nombre_cientifico='Limosa fedoa')
			db.Cat_conabio_aves.insert(
				nombre_comun='Picopando Cola Barrada',
				nombre_cientifico='Limosa lapponica')
			db.Cat_conabio_aves.insert(
				nombre_comun='Picopando del Este',
				nombre_cientifico='Limosa haemastica')
			db.Cat_conabio_aves.insert(
				nombre_comun='Picotuerto Rojo',
				nombre_cientifico='Loxia curvirostra')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pijije Alas Blancas',
				nombre_cientifico='Dendrocygna autumnalis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pijije Canelo',
				nombre_cientifico='Dendrocygna bicolor')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pinzón Colorado',
				nombre_cientifico='Haemorhous purpureus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pinzón Mexicano',
				nombre_cientifico='Haemorhous mexicanus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pinzón Serrano',
				nombre_cientifico='Haemorhous cassinii')
			db.Cat_conabio_aves.insert(
				nombre_comun='Piranga Alas Blancas',
				nombre_cientifico='Piranga leucoptera')
			db.Cat_conabio_aves.insert(
				nombre_comun='Piranga Cabeza Roja',
				nombre_cientifico='Piranga erythrocephala')
			db.Cat_conabio_aves.insert(
				nombre_comun='Piranga Capucha Roja',
				nombre_cientifico='Piranga ludoviciana')
			db.Cat_conabio_aves.insert(
				nombre_comun='Piranga Dorso Rayado',
				nombre_cientifico='Piranga bidentata')
			db.Cat_conabio_aves.insert(
				nombre_comun='Piranga Encinera',
				nombre_cientifico='Piranga flava')
			db.Cat_conabio_aves.insert(
				nombre_comun='Piranga Escarlata',
				nombre_cientifico='Piranga olivacea')
			db.Cat_conabio_aves.insert(
				nombre_comun='Piranga Hormiguera Corona Roja',
				nombre_cientifico='Habia rubica')
			db.Cat_conabio_aves.insert(
				nombre_comun='Piranga Hormiguera Garganta Roja',
				nombre_cientifico='Habia fuscicauda')
			db.Cat_conabio_aves.insert(
				nombre_comun='Piranga Roja',
				nombre_cientifico='Piranga rubra')
			db.Cat_conabio_aves.insert(
				nombre_comun='Piranga Yucateca',
				nombre_cientifico='Piranga roseogularis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Playero Alzacolita',
				nombre_cientifico='Actitis macularius')
			db.Cat_conabio_aves.insert(
				nombre_comun='Playero Andarríos',
				nombre_cientifico='Tringa glareola')
			db.Cat_conabio_aves.insert(
				nombre_comun='Playero Blanco',
				nombre_cientifico='Calidris alba')
			db.Cat_conabio_aves.insert(
				nombre_comun='Playero Brincaolas',
				nombre_cientifico='Calidris virgata')
			db.Cat_conabio_aves.insert(
				nombre_comun='Playero Combatiente',
				nombre_cientifico='Calidris pugnax')
			db.Cat_conabio_aves.insert(
				nombre_comun='Playero de Baird',
				nombre_cientifico='Calidris bairdii')
			db.Cat_conabio_aves.insert(
				nombre_comun='Playero Diminuto',
				nombre_cientifico='Calidris minutilla')
			db.Cat_conabio_aves.insert(
				nombre_comun='Playero Dorso Rojo',
				nombre_cientifico='Calidris alpina')
			db.Cat_conabio_aves.insert(
				nombre_comun='Playero Menor',
				nombre_cientifico='Calidris minuta')
			db.Cat_conabio_aves.insert(
				nombre_comun='Playero Occidental',
				nombre_cientifico='Calidris mauri')
			db.Cat_conabio_aves.insert(
				nombre_comun='Playero Ocre',
				nombre_cientifico='Calidris subruficollis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Playero Pectoral',
				nombre_cientifico='Calidris melanotos')
			db.Cat_conabio_aves.insert(
				nombre_comun='Playero Picopando',
				nombre_cientifico='Xenus cinereus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Playero Pihuiuí',
				nombre_cientifico='Tringa semipalmata')
			db.Cat_conabio_aves.insert(
				nombre_comun='Playero Rabadilla Blanca',
				nombre_cientifico='Calidris fuscicollis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Playero Rojo',
				nombre_cientifico='Calidris canutus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Playero Semipalmeado',
				nombre_cientifico='Calidris pusilla')
			db.Cat_conabio_aves.insert(
				nombre_comun='Playero Solitario',
				nombre_cientifico='Tringa solitaria')
			db.Cat_conabio_aves.insert(
				nombre_comun='Playero Vagabundo',
				nombre_cientifico='Tringa incana')
			db.Cat_conabio_aves.insert(
				nombre_comun='Playero Zancón',
				nombre_cientifico='Calidris himantopus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Playero Zarapito',
				nombre_cientifico='Calidris ferruginea')
			db.Cat_conabio_aves.insert(
				nombre_comun='Polluela Amarilla',
				nombre_cientifico='Coturnicops noveboracensis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Polluela Canela',
				nombre_cientifico='Laterallus ruber')
			db.Cat_conabio_aves.insert(
				nombre_comun='Polluela Negra',
				nombre_cientifico='Laterallus jamaicensis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Polluela Pecho Amarillo',
				nombre_cientifico='Porzana flaviventer')
			db.Cat_conabio_aves.insert(
				nombre_comun='Polluela Pecho Gris',
				nombre_cientifico='Laterallus exilis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Polluela Sora',
				nombre_cientifico='Porzana carolina')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pradero del Oeste',
				nombre_cientifico='Sturnella neglecta')
			db.Cat_conabio_aves.insert(
				nombre_comun='Pradero Tortillaconchile',
				nombre_cientifico='Sturnella magna')
			db.Cat_conabio_aves.insert(
				nombre_comun='Quetzal Mesoamericano',
				nombre_cientifico='Pharomachrus mocinno')
			db.Cat_conabio_aves.insert(
				nombre_comun='Quetzal Orejón',
				nombre_cientifico='Euptilotis neoxenus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Rabijunco Cola Blanca',
				nombre_cientifico='Phaethon lepturus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Rabijunco Cola Roja',
				nombre_cientifico='Phaethon rubricauda')
			db.Cat_conabio_aves.insert(
				nombre_comun='Rabijunco Pico Rojo',
				nombre_cientifico='Phaethon aethereus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Rascador Californiano',
				nombre_cientifico='Melozone crissalis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Rascador Cejas Verdes',
				nombre_cientifico='Arremon virenticeps')
			db.Cat_conabio_aves.insert(
				nombre_comun='Rascador Cola Verde',
				nombre_cientifico='Pipilo chlorurus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Rascador de Collar',
				nombre_cientifico='Pipilo ocai')
			db.Cat_conabio_aves.insert(
				nombre_comun='Rascador Dorso Verde',
				nombre_cientifico='Arremonops chloronotus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Rascador Enmascarado',
				nombre_cientifico='Melozone aberti')
			db.Cat_conabio_aves.insert(
				nombre_comun='Rascador Gorra Canela',
				nombre_cientifico='Atlapetes pileatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Rascador Gorra Castaña',
				nombre_cientifico='Arremon brunneinucha')
			db.Cat_conabio_aves.insert(
				nombre_comun='Rascador Moteado',
				nombre_cientifico='Pipilo maculatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Rascador Nuca Blanca',
				nombre_cientifico='Atlapetes albinucha')
			db.Cat_conabio_aves.insert(
				nombre_comun='Rascador Nuca Canela',
				nombre_cientifico='Melozone kieneri')
			db.Cat_conabio_aves.insert(
				nombre_comun='Rascador Oaxaqueño',
				nombre_cientifico='Melozone albicollis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Rascador Oliváceo',
				nombre_cientifico='Arremonops rufivirgatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Rascador Orejas Blancas',
				nombre_cientifico='Melozone leucotis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Rascador Patilludo',
				nombre_cientifico='Melozone biarcuata')
			db.Cat_conabio_aves.insert(
				nombre_comun='Rascador Pico Naranja',
				nombre_cientifico='Arremon aurantiirostris')
			db.Cat_conabio_aves.insert(
				nombre_comun='Rascador Viejita',
				nombre_cientifico='Melozone fusca')
			db.Cat_conabio_aves.insert(
				nombre_comun='Rascón Azteca',
				nombre_cientifico='Rallus tenuirostris')
			db.Cat_conabio_aves.insert(
				nombre_comun='Rascón Canelo',
				nombre_cientifico='Amaurolimnas concolor')
			db.Cat_conabio_aves.insert(
				nombre_comun='Rascón Cara Gris',
				nombre_cientifico='Rallus limicola')
			db.Cat_conabio_aves.insert(
				nombre_comun='Rascón Costero del Atlántico',
				nombre_cientifico='Rallus crepitans')
			db.Cat_conabio_aves.insert(
				nombre_comun='Rascón Costero del Pacífico',
				nombre_cientifico='Rallus obsoletus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Rascón Cuello Canela',
				nombre_cientifico='Aramides axillaris')
			db.Cat_conabio_aves.insert(
				nombre_comun='Rascón Cuello Gris',
				nombre_cientifico='Aramides cajaneus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Rascón Pinto',
				nombre_cientifico='Pardirallus maculatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Rayador Americano',
				nombre_cientifico='Rynchops niger')
			db.Cat_conabio_aves.insert(
				nombre_comun='Reinita Mielera',
				nombre_cientifico='Coereba flaveola')
			db.Cat_conabio_aves.insert(
				nombre_comun='Reyezuelo Corona Amarilla',
				nombre_cientifico='Regulus satrapa')
			db.Cat_conabio_aves.insert(
				nombre_comun='Reyezuelo Matraquita',
				nombre_cientifico='Regulus calendula')
			db.Cat_conabio_aves.insert(
				nombre_comun='Saltador Cabeza Negra',
				nombre_cientifico='Saltator atriceps')
			db.Cat_conabio_aves.insert(
				nombre_comun='Saltador Garganta Ocre',
				nombre_cientifico='Saltator maximus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Saltador Gris',
				nombre_cientifico='Saltator coerulescens')
			db.Cat_conabio_aves.insert(
				nombre_comun='Saltapared Albicanelo',
				nombre_cientifico='Thryophilus rufalbus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Saltapared Barrado',
				nombre_cientifico='Thryophilus pleurostictus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Saltapared Barranqueño',
				nombre_cientifico='Catherpes mexicanus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Saltapared Cejas Canela',
				nombre_cientifico='Troglodytes rufociliatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Saltapared Chinchibul',
				nombre_cientifico='Cantorchilus modestus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Saltapared Cholino del Este',
				nombre_cientifico='Troglodytes hiemalis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Saltapared Cholino del Oeste',
				nombre_cientifico='Troglodytes pacificus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Saltapared Cola Larga',
				nombre_cientifico='Thryomanes bewickii')
			db.Cat_conabio_aves.insert(
				nombre_comun='Saltapared Común',
				nombre_cientifico='Troglodytes aedon')
			db.Cat_conabio_aves.insert(
				nombre_comun='Saltapared de Carolina',
				nombre_cientifico='Thryothorus ludovicianus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Saltapared de Isla Clarión',
				nombre_cientifico='Troglodytes tanneri')
			db.Cat_conabio_aves.insert(
				nombre_comun='Saltapared de Isla Socorro',
				nombre_cientifico='Troglodytes sissonii')
			db.Cat_conabio_aves.insert(
				nombre_comun='Saltapared de Rocas',
				nombre_cientifico='Salpinctes obsoletus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Saltapared Feliz',
				nombre_cientifico='Pheugopedius felix')
			db.Cat_conabio_aves.insert(
				nombre_comun='Saltapared Moteado',
				nombre_cientifico='Pheugopedius maculipectus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Saltapared Pantanero',
				nombre_cientifico='Cistothorus palustris')
			db.Cat_conabio_aves.insert(
				nombre_comun='Saltapared Pecho Blanco',
				nombre_cientifico='Henicorhina leucosticta')
			db.Cat_conabio_aves.insert(
				nombre_comun='Saltapared Pecho Gris',
				nombre_cientifico='Henicorhina leucophrys')
			db.Cat_conabio_aves.insert(
				nombre_comun='Saltapared Ruiseñor',
				nombre_cientifico='Microcerculus philomela')
			db.Cat_conabio_aves.insert(
				nombre_comun='Saltapared Sabanero',
				nombre_cientifico='Cistothorus platensis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Saltapared Sinaloense',
				nombre_cientifico='Thryophilus sinaloa')
			db.Cat_conabio_aves.insert(
				nombre_comun='Saltapared Vientre Blanco',
				nombre_cientifico='Uropsila leucogastra')
			db.Cat_conabio_aves.insert(
				nombre_comun='Saltarín Cabeza Roja',
				nombre_cientifico='Ceratopipra mentalis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Saltarín Cuello Blanco',
				nombre_cientifico='Manacus candei')
			db.Cat_conabio_aves.insert(
				nombre_comun='Saltarín Toledo',
				nombre_cientifico='Chiroxiphia linearis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Salteador Cola Larga',
				nombre_cientifico='Stercorarius longicaudus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Salteador Parásito',
				nombre_cientifico='Stercorarius parasiticus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Salteador Robusto',
				nombre_cientifico='Stercorarius pomarinus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Saltón Picudo',
				nombre_cientifico='Ramphocaenus melanurus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Sastrecillo',
				nombre_cientifico='Psaltriparus minimus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Semillero Azul',
				nombre_cientifico='Amaurospiza concolor')
			db.Cat_conabio_aves.insert(
				nombre_comun='Semillero Brincador',
				nombre_cientifico='Volatinia jacarina')
			db.Cat_conabio_aves.insert(
				nombre_comun='Semillero de Collar',
				nombre_cientifico='Sporophila torqueola')
			db.Cat_conabio_aves.insert(
				nombre_comun='Semillero Oliváceo',
				nombre_cientifico='Tiaris olivaceus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Semillero Pecho Canela',
				nombre_cientifico='Sporophila minuta')
			db.Cat_conabio_aves.insert(
				nombre_comun='Semillero Pico Grueso',
				nombre_cientifico='Sporophila funerea')
			db.Cat_conabio_aves.insert(
				nombre_comun='Semillero Pizarra',
				nombre_cientifico='Haplospiza rustica')
			db.Cat_conabio_aves.insert(
				nombre_comun='Semillero Plomizo',
				nombre_cientifico='Sporophila schistacea')
			db.Cat_conabio_aves.insert(
				nombre_comun='Semillero Variable',
				nombre_cientifico='Sporophila corvina')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tangara Alas Amarillas',
				nombre_cientifico='Thraupis abbas')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tangara Azulgris',
				nombre_cientifico='Thraupis episcopus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tangara Cabeza Gris',
				nombre_cientifico='Eucometis penicillata')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tangara Cabeza Rayada',
				nombre_cientifico='Spindalis zena')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tangara Capucha Dorada',
				nombre_cientifico='Tangara larvata')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tangara Capucha Negra',
				nombre_cientifico='Lanio aurantius')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tangara Chiapaneca',
				nombre_cientifico='Tangara cabanisi')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tangara Pecho Rosa',
				nombre_cientifico='Rhodinocichla rosea')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tangara Rabadilla Roja',
				nombre_cientifico='Ramphocelus passerinii')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tangara Rojinegra',
				nombre_cientifico='Ramphocelus sanguinolentus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tapacaminos Cuerporruín Mexicano',
				nombre_cientifico='Antrostomus arizonae')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tapacaminos Cuerporruín Norteño',
				nombre_cientifico='Antrostomus vociferus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tapacaminos de Carolina',
				nombre_cientifico='Antrostomus carolinensis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tapacaminos Huil',
				nombre_cientifico='Nyctiphrynus yucatanicus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tapacaminos Pandeagua',
				nombre_cientifico='Phalaenoptilus nuttallii')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tapacaminos Prío',
				nombre_cientifico='Nyctiphrynus mcleodii')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tapacaminos Sabanero',
				nombre_cientifico='Hydropsalis maculicaudus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tapacaminos Ticurú',
				nombre_cientifico='Antrostomus salvini')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tapacaminos Tucuchillo',
				nombre_cientifico='Antrostomus ridgwayi')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tapacaminos Yucateco',
				nombre_cientifico='Antrostomus badius')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tecolote Bajeño',
				nombre_cientifico='Glaucidium brasilianum')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tecolote Barbudo',
				nombre_cientifico='Megascops barbarus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tecolote Colimense',
				nombre_cientifico='Glaucidium palmarum')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tecolote de Cooper',
				nombre_cientifico='Megascops cooperi')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tecolote del Balsas',
				nombre_cientifico='Megascops seductus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tecolote del Este',
				nombre_cientifico='Megascops asio')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tecolote del Oeste',
				nombre_cientifico='Megascops kennicottii')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tecolote Enano',
				nombre_cientifico='Micrathene whitneyi')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tecolote Llanero',
				nombre_cientifico='Athene cunicularia')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tecolote Mesoamericano',
				nombre_cientifico='Glaucidium griseiceps')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tecolote Ojos Oscuros',
				nombre_cientifico='Psiloscops flammeolus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tecolote Oyamelero Norteño',
				nombre_cientifico='Aegolius acadicus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tecolote Oyamelero Sureño',
				nombre_cientifico='Aegolius ridgwayi')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tecolote Rítmico',
				nombre_cientifico='Megascops trichopsis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tecolote Sapo',
				nombre_cientifico='Megascops guatemalae')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tecolote Serrano',
				nombre_cientifico='Glaucidium gnoma')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tecolote Tamaulipeco',
				nombre_cientifico='Glaucidium sanchezi')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tinamú Canelo',
				nombre_cientifico='Crypturellus cinnamomeus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tinamú Jamuey',
				nombre_cientifico='Crypturellus boucardi')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tinamú Mayor',
				nombre_cientifico='Tinamus major')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tinamú Menor',
				nombre_cientifico='Crypturellus soui')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tirano Chibiú',
				nombre_cientifico='Tyrannus vociferans')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tirano Cuír',
				nombre_cientifico='Tyrannus couchii')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tirano Dorso Negro',
				nombre_cientifico='Tyrannus tyrannus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tirano Gris',
				nombre_cientifico='Tyrannus dominicensis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tirano Pálido',
				nombre_cientifico='Tyrannus verticalis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tirano Pico Grueso',
				nombre_cientifico='Tyrannus crassirostris')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tirano Pirirí',
				nombre_cientifico='Tyrannus melancholicus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tirano Tijereta Gris',
				nombre_cientifico='Tyrannus savana')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tirano Tijereta Rosado',
				nombre_cientifico='Tyrannus forficatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Titira Pico Negro',
				nombre_cientifico='Tityra inquisitor')
			db.Cat_conabio_aves.insert(
				nombre_comun='Titira Puerquito',
				nombre_cientifico='Tityra semifasciata')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tordo Arrocero',
				nombre_cientifico='Dolichonyx oryzivorus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tordo Cabeza Amarilla',
				nombre_cientifico='Xanthocephalus xanthocephalus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tordo Cabeza Café',
				nombre_cientifico='Molothrus ater')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tordo Canadiense',
				nombre_cientifico='Euphagus carolinus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tordo Cantor',
				nombre_cientifico='Dives dives')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tordo Gigante',
				nombre_cientifico='Molothrus oryzivorus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tordo Ojos Amarillos',
				nombre_cientifico='Euphagus cyanocephalus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tordo Ojos Rojos',
				nombre_cientifico='Molothrus aeneus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tordo Sargento',
				nombre_cientifico='Agelaius phoeniceus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tordo Sudamericano',
				nombre_cientifico='Molothrus bonariensis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tordo Tricolor',
				nombre_cientifico='Agelaius tricolor')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tórtola Azul',
				nombre_cientifico='Claravis pretiosa')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tórtola Pecho Morado',
				nombre_cientifico='Claravis mondetoura')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tortolita Canela',
				nombre_cientifico='Columbina talpacoti')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tortolita Cola Larga',
				nombre_cientifico='Columbina inca')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tortolita Pecho Liso',
				nombre_cientifico='Columbina minuta')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tortolita Pico Rojo',
				nombre_cientifico='Columbina passerina')
			db.Cat_conabio_aves.insert(
				nombre_comun='Trepadorcito Americano',
				nombre_cientifico='Certhia americana')
			db.Cat_conabio_aves.insert(
				nombre_comun='Trepatroncos Barrado',
				nombre_cientifico='Dendrocolaptes sanctithomae')
			db.Cat_conabio_aves.insert(
				nombre_comun='Trepatroncos Bigotudo',
				nombre_cientifico='Xiphorhynchus flavigaster')
			db.Cat_conabio_aves.insert(
				nombre_comun='Trepatroncos Cabeza Gris',
				nombre_cientifico='Sittasomus griseicapillus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Trepatroncos Canelo',
				nombre_cientifico='Dendrocincla homochroa')
			db.Cat_conabio_aves.insert(
				nombre_comun='Trepatroncos Corona Punteada',
				nombre_cientifico='Lepidocolaptes affinis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Trepatroncos Corona Rayada',
				nombre_cientifico='Lepidocolaptes souleyetii')
			db.Cat_conabio_aves.insert(
				nombre_comun='Trepatroncos Gigante',
				nombre_cientifico='Xiphocolaptes promeropirhynchus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Trepatroncos Mexicano',
				nombre_cientifico='Lepidocolaptes leucogaster')
			db.Cat_conabio_aves.insert(
				nombre_comun='Trepatroncos Moteado',
				nombre_cientifico='Xiphorhynchus erythropygius')
			db.Cat_conabio_aves.insert(
				nombre_comun='Trepatroncos Pico Cuña',
				nombre_cientifico='Glyphorynchus spirurus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Trepatroncos Sepia',
				nombre_cientifico='Dendrocincla anabatina')
			db.Cat_conabio_aves.insert(
				nombre_comun='Trepatroncos Vientre Barrado',
				nombre_cientifico='Dendrocolaptes picumnus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tucán Pico Canoa',
				nombre_cientifico='Ramphastos sulfuratus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tucancillo Collarejo',
				nombre_cientifico='Pteroglossus torquatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Tucancillo Verde',
				nombre_cientifico='Aulacorhynchus prasinus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Urraca Cara Blanca',
				nombre_cientifico='Calocitta formosa')
			db.Cat_conabio_aves.insert(
				nombre_comun='Urraca Cara Negra',
				nombre_cientifico='Calocitta colliei')
			db.Cat_conabio_aves.insert(
				nombre_comun='Vencejo Cara Blanca',
				nombre_cientifico='Cypseloides storeri')
			db.Cat_conabio_aves.insert(
				nombre_comun='Vencejo Collar Blanco',
				nombre_cientifico='Streptoprocne zonaris')
			db.Cat_conabio_aves.insert(
				nombre_comun='Vencejo Cuello Castaño',
				nombre_cientifico='Streptoprocne rutila')
			db.Cat_conabio_aves.insert(
				nombre_comun='Vencejo de Chimenea',
				nombre_cientifico='Chaetura pelagica')
			db.Cat_conabio_aves.insert(
				nombre_comun='Vencejo de Vaux',
				nombre_cientifico='Chaetura vauxi')
			db.Cat_conabio_aves.insert(
				nombre_comun='Vencejo Negro',
				nombre_cientifico='Cypseloides niger')
			db.Cat_conabio_aves.insert(
				nombre_comun='Vencejo Nuca Blanca',
				nombre_cientifico='Streptoprocne semicollaris')
			db.Cat_conabio_aves.insert(
				nombre_comun='Vencejo Pecho Blanco',
				nombre_cientifico='Aeronautes saxatalis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Vencejo Tijereta Mayor',
				nombre_cientifico='Panyptila sanctihieronymi')
			db.Cat_conabio_aves.insert(
				nombre_comun='Vencejo Tijereta Menor',
				nombre_cientifico='Panyptila cayennensis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Verdugo Americano',
				nombre_cientifico='Lanius ludovicianus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Vireo Amarillo',
				nombre_cientifico='Vireo hypochryseus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Vireo Anteojillo',
				nombre_cientifico='Vireo solitarius')
			db.Cat_conabio_aves.insert(
				nombre_comun='Vireo Bigotudo',
				nombre_cientifico='Vireo altiloquus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Vireo de Bell',
				nombre_cientifico='Vireo bellii')
			db.Cat_conabio_aves.insert(
				nombre_comun='Vireo de Cassin',
				nombre_cientifico='Vireo cassinii')
			db.Cat_conabio_aves.insert(
				nombre_comun='Vireo de Cozumel',
				nombre_cientifico='Vireo bairdi')
			db.Cat_conabio_aves.insert(
				nombre_comun='Vireo de Filadelfia',
				nombre_cientifico='Vireo philadelphicus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Vireo Enano',
				nombre_cientifico='Vireo nelsoni')
			db.Cat_conabio_aves.insert(
				nombre_comun='Vireo Garganta Amarilla',
				nombre_cientifico='Vireo flavifrons')
			db.Cat_conabio_aves.insert(
				nombre_comun='Vireo Gorjeador',
				nombre_cientifico='Vireo gilvus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Vireo Gorra Café',
				nombre_cientifico='Vireo leucophrys')
			db.Cat_conabio_aves.insert(
				nombre_comun='Vireo Gorra Negra',
				nombre_cientifico='Vireo atricapilla')
			db.Cat_conabio_aves.insert(
				nombre_comun='Vireo Gris',
				nombre_cientifico='Vireo vicinior')
			db.Cat_conabio_aves.insert(
				nombre_comun='Vireo Manglero',
				nombre_cientifico='Vireo pallens')
			db.Cat_conabio_aves.insert(
				nombre_comun='Vireo Ojos Blancos',
				nombre_cientifico='Vireo griseus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Vireo Ojos Rojos',
				nombre_cientifico='Vireo olivaceus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Vireo Pizarra',
				nombre_cientifico='Vireo brevipennis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Vireo Plomizo',
				nombre_cientifico='Vireo plumbeus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Vireo Reyezuelo',
				nombre_cientifico='Vireo huttoni')
			db.Cat_conabio_aves.insert(
				nombre_comun='Vireo Verdeamarillo',
				nombre_cientifico='Vireo flavoviridis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Vireo Yucateco',
				nombre_cientifico='Vireo magister')
			db.Cat_conabio_aves.insert(
				nombre_comun='Vireocillo Cabeza Gris',
				nombre_cientifico='Hylophilus decurtatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Vireocillo Corona Canela',
				nombre_cientifico='Hylophilus ochraceiceps')
			db.Cat_conabio_aves.insert(
				nombre_comun='Vireón Arlequín',
				nombre_cientifico='Vireolanius melitophrys')
			db.Cat_conabio_aves.insert(
				nombre_comun='Vireón Cejas Canela',
				nombre_cientifico='Cyclarhis gujanensis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Vireón Esmeralda',
				nombre_cientifico='Vireolanius pulchellus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Vuelvepiedras Negro',
				nombre_cientifico='Arenaria melanocephala')
			db.Cat_conabio_aves.insert(
				nombre_comun='Vuelvepiedras Rojizo',
				nombre_cientifico='Arenaria interpres')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zacatonero Californiano',
				nombre_cientifico='Artemisiospiza belli')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zacatonero Canelo',
				nombre_cientifico='Aimophila rufescens')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zacatonero Cinco Rayas',
				nombre_cientifico='Amphispiza quinquestriata')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zacatonero Corona Canela',
				nombre_cientifico='Aimophila ruficeps')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zacatonero Corona Rayada',
				nombre_cientifico='Peucaea ruficauda')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zacatonero de Artemisas',
				nombre_cientifico='Artemisiospiza nevadensis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zacatonero de Botteri',
				nombre_cientifico='Peucaea botterii')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zacatonero de Cassin',
				nombre_cientifico='Peucaea cassinii')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zacatonero Embridado',
				nombre_cientifico='Peucaea mystacalis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zacatonero Garganta Negra',
				nombre_cientifico='Amphispiza bilineata')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zacatonero Hombros Canela',
				nombre_cientifico='Peucaea carpalis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zacatonero Istmeño',
				nombre_cientifico='Peucaea sumichrasti')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zacatonero Oaxaqueño',
				nombre_cientifico='Aimophila notosticta')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zacatonero Pecho Negro',
				nombre_cientifico='Peucaea humeralis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zacatonero Serrano',
				nombre_cientifico='Oriturus superciliosus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zafiro Bajacaliforniano',
				nombre_cientifico='Hylocharis xantusii')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zafiro Garganta Azul',
				nombre_cientifico='Hylocharis eliciae')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zafiro Orejas Blancas',
				nombre_cientifico='Hylocharis leucotis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zambullidor Cornudo',
				nombre_cientifico='Podiceps auritus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zambullidor Cuello Rojo',
				nombre_cientifico='Podiceps grisegena')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zambullidor Menor',
				nombre_cientifico='Tachybaptus dominicus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zambullidor Orejón',
				nombre_cientifico='Podiceps nigricollis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zambullidor Pico Grueso',
				nombre_cientifico='Podilymbus podiceps')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zanate del Lerma',
				nombre_cientifico='Quiscalus palustris')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zanate Mayor',
				nombre_cientifico='Quiscalus mexicanus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zanate Norteño',
				nombre_cientifico='Quiscalus quiscula')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zarapito Boreal',
				nombre_cientifico='Numenius borealis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zarapito Ganga',
				nombre_cientifico='Bartramia longicauda')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zarapito Pico Largo',
				nombre_cientifico='Numenius americanus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zarapito Trinador',
				nombre_cientifico='Numenius phaeopus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zopilote Aura',
				nombre_cientifico='Cathartes aura')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zopilote Común',
				nombre_cientifico='Coragyps atratus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zopilote Rey',
				nombre_cientifico='Sarcoramphus papa')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zopilote Sabanero',
				nombre_cientifico='Cathartes burrovianus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zorzal Canelo',
				nombre_cientifico='Catharus fuscescens')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zorzal Cara Gris',
				nombre_cientifico='Catharus minimus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zorzal Cola Canela',
				nombre_cientifico='Catharus guttatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zorzal Corona Negra',
				nombre_cientifico='Catharus mexicanus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zorzal de Anteojos',
				nombre_cientifico='Catharus ustulatus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zorzal de Frantzius',
				nombre_cientifico='Catharus frantzii')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zorzal Mexicano',
				nombre_cientifico='Catharus occidentalis')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zorzal Moteado',
				nombre_cientifico='Hylocichla mustelina')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zorzal Pecho Amarillo',
				nombre_cientifico='Catharus dryas')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zorzal Pico Naranja',
				nombre_cientifico='Catharus aurantiirostris')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zumbador Canelo',
				nombre_cientifico='Selasphorus rufus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zumbador Cola Ancha',
				nombre_cientifico='Selasphorus platycercus')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zumbador de Allen',
				nombre_cientifico='Selasphorus sasin')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zumbador Garganta Rayada',
				nombre_cientifico='Selasphorus calliope')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zumbador Guatemalteco',
				nombre_cientifico='Atthis ellioti')
			db.Cat_conabio_aves.insert(
				nombre_comun='Zumbador Mexicano',
				nombre_cientifico='Atthis heloisa')
			db.Cat_conabio_aves.insert(
				nombre_comun='Otros',
				nombre_cientifico='Otros')

		response.flash = 'Éxito'
		
	elif forma.errors:
		
	   response.flash = 'Por favor, introduzca archivos del tipo CSV'
	   
	else:
		response.flash ='Por favor, introduzca los archivos CSV a fusionar'
		
	return dict()
