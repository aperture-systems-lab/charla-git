"""Diapositiva 22a — ``git remote add``: enlazar el repo local con el de GitHub.

Primer comando del tramo remoto, y el único que se teclea una sola vez en la
vida de un repositorio. Hasta aquí todo ha pasado dentro de la carpeta; esta
diapositiva es la que ata esa carpeta a una dirección de internet.

Lo que hay que ver, y es lo único: **origin no es una palabra mágica de git,
es un apodo**. Es el nombre corto que le pones a una dirección larguísima para
no volver a escribirla nunca más. Podría llamarse ``pepe``; se llama ``origin``
porque es la convención, igual que la rama principal se llama ``main``.

Por eso ``git remote -v`` sale después: enseña la libreta de apodos —a la
izquierda el nombre, a la derecha la dirección— y de paso que hay dos líneas,
una para bajar y otra para subir, que en la práctica son la misma.
"""

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    FadeIn,
    VGroup,
)

from animaciones import flecha, teclear
from componentes import puntero, terminal, texto
from componentes import titulo as hacer_titulo
from estilo import CLARO, OK, SECUNDARIO

TITULO = "git remote add"

SESION = (
    ("git remote add origin git@github.com:ana/repo.git", "cmd"),
    ("", "sep"),
    ("git remote -v", "cmd"),
    ("origin  git@github.com:ana/repo.git (fetch)", "out"),
    ("origin  git@github.com:ana/repo.git (push)", "out"),
)
TAM_SESION = 15
Y_SESION = 0.85

# El apodo y lo que hay detrás, que es toda la idea de la diapositiva.
APODO = "origin"
DIRECCION = "git@github.com:ana/repo.git"
TAM_APODO = 21
TAM_DIRECCION = 17
SEPARACION_APODO = 1.15           # hueco para la flecha entre los dos
Y_APODO = -1.75

GLOSA = "origin es solo un apodo: la dirección larga se escribe una vez"
Y_GLOSA = -2.5
REMATE = "la dirección SSH la copias del botón verde del repo en GitHub"


def construir(scene):
    encabezado = hacer_titulo(TITULO)
    consola = terminal(SESION, tam=TAM_SESION).move_to([0, Y_SESION, 0])

    # El apodo a la izquierda, la dirección a la derecha y la flecha entre
    # medias: se monta pegado y se centra después, ya como un bloque.
    etiqueta = puntero(APODO, OK, TAM_APODO)
    direccion = texto(DIRECCION, TAM_DIRECCION, color=SECUNDARIO)
    direccion.next_to(etiqueta, RIGHT, buff=SEPARACION_APODO)
    puente = flecha(
        etiqueta.get_right() + RIGHT * 0.1,
        direccion.get_left() + LEFT * 0.1,
        OK, buff=0.04,
    )
    apodo = VGroup(etiqueta, puente, direccion).move_to([0, Y_APODO, 0])

    glosa = texto(GLOSA, 17, color=CLARO).move_to([0, Y_GLOSA, 0])
    remate = texto(REMATE, 15, color=SECUNDARIO).to_edge(DOWN, buff=0.62)

    # ------------------------------ montaje --------------------------------
    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(FadeIn(consola[0]), run_time=0.5)
    teclear(scene, consola, ritmo=0.32)
    scene.play(FadeIn(etiqueta, shift=RIGHT * 0.12), run_time=0.5)
    scene.play(FadeIn(puente), FadeIn(direccion, shift=RIGHT * 0.12),
               run_time=0.6)
    scene.play(FadeIn(glosa, shift=DOWN * 0.1), run_time=0.5)
    scene.play(FadeIn(remate), run_time=0.45)
    scene.wait(0.3)

    scene.next_slide()
