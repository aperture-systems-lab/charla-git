"""Diapositiva 32 — próximos pasos.

Lo que no dio tiempo a ver: nueve nombres en una cuadrícula de tres por tres,
cada uno en su caja y con el nombre tal cual se escribe, que es justo lo que
hace falta para buscarlo luego.

Debajo de cada uno, entre paréntesis, para qué sirve en una línea: lo justo
para saber si te hace falta. Sin enlaces y sin cierre debajo —cada uno es una
tarde de otro día—. El único que no explica nada es ``git push --force``,
donde el aviso es la explicación.
"""

from manim import (
    DOWN,
    FadeIn,
    LaggedStart,
    RoundedRectangle,
    VGroup,
)

from componentes import texto
from componentes import titulo as hacer_titulo
from estilo import CLARO, PRIMARIO, SECUNDARIO, SUPERFICIE

# (nombre, para qué sirve). Una línea corta: aquí no se enseña a usarlos.
CONCEPTOS = (
    ("github actions", "automatiza al hacer push"),
    ("git bisect", "encuentra el commit culpable"),
    ("git tags", "pone nombre a una versión"),
    ("git milestone", "agrupa issues por entrega"),
    ("git stash", "aparta lo que tienes a medias"),
    ("git squash", "junta varios commits en uno"),
    ("readme", "la portada del repositorio"),
    ("detached HEAD", "estás en un commit, sin rama"),
    ("git push --force", "por si tiembla"),
)

COLUMNAS = 3
ANCHO_CAJA = 4.1
ALTO_CAJA = 1.15
X_CAJA = (-4.65, 0.0, 4.65)
Y_CAJA = (1.2, -0.45, -2.10)
TAM_CONCEPTO = 20
TAM_APOSTILLA = 13


def _caja(indice):
    """Un concepto en su caja, centrado."""
    nombre, apostilla = CONCEPTOS[indice]
    caja = RoundedRectangle(
        width=ANCHO_CAJA, height=ALTO_CAJA, corner_radius=0.16,
        stroke_color=PRIMARIO, stroke_width=3,
    ).set_fill(SUPERFICIE, opacity=1.0)
    caja.move_to([X_CAJA[indice % COLUMNAS], Y_CAJA[indice // COLUMNAS], 0])

    letras = texto(nombre, TAM_CONCEPTO, color=CLARO)
    if not apostilla:
        return VGroup(caja, letras.move_to(caja))
    pie = texto(f"({apostilla})", TAM_APOSTILLA, color=SECUNDARIO)
    cuerpo = VGroup(letras, pie).arrange(DOWN, buff=0.12).move_to(caja)
    return VGroup(caja, cuerpo)


def construir(scene):
    encabezado = hacer_titulo("proximos pasos")
    cajas = VGroup(*[_caja(i) for i in range(len(CONCEPTOS))])

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(
        LaggedStart(*[FadeIn(c, shift=DOWN * 0.12) for c in cajas],
                    lag_ratio=0.22),
        run_time=2.4,
    )
    scene.wait(0.3)

    scene.next_slide()
