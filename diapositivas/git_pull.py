"""Diapositiva 22e — ``git pull``: traer y fusionar de una vez.

El último del tramo, y el que más quebraderos de cabeza da, porque hace dos
cosas y solo se ve una. La igualdad de arriba es toda la diapositiva:

    git pull  =  git fetch  +  git merge

La primera mitad ya se contó: baja los commits y adelanta ``origin/main``. La
segunda es la de la diapositiva del merge, con todo lo que eso trae —incluido
que pueda dar conflicto—, y es la que sorprende, porque quien teclea ``pull``
cree que solo está mirando el correo.

Las dos cajas de abajo son la chuleta: ``fetch`` toca ``origin/main`` y nada
más; ``pull`` toca además tu rama y tus archivos. El mismo viaje al servidor;
lo que cambia es si git te remueve el escritorio al volver.

Cuando alguien dice "hice pull y se me lió todo", casi siempre lo que quería
era un ``fetch`` para ver primero. De ahí el consejo del pie.
"""

from manim import (
    DOWN,
    UP,
    FadeIn,
    LaggedStart,
    RoundedRectangle,
    VGroup,
)

from animaciones import teclear
from componentes import terminal, texto
from componentes import titulo as hacer_titulo
from estilo import AMBAR, CLARO, OK, RAMA_MAIN, SECUNDARIO, SUPERFICIE

TITULO = "git pull"

ECUACION = "git pull  =  git fetch  +  git merge"
TAM_ECUACION = 21
Y_ECUACION = 2.4
# (trozo de la igualdad, color). Los mismos colores que las cajas de abajo.
PARTES = (
    ("git pull", OK),
    ("git fetch", AMBAR),
    ("git merge", RAMA_MAIN),
)

SESION = (
    ("git pull", "cmd"),
    ("Updating 9c1d..77ab", "out"),
    ("Fast-forward", "out"),
    (" informe.md | 12 ++++++-----", "out"),
)
TAM_SESION = 15
Y_SESION = 0.5

# (comando, qué toca, el apunte, color)
CAJAS = (
    ("git fetch", "solo actualiza origin/main", "tu trabajo no se toca", AMBAR),
    ("git pull", "fetch + merge, de una vez", "puede dar conflicto", OK),
)
X_CAJAS = (-3.5, 3.5)
Y_CAJAS = -2.15
ANCHO_CAJA, ALTO_CAJA = 5.4, 1.75
DY_NOMBRE, DY_LINEA, DY_NOTA = 0.48, -0.02, -0.5

CONSEJO = "si no sabes qué te vas a encontrar, haz fetch y mira primero"


def _ecuacion():
    """La igualdad con cada comando de su color.

    Por posición y no por palabra: las claves de ``t2c`` son expresiones
    regulares, y los índices se calculan sobre la propia cadena para que la
    igualdad se pueda reescribir sin recontar a mano.
    """
    t2c = {}
    for trozo, color in PARTES:
        i = ECUACION.index(trozo)
        t2c[f"[{i}:{i + len(trozo)}]"] = color
    return texto(ECUACION, TAM_ECUACION, color=CLARO, t2c=t2c)


def _caja(comando, que_hace, apunte, color, x):
    """Una de las dos cajas de la chuleta: el comando y hasta dónde llega."""
    caja = RoundedRectangle(
        width=ANCHO_CAJA, height=ALTO_CAJA, corner_radius=0.18,
        stroke_color=color, stroke_width=3,
    ).set_fill(SUPERFICIE, opacity=1.0).move_to([x, Y_CAJAS, 0])
    nombre = texto(comando, 21, color=color).move_to([x, Y_CAJAS + DY_NOMBRE, 0])
    linea = texto(que_hace, 17, color=CLARO).move_to([x, Y_CAJAS + DY_LINEA, 0])
    nota = texto(apunte, 15, color=SECUNDARIO).move_to([x, Y_CAJAS + DY_NOTA, 0])
    return VGroup(caja, nombre, linea, nota)


def construir(scene):
    encabezado = hacer_titulo(TITULO)
    igualdad = _ecuacion().move_to([0, Y_ECUACION, 0])
    consola = terminal(SESION, tam=TAM_SESION).move_to([0, Y_SESION, 0])
    cajas = VGroup(*[_caja(*datos, x) for datos, x in zip(CAJAS, X_CAJAS)])
    consejo = texto(CONSEJO, 17, color=CLARO).to_edge(DOWN, buff=0.5)

    # ------------------------------ montaje --------------------------------
    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(FadeIn(igualdad, shift=DOWN * 0.1), run_time=0.7)
    scene.play(FadeIn(consola[0]), run_time=0.5)
    teclear(scene, consola, ritmo=0.32)
    scene.play(
        LaggedStart(*[FadeIn(c, shift=UP * 0.12) for c in cajas],
                    lag_ratio=0.35),
        run_time=1.2,
    )
    scene.play(FadeIn(consejo), run_time=0.45)
    scene.wait(0.3)

    scene.next_slide()
