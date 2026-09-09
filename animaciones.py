"""Helpers de animación compartidos: reciben la escena como primer argumento.

Centraliza aquí los patrones de animación que repitas en varias diapositivas
(entradas escalonadas, transiciones, énfasis) para no copiarlos por todos lados.
"""

import numpy as np
from manim import (
    RIGHT,
    Arrow,
    FadeIn,
    FadeOut,
    LaggedStart,
    ShowPassingFlash,
)

from estilo import PRIMARIO, SECUNDARIO


def limpiar_pantalla(scene):
    """Desvanece todo lo que hay en escena salvo el marco fijo."""
    resto = [m for m in scene.mobjects if m is not getattr(scene, "marco", None)]
    for m in resto:
        m.clear_updaters()
    if resto:
        scene.play(*[FadeOut(m) for m in resto])


def aparecer_uno_a_uno(scene, grupo, run_time=0.4, shift=RIGHT * 0.2):
    """Hace aparecer los elementos de un VGroup uno tras otro."""
    for elemento in grupo:
        scene.play(FadeIn(elemento, shift=shift), run_time=run_time)


def teclear(scene, ventana, desde=0, hasta=None, ritmo=0.38):
    """Revela las líneas de una ``terminal`` como si se fueran escribiendo.

    Cada línea entra desplazándose desde la izquierda, una detrás de otra: el
    ritmo de las entradas sucesivas ya se lee como alguien tecleando, sin
    necesidad de meter pausas entre medias.

    Y conviene que no las haya: una ``wait`` corta genera un clip de un solo
    fotograma, y manim-slides revienta al concatenar la diapositiva ("Invalid
    argument" desde pyav). Si hace falta respirar, súbele el ``ritmo``.

    Las filas en blanco (``sep``) son rectángulos invisibles: solo marcan el
    hueco, así que se saltan sin gastar tiempo.
    """
    for fila in ventana[1][desde:hasta]:
        if getattr(fila, "es_separador", False):
            continue
        scene.play(FadeIn(fila, shift=RIGHT * 0.12), run_time=ritmo)


def pulso(camino, color=PRIMARIO, run_time=1.0, ancho=6, franja=0.35):
    """Luz que recorre un camino (una arista, una flecha) sin dejar rastro.

    Una copia del propio trazo con ``ShowPassingFlash``: mucho más barato que
    un ``Dot`` con updater, y en un grafo con veinte aristas es la diferencia
    entre que se lea la señal o que se lea ruido.
    """
    trazo = camino.copy().set_stroke(color=color, width=ancho, opacity=1)
    return ShowPassingFlash(trazo, time_width=franja, run_time=run_time)


def flecha(origen, destino, color=SECUNDARIO, buff=0.12, grosor=3.5):
    """Flecha fina entre dos mobjects o dos puntos, con la punta a escala."""
    a = origen.get_center() if hasattr(origen, "get_center") else np.array(origen)
    b = destino.get_center() if hasattr(destino, "get_center") else np.array(destino)
    return Arrow(
        a, b, color=color, stroke_width=grosor, buff=buff,
        max_tip_length_to_length_ratio=0.16,
    )


def entrar_escalonado(grupo, shift=None, lag=0.2, run_time=1.0):
    """``LaggedStart`` de ``FadeIn`` sobre los hijos de un grupo."""
    shift = np.array([0.0, 0.15, 0.0]) if shift is None else shift
    return LaggedStart(
        *[FadeIn(m, shift=shift) for m in grupo], lag_ratio=lag, run_time=run_time,
    )
