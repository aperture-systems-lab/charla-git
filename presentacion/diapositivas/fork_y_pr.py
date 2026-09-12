"""Diapositiva 23 — fork y pull request: contribuir a algo que no es tuyo.

Continúa el decorado de ``local_remoto`` —el logo de GitHub, los repos dibujados
como cadenas de commits dentro de un cajetín, los viajes en arco— pero con una
diferencia que es justo la idea de la diapositiva: arriba no hay **un** remoto,
hay **dos cuentas**.

    semillero/proyecto  --Fork-->  ana/proyecto        (las dos en github.com)
                                        |  ^
                                    clone  push
                                        v  |
                                    tu portátil

El eje de lectura es vertical: la columna de la derecha es tuya (tu fork y tu
portátil, conectados por ``clone`` y ``push``) y la de la izquierda es de otra
persona. Al lado izquierdo no le sale ninguna máquina a propósito: ahí no
tienes nada que hacer, y el hueco lo llena la leyenda de las tres copias.

Lo que hay que ver, y es lo único: **el fork no baja a tu ordenador, cruza de
cuenta a cuenta sin salir de la web**. Es un ``clone`` que hace GitHub para
dejarte una copia donde sí tienes permiso de escritura —los mismos commits, los
mismos hashes, otro dueño—. De ahí sale todo lo demás: clonas tu copia y no el
original, empujas a tu copia sin pedirle permiso a nadie, y lo que cruza de
vuelta no es un ``push`` sino un pull request, que no es un comando de git sino
una conversación abierta en la web.
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
from componentes import arista, avatar, imagen_circular, nodo_commit, texto
from componentes import ventana
from componentes import titulo as hacer_titulo
from estilo import (
    AMBAR,
    CLARO,
    OK,
    RAMA_FEATURE,
    RAMA_MAIN,
    SUPERFICIE,
)

TITULO = "fork y pull request"

# --- Arriba: las dos cuentas, con el logo de GitHub en medio ----------------
# El logo va centrado entre las dos cajas y no encima de una: las dos cuentas
# están en el mismo sitio, y eso es lo que hace que un fork no sea una descarga.
X_CUENTA = (-4.25, 4.25)
Y_CUENTA = 1.40
ANCHO_CUENTA = 4.7
ALTO_CUENTA = 1.5
Y_CABECERA = 2.50
CUENTAS = (
    ("S", "semillero/proyecto", RAMA_MAIN),
    ("A", "ana/proyecto", RAMA_FEATURE),
)
RADIO_AVATAR = 0.26
DIAMETRO_LOGO = 1.05
# El logo es cuadrado y el disco lo recorta en redondo: sin bajar la ocupación
# por debajo de 0.71 (un cuadrado inscrito en su círculo) le corta la palabra.
OCUPACION_LOGO = 0.7

# --- Abajo, en la columna de la derecha: tu portátil ------------------------
# El borde de abajo del portátil y el de la última caja de la izquierda caen a
# la misma altura: las dos columnas de abajo se apoyan en la misma línea. Y esa
# línea no baja de -2.88 porque el indicador de avance ocupa la esquina de
# abajo a la derecha, justo donde llega el portátil.
Y_SUELO = -2.88
ANCHO_MAQUINA = ANCHO_CUENTA
ALTO_MAQUINA = 2.05
Y_MAQUINA = Y_SUELO + ALTO_MAQUINA / 2
MAQUINA = "tu portátil"

# --- Los repos, del tamaño de un cajetín -----------------------------------
HASHES = ("0e5f", "77ab", "9c1d")
HASH_APORTE = "b412"
RAMA = "mi-aporte"
# La cadena nace centrada en su cajetín —tres commits y ni un hueco raro— y
# cuando llega el cuarto se corre media casilla a la izquierda para hacerle
# sitio. Reservar el hueco desde el principio dejaba las cajas cojas durante
# media diapositiva.
DX_NODOS = (-1.15, 0.0, 1.15)
DESPLAZAMIENTO = 0.575
DX_APORTE = 1.725
RADIO = 0.30
TAM_HASH = 13
TAM_RAMA = 14
BUFF_RAMA = 0.20
Y_CADENA_CUENTA = Y_CUENTA + 0.12
Y_CADENA_MAQUINA = -1.93

# --- Los viajes -------------------------------------------------------------
# Las dos travesías entre cuentas van por el centro, una por encima del logo y
# otra por debajo, y las dos con ángulo negativo: en un arco de manim el signo
# negativo abomba hacia la izquierda del sentido de la marcha, así que la de ida
# (a la derecha) sale por arriba y la de vuelta (a la izquierda) por abajo.
Y_FORK = 1.85
Y_PR = 0.95
X_TRAVESIA = 1.85
ANGULO_TRAVESIA = -PI / 5

# El clone y el push comparten los dos la columna derecha, así que van en
# paralelo y con el mismo ángulo positivo: al ir en sentidos contrarios, el
# mismo signo los abomba hacia lados opuestos y no se pisan.
X_CLONE, X_PUSH = 3.25, 5.25
Y_ARRIBA_VERTICAL = 0.52
Y_ABAJO_VERTICAL = -0.76
ANGULO_VERTICAL = PI / 4
X_ORDEN = (2.30, 6.10)
Y_ORDEN = -0.12
TAM_ORDEN = 15

# --- Los tres nombres, en el hueco de la izquierda --------------------------
# Sin explicación al lado: los tres nombres a secas, cada uno con el color de
# su pieza, para que se puedan señalar mientras se cuenta. Van apilados en la
# columna del original, así que el hueco de la izquierda deja de estar vacío
# sin competir con el diagrama.
LEYENDA = (
    ("upstream", RAMA_MAIN),
    ("origin", RAMA_FEATURE),
    ("local", OK),
)
X_LEYENDA = -4.25
ANCHO_LEYENDA = 3.2
ALTO_LEYENDA = 0.8
PASO_LEYENDA = 0.95
# La última se apoya en el mismo suelo que el portátil, y las otras dos suben
# desde ahí: la columna de la izquierda y la de la derecha acaban a la vez.
Y_LEYENDA = tuple(Y_SUELO + ALTO_LEYENDA / 2 + PASO_LEYENDA * i
                  for i in (2, 1, 0))
TAM_LEYENDA = 26


def _curva(inicio, fin, angulo, color=OK):
    """Un viaje, dibujado como un arco."""
    return CurvedArrow(
        np.array(inicio, dtype=float), np.array(fin, dtype=float),
        angle=angulo, color=color, stroke_width=4, tip_length=0.24,
    )


def _cuenta(indice):
    """Una cuenta de GitHub: su cajetín y, encima, el avatar con el nombre."""
    inicial, nombre, color = CUENTAS[indice]
    x = X_CUENTA[indice]
    caja = RoundedRectangle(
        width=ANCHO_CUENTA, height=ALTO_CUENTA, corner_radius=0.16,
        stroke_color=color, stroke_width=3,
    ).set_fill(SUPERFICIE, opacity=1.0).move_to([x, Y_CUENTA, 0])
    cabecera = VGroup(
        avatar(inicial, radio=RADIO_AVATAR, color=color),
        texto(nombre, 16, color=color),
    ).arrange(RIGHT, buff=0.18).move_to([x, Y_CABECERA, 0])
    return VGroup(caja, cabecera)


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
    rama.next_to(nodos[-1], DOWN, buff=BUFF_RAMA)
    return VGroup(hilos, nodos, rama)


def _aporte(repo, x, y, rotulo=None):
    """Tu commit: un nodo morado colgado del último de la cadena.

    Con ``rotulo`` lleva encima el nombre de la rama; sin él, no. En el original
    el commit acaba entrando en ``main``, así que allí no se dibuja la pegatina
    de tu rama: lo que se mueve es la de ellos.
    """
    nodo = nodo_commit(HASH_APORTE, RAMA_FEATURE, RADIO, TAM_HASH)
    nodo.move_to([x + DX_APORTE, y, 0])
    piezas = VGroup(arista(repo[1][-1], nodo, RAMA_FEATURE, RADIO), nodo)
    if rotulo:
        etiqueta = texto(rotulo, TAM_RAMA, color=RAMA_FEATURE)
        piezas.add(etiqueta.next_to(nodo, DOWN, buff=BUFF_RAMA))
    return piezas


def _fila_leyenda(indice):
    """Uno de los tres nombres, centrado en su caja."""
    nombre, color = LEYENDA[indice]
    caja = RoundedRectangle(
        width=ANCHO_LEYENDA, height=ALTO_LEYENDA, corner_radius=0.16,
        stroke_color=color, stroke_width=3,
    ).set_fill(SUPERFICIE, opacity=1.0).move_to([X_LEYENDA, Y_LEYENDA[indice], 0])
    return VGroup(caja, texto(nombre, TAM_LEYENDA, color=color).move_to(caja))


def _hacer_sitio(scene, repo):
    """Corre la cadena a la izquierda para que quepa el commit que llega."""
    scene.play(repo.animate.shift(LEFT * DESPLAZAMIENTO), run_time=0.45)


def _entrar_cadena(scene, repo):
    """Estrena una cadena: los commits uno a uno y luego los hilos y la rama."""
    scene.play(
        LaggedStart(*[GrowFromCenter(n) for n in repo[1]], lag_ratio=0.25),
        run_time=0.8,
    )
    scene.play(Create(repo[0]), FadeIn(repo[2], shift=UP * 0.1), run_time=0.6)


def construir(scene):
    encabezado = hacer_titulo(TITULO)

    # ---------------------- Paso 1: el original, en otra cuenta ------------
    logo = imagen_circular("github.jpg", diametro=DIAMETRO_LOGO,
                           ocupacion=OCUPACION_LOGO)
    logo.move_to([0, Y_CUENTA, 0])

    upstream = _cuenta(0)
    repo_upstream = _repo((X_CUENTA[0], Y_CADENA_CUENTA))

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(FadeIn(logo, shift=DOWN * 0.15), run_time=0.7)
    scene.play(Create(upstream[0]), FadeIn(upstream[1], shift=DOWN * 0.1),
               run_time=0.7)
    _entrar_cadena(scene, repo_upstream)
    scene.play(FadeIn(_fila_leyenda(0), shift=RIGHT * 0.15), run_time=0.5)
    scene.next_slide()

    # ---------------------- Paso 2: el fork cruza de cuenta a cuenta -------
    fork = _cuenta(1)
    repo_fork = _repo((X_CUENTA[1], Y_CADENA_CUENTA))
    viaje_fork = _curva([-X_TRAVESIA, Y_FORK, 0], [X_TRAVESIA, Y_FORK, 0],
                        ANGULO_TRAVESIA, RAMA_FEATURE)
    rotulo_fork = texto("Fork", 16, color=RAMA_FEATURE)
    rotulo_fork.next_to(viaje_fork, UP, buff=0.14)

    scene.play(Create(viaje_fork), FadeIn(rotulo_fork, shift=UP * 0.1),
               run_time=0.7)
    scene.play(pulso(viaje_fork, CLARO, run_time=0.9, ancho=9), run_time=0.9)
    # La caja aparece con el viaje, no antes: el repositorio en tu cuenta no
    # existía hasta que pulsaste el botón.
    scene.play(Create(fork[0]), FadeIn(fork[1], shift=DOWN * 0.1), run_time=0.7)
    _entrar_cadena(scene, repo_fork)
    scene.play(FadeIn(_fila_leyenda(1), shift=RIGHT * 0.15), run_time=0.5)
    # Los mismos hashes en las dos cuentas: eso es que sea una copia y no un
    # proyecto nuevo que se le parece.
    scene.play(
        *[Indicate(r[1], color=OK, scale_factor=1.08)
          for r in (repo_upstream, repo_fork)],
        run_time=0.9,
    )
    scene.next_slide()

    # ---------------------- Paso 3: clone, y a trabajar en una rama --------
    maquina = ventana(ANCHO_MAQUINA, ALTO_MAQUINA, MAQUINA, 14)
    maquina.move_to([X_CUENTA[1], Y_MAQUINA, 0])
    repo_local = _repo((X_CUENTA[1], Y_CADENA_MAQUINA))
    bajada = _curva([X_CLONE, Y_ARRIBA_VERTICAL, 0],
                    [X_CLONE, Y_ABAJO_VERTICAL, 0], ANGULO_VERTICAL)
    orden_clone = texto("git clone", TAM_ORDEN, color=CLARO)
    orden_clone.move_to([X_ORDEN[0], Y_ORDEN, 0])

    scene.play(FadeIn(maquina, shift=UP * 0.15), run_time=0.7)
    scene.play(FadeIn(_fila_leyenda(2), shift=RIGHT * 0.15), run_time=0.5)
    scene.play(FadeIn(orden_clone, shift=UP * 0.1), Create(bajada), run_time=0.7)
    scene.play(pulso(bajada, OK, run_time=0.9, ancho=9), run_time=0.9)
    _entrar_cadena(scene, repo_local)

    _hacer_sitio(scene, repo_local)
    aporte_local = _aporte(repo_local, X_CUENTA[1], Y_CADENA_MAQUINA, RAMA)
    scene.play(GrowFromCenter(aporte_local[1]), run_time=0.5)
    scene.play(Create(aporte_local[0]), FadeIn(aporte_local[2], shift=UP * 0.1),
               run_time=0.5)
    scene.next_slide()

    # ---------------------- Paso 4: push, a TU cuenta ----------------------
    subida = _curva([X_PUSH, Y_ABAJO_VERTICAL, 0],
                    [X_PUSH, Y_ARRIBA_VERTICAL, 0], ANGULO_VERTICAL)
    orden_push = texto("git push", TAM_ORDEN, color=CLARO)
    orden_push.move_to([X_ORDEN[1], Y_ORDEN, 0])

    scene.play(FadeIn(orden_push, shift=UP * 0.1), Create(subida), run_time=0.7)
    scene.play(pulso(subida, OK, run_time=0.9, ancho=9), run_time=0.9)

    _hacer_sitio(scene, repo_fork)
    aporte_fork = _aporte(repo_fork, X_CUENTA[1], Y_CADENA_CUENTA, RAMA)
    scene.play(GrowFromCenter(aporte_fork[1]), run_time=0.5)
    scene.play(Create(aporte_fork[0]), FadeIn(aporte_fork[2], shift=UP * 0.1),
               run_time=0.5)
    scene.next_slide()

    # ---------------------- Paso 5: el pull request, de vuelta -------------
    viaje_pr = _curva([X_TRAVESIA, Y_PR, 0], [-X_TRAVESIA, Y_PR, 0],
                      ANGULO_TRAVESIA, AMBAR)
    rotulo_pr = texto("Pull Request", 16, color=AMBAR)
    rotulo_pr.next_to(viaje_pr, DOWN, buff=0.14)

    scene.play(Create(viaje_pr), FadeIn(rotulo_pr, shift=DOWN * 0.1),
               run_time=0.7)
    scene.play(pulso(viaje_pr, CLARO, run_time=1.0, ancho=9), run_time=1.0)
    # Lo que cruza es una propuesta, no un push: tu commit sigue en tu cuenta.
    scene.play(Indicate(aporte_fork[1], color=AMBAR, scale_factor=1.12),
               run_time=0.7)
    scene.next_slide()

    # ---------------------- Paso 6: lo aceptan, y entra --------------------
    scene.play(pulso(viaje_pr, OK, run_time=0.8, ancho=9), run_time=0.8)
    _hacer_sitio(scene, repo_upstream)
    aporte_upstream = _aporte(repo_upstream, X_CUENTA[0], Y_CADENA_CUENTA)
    scene.play(GrowFromCenter(aporte_upstream[1]), run_time=0.5)
    # Y su main pasa a apuntar a tu commit: en el original no se dibuja tu rama
    # —esa se queda en tu fork—, lo que se mueve es la pegatina de ellos.
    scene.play(
        Create(aporte_upstream[0]),
        repo_upstream[2].animate.next_to(aporte_upstream[1], DOWN,
                                         buff=BUFF_RAMA),
        run_time=0.7,
    )
    scene.play(
        *[Indicate(n, color=OK, scale_factor=1.15)
          for n in (aporte_local[1], aporte_fork[1], aporte_upstream[1])],
        run_time=1.0,
    )
    scene.wait(0.3)
    scene.next_slide()
