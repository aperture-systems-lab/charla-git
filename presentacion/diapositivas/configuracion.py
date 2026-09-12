"""Diapositiva 8 — configurar git: decirle quién eres.

Lo primero que hay que hacer después de instalar, y lo único que git te va a
exigir antes de dejarte hacer un commit: decirle quién eres. Ese nombre y ese
correo se copian dentro de **cada commit que hagas**, así que conviene ponerlos
bien a la primera y con el mismo correo que se use luego en GitHub.

La tercera línea es la que evita el lío de nombres: git sigue creando la
primera rama como ``master`` cuando el estándar de hoy —GitHub el primero— es
``main``, así que se cambia una vez y ya nunca más.

Debajo, los tres niveles de configuración: gana siempre el más cercano al
repositorio, que es exactamente lo que uno quiere cuando trabaja con el correo
de la universidad en un sitio y el del trabajo en otro.
"""

from manim import (
    DOWN,
    RIGHT,
    UP,
    FadeIn,
    LaggedStart,
    RoundedRectangle,
    VGroup,
)

from animaciones import teclear
from componentes import terminal, texto
from componentes import titulo as hacer_titulo
from estilo import AMBAR, PRIMARIO, SECUNDARIO

IDENTIDAD = (
    ("git config --global user.name carmen_electra", "cmd"),
    ("git config --global user.email carmen.electra@unal.edu.co", "cmd"),
    ("", "sep"),
    ("para que la rama inicial se llame main, el estándar actual", "com"),
    ("git config --global init.defaultBranch main", "cmd"),
    ("", "sep"),
    ("git config --list", "cmd"),
    ("user.name=carmen_electra", "out"),
    ("user.email=carmen.electra@unal.edu.co", "out"),
    ("init.defaultBranch=main", "out"),
)

# (bandera, dónde vive, a qué afecta, color)
NIVELES = (
    ("--system", "todo el equipo", SECUNDARIO),
    ("--global", "~/.gitconfig", PRIMARIO),
    ("--local", ".git/config", AMBAR),
)


def _nivel(bandera, donde, color):
    """Una de las tres cajas de configuración, con su bandera y su archivo."""
    etiqueta = texto(bandera, 17, color=color)
    ruta = texto(donde, 13, color=SECUNDARIO)
    dentro = VGroup(etiqueta, ruta).arrange(DOWN, buff=0.12)
    caja = RoundedRectangle(
        width=dentro.width + 0.7, height=dentro.height + 0.45,
        corner_radius=0.12, stroke_color=color, stroke_width=2.5,
    ).set_fill(color, opacity=0.07)
    return VGroup(caja, dentro.move_to(caja.get_center()))


def construir(scene):
    encabezado = hacer_titulo("Configurar")

    # Diez renglones piden interlineado corto: con el buff por defecto la
    # ventana se comería el título por arriba y los niveles por abajo.
    consola = terminal(IDENTIDAD, tam=14, buff=0.12, margen=0.40)
    consola.move_to([0, 0.42, 0])

    niveles = VGroup(*[_nivel(*n) for n in NIVELES])
    niveles.arrange(RIGHT, buff=0.55).move_to([0, -2.60, 0])

    # ------------------------------ montaje --------------------------------
    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(FadeIn(consola[0]), run_time=0.5)
    teclear(scene, consola, ritmo=0.4)
    scene.play(
        LaggedStart(*[FadeIn(n, shift=UP * 0.12) for n in niveles],
                    lag_ratio=0.3),
        run_time=1.0,
    )
    scene.next_slide()
