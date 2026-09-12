"""Diapositiva 3 — la solución, en tres actos y casi sin texto.

Va justo detrás de "Motivación", y el título contesta a aquella: lo que allí
era un proyecto repartido por el chat, aquí es una sola línea de tiempo. La
diapositiva es un único dibujo que se va completando:

  1. La historia: una versión detrás de otra, en línea, hacia la derecha.
  2. La rama: una línea que se abre para trabajar aparte y vuelve a entrar.
  3. El equipo: las mismas tres personas del chat, ahora escribiendo todas en
     la misma historia.

Abajo se van encendiendo las tres palabras que, juntas, dicen qué es lo que
resuelve. No hay más texto: lo que hay que entender está dibujado, y es el
mismo dibujo de la portada y del cierre, a propósito.
"""

from manim import (
    DOWN,
    RIGHT,
    UP,
    Create,
    DashedLine,
    FadeIn,
    Flash,
    GrowFromCenter,
    LaggedStart,
    VGroup,
)

from animaciones import pulso
from componentes import arista, avatar, nodo_commit, puntero, texto
from componentes import titulo as hacer_titulo
from estilo import (
    CLARO,
    FONT_TITULO,
    RAMA_FEATURE,
    RAMA_MAIN,
    SECUNDARIO,
)

TITULO = "La solución"

# --- La línea de tiempo ----------------------------------------------------
# Cinco versiones en fila y, en el segundo acto, el merge que cierra la rama.
X_MAIN = (-5.4, -3.6, -1.8, 0.0, 1.8)
X_MERGE = 3.6
Y_MAIN = 0.35
VERSIONES = ("v1", "v2", "v3", "v4", "v5")
VERSION_MERGE = "v6"

# La rama sale de v2 y vuelve en el merge, por encima del tronco. Sus nodos van
# sin etiqueta: aquí todavía no toca hablar de hashes, y así se lee de un
# vistazo cuál es la línea principal.
X_RAMA = (-1.8, 0.0)
Y_RAMA = 1.75
R = 0.32

# Continuación de puntos a la derecha: la historia no se acaba en el dibujo.
# Empiezan pegados a la última versión y se apartan cuando llega el merge, para
# que en el primer acto no queden flotando en mitad de la nada.
X_TIEMPO = (2.4, 3.7)
APARTA_TIEMPO = RIGHT * 1.9

# --- El equipo -------------------------------------------------------------
# Las mismas tres del chat de la diapositiva anterior, cada una colgando de la
# versión que hizo. Ninguna cuelga del merge: ahí abajo va el puntero ``main``.
EQUIPO = (("A", "ana", 0), ("L", "luis", 2), ("M", "mar", 4))
Y_EQUIPO = -1.75
RADIO_AVATAR = 0.42

# --- Las tres palabras de abajo -------------------------------------------
PALABRAS = (
    ("VERSIONES", RAMA_MAIN),
    ("RAMAS", RAMA_FEATURE),
    ("EN EQUIPO", CLARO),
)
Y_PALABRAS = -3.2
TAM_PALABRA = 17


def _historia():
    """Los cinco nodos de la línea principal y los tramos que los unen."""
    nodos = VGroup(*[
        nodo_commit(v, RAMA_MAIN, R).move_to([x, Y_MAIN, 0])
        for x, v in zip(X_MAIN, VERSIONES)
    ])
    tramos = VGroup(*[
        arista(a, b, RAMA_MAIN, R) for a, b in zip(nodos, nodos[1:])
    ])
    return nodos, tramos


def _rama(desde, hasta):
    """La rama que sale de ``desde``, trabaja arriba y vuelve en ``hasta``."""
    nodos = VGroup(*[
        nodo_commit("", RAMA_FEATURE, R).move_to([x, Y_RAMA, 0]) for x in X_RAMA
    ])
    tramos = VGroup(
        arista(desde, nodos[0], RAMA_FEATURE, R),      # se abre
        arista(nodos[0], nodos[1], RAMA_FEATURE, R),
        arista(nodos[1], hasta, RAMA_FEATURE, R),      # y se cierra
    )
    return nodos, tramos


def _fichas(nodos):
    """Las tres personas, colgadas de la versión que hizo cada una."""
    fichas, cuerdas = VGroup(), VGroup()
    for inicial, nombre, indice in EQUIPO:
        x = nodos[indice].get_center()[0]
        ficha = avatar(inicial, nombre, RADIO_AVATAR).move_to([x, Y_EQUIPO, 0])
        fichas.add(ficha)
        cuerdas.add(DashedLine(
            [x, Y_MAIN - R, 0], [x, ficha.get_top()[1], 0],
            color=SECUNDARIO, stroke_width=2, dash_length=0.09,
        ).set_stroke(opacity=0.55))
    return fichas, cuerdas


def _palabras():
    """Las tres palabras del pie, ya colocadas: se encienden de una en una."""
    fila = VGroup()
    for i, (palabra, color) in enumerate(PALABRAS):
        if i:
            fila.add(texto("·", TAM_PALABRA, color=SECUNDARIO))
        fila.add(texto(palabra, TAM_PALABRA, color=color, font=FONT_TITULO))
    return fila.arrange(RIGHT, buff=0.5).move_to([0, Y_PALABRAS, 0])


def construir(scene):
    encabezado = hacer_titulo(TITULO)
    nodos, tramos = _historia()
    merge = nodo_commit(VERSION_MERGE, RAMA_MAIN, R).move_to([X_MERGE, Y_MAIN, 0])
    rama, tramos_rama = _rama(nodos[1], merge)
    cierre_main = arista(nodos[-1], merge, RAMA_MAIN, R)
    fichas, cuerdas = _fichas(nodos)
    palabras = _palabras()

    p_main = puntero("main", RAMA_MAIN, 15).next_to(merge, DOWN, buff=0.3)
    p_rama = puntero("feature", RAMA_FEATURE, 15).next_to(rama[1], UP, buff=0.3)

    tiempo = DashedLine([X_TIEMPO[0], Y_MAIN, 0], [X_TIEMPO[1], Y_MAIN, 0],
                        color=SECUNDARIO, stroke_width=2, dash_length=0.12)
    tiempo.set_stroke(opacity=0.5)
    rotulo_tiempo = texto("tiempo", 14, color=SECUNDARIO)
    rotulo_tiempo.next_to(tiempo, RIGHT, buff=0.22)

    # ---------------------- Acto 1: la historia ----------------------------
    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(GrowFromCenter(nodos[0]), run_time=0.45)
    for tramo, nodo in zip(tramos, nodos[1:]):
        scene.play(Create(tramo), GrowFromCenter(nodo), run_time=0.45)
    scene.play(Create(tiempo), FadeIn(rotulo_tiempo), run_time=0.5)
    scene.play(FadeIn(palabras[0], shift=UP * 0.12), run_time=0.5)
    scene.next_slide()

    # ---------------------- Acto 2: la rama --------------------------------
    scene.play(Create(tramos_rama[0]), run_time=0.5)   # la curva cuenta el qué
    scene.play(GrowFromCenter(rama[0]), run_time=0.35)
    scene.play(Create(tramos_rama[1]), GrowFromCenter(rama[1]), run_time=0.45)
    scene.play(FadeIn(p_rama, shift=DOWN * 0.12), run_time=0.35)

    # La historia sigue: los puntos del final se apartan y entra el merge.
    scene.play(VGroup(tiempo, rotulo_tiempo).animate.shift(APARTA_TIEMPO),
               run_time=0.45)
    scene.play(Create(cierre_main), Create(tramos_rama[2]), run_time=0.7)
    scene.play(
        GrowFromCenter(merge),
        Flash(merge, color=RAMA_MAIN, line_length=0.22, num_lines=14,
              flash_radius=R + 0.35),
        run_time=0.6,
    )
    scene.play(FadeIn(p_main, shift=UP * 0.12), run_time=0.35)
    scene.play(FadeIn(palabras[1]), FadeIn(palabras[2], shift=UP * 0.12),
               run_time=0.5)
    scene.next_slide()

    # ---------------------- Acto 3: el equipo ------------------------------
    scene.play(
        LaggedStart(*[
            LaggedStart(Create(cuerda), GrowFromCenter(ficha), lag_ratio=0.4)
            for cuerda, ficha in zip(cuerdas, fichas)
        ], lag_ratio=0.35),
        run_time=1.6,
    )
    scene.play(FadeIn(palabras[3]), FadeIn(palabras[4], shift=UP * 0.12),
               run_time=0.5)

    # Un barrido de luz por toda la historia: una sola línea de tiempo, de
    # todos, con sus ramas dentro.
    scene.play(
        *[pulso(t, CLARO, 0.7) for t in tramos],
        *[pulso(t, CLARO, 0.9) for t in tramos_rama],
        pulso(cierre_main, CLARO, 0.7),
        run_time=1.2,
    )
    scene.wait(0.3)

    scene.next_slide()
