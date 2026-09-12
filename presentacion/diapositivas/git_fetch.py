"""Diapositiva 22d — ``git fetch``: mirar sin tocar.

El viaje de vuelta, en su versión prudente. Y la diapositiva existe por una
palabra que aparece aquí por primera vez y que confunde a todo el mundo:
``origin/main``.

``origin/main`` **no es la rama del servidor**: es tu copia local de cómo
estaba la rama del servidor la última vez que preguntaste. Vive en tu carpeta,
igual que ``main``, y solo se mueve cuando tú hablas con el remoto. Eso es
exactamente lo que hace ``fetch``, y no hace nada más: baja los commits nuevos
y adelanta ese puntero.

Por eso el dibujo tiene los commits en dos colores y **dos punteros**: en cian
lo que ya tenías, con ``main`` donde lo dejaste, y en verde lo que acaba de
bajar, con ``origin/main`` al final. Tu rama no se ha movido, tus archivos
tampoco: hay dos historias en la misma carpeta, todavía sin juntar.

De ahí el remate, que es la razón de enseñar ``fetch`` antes que ``pull``:
como no toca tu directorio de trabajo, no puede dar conflicto. Es el comando
que se teclea cuando no sabes qué te vas a encontrar.
"""

from manim import (
    DOWN,
    RIGHT,
    UP,
    Create,
    FadeIn,
    GrowFromCenter,
    LaggedStart,
    VGroup,
)

from animaciones import teclear
from componentes import arista, nodo_commit, puntero, terminal, texto
from componentes import titulo as hacer_titulo
from estilo import CLARO, OK, RAMA_MAIN, SECUNDARIO

TITULO = "git fetch"

SESION = (
    ("git fetch", "cmd"),
    ("From github.com:ana/repo", "out"),
    ("  9c1d..77ab  main -> origin/main", "out"),
    ("", "sep"),
    ("git log origin/main --oneline", "cmd"),
    ("77ab  feat: exporta el informe", "out"),
)
TAM_SESION = 14
POS_SESION = [-4.05, 0.6, 0]
CORTE_SESION = 3                  # hasta aquí se teclea antes de bajar nada

# --- El grafo: lo que ya tenías y lo que baja ------------------------------
MIOS = ("0e5f", "3a71", "9c1d")
NUEVOS = ("b204", "77ab")
X_GRAFO = 2.05
Y_GRAFO = 1.3
PASO_NODO = 1.05
RADIO = 0.28
TAM_HASH = 13

BAJADA_PUNTERO = 0.78
TAM_PUNTERO = 15
SUBIDA_ROTULO = 0.75
TAM_ROTULO = 14
ROTULOS = (                       # (texto, x, color)
    ("ya lo tenías", 0.85, RAMA_MAIN),
    ("esto lo trajo fetch", 3.8, OK),
)

CIERRE = (
    ("origin/main es tu copia local de cómo está el servidor", CLARO),
    ("tu rama main y tus archivos se quedan donde estaban", SECUNDARIO),
)
Y_CIERRE = -2.35
BUFF_CIERRE = 0.28
TAM_CIERRE = 17

REMATE = "por eso fetch nunca da conflicto: mira, no toca"


def _nodo(indice, etiqueta, color):
    """Un commit del grafo, colocado por su posición en la fila."""
    x = X_GRAFO + (indice - 2) * PASO_NODO
    return nodo_commit(etiqueta, color, RADIO, TAM_HASH).move_to([x, Y_GRAFO, 0])


def construir(scene):
    encabezado = hacer_titulo(TITULO)
    consola = terminal(SESION, tam=TAM_SESION).move_to(POS_SESION)

    # --- lo que ya tenías: tres commits y tu rama --------------------------
    mios = VGroup(*[_nodo(i, h, RAMA_MAIN) for i, h in enumerate(MIOS)])
    hilos_mios = VGroup(*[
        arista(mios[i], mios[i + 1], RAMA_MAIN, RADIO)
        for i in range(len(mios) - 1)
    ])
    rama = puntero("main", RAMA_MAIN, TAM_PUNTERO)
    rama.move_to([mios[-1].get_center()[0], Y_GRAFO - BAJADA_PUNTERO, 0])

    # --- lo que baja con fetch: dos commits más y origin/main --------------
    nuevos = VGroup(*[
        _nodo(len(MIOS) + i, h, OK) for i, h in enumerate(NUEVOS)
    ])
    hilos_nuevos = VGroup(
        arista(mios[-1], nuevos[0], OK, RADIO),
        arista(nuevos[0], nuevos[1], OK, RADIO),
    )
    seguimiento = puntero("origin/main", OK, TAM_PUNTERO)
    seguimiento.move_to([nuevos[-1].get_center()[0],
                         Y_GRAFO - BAJADA_PUNTERO, 0])

    rotulos = VGroup(*[
        texto(t, TAM_ROTULO, color=color).move_to(
            [x, Y_GRAFO + SUBIDA_ROTULO, 0])
        for t, x, color in ROTULOS
    ])

    cierre = VGroup(*[
        texto(t, TAM_CIERRE, color=color) for t, color in CIERRE
    ]).arrange(DOWN, buff=BUFF_CIERRE).move_to([0, Y_CIERRE, 0])
    remate = texto(REMATE, 15, color=OK).to_edge(DOWN, buff=0.62)

    # ------------------------------ montaje --------------------------------
    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)

    # Primero el estado de partida: sin esto, lo que baja después no se lee.
    scene.play(
        LaggedStart(*[GrowFromCenter(n) for n in mios], lag_ratio=0.25),
        run_time=0.8,
    )
    scene.play(Create(hilos_mios), FadeIn(rama, shift=UP * 0.1), run_time=0.6)
    scene.play(FadeIn(rotulos[0], shift=DOWN * 0.1), run_time=0.4)

    scene.play(FadeIn(consola[0]), run_time=0.5)
    teclear(scene, consola, hasta=CORTE_SESION, ritmo=0.32)

    scene.play(
        LaggedStart(*[GrowFromCenter(n) for n in nuevos], lag_ratio=0.25),
        run_time=0.8,
    )
    scene.play(Create(hilos_nuevos), FadeIn(seguimiento, shift=UP * 0.1),
               run_time=0.6)
    scene.play(FadeIn(rotulos[1], shift=DOWN * 0.1), run_time=0.4)

    # Y ya se puede leer lo que bajó, sin haber tocado nada de lo tuyo.
    teclear(scene, consola, desde=CORTE_SESION, ritmo=0.32)
    scene.play(
        LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in cierre],
                    lag_ratio=0.3),
        run_time=1.0,
    )
    scene.play(FadeIn(remate), run_time=0.45)
    scene.wait(0.3)

    scene.next_slide()
