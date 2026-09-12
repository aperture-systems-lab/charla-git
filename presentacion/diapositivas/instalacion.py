"""Diapositiva 7 — instalar git.

Los tres pantallazos que vas a ver de verdad al instalarlo, en fila y en orden:
el navegador en ``git-scm.com/install``, el instalador de siguiente-siguiente
y la terminal contestando una versión. Ni una frase: si los tres se reconocen
de un vistazo, ya está contada.

El color hace de barra de progreso de la propia diapositiva —cian lo que
empiezas, ámbar lo que está a medias, verde lo que ya funciona— y las tres
tarjetas comparten rejilla: mismo tamaño, misma altura de contenido y la
píldora de color a la misma cota en las tres.
"""

from manim import (
    BOLD,
    DOWN,
    LEFT,
    RIGHT,
    Create,
    FadeIn,
    GrowFromCenter,
    GrowFromEdge,
    LaggedStart,
    Line,
    VGroup,
)

from animaciones import teclear
from componentes import (
    ALTO_BARRA,
    barra,
    descarga,
    linea_terminal,
    nodo_commit,
    tarjeta,
    texto,
    ventana,
)
from componentes import titulo as hacer_titulo
from estilo import AMBAR, OK, PRIMARIO, SECUNDARIO

# --- Las tres columnas -----------------------------------------------------
# (número, rótulo, color, título de la ventana)
PASOS = (
    ("1", "Descargar", PRIMARIO, "git-scm.com/install"),
    ("2", "Instalar", AMBAR, "Instalador"),
    ("3", "Comprobar", OK, "terminal"),
)

COMPROBACION = (
    ("git --version", "cmd"),
    ("git version 2.51.0", "ok"),
)

# --- Rejilla ---------------------------------------------------------------
ANCHO, ALTO = 3.7, 3.5    # las tres tarjetas miden lo mismo
X_COLUMNAS = (-4.6, 0.0, 4.6)
Y_CENTRO = -0.72          # eje de las tarjetas
Y_PASO = 1.45             # fila de cabeceras, encima
X_CHEVRON = (-2.3, 2.3)   # los dos huecos entre tarjetas

MARGEN = 0.40             # aire entre el borde de la ventana y su contenido
Y_CONTENIDO = 0.32        # el dibujo de cada tarjeta, respecto a su centro
Y_PILDORA = -1.00         # y la píldora de color: misma cota en las tres
TAM_CONSOLA = 19


def _paso(numero, rotulo, color, x):
    """Cabecera de una columna: el número del paso y qué se hace en él."""
    marcador = nodo_commit(numero, color, 0.28, 19)
    etiqueta = texto(rotulo, 20, color=color)
    fila = VGroup(marcador, etiqueta).arrange(RIGHT, buff=0.26)
    return fila.move_to([x, Y_PASO, 0])


def _chevron(x, color=SECUNDARIO):
    """El ``>`` que encadena una tarjeta con la siguiente.

    Una flecha en un hueco de nueve milímetros sale con la punta ridícula; dos
    líneas dan el mismo "y luego" y pesan menos.
    """
    p, alto, ancho = [x, Y_CENTRO, 0], 0.22, 0.13
    return VGroup(
        Line([x - ancho, Y_CENTRO + alto, 0], p, color=color, stroke_width=5),
        Line(p, [x - ancho, Y_CENTRO - alto, 0], color=color, stroke_width=5),
    )


def _pildora(contenido, color, x):
    """El botón (o el sello) de una tarjeta, a la misma altura en las tres."""
    return tarjeta([(contenido, 15, BOLD)], color=color).move_to(
        [x, Y_CENTRO + Y_PILDORA, 0]
    )


def _renglones_falsos(x, y):
    """Las dos líneas grises del cuadro de diálogo: texto que no hay que leer.

    Un instalador es un párrafo de licencia y un botón; el párrafo aquí solo
    tiene que ocupar su sitio, así que se dibuja y no se escribe.
    """
    lineas = VGroup(
        barra(2.5, 0.13, SECUNDARIO, 0.25),
        barra(1.6, 0.13, SECUNDARIO, 0.25),
    ).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
    return lineas.move_to([x - (ANCHO / 2 - MARGEN), y, 0], LEFT)


def construir(scene):
    encabezado = hacer_titulo("Instalación")

    cabeceras = VGroup(*[
        _paso(n, rotulo, color, x)
        for (n, rotulo, color, _), x in zip(PASOS, X_COLUMNAS)
    ])
    tarjetas = VGroup(*[
        ventana(ANCHO, ALTO, nombre, 14, color=color).move_to([x, Y_CENTRO, 0])
        for (_, _, color, nombre), x in zip(PASOS, X_COLUMNAS)
    ])
    chevrones = VGroup(*[_chevron(x) for x in X_CHEVRON])

    # --- 1. el navegador: el icono de descargar y su botón ------------------
    icono = descarga(1.15).move_to([X_COLUMNAS[0], Y_CENTRO + Y_CONTENIDO, 0])
    descargar = _pildora("Descargar", PRIMARIO, X_COLUMNAS[0])

    # --- 2. el instalador: párrafo mudo, progreso y el botón de siempre -----
    renglones = _renglones_falsos(X_COLUMNAS[1], Y_CENTRO + Y_CONTENIDO + 0.42)
    pista = barra(2.6, 0.22, SECUNDARIO, 0.22)
    pista.move_to([X_COLUMNAS[1], Y_CENTRO + Y_CONTENIDO - 0.45, 0])
    progreso = barra(2.6 * 0.62, 0.22, AMBAR).move_to(pista.get_left(), LEFT)
    siguiente = _pildora("Siguiente", AMBAR, X_COLUMNAS[1])

    # --- 3. la terminal: la pregunta, la respuesta y el sello ---------------
    filas = VGroup(*[
        linea_terminal(c, t, TAM_CONSOLA) for c, t in COMPROBACION
    ]).arrange(DOWN, buff=0.26, aligned_edge=LEFT)
    filas.move_to([X_COLUMNAS[2], Y_CENTRO + Y_CONTENIDO, 0])
    filas.align_to(tarjetas[2][0].get_left() + RIGHT * MARGEN, LEFT)
    consola = VGroup(tarjetas[2], filas)   # la forma que espera ``teclear``
    sello = _pildora("Instalado", OK, X_COLUMNAS[2])

    # ------------------------------ montaje --------------------------------
    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)

    scene.play(
        GrowFromCenter(cabeceras[0][0]),
        FadeIn(cabeceras[0][1], shift=RIGHT * 0.15),
        FadeIn(tarjetas[0]),
        run_time=0.7,
    )
    scene.play(Create(icono), run_time=0.8)
    scene.play(FadeIn(descargar, scale=0.9), run_time=0.5)

    scene.play(
        FadeIn(chevrones[0], shift=RIGHT * 0.15),
        GrowFromCenter(cabeceras[1][0]),
        FadeIn(cabeceras[1][1], shift=RIGHT * 0.15),
        FadeIn(tarjetas[1]),
        run_time=0.7,
    )
    scene.play(
        LaggedStart(*[FadeIn(r) for r in renglones], lag_ratio=0.35),
        FadeIn(pista),
        run_time=0.6,
    )
    scene.play(GrowFromEdge(progreso, LEFT), run_time=0.9)
    scene.play(FadeIn(siguiente, scale=0.9), run_time=0.5)

    scene.play(
        FadeIn(chevrones[1], shift=RIGHT * 0.15),
        GrowFromCenter(cabeceras[2][0]),
        FadeIn(cabeceras[2][1], shift=RIGHT * 0.15),
        FadeIn(tarjetas[2]),
        run_time=0.7,
    )
    teclear(scene, consola, ritmo=0.5)
    scene.play(FadeIn(sello, scale=0.9), run_time=0.5)
    scene.wait(0.4)

    scene.next_slide()
