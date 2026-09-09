"""Diapositiva 22 — los comandos del remoto, en orden.

Ya está el repositorio local, ya está la llave: toca conectarlos. Esta
diapositiva es deliberadamente mecánica, para que se pueda seguir tecleando en
directo: enlazar el remoto, subir por primera vez con ``-u``, y a partir de ahí
``git push`` a secas.

Y después la distinción que más quebraderos ahorra: ``fetch`` **mira** y
``pull`` **mira y fusiona**. Son el mismo viaje al servidor; lo que cambia es
si git toca tu directorio de trabajo al volver. Cuando alguien dice "hice pull
y se me lió todo", casi siempre lo que quería era un fetch para ver primero.
"""

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    FadeIn,
    FadeOut,
    LaggedStart,
    RoundedRectangle,
    VGroup,
)

from animaciones import teclear
from componentes import terminal, texto
from componentes import titulo as hacer_titulo
from estilo import (
    AMBAR,
    CLARO,
    OK,
    RAMA_MAIN,
    SECUNDARIO,
    SUPERFICIE,
)

ENLAZAR = (
    ("git remote add origin git@github.com:ana/repo.git", "cmd"),
    ("git remote -v", "cmd"),
    ("origin  git@github.com:ana/repo.git (fetch)", "out"),
    ("", "sep"),
    ("git push -u origin main", "cmd"),
    ("la primera vez con -u: enlaza tu main con el suyo", "com"),
    ("", "sep"),
    ("git push", "cmd"),
    ("a partir de ahi, asi de corto", "com"),
)

CLONAR = (
    ("git clone git@github.com:ana/repo.git", "cmd"),
    ("Cloning into 'repo'...", "out"),
    ("", "sep"),
    ("trae el proyecto, todo el historial", "com"),
    ("y deja el remoto puesto como origin", "com"),
)

# (comando, qué toca, color)
MIRAR = (
    ("git fetch", "solo actualiza origin/main", "tu trabajo no se toca", AMBAR),
    ("git pull", "fetch + merge, de una vez", "puede dar conflicto", OK),
)


def _caja(comando, que_hace, apunte, color, x):
    """Una de las dos cajas de fetch / pull."""
    caja = RoundedRectangle(
        width=5.4, height=2.1, corner_radius=0.18,
        stroke_color=color, stroke_width=3,
    ).set_fill(SUPERFICIE, opacity=1.0).move_to([x, -0.55, 0])
    nombre = texto(comando, 21, color=color).move_to([x, 0.05, 0])
    linea = texto(que_hace, 15, color=CLARO).move_to([x, -0.5, 0])
    nota = texto(apunte, 14, color=SECUNDARIO).move_to([x, -0.95, 0])
    return VGroup(caja, nombre, linea, nota)


def construir(scene):
    encabezado = hacer_titulo("Enlazar y subir")

    consola = terminal(ENLAZAR, tam=15, buff=0.2).move_to([0, -0.15, 0])
    nota = texto("git@github.com:usuario/repo.git es la dirección SSH; "
                 "la copias del botón verde", 14, color=SECUNDARIO)
    nota.to_edge(DOWN, buff=0.62)
    if nota.width > 12.4:
        nota.scale(12.4 / nota.width)

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(FadeIn(consola[0]), run_time=0.5)
    teclear(scene, consola, ritmo=0.3)
    scene.play(FadeIn(nota), run_time=0.45)
    scene.next_slide()

    # ---------------------- Pantalla 2: clonar -----------------------------
    otro_encabezado = hacer_titulo("Al revés: git clone")

    clonar = terminal(CLONAR, tam=15).move_to([-3.2, 0.3, 0])
    cuando = VGroup(
        texto("clone es para empezar", 17, color=RAMA_MAIN),
        texto("cuando el repositorio ya", 15, color=SECUNDARIO),
        texto("existe y tú aún no lo tienes", 15, color=SECUNDARIO),
        texto("init + remote add es para", 15, color=SECUNDARIO),
        texto("el camino contrario", 15, color=SECUNDARIO),
    ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
    cuando.move_to([1.2, 0.3, 0], LEFT)

    scene.play(
        FadeOut(consola), FadeOut(nota),
        FadeOut(encabezado), FadeIn(otro_encabezado, shift=DOWN * 0.2),
        run_time=0.8,
    )
    scene.play(FadeIn(clonar[0]), run_time=0.5)
    teclear(scene, clonar, ritmo=0.3)
    scene.play(
        LaggedStart(*[FadeIn(t, shift=RIGHT * 0.12) for t in cuando],
                    lag_ratio=0.25),
        run_time=1.3,
    )
    scene.next_slide()

    # ---------------------- Pantalla 3: fetch vs pull ----------------------
    ultimo_encabezado = hacer_titulo("fetch mira, pull fusiona")

    cajas = VGroup(*[
        _caja(c, q, a, color, x)
        for (c, q, a, color), x in zip(MIRAR, (-3.5, 3.5))
    ])
    igualdad = texto("git pull  =  git fetch  +  git merge", 18, color=CLARO)
    igualdad.move_to([0, 1.55, 0])
    consejo = VGroup(
        texto("si no sabes qué te vas a encontrar, fetch primero",
              16, color=CLARO),
        texto("miras con git log origin/main y luego decides", 14,
              color=SECUNDARIO),
    ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.68)

    scene.play(
        FadeOut(clonar), FadeOut(cuando),
        FadeOut(otro_encabezado), FadeIn(ultimo_encabezado, shift=DOWN * 0.2),
        run_time=0.8,
    )
    scene.play(FadeIn(igualdad, shift=DOWN * 0.1), run_time=0.5)
    scene.play(FadeIn(cajas[0], shift=RIGHT * 0.15), run_time=0.7)
    scene.play(FadeIn(cajas[1], shift=RIGHT * 0.15), run_time=0.7)
    scene.play(
        LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in consejo],
                    lag_ratio=0.3),
        run_time=1.0,
    )
    scene.wait(0.3)

    scene.next_slide()
