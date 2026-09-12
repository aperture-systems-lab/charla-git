"""Diapositiva 22c — ``git clone``: el camino contrario.

Las dos anteriores van de abajo arriba: tenías una carpeta y la subiste. Esta
va de arriba abajo, y es con diferencia la más frecuente: el repositorio ya
existe —el de la asignatura, el del semillero, el de una librería— y lo que
quieres es tenerlo.

Lo que hay que ver: ``clone`` **no es descargar un zip**. Hace de un tirón lo
que en las dos diapositivas anteriores costó dos comandos, y crea la carpeta
de paso: baja el proyecto con todo su historial —los commits de los demás, con
sus mensajes y sus fechas— y deja el remoto ya apuntado como ``origin``. Por
eso los tres vistos de abajo, que son justo las tres cosas que uno ya no tiene
que hacer.

De ahí el error clásico de la primera clase: entrar en la carpeta recién
clonada y teclear ``git init``. No hace falta. Ya es un repositorio.
"""

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    FadeIn,
    LaggedStart,
    VGroup,
)

from animaciones import teclear
from componentes import terminal, texto, visto
from componentes import titulo as hacer_titulo
from estilo import CLARO, OK, RAMA_MAIN, SECUNDARIO

TITULO = "git clone"

SESION = (
    ("git clone git@github.com:ana/repo.git", "cmd"),
    ("Cloning into 'repo'...", "out"),
    ("remote: Enumerating objects: 128, done.", "out"),
    ("Receiving objects: 100% (128/128), done.", "out"),
)
TAM_SESION = 14
POS_SESION = [-3.55, 0.75, 0]

# (línea, tamaño, color). Dos bloques separados: para qué sirve clone y, en
# gris, el camino de las dos diapositivas anteriores.
MOTIVO = (
    ("clone es para empezar", 21, RAMA_MAIN),
    ("cuando el repositorio ya existe", 17, CLARO),
    ("y tú aún no lo tienes", 17, CLARO),
)
CONTRARIO = (
    ("init + remote add es para", 17, SECUNDARIO),
    ("el camino contrario", 17, SECUNDARIO),
)
X_CUANDO = -0.55
Y_CUANDO = 0.85
BUFF_LINEA = 0.3
BUFF_BLOQUE = 0.62

TRAE = ("la carpeta, ya creada", "todo el historial", "origin ya enlazado")
Y_TRAE = -2.05
BUFF_TRAE = 0.75
TAM_TRAE = 17

REMATE = "no hace falta git init: lo que clonas ya es un repositorio"


def _bloque(lineas):
    """Un bloque de la columna derecha, alineado a la izquierda."""
    return VGroup(*[
        texto(linea, tam, color=color) for linea, tam, color in lineas
    ]).arrange(DOWN, buff=BUFF_LINEA, aligned_edge=LEFT)


def _traido(que):
    """Uno de los tres vistos de abajo: la marca y lo que trae."""
    marca = visto(OK, 0.13)
    return VGroup(marca, texto(que, TAM_TRAE, color=CLARO)).arrange(
        RIGHT, buff=0.24)


def construir(scene):
    encabezado = hacer_titulo(TITULO)
    consola = terminal(SESION, tam=TAM_SESION).move_to(POS_SESION)

    motivo, contrario = _bloque(MOTIVO), _bloque(CONTRARIO)
    cuando = VGroup(motivo, contrario).arrange(
        DOWN, buff=BUFF_BLOQUE, aligned_edge=LEFT)
    cuando.move_to([X_CUANDO, Y_CUANDO, 0], LEFT)

    trae = VGroup(*[_traido(t) for t in TRAE])
    trae.arrange(RIGHT, buff=BUFF_TRAE).move_to([0, Y_TRAE, 0])

    remate = texto(REMATE, 15, color=SECUNDARIO).to_edge(DOWN, buff=0.62)

    # ------------------------------ montaje --------------------------------
    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(FadeIn(consola[0]), run_time=0.5)
    teclear(scene, consola, ritmo=0.3)
    scene.play(
        LaggedStart(*[FadeIn(t, shift=RIGHT * 0.12)
                      for t in (*motivo, *contrario)],
                    lag_ratio=0.25),
        run_time=1.4,
    )
    scene.play(
        LaggedStart(*[FadeIn(t, shift=UP * 0.12) for t in trae],
                    lag_ratio=0.35),
        run_time=1.1,
    )
    scene.play(FadeIn(remate), run_time=0.45)
    scene.wait(0.3)

    scene.next_slide()
