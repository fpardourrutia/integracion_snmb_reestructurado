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

# Implementación del proceso de migración.

0. Descargar el código fuente de Web2py v2.11.1 (commit [01474c9](https://github.com/web2py/web2py/commit/01474c99b01eb422a413b5de322e5d5be611b6b2))
1. Descargar el "fusionador_v3_hotfix" (commit [9687c97](https://github.com/fpardourrutia/fusionador_snmb/commit/9687c9764d2430f7bd153aa3b1688058742b5bb6))

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


