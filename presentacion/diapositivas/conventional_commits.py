"""Diapositiva 15 — cómo se escribe el mensaje: Conventional Commits.

La anterior deja claro que el mensaje importa; esta dice cómo se escribe, y lo
dice con el mismo commit —se importa de allí, pieza a pieza— para que no haya
que empezar un ejemplo nuevo.

La convención es **Conventional Commits 1.0.0**, que no es una opinión sino
una especificación pequeña y muy extendida: un tipo, un ámbito opcional y una
descripción. Va en cuatro pantallas:

  * **la línea, despiezada.** El comando entero tal y como se teclea, con cada
    parte de su color, y debajo la misma parte repetida y explicada. El color
    es lo que empareja las dos cosas, así que no hacen falta flechas cruzando
    la pantalla;
  * **``feat`` y ``fix``**, que son el 90 % de los commits de cualquiera. Cada
    uno con el caso en el que se usa —en una línea— y su comando entero
    debajo, para que se vea escrito y no solo nombrado;
  * **los demás**, en rejilla y todos del mismo gris: ``docs``, ``refactor``,
    ``test`` y ``chore``. El gris es la explicación: ninguno cambia lo que el
    programa hace, y por eso se agrupan;
  * y **el cuerpo**, que es opcional y por eso va al final: el porqué, si
    hace falta, escrito con un segundo ``-m``.

Cada tipo sube además un dígito distinto de la versión (el versionado
semántico), pero eso no se cuenta aquí para no meter dos convenciones a la
vez.

Fuente: https://www.conventionalcommits.org/es/v1.0.0/
"""

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    FadeIn,
    FadeOut,
    LaggedStart,
    VGroup,
)

from animaciones import teclear
from componentes import linea_terminal, puntero, terminal, texto
from componentes import titulo as hacer_titulo
from estilo import AMBAR, CLARO, OK, RAMA_MAIN, SECUNDARIO

from .mensajes_commit import AMBITO, DESCRIPCION, TIPO

TITULOS = (
    "Conventional Commits",
    "feat y fix",
    "El resto",
    "Cuerpo del commit",
)

# --- Pantalla 1: la línea, despiezada ---------------------------------------
FORMA = "<tipo>[ámbito]: <descripción>"
ORDEN_LINEA = f'git commit -m "{TIPO}{AMBITO}: {DESCRIPCION}"'
TAM_LINEA = 21
Y_LINEA = 1.35

# (trozo tal cual sale en la línea, qué es, color)
PIEZAS = (
    (TIPO, "el tipo: qué clase de cambio es", OK),
    (AMBITO, "el ámbito: qué parte tocaste, opcional", AMBAR),
    ("entrena...", "la descripción: qué hace, en presente", CLARO),
)
X_PIEZA, X_QUE_ES = -6.0, -3.55
Y_PIEZAS = 0.1
PASO_PIEZA = 1.15
TAM_FORMA = 21

# --- Pantalla 2: los dos tipos que se usan todos los días ------------------
# (tipo, color, cuándo se usa, el comando entero). Van con su color de rol
# porque son los dos que cambian lo que el programa hace.
PRINCIPALES = (
    ("feat", OK, "introduce una funcionalidad nueva",
     'git commit -m "feat: anade el cargador de CSV"'),
    ("fix", RAMA_MAIN, "corrige un error en el código",
     f'git commit -m "{TIPO}: {DESCRIPCION}"'),
)
X_CHIP = -6.0
X_CUANDO = -5.0
TAM_CUANDO = 21
TAM_ORDEN = 21
Y_PRINCIPALES = (1.05, -1.2)      # el alto de cada bloque
BAJADA_ORDEN = 0.8                # y su comando, justo debajo

# --- Pantalla 3: los demás, todos del mismo gris ---------------------------
# (tipo, cuándo). Ninguno cambia lo que el programa hace: por eso van juntos y
# todos del mismo gris. En una sola columna, que en rejilla la vista salta y
# la lista se lee de arriba abajo. El ejemplo de abajo enseña que se escriben
# igual que los otros dos.
SECUNDARIOS = (
    ("docs", "solo documentación"),
    ("style", "formato, sin tocar el código"),
    ("refactor", "otro código, mismo resultado"),
    ("perf", "lo mismo, pero más rápido"),
    ("test", "solo pruebas"),
    ("ci", "el pipeline, los workflows"),
    ("chore", "dependencias y limpieza"),
)
X_TIPO_RESTO, X_GLOSA_RESTO = -5.2, -2.9
Y_RESTO = 1.9
PASO_RESTO = 0.66
TAM_RESTO = 21
ORDEN_SECUNDARIO = 'git commit -m "chore: sube pandas a 2.2"'
Y_ORDEN_SECUNDARIO = -2.9

# --- Pantalla 4: el cuerpo, escrito en la terminal -------------------------
# ``-m`` se puede repetir, y cada uno es un párrafo del mensaje: el título y,
# si hace falta, el cuerpo. Eso se enseña mejor tecleado que dibujado, así que
# aquí va la sesión entera y no una ventana con el mensaje ya escrito.
CORTE = "\\"                      # el que parte la orden en varios renglones
SESION = (
    (f'git commit -m "{TIPO}{AMBITO}: {DESCRIPCION}" {CORTE}', "cmd"),
    ('-m "Ajustaba con el conjunto de prueba y eso sesgaba la metrica."',
     "out"),
)
TAM_SESION = 17
MARGEN_SESION = 0.6
Y_SESION = 1.0
SANGRIA_SESION = 1.95             # 13 columnas: bajo el primer ``-m``

# (qué es cada ``-m``, de qué color va su línea)
PARRAFOS = (
    ("el título resume el cambio en una línea", CLARO),
    ("el cuerpo explica por qué era necesario", SECUNDARIO),
)
X_PARRAFO = -5.2
BUFF_PARRAFO = 0.9                # del ``-m`` a su rótulo
Y_PARRAFOS = -1.55
PASO_PARRAFO = 1.0
TAM_PARRAFO = 27


def _orden_despiezada():
    """El comando de ejemplo con cada parte de su color.

    Los colores van por posición y no por palabra: las claves de ``t2c`` son
    expresiones regulares y un paréntesis dentro de la clave —``(modelo)``—
    haría de grupo. Las posiciones se calculan sobre la cadena ya con el
    prompt delante, que es la que se dibuja.
    """
    completa = f"$ {ORDEN_LINEA}"
    t2c = {"[0:1]": OK, "[2:12]": RAMA_MAIN}
    for trozo, color in ((TIPO, OK), (AMBITO, AMBAR)):
        i = completa.index(trozo)
        t2c[f"[{i}:{i + len(trozo)}]"] = color
    return texto(completa, TAM_LINEA, color=CLARO, t2c=t2c)


def construir(scene):
    # ---------------------- La línea, despiezada ---------------------------
    encabezado = hacer_titulo(TITULOS[0])
    forma = texto(FORMA, TAM_FORMA, color=RAMA_MAIN).move_to([0, 2.4, 0])
    linea = _orden_despiezada().move_to([0, Y_LINEA, 0])
    piezas = VGroup()
    for i, (trozo, que_es, color) in enumerate(PIEZAS):
        y = Y_PIEZAS - i * PASO_PIEZA
        piezas.add(VGroup(
            texto(trozo, TAM_LINEA, color=color).move_to(
                [X_PIEZA, y, 0], LEFT),
            texto(que_es, TAM_LINEA, color=SECUNDARIO).move_to(
                [X_QUE_ES, y, 0], LEFT),
        ))

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(FadeIn(forma, shift=DOWN * 0.1), run_time=0.5)
    scene.play(FadeIn(linea, shift=RIGHT * 0.15), run_time=0.7)
    for pieza in piezas:
        scene.play(FadeIn(pieza, shift=RIGHT * 0.12), run_time=0.6)
    scene.next_slide()

    # ---------------------- feat y fix -------------------------------------
    # Los dos que se usan todos los días, cada uno con su caso y su comando.
    tipos_encabezado = hacer_titulo(TITULOS[1])
    bloques = VGroup()
    for (tipo, color, cuando, orden), y in zip(PRINCIPALES, Y_PRINCIPALES):
        chip = puntero(tipo, color, 21).move_to([X_CHIP, y, 0])
        bloques.add(VGroup(
            chip,
            texto(cuando, TAM_CUANDO, color=CLARO).move_to(
                [X_CUANDO, y, 0], LEFT),
            linea_terminal(orden, "cmd", TAM_ORDEN).move_to(
                [X_CUANDO, y - BAJADA_ORDEN, 0], LEFT),
        ))

    scene.play(
        FadeOut(forma), FadeOut(linea), FadeOut(piezas),
        FadeOut(encabezado), FadeIn(tipos_encabezado, shift=DOWN * 0.2),
        run_time=0.8,
    )
    for bloque in bloques:
        scene.play(
            LaggedStart(*[FadeIn(m, shift=RIGHT * 0.12) for m in bloque],
                        lag_ratio=0.4),
            run_time=1.2,
        )
    scene.next_slide()

    # ---------------------- Y los demás ------------------------------------
    # Todos del mismo gris a propósito: ninguno cambia lo que el programa
    # hace, y con eso queda dicho en qué caso va cada uno.
    resto_encabezado = hacer_titulo(TITULOS[2])
    rejilla = VGroup()
    for i, (tipo, cuando) in enumerate(SECUNDARIOS):
        y = Y_RESTO - i * PASO_RESTO
        chip = puntero(tipo, SECUNDARIO, TAM_RESTO)
        chip.move_to([X_TIPO_RESTO, y, 0], LEFT)
        rejilla.add(VGroup(chip, texto(cuando, TAM_RESTO, color=CLARO)
                           .move_to([X_GLOSA_RESTO, y, 0], LEFT)))
    ejemplo = linea_terminal(ORDEN_SECUNDARIO, "cmd", TAM_RESTO)
    ejemplo.move_to([0, Y_ORDEN_SECUNDARIO, 0])

    scene.play(
        FadeOut(bloques),
        FadeOut(tipos_encabezado), FadeIn(resto_encabezado, shift=DOWN * 0.2),
        run_time=0.8,
    )
    scene.play(
        LaggedStart(*[FadeIn(f, shift=RIGHT * 0.12) for f in rejilla],
                    lag_ratio=0.25),
        run_time=2.0,
    )
    scene.play(FadeIn(ejemplo, shift=DOWN * 0.1), run_time=0.5)
    scene.next_slide()

    # ---------------------- El cuerpo, en la terminal ----------------------
    # Cada ``-m`` es un párrafo, y el rótulo de abajo lleva su ``-m`` del
    # mismo color que la línea: con eso se emparejan sin flechas.
    ultimo_encabezado = hacer_titulo(TITULOS[3])
    # El ancho se calcula contando la sangría: ``terminal`` mide sus filas
    # antes de que las continuaciones se corran, y sin esto la segunda se
    # saldría de la ventana.
    anchos = [
        linea_terminal(c, t, TAM_SESION).width + (SANGRIA_SESION if i else 0)
        for i, (c, t) in enumerate(SESION)
    ]
    sesion = terminal(SESION, tam=TAM_SESION, margen=MARGEN_SESION,
                      ancho=max(anchos) + 2 * MARGEN_SESION, nombre="terminal")
    sesion.move_to([0, Y_SESION, 0])
    for fila in sesion[1][1:]:
        fila.shift(RIGHT * SANGRIA_SESION)

    parrafos = VGroup()
    for i, (que_es, color) in enumerate(PARRAFOS):
        y = Y_PARRAFOS - i * PASO_PARRAFO
        parrafos.add(VGroup(
            texto("-m", TAM_PARRAFO, color=color).move_to(
                [X_PARRAFO, y, 0], LEFT),
            texto(que_es, TAM_PARRAFO, color=CLARO).move_to(
                [X_PARRAFO + BUFF_PARRAFO, y, 0], LEFT),
        ))

    scene.play(
        FadeOut(rejilla), FadeOut(ejemplo),
        FadeOut(resto_encabezado), FadeIn(ultimo_encabezado, shift=DOWN * 0.2),
        run_time=0.8,
    )
    scene.play(FadeIn(sesion[0]), run_time=0.5)
    teclear(scene, sesion, ritmo=0.35)
    for parrafo in parrafos:
        scene.play(FadeIn(parrafo, shift=RIGHT * 0.12), run_time=0.5)
    scene.next_slide()
