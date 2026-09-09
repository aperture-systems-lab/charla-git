"""Diapositiva 4 — el mismo dibujo, pero con un proyecto que todos conocen.

Minecraft se desarrolla exactamente así, y encima lo enseña en público: cada
update es una versión publicada, las snapshots son la rama donde se cuece la
siguiente, y Java y Bedrock son dos líneas de producción que avanzan en
paralelo desde el mismo juego.

Tres actos sobre el mismo grafo:

  1. La línea de versiones, con el arte oficial de cada update: 1.12 a 1.16.
  2. Las snapshots: una rama que sale de 1.15, trabaja aparte y entra en 1.16.
  3. Las dos ediciones: el grafo sube para hacer sitio y abajo aparece Bedrock,
     que no publica en los mismos momentos que Java.

El arte lo cargan las tarjetas desde ``assets/mc``; los .webp y .avif
originales están convertidos a .png al lado.
"""

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    FadeIn,
    Flash,
    GrowFromCenter,
    Group,
    LaggedStart,
    VGroup,
)

from componentes import (
    enlace,
    enmarcar,
    imagen_recortada,
    nodo_commit,
    parrafo,
    puntero,
    texto,
)
from componentes import titulo as hacer_titulo
from estilo import CLARO, RAMA_FEATURE, RAMA_MAIN, SECUNDARIO, VERDE

TITULO = "Un ejemplo: Minecraft"

# --- La línea de Java ------------------------------------------------------
# El último salto es ancho a propósito: ahí es donde caben las snapshots.
VERSIONES = (
    ("mc/mc_1.12", "1.12", -4.6),
    ("mc/mc_1.13", "1.13", -2.9),
    ("mc/mc_1.14", "1.14", -1.2),
    ("mc/mc_1.15", "1.15", 0.5),
    ("mc/mc_1.16", "1.16", 5.2),
)
ANCHO_ARTE = 1.5
MEDIA_TARJETA = ANCHO_ARTE / 2 + 0.07     # media tarjeta, marco incluido
Y_JAVA = 0.3

# --- La rama de snapshots --------------------------------------------------
X_SNAPSHOT = (2.4, 3.3)
Y_SNAPSHOT = 1.2
R_NODO = 0.26

# --- Las dos ediciones -----------------------------------------------------
# El grafo entero sube para dejar sitio abajo a la segunda línea. Bedrock se
# salta 1.14: las dos ediciones no publican a la vez, y eso es justo lo que
# hace que sean dos ramas y no una.
SUBE = UP * 0.55
Y_BEDROCK = -1.95
BEDROCK = (("1.12", -4.6), ("1.13", -2.9), ("1.15", 0.5), ("1.16", 5.2))
R_BEDROCK = 0.3
# Verde para la segunda línea de producción: aquí es una categoría más, no el
# "esto ha salido bien" de los diagramas de commits.
COLOR_BEDROCK = VERDE


def _tarjeta(archivo, version, x):
    """Una versión publicada: su arte, el marco de la charla y el número.

    El número va encima y no debajo porque debajo, en el tercer acto, baja la
    línea que abre la edición Bedrock.
    """
    arte = imagen_recortada(archivo, ANCHO_ARTE).move_to([x, Y_JAVA, 0])
    marco = enmarcar(arte, margen=0.14, color=RAMA_MAIN).set_stroke(width=2.5)
    etiqueta = texto(version, 16, color=CLARO).next_to(marco, UP, buff=0.18)
    return Group(arte, marco, etiqueta)


def _fila_java():
    """Las cinco tarjetas y los tramos de línea que las encadenan."""
    tarjetas = [_tarjeta(*v) for v in VERSIONES]
    tramos = VGroup(*[
        enlace([VERSIONES[i][2] + MEDIA_TARJETA, Y_JAVA, 0],
               [VERSIONES[i + 1][2] - MEDIA_TARJETA, Y_JAVA, 0], RAMA_MAIN)
        for i in range(len(VERSIONES) - 1)
    ])
    return tarjetas, tramos


def _rama_snapshots():
    """La rama que sale de 1.15, hace dos snapshots y entra en 1.16."""
    nodos = VGroup(*[
        nodo_commit("", RAMA_FEATURE, R_NODO).move_to([x, Y_SNAPSHOT, 0])
        for x in X_SNAPSHOT
    ])
    x_sale, x_entra = VERSIONES[3][2], VERSIONES[4][2]
    tramos = VGroup(
        enlace([x_sale + MEDIA_TARJETA, Y_JAVA, 0],
               [X_SNAPSHOT[0] - R_NODO, Y_SNAPSHOT, 0], RAMA_FEATURE),
        enlace([X_SNAPSHOT[0] + R_NODO, Y_SNAPSHOT, 0],
               [X_SNAPSHOT[1] - R_NODO, Y_SNAPSHOT, 0], RAMA_FEATURE),
        enlace([X_SNAPSHOT[1] + R_NODO, Y_SNAPSHOT, 0],
               [x_entra - MEDIA_TARJETA, Y_JAVA, 0], RAMA_FEATURE),
    )
    rotulo = puntero("snapshots", RAMA_FEATURE, 14)
    rotulo.next_to(nodos, UP, buff=0.28)
    return nodos, tramos, rotulo


def _linea_bedrock():
    """La segunda línea de producción, ya en su sitio definitivo.

    Sus versiones van rotuladas debajo justamente para que se vea el hueco de
    la 1.14: cada edición publica cuando le toca.
    """
    equis = [x for _, x in BEDROCK]
    nodos = VGroup(*[
        nodo_commit("", COLOR_BEDROCK, R_BEDROCK).move_to([x, Y_BEDROCK, 0])
        for x in equis
    ])
    etiquetas = VGroup(*[
        texto(version, 15, color=SECUNDARIO).move_to(
            [x, Y_BEDROCK - R_BEDROCK - 0.32, 0])
        for version, x in BEDROCK
    ])
    tramos = VGroup(*[
        enlace([a + R_BEDROCK, Y_BEDROCK, 0], [b - R_BEDROCK, Y_BEDROCK, 0],
               COLOR_BEDROCK)
        for a, b in zip(equis, equis[1:])
    ])
    # De la primera versión de Java baja la línea que abre la otra edición.
    salida = enlace([equis[0], Y_JAVA + SUBE[1] - MEDIA_TARJETA, 0],
                    [equis[0], Y_BEDROCK + R_BEDROCK, 0], COLOR_BEDROCK)
    return nodos, etiquetas, tramos, salida


def _rotulo_fila(nombre, color, y):
    """El nombre de una edición, a la izquierda de su línea."""
    bloque = parrafo([(nombre, 17, color), ("Edition", 12, SECUNDARIO)],
                     buff=0.08, alinear=LEFT)
    return bloque.move_to([-6.15, y, 0])


def construir(scene):
    encabezado = hacer_titulo(TITULO)
    tarjetas, tramos = _fila_java()
    snapshots, tramos_snap, rotulo_snap = _rama_snapshots()

    # ---------------------- Acto 1: las versiones --------------------------
    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(FadeIn(tarjetas[0], scale=0.92), run_time=0.6)
    for tramo, tarjeta in zip(tramos, tarjetas[1:]):
        scene.play(Create(tramo), FadeIn(tarjeta, scale=0.92), run_time=0.55)
    scene.next_slide()

    # ---------------------- Acto 2: las snapshots --------------------------
    scene.play(Create(tramos_snap[0]), run_time=0.45)
    scene.play(GrowFromCenter(snapshots[0]), run_time=0.3)
    scene.play(Create(tramos_snap[1]), GrowFromCenter(snapshots[1]),
               run_time=0.45)
    scene.play(FadeIn(rotulo_snap, shift=DOWN * 0.12), run_time=0.35)
    scene.play(Create(tramos_snap[2]), run_time=0.5)
    scene.play(
        Flash(tarjetas[4], color=RAMA_FEATURE, line_length=0.25, num_lines=16,
              flash_radius=MEDIA_TARJETA + 0.5),
        run_time=0.7,
    )
    scene.next_slide()

    # ---------------------- Acto 3: las dos ediciones ----------------------
    java_entero = Group(*tarjetas, tramos, snapshots, tramos_snap, rotulo_snap)
    nodos_bed, etiquetas_bed, tramos_bed, salida_bed = _linea_bedrock()
    rotulo_java = _rotulo_fila("Java", RAMA_MAIN, Y_JAVA + SUBE[1])
    rotulo_bed = _rotulo_fila("Bedrock", COLOR_BEDROCK, Y_BEDROCK)

    # El grafo sube: lo que había era solo una de las dos ediciones.
    scene.play(java_entero.animate.shift(SUBE), run_time=0.8)
    scene.play(FadeIn(rotulo_java, shift=RIGHT * 0.15), run_time=0.4)

    scene.play(Create(salida_bed), run_time=0.6)
    scene.play(GrowFromCenter(nodos_bed[0]), FadeIn(etiquetas_bed[0]),
               run_time=0.4)
    for tramo, nodo, etiqueta in zip(tramos_bed, nodos_bed[1:],
                                     etiquetas_bed[1:]):
        scene.play(Create(tramo), GrowFromCenter(nodo), FadeIn(etiqueta),
                   run_time=0.5)
    scene.play(FadeIn(rotulo_bed, shift=RIGHT * 0.15), run_time=0.4)
    scene.wait(0.3)

    scene.next_slide()
