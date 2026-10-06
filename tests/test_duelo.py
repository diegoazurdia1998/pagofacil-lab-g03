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
# --- Tramos y límites ---

@pytest.mark.parametrize("monto, esperado", [
    (100.00, 0.00),
    (100.01, 1.50),
    (1000.00, 15.00),
    (1000.01, 10.00),
    (2500.00, 25.00),
    (3000.00, 25.00),
])
def test_limites_de_tramo(monto, esperado):
    assert calcular_comision(monto) == esperado


# --- Tramo 1: sin comisión hasta Q100 ---

@pytest.mark.parametrize("monto", [0.01, 1.00, 50.00, 99.99, 100.00])
def test_tramo_1_sin_comision(monto):
    assert calcular_comision(monto) == 0.00


# --- Tramo 2: 1.5% entre Q100.01 y Q1000 ---

@pytest.mark.parametrize("monto, esperado", [
    (100.01, 1.50),
    (200.00, 3.00),
    (500.00, 7.50),
    (1000.00, 15.00),
])
def test_tramo_2_uno_y_medio_por_ciento(monto, esperado):
    assert calcular_comision(monto) == esperado


# --- Tramo 3: 1% arriba de Q1000 ---

@pytest.mark.parametrize("monto, esperado", [
    (1000.01, 10.00),
    (1500.00, 15.00),
    (2000.00, 20.00),
    (2490.00, 24.90),
])
def test_tramo_3_uno_por_ciento(monto, esperado):
    assert calcular_comision(monto) == esperado


# --- Tope de Q25 ---

@pytest.mark.parametrize("monto", [2500.00, 2510.00, 5000.00, 10000.00])
def test_tope_de_comision(monto):
    assert calcular_comision(monto) == 25.00


# --- Montos inválidos ---

@pytest.mark.parametrize("monto", [0, -0.01, -1, -100])
def test_monto_no_positivo(monto):
    with pytest.raises(ValueError):
        calcular_comision(monto)


@pytest.mark.parametrize("valor", [
    True,
    False,
    "100",
    None,
    [100],
    (100,),
    {"monto": 100},
    complex(100, 0),
])
def test_tipo_invalido(valor):
    with pytest.raises(TypeError):
        calcular_comision(valor)


# --- calcular_total ---

@pytest.mark.parametrize("monto, esperado", [
    (0.01, 0.01),
    (100.00, 100.00),
    (100.01, 101.51),
    (1000.00, 1015.00),
    (1000.01, 1010.01),
    (2500.00, 2525.00),
    (3000.00, 3025.00),
])
def test_calcular_total(monto, esperado):
    assert calcular_total(monto) == esperado


@pytest.mark.parametrize("monto", [
    0.01, 100.00, 100.01, 1000.00, 1000.01, 2000.00, 2500.00, 10000.00,
])
def test_total_es_monto_mas_comision(monto):
    assert calcular_total(monto) == pytest.approx(
        monto + calcular_comision(monto), abs=1e-9
    )
