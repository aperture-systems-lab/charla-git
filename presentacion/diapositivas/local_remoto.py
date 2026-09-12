"""Diapositiva 20 — local y remoto: git es distribuido.

La primera vez que aparece un servidor en la charla, y con las tres piezas a la
vez en pantalla para que no haga falta explicarlo antes:

    tu portátil  --push-->  GitHub  --clone-->  el portátil de Carmen

Arriba el repositorio remoto —con el logo de GitHub encima, para que se vea que
"el remoto" es ese sitio y no una abstracción— y abajo los dos ordenadores,
cada uno con su ventana. El de la izquierda tiene su rama; los otros dos
empiezan vacíos, que es la parte que suele sorprender: un repo recién creado en
GitHub no tiene nada hasta que alguien sube algo.

Lo que hay que ver, y es lo único: **nada se mueve, todo se copia**. Tras el
``push`` la cadena sigue entera en tu portátil y además está arriba; tras el
``clone`` está en los tres sitios, con los mismos commits y los mismos hashes.
Eso es que git sea distribuido —tres historiales completos, no tres accesos al
mismo— y de ahí sale que se pueda trabajar sin internet y que si mañana cerrara
GitHub el proyecto siguiera vivo en dos portátiles.

Los dos comandos salen a secas, sin desmenuzar: aquí solo hacen de rótulo del
viaje. Lo que hace cada uno, con sus banderas y sus vueltas, viene en las
cinco diapositivas siguientes, una por comando.
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    PI,
    RIGHT,
    UP,
    Create,
    CurvedArrow,
    FadeIn,
    GrowFromCenter,
    Indicate,
    LaggedStart,
    RoundedRectangle,
    VGroup,
)

from animaciones import pulso
from componentes import arista, imagen_circular, nodo_commit, texto, ventana
from componentes import titulo as hacer_titulo
from estilo import CLARO, OK, RAMA_MAIN, SECUNDARIO, SUPERFICIE

TITULO = "local y remoto"

# --- Arriba: el repositorio remoto -----------------------------------------
X_LOGO = 2.95
DIAMETRO_LOGO = 1.4
# El logo es cuadrado y el disco lo recorta en redondo: sin bajar la ocupación
# por debajo de 0.71 (un cuadrado inscrito en su círculo) le corta la palabra.
OCUPACION_LOGO = 0.7
ANCHO_REMOTO = 3.6
ALTO_REMOTO = 1.4
Y_REMOTO = 1.2
NOMBRE_REMOTO = "origin"

# --- Abajo: los dos ordenadores --------------------------------------------
X_MAQUINA = (-4.0, 4.0)
Y_MAQUINA = -1.8
ANCHO_MAQUINA = 4.6
ALTO_MAQUINA = 2.0
MAQUINAS = ("tu portátil", "el portátil de Carmen")
Y_CADENA_MAQUINA = -1.85

# --- Los repos, del tamaño de un cajetín -----------------------------------
HASHES = ("0e5f", "77ab", "9c1d")
DX_NODOS = (-1.15, 0.0, 1.15)
RADIO = 0.3
TAM_HASH = 13
TAM_RAMA = 14

# --- Los dos viajes --------------------------------------------------------
SALIDA_PUSH = (-2.6, -0.8, 0)
LLEGADA_PUSH = (-1.75, 0.55, 0)
SALIDA_CLONE = (1.75, 0.55, 0)
LLEGADA_CLONE = (2.6, -0.8, 0)
# Curvadas y no rectas: el viaje al servidor se lee mejor como un arco. El
# ángulo va en negativo para que las dos abran hacia fuera —la de subida por la
# izquierda y la de bajada por la derecha— y dejen libre el centro.
ANGULO = -PI / 3
X_ORDEN = (-4.4, 4.4)
Y_ORDEN = -0.2
TAM_ORDEN = 17


def _curva(inicio, fin, angulo=ANGULO):
    """La flecha de un viaje, como un arco."""
    return CurvedArrow(
        np.array(inicio, dtype=float), np.array(fin, dtype=float),
        angle=angulo, color=OK, stroke_width=4, tip_length=0.24,
    )


def _repo(centro, color=RAMA_MAIN):
    """Una cadena de tres commits con su rama, del tamaño de un cajetín."""
    x, y = centro
    nodos = VGroup(*[
        nodo_commit(h, color, RADIO, TAM_HASH).move_to([x + dx, y, 0])
        for dx, h in zip(DX_NODOS, HASHES)
    ])
    hilos = VGroup(*[
        arista(nodos[i], nodos[i + 1], color, RADIO)
        for i in range(len(nodos) - 1)
    ])
    rama = texto("main", TAM_RAMA, color=color)
    rama.next_to(nodos[-1], DOWN, buff=0.2)
    return VGroup(hilos, nodos, rama)


def _maquina(indice):
    """La ventana de un ordenador, con su nombre en la barra de título."""
    marco = ventana(ANCHO_MAQUINA, ALTO_MAQUINA, MAQUINAS[indice], 14)
    return marco.move_to([X_MAQUINA[indice], Y_MAQUINA, 0])


def construir(scene):
    encabezado = hacer_titulo(TITULO)

    # ---------------------- Las tres piezas --------------------------------
    logo = imagen_circular("github.jpg", diametro=DIAMETRO_LOGO,
                           ocupacion=OCUPACION_LOGO)
    logo.move_to([X_LOGO, Y_REMOTO, 0])
    caja_remoto = RoundedRectangle(
        width=ANCHO_REMOTO, height=ALTO_REMOTO, corner_radius=0.16,
        stroke_color=SECUNDARIO, stroke_width=3,
    ).set_fill(SUPERFICIE, opacity=1.0).move_to([0, Y_REMOTO, 0])
    rotulo_remoto = texto(NOMBRE_REMOTO, 14, color=SECUNDARIO)
    rotulo_remoto.next_to(caja_remoto, LEFT, buff=0.25)

    maquinas = VGroup(_maquina(0), _maquina(1))
    mio = _repo((X_MAQUINA[0], Y_CADENA_MAQUINA))

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(FadeIn(logo, shift=DOWN * 0.15), run_time=0.7)
    scene.play(Create(caja_remoto), FadeIn(rotulo_remoto, shift=RIGHT * 0.1),
               run_time=0.6)
    scene.play(
        LaggedStart(*[FadeIn(m, shift=UP * 0.15) for m in maquinas],
                    lag_ratio=0.3),
        run_time=0.9,
    )
    # Solo tu portátil tiene algo: el remoto está recién creado y vacío, y
    # Carmen todavía no sabe que esto existe.
    scene.play(
        LaggedStart(*[GrowFromCenter(n) for n in mio[1]], lag_ratio=0.25),
        run_time=0.8,
    )
    scene.play(Create(mio[0]), FadeIn(mio[2], shift=UP * 0.1), run_time=0.6)
    scene.next_slide()

    # ---------------------- push: sube una copia ---------------------------
    orden_push = texto("git push", TAM_ORDEN, color=CLARO)
    orden_push.move_to([X_ORDEN[0], Y_ORDEN, 0])
    subida = _curva(SALIDA_PUSH, LLEGADA_PUSH)

    scene.play(FadeIn(orden_push, shift=UP * 0.1), run_time=0.45)
    scene.play(Create(subida), run_time=0.6)
    scene.play(pulso(subida, OK, run_time=0.9, ancho=9), run_time=0.9)

    remoto = _repo((0, Y_REMOTO + 0.15))
    scene.play(
        LaggedStart(*[GrowFromCenter(n) for n in remoto[1]], lag_ratio=0.2),
        run_time=0.8,
    )
    scene.play(Create(remoto[0]), FadeIn(remoto[2], shift=UP * 0.1),
               run_time=0.5)
    scene.next_slide()

    # ---------------------- clone: y otra copia más ------------------------
    orden_clone = texto("git clone", TAM_ORDEN, color=CLARO)
    orden_clone.move_to([X_ORDEN[1], Y_ORDEN, 0])
    bajada = _curva(SALIDA_CLONE, LLEGADA_CLONE)

    scene.play(FadeIn(orden_clone, shift=UP * 0.1), run_time=0.45)
    scene.play(Create(bajada), run_time=0.6)
    scene.play(pulso(bajada, OK, run_time=0.9, ancho=9), run_time=0.9)

    suyo = _repo((X_MAQUINA[1], Y_CADENA_MAQUINA))
    scene.play(
        LaggedStart(*[GrowFromCenter(n) for n in suyo[1]], lag_ratio=0.2),
        run_time=0.8,
    )
    scene.play(Create(suyo[0]), FadeIn(suyo[2], shift=UP * 0.1), run_time=0.5)

    # Tres copias completas del mismo historial: eso es "distribuido". Un
    # pulso corto y las tres a la vez, que es lo que hay que mirar.
    scene.play(
        *[Indicate(r[1], color=OK, scale_factor=1.08)
          for r in (mio, remoto, suyo)],
        run_time=0.9,
    )
    scene.wait(0.3)

    scene.next_slide()
