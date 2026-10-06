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

# --- Tramo 1: sin comisión (hasta Q100 inclusive) ---
@pytest.mark.parametrize(
    "monto, esperado",
    [
        (0.01, 0.00),
        (0.10, 0.00),
        (1.00, 0.00),
        (10.00, 0.00),
        (50.00, 0.00),
        (99.99, 0.00),
        (100.00, 0.00),   # límite superior del Tramo 1 (incluido)
    ],
)
def test_tramo_1_sin_comision(monto, esperado):
    assert calcular_comision(monto) == esperado


# --- Tramo 2: 1.5% (más de Q100 hasta Q1,000 inclusive) ---
@pytest.mark.parametrize(
    "monto, esperado",
    [
        (100.01, 1.50),   # límite inferior del Tramo 2
        (110.00, 1.65),
        (120.00, 1.80),
        (150.00, 2.25),
        (200.00, 3.00),
        (500.00, 7.50),
        (990.00, 14.85),
        (1000.00, 15.00), # límite superior del Tramo 2 (incluido)
    ],
)
def test_tramo_2_1_5_por_ciento(monto, esperado):
    assert calcular_comision(monto) == esperado


# --- Tramo 3: 1% (más de Q1,000) ---
@pytest.mark.parametrize(
    "monto, esperado",
    [
        (1000.01, 10.00), # límite inferior del Tramo 3
        (1010.00, 10.10),
        (1100.00, 11.00),
        (1500.00, 15.00),
        (2000.00, 20.00),
        (2400.00, 24.00),
        (2490.00, 24.90), # justo por debajo del tope
    ],
)
def test_tramo_3_1_por_ciento(monto, esperado):
    assert calcular_comision(monto) == esperado


# --- Tope de comisión: máximo Q25.00 ---
@pytest.mark.parametrize(
    "monto, esperado",
    [
        (2500.00, 25.00), # tope exacto
        (2510.00, 25.00), # supera el tope
        (3000.00, 25.00),
        (5000.00, 25.00),
        (10000.00, 25.00),
    ],
)
def test_tope_comision(monto, esperado):
    assert calcular_comision(monto) == esperado


# --- Montos inválidos: ≤ 0 → ValueError ---
@pytest.mark.parametrize("monto_invalido", [0, -0.01, -1, -100, -1000])
def test_monto_menor_o_igual_a_cero(monto_invalido):
    with pytest.raises(ValueError):
        calcular_comision(monto_invalido)


# --- Tipos inválidos: no números → TypeError ---
@pytest.mark.parametrize(
    "tipo_invalido",
    [
        True,    # bool es subclase de int en Python; el mutante bonus podría aceptarlo
        False,   # ídem
        "100",
        "abc",
        None,
        [100],
        (100,),
        {"monto": 100},
        complex(100, 0),
    ],
)
def test_tipo_invalido(tipo_invalido):
    with pytest.raises(TypeError):
        calcular_comision(tipo_invalido)


# --- Consistencia de calcular_total: monto + comisión ---
@pytest.mark.parametrize(
    "monto, total_esperado",
    [
        (0.01, 0.01),     # Tramo 1: 0.01 + 0
        (50.00, 50.00),   # Tramo 1: 50 + 0
        (100.00, 100.00), # Tramo 1: 100 + 0
        (100.01, 101.51), # Tramo 2: 100.01 + 1.50
        (200.00, 203.00), # Tramo 2: 200 + 3
        (1000.00, 1015.00), # Tramo 2: 1000 + 15
        (1000.01, 1010.01), # Tramo 3: 1000.01 + 10
        (2000.00, 2020.00), # Tramo 3: 2000 + 20
        (2500.00, 2525.00), # Tope: 2500 + 25
        (3000.00, 3025.00), # Tope: 3000 + 25
        (10000.00, 10025.00), # Tope: 10000 + 25
    ],
)
def test_calcular_total_consistencia(monto, total_esperado):
    assert calcular_total(monto) == total_esperado


# --- Consistencia entre calcular_comision y calcular_total ---
@pytest.mark.parametrize(
    "monto",
    [0.01, 50.00, 100.00, 100.01, 200.00, 1000.00, 1000.01, 2000.00, 2500.00, 3000.00, 10000.00],
)
def test_total_es_monto_mas_comision(monto):
    """El total debe ser exactamente monto + comisión."""
    comision = calcular_comision(monto)
    total = calcular_total(monto)
    assert total == pytest.approx(monto + comision, abs=1e-9)
