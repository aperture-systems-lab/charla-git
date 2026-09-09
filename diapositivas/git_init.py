"""Diapositiva 9 — ``git init``: crear el repositorio.

Un antes y un después de la misma carpeta, y en medio el comando. Antes es una
carpeta como cualquier otra; después tiene dentro un ``.git`` y por eso ya es
un repositorio. Nada más cambia: los archivos son los mismos, en el mismo
sitio.

Ese ``.git`` sale vacío a propósito —``git init`` crea un repositorio sin un
solo commit— y es el hueco que la diapositiva siguiente empieza a llenar. Decir
en voz alta que ahí dentro vivirá todo explica de golpe por qué copiar la
carpeta se lleva el historial y por qué borrar ``.git`` lo pierde.
"""

from manim import (
    DOWN,
    RIGHT,
    UP,
    Create,
    FadeIn,
    Flash,
    GrowArrow,
    LaggedStart,
    VGroup,
)

from animaciones import flecha
from componentes import archivo, texto, zona
from componentes import titulo as hacer_titulo
from estilo import PRIMARIO, SECUNDARIO, VERDE

ARCHIVOS = ("informe.md", "datos.csv", "notas.md")

ANCHO_CARPETA, ALTO_CARPETA = 4.7, 3.7
X_CARPETAS = (-3.75, 3.75)
Y_CARPETAS = -0.45
Y_PIE = -2.75            # el rótulo de qué es cada caja, debajo


def _archivos():
    """Los tres archivos del proyecto, en fila. Los mismos antes y después."""
    return VGroup(*[
        archivo(nombre, SECUNDARIO, alto=0.6, tam=12) for nombre in ARCHIVOS
    ]).arrange(RIGHT, buff=0.42)


def _rotulo(contenido, color, x):
    """Qué es la caja: una carpeta a secas o ya un repositorio."""
    return texto(contenido, 17, color=color).move_to([x, Y_PIE, 0])


def construir(scene):
    encabezado = hacer_titulo("git init: crear el repositorio")

    # Izquierda: una carpeta y ya. De ahí el borde discontinuo y el gris.
    antes = zona("mi-proyecto/", SECUNDARIO, ANCHO_CARPETA, ALTO_CARPETA, 18)
    antes.move_to([X_CARPETAS[0], Y_CARPETAS, 0])
    sueltos = _archivos().move_to(antes[0].get_center())

    # Derecha: la misma carpeta, con línea continua, porque ya es otra cosa.
    despues = zona("mi-proyecto/", PRIMARIO, ANCHO_CARPETA, ALTO_CARPETA, 18,
                   discontinua=False)
    despues.move_to([X_CARPETAS[1], Y_CARPETAS, 0])

    # El .git sale vacío: "Initialized empty Git repository", literalmente.
    punto_git = zona(".git/", VERDE, 3.5, 1.0, 17, discontinua=False)
    vacio = texto("vacío, por ahora", 13, color=SECUNDARIO)
    vacio.move_to(punto_git[0].get_center())

    dentro = VGroup(_archivos(), VGroup(punto_git, vacio))
    dentro.arrange(DOWN, buff=0.42).move_to(despues[0].get_center())

    puente = flecha([X_CARPETAS[0] + ANCHO_CARPETA / 2 + 0.18, Y_CARPETAS, 0],
                    [X_CARPETAS[1] - ANCHO_CARPETA / 2 - 0.18, Y_CARPETAS, 0],
                    color=PRIMARIO, buff=0, grosor=4)
    comando = texto("git init", 20, color=PRIMARIO).next_to(puente, UP, buff=0.2)

    carpeta_normal = _rotulo("una carpeta", SECUNDARIO, X_CARPETAS[0])
    repositorio = _rotulo("un repositorio", PRIMARIO, X_CARPETAS[1])

    # ------------------------------ montaje --------------------------------
    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(FadeIn(antes), run_time=0.6)
    scene.play(
        LaggedStart(*[FadeIn(a, shift=UP * 0.12) for a in sueltos],
                    lag_ratio=0.25),
        FadeIn(carpeta_normal),
        run_time=0.9,
    )

    scene.play(GrowArrow(puente), FadeIn(comando, shift=DOWN * 0.1),
               run_time=0.7)

    scene.play(FadeIn(despues), FadeIn(dentro[0]), FadeIn(repositorio),
               run_time=0.7)
    scene.play(Create(punto_git), run_time=0.7)
    scene.play(
        Flash(punto_git[0], color=VERDE, line_length=0.22, num_lines=16,
              flash_radius=1.1),
        FadeIn(vacio),
        run_time=0.8,
    )
    scene.wait(0.3)

    scene.next_slide()
