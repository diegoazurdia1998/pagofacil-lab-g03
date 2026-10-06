"""MINI DUELO - Parte 2 del laboratorio.

Escribe aquí tus pruebas. El docente las ejecutará contra versiones del código
con defectos escondidos ("mutantes") y contará cuántos logran detectar.

REGLAS
  1. Solo puedes importar de `pytest` y de `pagofacil.comision`.
  2. TODAS tus pruebas deben PASAR con el código correcto (el que cumple
     ESPECIFICACION.md). Si una falla con el código correcto, no puntúas.
  3. Diseña desde la especificación (caja negra): particiones y valores límite.
  4. Evita montos cuyo resultado caiga justo en medio centavo (redondeo ambiguo).
  5. Trabaja SOLO en este archivo durante el duelo.
"""
import pytest

from pagofacil.comision import calcular_comision, calcular_total, validar_monto  # noqa: F401


def test_ejemplo_monto_bajo():  # ejemplo que ya pasa; puedes borrarlo o conservarlo
    assert calcular_comision(50) == 0


# --- Tus pruebas empiezan aquí ---
# 1. Pruebas de tramos y valores límite de comisiones
@pytest.mark.parametrize("monto, esperado", [
    (100.0, 0.0),       # Límite superior Tramo 1 (hasta Q100 exento)
    (100.01, 1.50),    # Límite inferior Tramo 2 (1.5%)
    (1000.0, 15.0),    # Límite superior Tramo 2 (1.5%)
    (1000.01, 10.0),   # Límite inferior Tramo 3 (1%)
    (3000.0, 25.0),    # Tope máximo de comisión (Q25)
])
def test_comision_por_tramos(monto, esperado):
    assert calcular_comision(monto) == esperado

# 2. Pruebas para montos inválidos (<= 0)
@pytest.mark.parametrize("monto_invalido", [0, -10])
def test_monto_invalido(monto_invalido):
    with pytest.raises(ValueError):
        calcular_comision(monto_invalido)

# 3. Pruebas para tipos de datos inválidos
@pytest.mark.parametrize("tipo_invalido", ["100", None, True, False])
def test_tipo_invalido(tipo_invalido):
    with pytest.raises(TypeError):
        calcular_comision(tipo_invalido)
