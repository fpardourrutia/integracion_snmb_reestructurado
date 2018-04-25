# coding: utf8

# usados en "index2", "validarArchivos", "asignarInformacionArchivo"
import os 
import estructura_archivos_admin as eaa
import re

import base64 # usado en "asignarInformacionArchivo"

def index():

    ## Controlador correspondiente a la pestaña "Selección de fauna", de
    ## la sección "Trampa cámara". Esta función no incluye una forma, puesto que
    ## cuando se presione el botón "enviar" en la vista correspondiente, la
    ## información será procesada mediante AJAX, para no tener que recargar la
    ## página entre información de cada fotografía.

    ##############################################################
    # Procesando la información de la dropdown de conglomerado
    ##############################################################

    # Regresando los nombres de todos los conglomerados insertados en la tabla de
    # conglomerado junto con sus id's para llenar la combobox de conglomerado.

    listaConglomerado = db(db.Conglomerado_muestra).select(
        db.Conglomerado_muestra.id, db.Conglomerado_muestra.nombre)

    return dict(listaConglomerado = listaConglomerado)

    # Obteniendo los registros en la tabla de Archivo_camara
    #fotosCamara = db(db.Archivo_camara).select()
    #return dict(fotosCamara=fotosCamara)

# Se usan la funciones: asignarSitios() y asignarCamara() definidas con anterioridad

def asignarSitios():

    ## Función invocada mediante AJAX para llenar la combobox "sitio_muestra_id"
    ## a partir de los sitios existentes de un conglomerado seleccionado.

    # Obteniendo la información del conglomerado que seleccionó el usuario:
    conglomeradoElegidoID = request.vars.conglomerado_muestra_id

    # Obteniendo los sitios que existen en dicho conglomerado
    sitiosAsignados = db(
        (db.Sitio_muestra.conglomerado_muestra_id == conglomeradoElegidoID) &\
        (db.Sitio_muestra.existe == True) &\
        (db.Sitio_muestra.sitio_numero != 'Punto de control')
        ).select(db.Sitio_muestra.sitio_numero, db.Sitio_muestra.id)

    # Creando la dropdown de sitios y enviándola a la vista para que sea desplegada:

    dropdownHTML = "<select class='generic-widget' name='sitio_muestra_id' id='sitio_muestra_id'>"

    dropdownHTML += "<option value=''/>"

    for sitio in sitiosAsignados:

        dropdownHTML += "<option value='" + str(sitio.id) + "'>" + sitio.sitio_numero + "</option>"  
    
    dropdownHTML += "</select>"
    
    return XML(dropdownHTML)

def asignarCamara():
    
    ## Función invocada mediante AJAX para de la misma manera, enviar información 
    ## de la trampa cámara para el conglomerado y sitio seleccionados. El AJAX se
    ## activará al seleccionar un sitio asociado a un conglomerado.

    # El campo sitio_muestra_id es únicamente auxiliar y se utiliza para buscar
    # la cámara asociada a un sitio (mediante AJAX).

    sitioElegidoID = request.vars.sitio_muestra_id

    # Obteniendo las cámaras que han sido declaradas en dicho sitio

    camarasAsignadas = db(db.Camara.sitio_muestra_id ==\
        sitioElegidoID).select(db.Camara.id, db.Camara.nombre)

    camara = camarasAsignadas.first()

    # Bajo el supuesto que sólo existe una cámara por sitio, no se requiere
    # hacer dropdowns:

    respuestaHTML = "<p>Cámara localizada: </p>"

    if len(camarasAsignadas) == 0:

        respuestaHTML += "<p>No se encontró ninguna cámara declarada en el sitio elegido</p>"

        # La vista no permitirá enviar la forma si "camara_id" está vacío.
        respuestaHTML += "<input type='hidden' name='camara_id' "+\
            "id='camara_id' value=''/>"

    else:

        respuestaHTML += "<p>" + str(camara.nombre) +"</p>"

        respuestaHTML += "<input type='hidden' name='camara_id' "+\
            "id='camara_id' value='" + str(camara.id)+ "'/>"

    return XML(respuestaHTML)

def asignarArchivos():

    ## Función invocada mediante AJAX para de la misma manera, enviar información 
    ## de los archivos correspondientes a la cámara seleccionada. El AJAX se
    ## activa al seleccionar un sitio asociado a un conglomerado, después de que
    ## se asigna "camara_id" (también mediante AJAX).

    # El campo camara_id es únicamente auxiliar y se utiliza para buscar
    # los archivos asociados a una cámara (mediante AJAX).

    camaraElegidaID = request.vars.camara_id

    # Obteniendo los archivos correspondientes a la cámara seleccionada

    archivosCamara = db(db.Archivo_camara.camara_id == camaraElegidaID).select(
        db.Archivo_camara.id, db.Archivo_camara.archivo_nombre_original)


    if len(archivosCamara) == 0:

    # Si no encontraron archivos asociados a la cámara seleccionada:

        dropdownHTML = "<select class='generic-widget' name='archivo_camara_id' " +\
            "id='archivo_camara_id'>"

        dropdownHTML += "<option value=''/>"

        dropdownHTML += "</select>"

    else:

        # Creando la dropdown de archivos y enviándola a la vista para que sea
        # desplegada:

        dropdownHTML = "<select class='generic-widget' name='archivo_camara_id' " +\
            "id='archivo_camara_id'>"

        dropdownHTML += "<option value=''/>"

        for archivo in archivosCamara:

            dropdownHTML += "<option value='" + str(archivo.id) + "'>" +\
                archivo.archivo_nombre_original + "</option>"  
        
        dropdownHTML += "</select>"
        
    return XML(dropdownHTML)

def asignarInformacionArchivo():

    ## Ésta funcion se invoca mediante AJAX, y genera una forma para
    ## ingresar/modificar la información de la fotografía que seleccionó el
    ## usuario en el menú desplegable. El AJAX se activa al seleccionar un
    ## archivo de la lista desplegable.

    # Obteniendo la información del archivo que seleccionó el usuario:

    archivoElegidoID = request.vars.archivo_camara_id

    # Obteniendo la información del archivo

    datosArchivoAux = db(db.Archivo_camara.id == archivoElegidoID).select()

    datosArchivo = datosArchivoAux.first()

    # Creando la pantalla de revisión de archivos, considerando el caso en el
    # que datosArchivo esté vacía:

    if len(datosArchivoAux) == 0:

        revisionHTML = "<form id='forma_shadow'></form>"

    else:

        #HTML generado:

        # <form id='forma_shadow'>
        #   <input type='hidden' name='id_archivo' value='str(datosArchivo.id)'/>

        #   <center>
        #       <img src='data:image/jpeg;base64,imagen_codificada'
        #       alt='Error al cargar la fotografía' style='width:800px;height:600px;'/>
        #   </center>
        #   <hr/>

        #   <div style='float:left;padding-right:60px;'>
        #       <label for='con_fauna_evidente' style='float:left;padding-right:20px;'>
        #           Con fauna evidente
        #       </label>
        #       <input type='radio' name='fauna_evidente' value='encontrada'
        #       id='con_fauna_evidente' checked='true'/>"
        #   </div>
        #   <div style='float:left;'>
        #       <label for='sin_fauna_evidente' style='float:left;padding-right:20px;'>
        #           Sin fauna evidente
        #       </label>
        #       <input type='radio' name='fauna_evidente' value='no_encontrada'
        #       id='sin_fauna_evidente' checked='true'/>
        #   </div>
        #   <div style='clear:both;'></div>
        #   <br/>
        #   <!--Para el fade-in/out:-->
        #   <div id='info_fauna'>
        #       <label for='nombre_comun' style='float:left;padding-right:49px;'>
        #           Nombre común:
        #       </label>
        #       <input type='text' name='nombre_comun' class='string'
        #       id='nombre_comun' value='datosArchivo.nombre_comun'/>
        #       <br/>

        #       <label for='nombre_cientifico' style='float:left;padding-right:37px;'>
        #           Nombre científico:
        #       </label>
        #       <input type='text' name='nombre_cientifico' class='string'
        #       id='nombre_cientifico' value='datosArchivo.nombre_cientifico'/>
        #       <br/>

        #       <label for='numero_individuos' style='float:left;padding-right:10px;'>
        #           Número de individuos:
        #       </label>
        #       <input type='text' name='numero_individuos' class='integer'
        #       id='numero_individuos' value='datosArchivo.numero_individuos'/>
        #   </div>
        #   <br/>
        #   <input type='button' accesskey='a' style='float:left;' value='Anterior' id='anterior'/>
        #   <input type='button' accesskey='s' style='float:right;' value='Siguiente' id='siguiente'/>
        #
        #   <!--Se pone el center hasta el final, para que tome en cuenta el
        #   margen del elemento que flota a la derecha. -->
        #
        #   <center>
        #       <input type='button' value='Enviar' id='enviar'/>
        #   </center>
        # </form>

        # Obteniendo la información del conglomerado en el que se declararon los
        # archivos con el fin de reconstruir la ruta hacia ellos y poder visualizarlos.

        conglomeradoElegidoID = request.vars.conglomerado_muestra_id

        # Obteniendo la información del conglomerado

        datosConglomeradoAux = db(
            db.Conglomerado_muestra.id == conglomeradoElegidoID).select(
            db.Conglomerado_muestra.nombre, db.Conglomerado_muestra.fecha_visita)

        datosConglomerado = datosConglomeradoAux.first()

        datosConglomeradoNombre = str(datosConglomerado.nombre)
        datosConglomeradoFechaVisita = str(datosConglomerado.fecha_visita)

        # Creando el path hacia la imagen seleccionada (en caso de que se haya
        # seleccionado, recordar que el AJAX se activa para resetear la lista de
        # imágenes al cambiar cualquier combobox de la cascada).

        rutaCarpetaCglMuestra = eaa.crearRutaCarpeta(
            datosConglomeradoNombre,
            datosConglomeradoFechaVisita)

        pathImagen = os.path.join(rutaCarpetaCglMuestra,'c',datosArchivo.archivo)

        # Leyendo la imagen, pasándola a base 64 y guardándola en una variable
        # (hay que poner un try catch, por si no se puede leer la imagen).

        try:

            imagen = open(pathImagen, "rb")
            imagenCodificada = base64.b64encode(imagen.read())

        except:

            imagenCodificada = ""

        revisionHTML = "<form id='forma_shadow'><input type='hidden' " +\
            "name='id_archivo' value='" + str(datosArchivo.id) + "'/><center>"

        revisionHTML += "<img src='data:image/jpeg;base64," + imagenCodificada +\
            "' alt='Error al cargar la fotografía' style='width:800px;height:600px;'/>"

        # Descomentar el código siguiente para utilizar la función download() de
        # Web2py para descargar la imagen en la vista (sólo funciona para imágenes
        # guardadas en "uploads" usando el método "store()" de Web2py.)

        #revisionHTML += "<img src='/init/02_camara/download/" + datosArchivo.archivo +\
        #    "' alt='Error al cargar la fotografía' style='width:800px;height:600px;'/>"

        revisionHTML += "</center><hr/><div style='float:left;padding-right:60px;'>" +\
                "<label for='con_fauna_evidente' style='float:left;padding-right:20px;'>" +\
                "Con fauna evidente</label><input type='radio' name='fauna_evidente' " +\
                "value='encontrada' id='con_fauna_evidente'"

        # Si el campo de presencia de la foto elegida es True, entonces la
        # casilla "fauna evidente" aparece marcada.

        if datosArchivo.presencia:

            revisionHTML += " checked='true'/>"

        else:

            revisionHTML += "/>"

        revisionHTML += "</div><div style='float:left;'><label for='sin_fauna_evidente' " +\
            "style='float:left;padding-right:20px;'>Sin fauna evidente</label><input type='radio' " +\
            "name='fauna_evidente' value='no_encontrada' id='sin_fauna_evidente'"
        
        # Si el campo de presencia de la foto elegida es False, entonces la
        # casilla "Sin fauna evidente" aparece marcada.
        # Hay que revisar que sea igual a false, porque podría ser None.

        if datosArchivo.presencia == False:

            revisionHTML += " checked='true'/>"

        else:

            revisionHTML += "/>"

        revisionHTML += "</div><div style='clear:both;'></div><br/><div id='info_fauna'>" +\
            "<label for='nombre_comun' style='float:left;padding-right:49px;'>" +\
            "Nombre común:</label><input type='text' name='nombre_comun' class='string' " +\
            "id='nombre_comun' value='"

        #Si hay nombre común, éste aparece en la casilla para ingresar el texto.
        if datosArchivo.nombre_comun:

            revisionHTML += datosArchivo.nombre_comun

        revisionHTML += "'/><br/><label for='nombre_cientifico' " +\
            "style='float:left;padding-right:37px;'>Nombre científico:</label>" +\
            "<input type='text' name='nombre_cientifico' class='string' id='nombre_cientifico' value='"

        #Si hay nombre científico, éste aparece en la casilla para ingresar el texto.
        if datosArchivo.nombre_cientifico:

            revisionHTML += datosArchivo.nombre_cientifico

        revisionHTML += "'/><br/><label for='numero_individuos' " +\
            "style='float:left;padding-right:10px;'>Número de individuos:</label>" +\
            "<input type='text' name='numero_individuos' class='integer' id='numero_individuos' value='"

        if datosArchivo.numero_individuos:

            revisionHTML += str(datosArchivo.numero_individuos)

        revisionHTML += "'/></div><br/>" +\
            "<input type='button' accesskey='a' style='float:left;' value='Anterior' id='anterior'/>" +\
            "<input type='button' accesskey='s' style='float:right;' value='Siguiente' id='siguiente'/>" +\
            "<center><input type='button' value='Enviar' id='enviar'/></center>" +\
            "</form>"
    
    return XML(revisionHTML)

def actualizarArchivo():

    ## Ésta funcion se invoca mediante AJAX, y guarda la información que se introdujo/
    ## modificó en la forma generada para el archivo seleccionada. El AJAX se
    ## activa al presionar el botón "Enviar" en la forma correspondiente

    # Utilizando los datos enviados de la forma_shadow, se actualiza el registro
    # de una foto en la base de datos.

    archivoElegidoID = request.vars.id_archivo
    faunaEvidente = request.vars.fauna_evidente
    nombreComun = request.vars.nombre_comun
    nombreCientifico = request.vars.nombre_cientifico
    numeroIndividuos = request.vars.numero_individuos

    # Viendo si se encontró fauna evidente, no se encontró o la foto simplemente
    # no fue revisada.
    if faunaEvidente == 'encontrada':

        db(db.Archivo_camara.id == archivoElegidoID).update(
            presencia = True,
            nombre_comun = nombreComun,
            nombre_cientifico = nombreCientifico,
            numero_individuos = numeroIndividuos
        )

    else:

        db(db.Archivo_camara.id == archivoElegidoID).update(
            presencia = False,
            nombre_comun = None,
            nombre_cientifico = None,
            numero_individuos = None)

