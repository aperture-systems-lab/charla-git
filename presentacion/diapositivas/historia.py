"""Diapositiva 5 — el origen de git, contado como historia y casi sin texto.

La foto de Linus, montada como una fotografía de las de revelar, se queda a la
izquierda los tres primeros actos; lo que cambia es el bloque de la derecha.
Cada acto es una idea, una cifra grande y poco más:

  1. Quién es, medido por lo que ya había hecho: Tux, y el 100 % de los 500
     supercomputadores más potentes del mundo.
  2. El atasco: mil personas, un kernel, y ninguna herramienta a la altura.
     Las libres no aguantaban el ritmo; la que sí, era de pago. En 2005 le
     retiran la licencia.
  3. La rabia: diez cuadraditos, uno por día, y al final el logo de git.
  4. Hoy: la encuesta de Stack Overflow.

Fuentes:
  * Linux en el TOP500 — SQ Magazine, "Linux statistics"
    (https://sqmagazine.co.uk/linux-statistics/).
  * La gráfica — Stack Overflow Developer Survey 2022, "Version control system"
    (https://survey.stackoverflow.co/2022/#technology-version-control).

Sobre la gráfica: es una magnitud, no cuatro identidades que compitan, así que
va en una sola serie —acento de marca para git, gris recesivo para el resto—,
ordenada de mayor a menor, con el valor escrito en cada barra y sin rejilla. En
rojo no va nada: en esta charla el rojo significa "esto está mal".
"""

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    FadeIn,
    Line,
    FadeOut,
    Flash,
    GrowFromCenter,
    GrowFromEdge,
    Group,
    LaggedStart,
    VGroup,
)

from componentes import barra, fotografia, puntero, texto
from componentes import titulo as hacer_titulo
from estilo import AMBAR, CLARO, ERROR, FONT_TITULO, PRIMARIO, SECUNDARIO

TITULO = "El origen"
TITULO_HOY = "El estándar"

# --- El retrato, que se queda tres actos -----------------------------------
X_FOTO = -4.55
Y_FOTO = -0.1
ANCHO_FOTO = 3.8

# La columna de la derecha: todos los bloques arrancan en la misma x.
X_COL = -1.9
Y_COL = -0.1

# --- Acto 1: el tamaño de lo que ya había hecho ----------------------------
# Tux va sobre su propio papel blanco: el .jpg ya viene con fondo blanco, así
# que la ficha lo continúa en vez de recortarlo.
TOP500 = "de los 500 supercomputadores del mundo"
FUENTE_TOP500 = "TOP500 · SQ Magazine"

# --- Acto 2: por qué no le valía nada de lo que había ----------------------
# Libres había —CVS, Subversion—, pero no a la escala del kernel; la que sí
# aguantaba era propietaria. Ese matiz es lo que hace que git tenga sentido.
ATASCO = (
    ("CVS · Subversion", "demasiado lentas"),
    ("BitKeeper", "de pago"),
)
X_PEGA = 4.5             # columna fija: las pegas se leen en vertical
GOLPE = "2005 · le retiran la licencia"

# --- Acto 3: diez días -----------------------------------------------------
DIAS = 10
LADO_DIA = 0.34

# --- Acto 4: la gráfica ----------------------------------------------------
# Stack Overflow Developer Survey 2022 — "Version control system", respuesta
# múltiple, así que los porcentajes no suman 100.
ENCUESTA = (
    ("Git", 93.87),
    ("SVN", 5.18),
    ("no uso ninguno", 4.31),
    ("Mercurial", 1.13),
)
X_ETIQUETA = -3.9        # borde derecho de los nombres
X_BARRA = -3.6           # donde arrancan todas las barras
LARGO_100 = 7.8          # cuánto mide el 100 %
ALTO_BARRA = 0.6
Y_PRIMERA_BARRA = 1.55
PASO_BARRA = 1.15
# El enlace completo no va en pantalla —nadie lo teclea desde una proyección—:
# vive en el docstring de arriba y en la sección de fuentes del README.
FUENTE_ENCUESTA = "Stack Overflow Developer Survey 2022"


def _colocar(bloque):
    """Deja un bloque en la columna de la derecha, alineado por la izquierda."""
    return bloque.arrange(DOWN, buff=0.42, aligned_edge=LEFT).move_to(
        [X_COL, Y_COL, 0], LEFT)


def _acto_linux():
    """Tux y una cifra: quién era Linus antes de escribir git."""
    ficha = Group(
        fotografia("linux", 1.5, giro=0),
        texto("Linux · 1991", 26, color=CLARO),
    ).arrange(RIGHT, buff=0.5)
    return _colocar(Group(
        ficha,
        texto("100%", 64, color=PRIMARIO, font=FONT_TITULO),
        texto(TOP500, 22),
        texto(FUENTE_TOP500, 14, color=SECUNDARIO).set_opacity(0.7),
    ))


def _fila_atasco(nombre, pega):
    """La herramienta en su ficha, tachada, y por qué no valía.

    El tachón dice "descartada" sin escribirlo, que es más rápido de leer que
    un aspa al lado y además se ve desde el fondo del aula.
    """
    ficha = puntero(nombre, SECUNDARIO, 22, relleno=0.08)
    ficha.move_to([0, 0, 0], LEFT)
    # El tachón no llega a tocar el borde de la ficha: si lo toca, parece que
    # lo tachado es la caja y no el nombre.
    tachon = Line(ficha.get_left() + RIGHT * 0.14,
                  ficha.get_right() + LEFT * 0.14,
                  color=ERROR, stroke_width=4)
    return VGroup(
        ficha, tachon,
        texto(pega, 22, color=ERROR).move_to([X_PEGA, 0, 0], LEFT),
    )


def _acto_atasco():
    """Mil personas, un kernel, y nada que sirva."""
    cabecera = VGroup(
        texto("1.000", 40, color=CLARO),
        texto("personas, un kernel", 24, color=SECUNDARIO),
    ).arrange(RIGHT, buff=0.35, aligned_edge=DOWN)
    return _colocar(Group(
        cabecera,
        _fila_atasco(*ATASCO[0]),
        _fila_atasco(*ATASCO[1]),
        texto(GOLPE, 24, color=AMBAR),
    ))


def _acto_diez_dias():
    """Diez cuadraditos, uno por día, y de ahí sale el logo."""
    dias = VGroup(*[
        barra(LADO_DIA, LADO_DIA, PRIMARIO, 0.9) for _ in range(DIAS)
    ]).arrange(RIGHT, buff=0.16)
    remate = Group(
        texto("10", 64, color=PRIMARIO, font=FONT_TITULO),
        texto("días", 26, color=CLARO),
        fotografia("git", 2.3, giro=0),
    ).arrange(RIGHT, buff=0.45, aligned_edge=DOWN)
    return _colocar(Group(
        dias,
        remate,
        texto("y a los 4 meses, a la comunidad", 22, color=SECUNDARIO),
    ))


def _grafica():
    """Las cuatro barras, ordenadas de mayor a menor, y la fuente debajo."""
    filas = VGroup()
    for i, (nombre, porcentaje) in enumerate(ENCUESTA):
        y = Y_PRIMERA_BARRA - i * PASO_BARRA
        destacado = i == 0          # git; el resto se lee como contexto
        color = PRIMARIO if destacado else SECUNDARIO
        etiqueta = texto(nombre, 22, color=CLARO if destacado else SECUNDARIO)
        etiqueta.move_to([X_ETIQUETA, y, 0], RIGHT)
        trazo = barra(LARGO_100 * porcentaje / 100, ALTO_BARRA, color,
                      1.0 if destacado else 0.55)
        trazo.move_to([X_BARRA, y, 0], LEFT)
        valor = texto(f"{porcentaje:.2f} %".replace(".", ","), 22,
                      color=CLARO if destacado else SECUNDARIO)
        valor.next_to(trazo, RIGHT, buff=0.22)
        filas.add(VGroup(etiqueta, trazo, valor))

    fuente = texto(FUENTE_ENCUESTA, 18, color=SECUNDARIO).move_to([0, -3.05, 0])
    return filas, fuente


def construir(scene):
    encabezado = hacer_titulo(TITULO)
    retrato = fotografia("trovalds", ANCHO_FOTO, pie="Linus Torvalds")
    retrato.move_to([X_FOTO, Y_FOTO, 0])

    # ---------------------- Acto 1: quién es -------------------------------
    linux = _acto_linux()
    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(FadeIn(retrato, scale=0.92), run_time=0.8)
    scene.play(
        LaggedStart(*[FadeIn(m, shift=RIGHT * 0.15) for m in linux],
                    lag_ratio=0.35),
        run_time=1.4,
    )
    scene.next_slide()

    # ---------------------- Acto 2: el atasco ------------------------------
    atasco = _acto_atasco()
    scene.play(FadeOut(linux), run_time=0.5)
    scene.play(
        LaggedStart(*[FadeIn(m, shift=RIGHT * 0.15) for m in atasco[:-1]],
                    lag_ratio=0.4),
        run_time=1.3,
    )
    scene.play(FadeIn(atasco[-1], shift=UP * 0.12), run_time=0.5)
    scene.next_slide()

    # ---------------------- Acto 3: diez días ------------------------------
    diez = _acto_diez_dias()
    dias, remate, cierre = diez
    scene.play(FadeOut(atasco), run_time=0.5)
    # Un cuadradito por día: el chiste es que se acaban enseguida.
    scene.play(
        LaggedStart(*[GrowFromCenter(d) for d in dias], lag_ratio=0.35),
        run_time=1.5,
    )
    scene.play(FadeIn(remate[0], shift=UP * 0.12), FadeIn(remate[1]),
               run_time=0.5)
    scene.play(FadeIn(remate[2], scale=0.9), run_time=0.5)
    scene.play(
        Flash(remate[2], color=PRIMARIO, line_length=0.3, num_lines=18,
              flash_radius=1.3),
        run_time=0.7,
    )
    scene.play(FadeIn(cierre, shift=RIGHT * 0.15), run_time=0.5)
    scene.next_slide()

    # ---------------------- Acto 4: hoy ------------------------------------
    encabezado_hoy = hacer_titulo(TITULO_HOY)
    filas, fuente = _grafica()

    scene.play(
        FadeOut(retrato), FadeOut(diez),
        FadeOut(encabezado), FadeIn(encabezado_hoy, shift=DOWN * 0.2),
        run_time=0.8,
    )
    for etiqueta, trazo, valor in filas:
        scene.play(
            FadeIn(etiqueta, shift=RIGHT * 0.1),
            GrowFromEdge(trazo, LEFT),
            run_time=0.55,
        )
        scene.play(FadeIn(valor, shift=LEFT * 0.1), run_time=0.25)
    scene.play(FadeIn(fuente), run_time=0.5)
    scene.wait(0.3)

    scene.next_slide()
