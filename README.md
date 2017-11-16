# Introducción

Este repositorio contiene:
1. El script para migrar la base de datos del SNMB del esquema v12 al esquema v14.
2. El código rediseñado para integrar datos provenientes de varios clientes de captura a la base de datos del SNMB.

# Supuestos del proceso de migración:

__"Transecto_especies_invasoras_muestra" / "Transecto_huellas_excretas_muestra" -> "Transecto_muestra"__: Notar que en el esquema v14 se encuentra el campo: "Transecto_muestra.existe". Esto va de la mano con el cliente de captura v5, donde se tienen que declarar los 3 transectos (y si existen o no), para poder tener una diferencia más clara entre transectos que sí existen pero no tuvieron observaciones y transectos que no existen.

Declarar todos los transectos, independientemente de si existían o no, no era exigido estrictamente por los clientes  anteriores, por lo que sólo se introdujeron a la base los transectos declarados en los clientes anteriores (con respecto a los
no declarados, se tiene la ambigüedad si existieron y no tuvieron registros o simplemente no existieron). Es importante tomar en cuenta este punto a la hora de analizar los datos

__"Arbol_cuadrante"__: al analizar los protocolos de campo (manuales) correspondientes a los esquemas v12 y v14, se puede observar que el método para la toma de datos de árboles grandes cambió drásticamente. El cambio principal era que antes se muestreaban máximo 8 árboles por sitio, y ahora se censan todos los árboles.

Con respecto a los datos contenidos en la base, antes (esquema v12) se declaraban 8 árboles por sitio con el campo "existe" siempre no vacío. Ahora (esquema v14) se declaran con el campo existe vacío. De esta manera, es posible diferenciar cuáles árboles fueron muestreados con qué protocolo de campo.

### Requerimientos para el proceso de migración.

1. [Instalar PostgreSQL con ayuda de Homebrew](https://marcinkubala.wordpress.com/2013/11/11/postgresql-on-os-x-mavericks/).
2. Instalar la librería de Python [psycopg2](http://initd.org/psycopg/):
```
> pip install psycopg2
```

3. Descargar el código fuente de Web2py v2.11.2 (commit [236fdcf](https://github.com/web2py/web2py/commit/236fdcfafc60436c23d0ed5ce6e04eb1e1cde4b1)). É
Descargar el código fuente de Web2py v2.11.2 (commit [236fdcf](https://github.com/web2py/web2py/commit/236fdcfafc60436c23d0ed5ce6e04eb1e1cde4b1)) este utiliza el python local para funcionar.
4. Descargar el "fusionador_v3_hotfix" (commit [9687c97](https://github.com/fpardourrutia/fusionador_snmb/commit/9687c9764d2430f7bd153aa3b1688058742b5bb6)) en la carpeta de "applications" dentro de Web2py.
5. Abrir la terminal para crear la base de datos postgres:
```
> cd /usr/local/var
> #creando la base de datos:
> initdb nombre_base
> #encendiendo el servidor
> postgres -D postgres
> #registrándola adecuadamente
> createdb nombre_base
```
6. Abrir el archivo: *fusionador_postgres/models/00_0_db_f.py*, y revisar que la siguiente línea esté correcta:
```
db = DAL('postgres://usuario:contrasena@localhost/nombre_base', db_codec='UTF-8',check_reserved=['all'], migrate = True)
```
Nota: `migrate = False` se utiliza para bases de datos preexistentes (por ejemplo, que hayan sido pobladas mediante algún ETL,
antes de utilizarlas de esta manera.

# Plan de trabajo:

1. Crear nuevas funciones para integrar el cliente v3 (esquema v10) -> base postgres esquema v12 (reestructuración).
2. Crear nuevas funciones para integrar el cliente v4 (esquema v12) -> base postgres esquema v12
3. Crear nuevas funciones para integrar el cliente v5 (esquema v13 y v14) -> base postgres esquema v14.
4. Migrar de la base postgres v12 a la base postgres v14 (migración temporal.

# Procedimiento de integracion de datos

1. Integrar los datos de CONANP y FMCN tomados con el cliente v5 a la base temporal postgres v14.
2. Cuando lleguen los datos de CONAFOR tomados con el cliente v3 y v4, integrarlos a la base postgres esquema v12
3. Realizar la migración final a la base postgres v14 definitiva.
4. Integrar los datos de CONANP/FMCN/CONAFOR tomados con el cliente v5 a la base postgres v14 definitiva.


