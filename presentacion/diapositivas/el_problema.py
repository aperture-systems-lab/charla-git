"""Diapositiva 2 — el problema que git vino a resolver.

Dos actos bajo el mismo título, porque son la misma historia:

  1. El encargo. La materia pide un proyecto final en equipos de tres, con un
     único entregable. Nada raro: es el semestre de cualquiera.
  2. Cómo se hace en realidad. El proyecto acaba viajando por el chat del
     grupo: a la izquierda el móvil, que enseña la silueta del hilo —largo,
     con adjuntos, y acabando en rojo—; al lado, los mensajes que importan a
     tamaño legible. El móvil dice que aquello es un chat y las burbujas dicen
     lo que pone: ninguna de las dos repite a la otra.

Es la única diapositiva que no explica git: lo vende. Si esta funciona, el
resto de la charla se escucha distinto.
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    FadeIn,
    FadeOut,
    GrowFromCenter,
    LaggedStart,
    VGroup,
)

from animaciones import teclear
from componentes import (
    avatar,
    burbuja,
    globo_mudo,
    telefono,
    terminal,
    texto,
)
from componentes import titulo as hacer_titulo
from estilo import AMBAR, ERROR, SECUNDARIO

TITULO = "Motivación"
Y_ACTO = -0.35           # los dos actos comparten altura de composición

# --- Acto 1: el encargo ----------------------------------------------------
AULA = "aula virtual"
TAREA = (
    ("Proyecto final", "txt"),
    ("", "sep"),
    ("En equipos de 3 personas.", "out"),
    ("Un entregable por equipo.", "out"),
    ("", "sep"),
    ("Entrega: 15 de junio", "avi"),
)
EQUIPO = (("A", "ana"), ("L", "luis"), ("M", "mar"))
X_TAREA = -2.85
X_EQUIPO = 3.5
RADIO_AVATAR = 0.52

# --- Acto 2: cómo se hace en realidad --------------------------------------
# El crescendo está en los nombres: cada uno es un parche sobre el anterior, y
# el color va avisando de que la cosa se está yendo de las manos.
CHAT = (
    ("ana", "proyecto.zip", SECUNDARIO, True),
    ("luis", "proyecto_v2.zip", SECUNDARIO, True),
    ("mar", "proyecto_MIO.zip", AMBAR, True),
    ("ana", "¿cuál es el bueno?", ERROR, False),
)
LADO = (LEFT, RIGHT, LEFT, RIGHT)   # quién escribe a cada lado de la pantalla
CHAT_NOMBRE = "proyecto final"
CHAT_SUB = "ana, luis, mar"

# El hilo tal y como se ve dentro del móvil: solo la forma. Los altos grandes
# son los adjuntos, y el último globo en rojo es la pregunta que nadie contesta.
# (ancho relativo al hueco de la pantalla, alto, color, lado)
HILO = (
    (0.60, 0.30, SECUNDARIO, LEFT),
    (0.52, 0.50, SECUNDARIO, RIGHT),
    (0.44, 0.30, SECUNDARIO, LEFT),
    (0.62, 0.50, SECUNDARIO, RIGHT),
    (0.50, 0.30, SECUNDARIO, LEFT),
    (0.58, 0.50, AMBAR, LEFT),
    (0.54, 0.32, ERROR, RIGHT),
)

ANCHO_MOVIL = 3.5
ALTO_MOVIL = 5.5
X_MOVIL = -3.35
TAM_BURBUJA = 22         # los mensajes legibles, al lado del móvil
MARGEN_BURBUJA = 0.12
# Bordes de la columna de burbujas grandes. Poco más anchos que la burbuja más
# ancha: si se separan más, el zigzag deja de leerse como una conversación y
# pasan a ser cuatro cajas sueltas.
X_COLUMNA = (-0.7, 5.1)


def _equipo():
    """Las tres del equipo: su inicial en un círculo y el nombre debajo.

    Son las mismas tres que escriben en el chat del acto siguiente, así que
    cuando aparezcan las burbujas ya se sabe quién es quién.
    """
    fichas = VGroup(*[
        avatar(inicial, nombre, RADIO_AVATAR) for inicial, nombre in EQUIPO
    ]).arrange(RIGHT, buff=0.5).move_to([X_EQUIPO, Y_ACTO, 0])
    rotulo = texto("el equipo", 15, color=SECUNDARIO)
    return rotulo.next_to(fichas, UP, buff=0.55), fichas


def _hilo_en(lienzo):
    """La silueta del hilo, apoyada abajo dentro de la pantalla del móvil."""
    util = lienzo.width - 2 * MARGEN_BURBUJA
    globos = VGroup(*[
        globo_mudo(util * ancho, alto, color) for ancho, alto, color, _ in HILO
    ]).arrange(DOWN, buff=0.16)
    if globos.height > lienzo.height:
        globos.scale(lienzo.height / globos.height)

    globos.move_to(lienzo).align_to(lienzo, DOWN)
    for globo, (_, _, _, lado) in zip(globos, HILO):
        globo.align_to(lienzo, lado).shift(-lado * MARGEN_BURBUJA)
    return globos


def _conversacion():
    """Los cuatro mensajes que importan, en su columna y con el pico a su lado."""
    izquierdo, derecho = X_COLUMNA
    globos = VGroup(*[
        burbuja(autor, mensaje, color, tam=TAM_BURBUJA, adjunto=adjunto,
                cola=lado)
        for (autor, mensaje, color, adjunto), lado in zip(CHAT, LADO)
    ]).arrange(DOWN, buff=0.32)
    globos.move_to([(izquierdo + derecho) / 2, Y_ACTO, 0])
    for globo, lado in zip(globos, LADO):
        x = derecho if lado[0] > 0 else izquierdo   # lado[0] > 0 es RIGHT
        globo.align_to(np.array([x, 0, 0]), lado)
    return globos


def _chat():
    """El móvil con la forma del hilo dentro, y los mensajes legibles al lado."""
    movil = telefono(ANCHO_MOVIL, ALTO_MOVIL, rotulo=CHAT_NOMBRE, sub=CHAT_SUB)
    movil.move_to([X_MOVIL, Y_ACTO, 0])
    return movil, _hilo_en(movil[1]), _conversacion()


def construir(scene):
    # El título se queda en pantalla en los dos actos: es la misma historia.
    encabezado = hacer_titulo(TITULO)
    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)

    # ---------------------- Acto 1: el encargo -----------------------------
    tarea = terminal(TAREA, tam=20, nombre=AULA)
    tarea.move_to([X_TAREA, Y_ACTO, 0])
    rotulo_equipo, avatares = _equipo()

    scene.play(FadeIn(tarea[0]), run_time=0.6)   # la ventana, todavía vacía
    teclear(scene, tarea, ritmo=0.42)            # y el enunciado, línea a línea
    scene.play(FadeIn(rotulo_equipo), run_time=0.35)
    scene.play(
        LaggedStart(*[GrowFromCenter(f) for f in avatares], lag_ratio=0.25),
        run_time=0.9,
    )
    scene.next_slide()

    # ---------------------- Acto 2: y esto es lo que pasa ------------------
    movil, hilo, al_lado = _chat()

    scene.play(FadeOut(tarea), FadeOut(rotulo_equipo), FadeOut(avatares),
               run_time=0.7)
    scene.play(FadeIn(movil, shift=UP * 0.15), run_time=0.7)
    scene.play(
        LaggedStart(*[FadeIn(g, shift=UP * 0.1) for g in hilo], lag_ratio=0.18),
        run_time=1.0,
    )
    for globo in al_lado:
        scene.play(FadeIn(globo, shift=RIGHT * 0.18, scale=0.95), run_time=0.45)
    scene.wait(0.3)

    scene.next_slide()
