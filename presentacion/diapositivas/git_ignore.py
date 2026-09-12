"""Diapositiva 16 — ``.gitignore``: lo que no sube.

El portero del repositorio, y en un proyecto de datos hace más falta que en
ninguno. Se pone el primer día.

Primero el proyecto entero, con sus carpetas y sus archivos de verdad, y al
lado de cada uno si sube o no y **por qué no**, que es lo que convence:

  * ``data/`` y ``models/`` pesan gigas y git guarda una copia entera de cada
    versión, así que un ``.csv`` de dos gigas commiteado cinco veces son diez
    gigas en el repositorio para siempre;
  * ``.venv/`` se recrea en segundos con ``uv sync`` —lo que sí sube son el
    ``pyproject.toml`` y el ``uv.lock``, que son la receta— y además es de tu
    máquina: ni siquiera funcionaría en otra;
  * ``.env`` son credenciales, y eso no se sube nunca. Es el único de los tres
    que no tiene arreglo después.

Después el archivo que dice todo eso, con un bloque por motivo, y el matiz que
se le escapa a todo el mundo: ``.gitignore`` solo vale para lo que git
**todavía no sigue**. Si ya está commiteado hay que sacarlo antes con ``git rm
--cached``, y si era una credencial, además, darla por quemada.

Y al final, cómo se escribe una regla: el comodín, la carpeta entera, el ancla
de la raíz, el ``**`` de cualquier nivel y —la que nadie recuerda— el ``!`` de
la excepción, que va en verde porque hace justo lo contrario que las otras
cuatro. Con su trampa al pie: el ``!`` no rescata nada de una carpeta que está
ignorada entera, porque git ni siquiera entra a mirar.
"""

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    FadeIn,
    FadeOut,
    LaggedStart,
    VGroup,
)

from animaciones import teclear
from componentes import archivo, aspa, carpeta, terminal, texto, visto
from componentes import titulo as hacer_titulo
from estilo import AMBAR, CLARO, ERROR, OK, SECUNDARIO

TITULOS = (
    "Un proyecto de datos",
    ".gitignore",
    "Patrones y excepciones",
)

# --- Pantalla 1: el proyecto, pieza por pieza ------------------------------
# (es carpeta, nombre, ¿sube?, por qué no, color del motivo). El orden es el
# de un repositorio de datos cualquiera: primero lo pesado, luego el código.
PROYECTO = (
    (True, "data/", False, "2.1 GB", AMBAR),
    (True, "models/", False, "480 MB", AMBAR),
    (True, "notebooks/", True, "", None),
    (True, "src/", True, "", None),
    (True, ".venv/", False, "se recrea con uv sync", SECUNDARIO),
    (False, ".env", False, "credenciales", ERROR),
    (False, "pyproject.toml", True, "", None),
    (False, "uv.lock", True, "", None),
    (False, "README.md", True, "", None),
)
X_ICONO, X_NOMBRE = -4.7, -4.1
X_MARCA, X_MOTIVO = -0.5, -0.05
Y_PRIMERO = 2.0
PASO_FILA = 0.62
ALTO_ICONO = 0.42
TAM_NOMBRE = 21
TAM_MOTIVO = 18
APAGADO = 0.55                    # el ignorado sigue ahí, pero apagado

# --- Pantalla 2: el archivo que lo dice -----------------------------------
IGNORE = (
    ("datos y modelos, que pesan gigas", "com"),
    ("data/", "txt"),
    ("models/", "txt"),
    ("", "sep"),
    ("el entorno se recrea con uv sync", "com"),
    (".venv/", "txt"),
    ("__pycache__/", "txt"),
    ("", "sep"),
    ("credenciales que no se suben nunca", "com"),
    (".env", "txt"),
)
TAM_IGNORE = 18
Y_IGNORE = -0.1                   # el archivo entero cabe justo
BUFF_IGNORE = 0.15                # apretado: son diez renglones
# El matiz que se le escapa a todo el mundo, en una línea y accionable.
MATIZ = "si ya lo commiteaste, sácalo antes con git rm --cached"

# --- Pantalla 3: cómo se escribe una regla --------------------------------
# (patrón, qué coge, ¿lo ignora?). El último es la excepción, y va en verde
# porque hace lo contrario que los otros cuatro.
PATRONES = (
    ("*.csv", "cualquier archivo .csv", True),
    ("models/", "la carpeta entera", True),
    ("/notas.txt", "solo el de la raíz", True),
    ("**/tmp/", "en cualquier nivel", True),
    ("!data/muestra.csv", "menos este, que sí sube", False),
)
X_PATRON, X_MARCA_PATRON, X_QUE_COGE = -5.6, -1.5, -1.0
Y_PATRONES = 1.5
PASO_PATRON = 0.78
TAM_PATRON = 21
TAM_QUE_COGE = 18
TRAMPA = "una excepción no rescata nada de una carpeta ignorada"
TAM_TRAMPA = 21
Y_TRAMPA = -2.5


def _fila(es_carpeta, nombre, sube, motivo, color, y):
    """Una pieza del proyecto: su icono, su nombre y si sube o no."""
    tinte = CLARO if sube else SECUNDARIO
    icono = (carpeta(ALTO_ICONO, tinte) if es_carpeta
             else archivo("", tinte, ALTO_ICONO))
    icono.move_to([X_ICONO, y, 0])
    etiqueta = texto(nombre, TAM_NOMBRE, color=tinte)
    etiqueta.move_to([X_NOMBRE, y, 0], LEFT)
    marca = visto(OK) if sube else aspa(ERROR)
    marca.move_to([X_MARCA, y, 0])
    fila = VGroup(icono, etiqueta, marca)
    if not sube:
        VGroup(icono, etiqueta).set_opacity(APAGADO)
        fila.add(texto(motivo, TAM_MOTIVO, color=color).move_to(
            [X_MOTIVO, y, 0], LEFT))
    return fila


def construir(scene):
    encabezado = hacer_titulo(TITULOS[0])
    filas = VGroup(*[
        _fila(*pieza, Y_PRIMERO - i * PASO_FILA)
        for i, pieza in enumerate(PROYECTO)
    ])
    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(
        LaggedStart(*[FadeIn(f, shift=RIGHT * 0.15) for f in filas],
                    lag_ratio=0.25),
        run_time=2.4,
    )
    scene.next_slide()

    # ---------------------- El archivo que lo dice -------------------------
    otro_encabezado = hacer_titulo(TITULOS[1])
    fichero = terminal(IGNORE, tam=TAM_IGNORE, buff=BUFF_IGNORE,
                       nombre=".gitignore")
    fichero.move_to([0, Y_IGNORE, 0])
    matiz = texto(MATIZ, 16, color=SECUNDARIO).to_edge(DOWN, buff=0.6)

    scene.play(
        FadeOut(filas),
        FadeOut(encabezado), FadeIn(otro_encabezado, shift=DOWN * 0.2),
        run_time=0.8,
    )
    scene.play(FadeIn(fichero[0]), run_time=0.5)
    teclear(scene, fichero, ritmo=0.24)
    scene.play(FadeIn(matiz, shift=UP * 0.1), run_time=0.5)
    scene.next_slide()

    # ---------------------- Cómo se escribe una regla ----------------------
    # Cuatro formas de decir "esto no" y una de decir "esto sí", que es la
    # que nadie recuerda. El color hace la diferencia: la excepción es la
    # única en verde.
    ultimo_encabezado = hacer_titulo(TITULOS[2])
    reglas = VGroup()
    for i, (patron, que_coge, ignora) in enumerate(PATRONES):
        y = Y_PATRONES - i * PASO_PATRON
        color = CLARO if ignora else OK
        marca = aspa(ERROR) if ignora else visto(OK)
        reglas.add(VGroup(
            texto(patron, TAM_PATRON, color=color).move_to(
                [X_PATRON, y, 0], LEFT),
            marca.move_to([X_MARCA_PATRON, y, 0]),
            texto(que_coge, TAM_QUE_COGE, color=SECUNDARIO).move_to(
                [X_QUE_COGE, y, 0], LEFT),
        ))
    trampa = texto(TRAMPA, TAM_TRAMPA, color=AMBAR)
    trampa.move_to([0, Y_TRAMPA, 0])

    scene.play(
        FadeOut(fichero), FadeOut(matiz),
        FadeOut(otro_encabezado),
        FadeIn(ultimo_encabezado, shift=DOWN * 0.2),
        run_time=0.8,
    )
    scene.play(
        LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in reglas],
                    lag_ratio=0.3),
        run_time=1.8,
    )
    scene.play(FadeIn(trampa, shift=UP * 0.1), run_time=0.5)
    scene.next_slide()
