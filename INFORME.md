# Informe del laboratorio · Pruebas y versionamiento

> Reemplaza **cada** `<<COMPLETAR>>` con tu respuesta. No borres los encabezados.
> Extensión esperada: 1.5 a 2 páginas. Se entrega haciendo `git push` de este archivo.

## 1. Datos del equipo

- **Equipo (gNN):** Grupo 03 - IA
- **Repositorio (URL):** https://github.com/diegoazurdia1998/pagofacil-lab-g03

| Integrante | Carnet | Usuario de GitHub |
|------------|--------|-------------------|
| Pablo Javier Gonzalez Perez | 1211624 | Pablo1211624 |
| Diego Andres Azurdia Ortiz | 2528119 | diegoazurdia1998 |
| Andrea Sofía Miranda Abrego | 1065824 | AndreaMiranda1065824 |
| Jarod Michael Bolaños | 1251621 | jarod54654658 |
| Gabriel Ajin | 1184924 | gabrielajiizaaa |

## 2. Evidencia

Pega la salida real de estos comandos (bloque de código):

`python -m pytest -q`
..............................................................              [100%]
62 passed in 0.06s

`git log v1.0.0..v1.0.1 --oneline --decorate`
3b0e6e9 (tag: v1.0.0) Initial commit

## 3. Bitácora de defectos

| # | Pruebas que fallaban | Síntoma (mensaje del error) | Causa raíz | Corrección (qué línea cambió) | Commit | Quién |
|---|----------------------|-----------------------------|------------|-------------------------------|--------|-------|
| 1 | tests/test_comision.py::test_monto_exacto_100_no_paga_comision | assert 1.5 == 0<br>+ where 1.5 = calcular_comision(100) | El valor de 100, no está incluido en > debe ser >= | Se cambió en > a >= | fix(comision): incluir Q100 en tramo 1 exento | diegoazurdia1998 |
| 2 | tests/test_comision.py::test_tope_maximo_de_q25[3000],<br>tests/test_comision.py::test_tope_maximo_de_q25[10000],<br>tests/test_comision.py::test_tope_maximo_de_q25[1000000] | assert 30.0 == 25<br>+ where 30.0 = calcular_comision(3000),<br>assert 100.0 == 25<br>+ where 100.0 = calcular_comision(10000),<br>assert 10000.0 == 25<br>+ where 10000.0 = calcular_comision(1000000) | La línea return round(comision, 2) no aplicaba el tope máximo de Q25 | return round(min(comision, TOPE_COMISION), 2) | Cambio tope 25 agregado | Pablo1211624 |
| 3 | tests/test_total.py::test_total_incluye_la_comision[200-203.0],<br>tests/test_total.py::test_total_incluye_la_comision[500-507.5] | assert 197.0 == 203.0,<br>assert 492.5 == 507.5 | calcular_total restaba la comisión en lugar de sumarla, lo que contradice RN3 (total = monto + comisión) | return round(monto - comision, 2) → return round(monto + comision, 2) | fix(total): sumar comision al monto en calcular_total | gabrielajiizaaa |


**Pregunta:** al inicio había 6 pruebas fallando pero solo 3 defectos. ¿Por qué? ¿Qué diferencia hay entre *síntoma* y *causa raíz*?
*Respuesta:* Primero, un síntoma es algún error que se presenta cuando se ejecutan las pruebas, es la consecuencia de alguna causa raíz que no necesariamente debe estar ahí mismo. La causa raíz es el problema principal que está produciendo los síntomas. Al inicio habían 6 pruebas pero solo 3 defectos porque un defecto puede causar varios problemas.


## 4. Versionamiento

1. Corrigieron 3 defectos sin cambiar la interfaz pública. ¿Por qué la nueva versión es `1.0.1` y no `1.1.0` ni `2.0.0`?
   Por la misma estructura con la que se trabajan las etiquetas. Los cambios solo fueron correcciones sin cambiar la interfaz pública, por lo que solo se modifica el número dle final.
2. Si agregaran la función nueva `calcular_comision_con_iva(monto)` sin tocar nada existente, ¿qué versión sería y por qué?
   Sería la versión 1.1.0 porque ya no es corregir errores con funcionalidades actuales sino que es agregar una nueva funcionalidad sin cambiar completamente la interfaz.
3. Si cambiaran `calcular_comision(monto)` para exigir un segundo parámetro obligatorio `moneda`, ¿qué versión sería y por qué?
   Sería 2.0.0 porque se está modificando toda la estructura.
4. Ejecuten `git diff v1.0.0 v1.0.1 --stat`. ¿Qué archivos cambiaron y por qué es útil poder comparar dos versiones?

 CHANGELOG.md              |   2 +
 INFORME.md                |  14 ++++---
 Tarea_Previa_Lab06.pdf    | Bin 0 -> 378254 bytes
 src/pagofacil/comision.py |   6 +--
 tarea_previa/edad.py      |   2 +-
 tarea_previa/test_edad.py |  16 ++++++++
 tests/test_duelo.py       |  97 ++++++++++++++++++++++++++++++++++++++++++++++
 7 files changed, 128 insertions(+), 9 deletions(-)

## 5. Mini duelo

Tabla de casos que diseñaron (mínimo 6 filas; indiquen la técnica):

| Partición o límite que cubre | Entrada | Resultado esperado | Técnica |
|------------------------------|---------|--------------------|---------|
| Límite Tramo 1 | 100.0 |  0.0 | Valores límite |
| Límite Tramo 2 | 100.01 | 1.50 | Valores límite |
| Límite Tramo 2 (sup) | 1000.0 | 15.0 | Valores límite |
| Límite Tramo 3 | 1000.01 | 10.0 | Valores límite |
| Tope de Comisión | 3000.0 | 25.0 | Valores límite |
| Números Inválidos | 0, -10 | ValueError | Partición de equivalencia |
| Tipos Inválidos | "100", None, True | TypeError | <Partición de equivalencia |

- **Resultado del marcador (mutantes detectados de 7):** *PENDIENTE*
- **¿Qué mutantes sobrevivieron (si alguno) y qué caso de prueba les habría faltado?** *PENDIENTE*

## 6. Reflexión (5 a 8 líneas)

Su suite visible quedó 100 % en verde y, aun así, el duelo puede encontrar defectos escondidos.
¿Qué implica eso para la estrategia de pruebas? Relaciónenlo con la pirámide de pruebas, con
qué conviene automatizar y con el caso Knight Capital de la clase.

Como se menciona, que la suite visible quede 100% en verde no garantiza que no haya defectos escondidos porque solamente se pasaron cierta cantidad de pruebas, pudieron haber otras pruebas que se omitieron por lo que en esa área pueden haber errores no tan visibles. Esto implica que la estrategia de pruebas no debe confiarse solo de lo que esté en verde, sino que hay que diseñar casos de prueba específicos que puedan cubrir varios aspectos. La pirámide de pruebas ayuda a organizar eso. Conviene automatizar pruebas simples y unitarias. En cuanto al caso de Knight Capital, se puede relacionar con el laboratorio al evaluar la situación de pruebas que tuvieron debido a que perdieron mucho por no establecer un plan de pruebas correcto, hecho que se debe evitar. 
