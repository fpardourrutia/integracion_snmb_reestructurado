# Introducción

Este repositorio contiene:
1. El script para migrar la base de datos del SNMB del esquema v12 al esquema v14.
2. El código rediseñado para integrar datos provenientes de varios clientes de captura a la base de datos del SNMB.

# Supuestos del proceso de migración:

1. "Transecto_especies_invasoras_muestra" / "Transecto_huellas_excretas_muestra" -> "Transecto_muestra". Notar que en el esquema v14 se encuentra el campo: "Transecto_muestra.existe". Esto va de la mano con el cliente de captura v5, donde se tienen que declarar los 3 transectos (y si existen o no), para poder tener una diferencia más clara entre transectos que sí existen pero no tuvieron observaciones y transectos que no existen.

Declarar todos los transectos, independientemente de si existían o no, no era exigido estrictamente por los clientes anteriores, por lo que sólo se introdujeron a la base los transectos declarados en los clientes anteriores (con respecto a los
no declarados, se tiene la ambigüedad si existieron y no tuvieron registros o simplemente no existieron). Es importante tomar en cuenta este punto a la hora de analizar los datos
