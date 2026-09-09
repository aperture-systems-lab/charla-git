"""Diapositiva 17 — ``git diff``: qué cambió.

La lupa. No cambia nada, así que se puede teclear sin miedo, y su lío viene
otra vez de las tres zonas: sin argumentos compara el directorio de trabajo
contra el staging, y con ``--staged`` compara el staging contra el último
commit. Siempre mide el hueco **entre dos sitios**, y saber cuáles son es todo
el truco.

A la izquierda la salida entera, con su cabecera de hunk y sus renglones en
rojo y verde —el mismo lenguaje que ya se usó en ``mensajes_commit``—, y a la
derecha las tres variantes que se usan, cada una diciendo qué dos cosas
compara.
"""

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    FadeIn,
    LaggedStart,
    VGroup,
)

from animaciones import teclear
from componentes import terminal, texto
from componentes import titulo as hacer_titulo
from estilo import CLARO, OK, RAMA_MAIN, SECUNDARIO, STAGING

TITULO = "git diff: ¿qué cambió?"

DIFF = (
    ("git diff", "cmd"),
    ("--- a/informe.md", "out"),
    ("+++ b/informe.md", "out"),
    ("@@ -12,4 +12,5 @@", "avi"),
    ("  ## Resultados", "out"),
    ("- El modelo acierta un 80 %", "err"),
    ("+ El modelo acierta un 87 %", "ok"),
    ("+ con validacion cruzada", "ok"),
)
TAM_DIFF = 16
X_DIFF, Y_DIFF = -3.5, 0.35

# (variante, qué compara, color). El color es el de la zona que mide.
VARIANTES = (
    ("git diff", "trabajo  vs  staging", STAGING),
    ("git diff --staged", "staging  vs  último commit", RAMA_MAIN),
    ("git diff main..rama", "una rama  vs  otra", CLARO),
)
X_VARIANTE = 1.15
Y_VARIANTES = 1.35
PASO_VARIANTE = 1.0
BAJADA_COMPARA = 0.36
REMATE = "otra vez las tres zonas: el diff mide el hueco entre dos"


def construir(scene):
    encabezado = hacer_titulo(TITULO)
    consola = terminal(DIFF, tam=TAM_DIFF).move_to([X_DIFF, Y_DIFF, 0])

    variantes = VGroup()
    for i, (comando, compara, color) in enumerate(VARIANTES):
        y = Y_VARIANTES - i * PASO_VARIANTE
        arriba = texto(comando, 17, color=color)
        arriba.move_to([X_VARIANTE, y, 0], LEFT)
        abajo = texto(compara, 14, color=SECUNDARIO)
        abajo.move_to([X_VARIANTE, y - BAJADA_COMPARA, 0], LEFT)
        variantes.add(VGroup(arriba, abajo))

    remate = texto(REMATE, 15, color=OK).to_edge(DOWN, buff=0.6)

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(FadeIn(consola[0]), run_time=0.5)
    teclear(scene, consola, ritmo=0.28)
    scene.play(
        LaggedStart(*[FadeIn(v, shift=RIGHT * 0.15) for v in variantes],
                    lag_ratio=0.3),
        run_time=1.3,
    )
    scene.play(FadeIn(remate), run_time=0.45)
    scene.wait(0.3)
    scene.next_slide()
