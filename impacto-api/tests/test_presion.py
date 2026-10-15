from app.calculos.presion import banda_normal, evaluar, la_mas_alta
from app.datos_ejemplo import banco_central as bc
from app.modelos.termometros import Presion

HISTORIA = [float(v) for v in range(1, 101)]


def test_banda_normal_son_los_percentiles_20_y_80():
    banda = banda_normal(HISTORIA)
    assert round(banda.min, 1) == 20.8
    assert round(banda.max, 1) == 80.2


def test_presion_segun_la_historia():
    assert evaluar(95, HISTORIA)[0] is Presion.alta
    assert evaluar(50, HISTORIA)[0] is Presion.media
    assert evaluar(5, HISTORIA)[0] is Presion.baja


def test_presion_invertida():
    assert evaluar(5, HISTORIA, invertida=True)[0] is Presion.alta
    assert evaluar(95, HISTORIA, invertida=True)[0] is Presion.baja


def test_sin_historia_suficiente_es_media_y_sin_banda():
    assert evaluar(5, [1.0, 2.0]) == (Presion.media, None)


def test_la_mas_alta():
    assert la_mas_alta(Presion.baja, Presion.alta, Presion.media) is Presion.alta


def test_foto_del_banco_central_tiene_historia_de_5_anios():
    for serie in bc.SERIES.values():
        assert len(serie.historia()) >= 12, serie.id
        assert serie.grafico(), serie.id


def test_formatos_en_espanol():
    assert bc.tasa(4.5) == "4,5 %"
    assert bc.tasa(4.25) == "4,25 %"
    assert bc.pesos(41162.73) == "$41.163"
    assert bc.pct(-1.01, signo=True) == "−1,0 %"
