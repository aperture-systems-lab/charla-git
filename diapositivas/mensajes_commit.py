"""Diapositiva 14 — el mensaje: lo único del commit que escribes tú.

El historial solo sirve si se puede leer, y un ``git log`` lleno de "cambios",
"update" y "ahora sí" no vale para nada. Escribir bien el mensaje cuesta diez
segundos y se los ahorra a quien venga —que casi siempre eres tú, tres meses
después.

Esta diapositiva es el argumento, y va montada sobre cosas concretas en vez de
sobre una lista de mensajes buenos y otra de malos:

  * el diff de verdad —tres renglones de un archivo, con su ``-`` en rojo y su
    ``+`` en verde— y debajo, solo, el mensaje que se escribe casi siempre.
    Ahí hay una pausa a propósito: es el momento de preguntar qué pasó en ese
    commit. Después, contra el mismo diff, el mensaje que sí lo dice;
  * y la consecuencia, que es ``log`` cobrada: dos ``git log --oneline`` uno
    al lado del otro, el mismo proyecto con los dos historiales. Uno no dice
    qué cambió ni por qué, que es exactamente para lo que sirve un historial;
    el otro sí.

Cómo se escribe ese mensaje bueno lo cuenta la siguiente,
``conventional_commits``, que importa de aquí las piezas del ejemplo para que
sea literalmente el mismo commit.
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
from componentes import aspa, linea_terminal, terminal, texto, visto
from componentes import titulo as hacer_titulo
from estilo import ERROR, OK

TITULOS = (
    "El mismo cambio, dos mensajes",
    "Crear un buen historial",
)

# El commit de ejemplo, despiezado: ``conventional_commits`` lo importa de
# aquí para explicarlo parte por parte.
TIPO, AMBITO = "fix", "(modelo)"
DESCRIPCION = "entrena sin el conjunto de prueba"
MENSAJE = f"{TIPO}: {DESCRIPCION}"

# --- Pantalla 1: el cambio, y lo que se escribe sobre él --------------------
# Un diff de verdad: su cabecera de hunk, el renglón que se va y el que entra.
# El cambio es el error clásico de la casa —entrenar con el conjunto de
# prueba y creerse la métrica—, así que el mensaje bueno tiene algo que
# decir. Sin sangría a la izquierda, que Pango se la come; la de dentro sí.
ARCHIVO = "modelo.py"
DIFF = (
    ("@@ -18,7 +18,7 @@ def entrenar(datos):", "out"),
    ("-   modelo.fit(X_test, y_test)", "err"),
    ("+   modelo.fit(X_train, y_train)", "ok"),
)
TAM_DIFF = 21                     # el diff es el protagonista: se lee grande
MARGEN_DIFF = 0.5
Y_DIFF = 1.15

# (mensaje, si vale). El mismo cambio, con el mensaje que no dice nada y con
# el que sí.
MENSAJES = (
    ('git commit -m "cambios"', False),
    (f'git commit -m "{MENSAJE}"', True),
)
TAM_MENSAJE = 21
Y_MENSAJES = (-1.3, -2.45)
X_MARCA = -6.2
BUFF_MARCA = 0.5
APAGADO = 0.5                     # lo que se atenúa el mensaje que no vale

# --- Pantalla 2: los dos historiales ---------------------------------------
LOG_MALO = (
    ("git log --oneline", "cmd"),
    ("3f2a cambios", "out"),
    ("9d1c update", "out"),
    ("7b0e asdf", "out"),
    ("1a4d ahora si", "out"),
)
LOG_BUENO = (
    ("git log --oneline", "cmd"),
    (f"3f2a {MENSAJE}", "out"),
    ("9d1c feat: anade el cargador de CSV", "out"),
    ("7b0e docs: explica como entrenar", "out"),
    ("1a4d test: cubre el caso vacio", "out"),
)
TAM_LOG = 14                      # lo más grande que cabe en media pantalla
ANCHO_LOG = 6.2
X_LOGS = (-3.4, 3.4)
Y_LOGS = -0.55                    # el bloque, centrado en el hueco del título
GLOSA_MALO = "no dice qué cambió ni por qué"
GLOSA_BUENO = "dice qué cambió y por qué"
TAM_GLOSA = 21
Y_GLOSA = 1.7


def _marcado(mob, vale):
    """Pone el ✓ o el ✗ a la izquierda de una línea, en su color."""
    marca = (visto(OK, tam=0.13) if vale else aspa(ERROR, tam=0.13))
    marca.move_to([X_MARCA, mob.get_y(), 0])
    if not vale:
        mob.set_opacity(APAGADO)
    return VGroup(marca, mob)


def construir(scene):
    encabezado = hacer_titulo(TITULOS[0])

    # ---------------------- El cambio, y sus dos mensajes ------------------
    diff = terminal(DIFF, tam=TAM_DIFF, nombre=ARCHIVO,
                    margen=MARGEN_DIFF)
    diff.move_to([0, Y_DIFF, 0])
    mensajes = VGroup(*[
        _marcado(
            linea_terminal(orden, "cmd", TAM_MENSAJE)
            .move_to([X_MARCA + BUFF_MARCA, y, 0], LEFT),
            vale,
        )
        for (orden, vale), y in zip(MENSAJES, Y_MENSAJES)
    ])

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(FadeIn(diff[0]), run_time=0.5)
    scene.play(
        LaggedStart(*[FadeIn(f, shift=RIGHT * 0.12) for f in diff[1]],
                    lag_ratio=0.35),
        run_time=1.1,
    )
    # El malo se queda solo en pantalla y con su pausa: es el momento de
    # preguntar qué pasó aquí. El bueno llega después, contra el mismo diff.
    scene.play(FadeIn(mensajes[0], shift=UP * 0.12), run_time=0.6)
    scene.next_slide()
    scene.play(FadeIn(mensajes[1], shift=UP * 0.12), run_time=0.6)
    scene.next_slide()

    # ---------------------- Y el historial que dejan -----------------------
    otro_encabezado = hacer_titulo(TITULOS[1])
    logs, glosas = VGroup(), VGroup()
    for lineas, x, glosa, color, marca in (
        (LOG_MALO, X_LOGS[0], GLOSA_MALO, ERROR, aspa(ERROR, tam=0.16)),
        (LOG_BUENO, X_LOGS[1], GLOSA_BUENO, OK, visto(OK, tam=0.16)),
    ):
        ventana = terminal(lineas, tam=TAM_LOG, ancho=ANCHO_LOG,
                           nombre="terminal")
        logs.add(ventana.move_to([x, Y_LOGS, 0]))
        rotulo = texto(glosa, TAM_GLOSA, color=color)
        glosas.add(VGroup(marca, rotulo).arrange(RIGHT, buff=0.25)
                   .move_to([x, Y_GLOSA, 0]))

    scene.play(
        FadeOut(diff), FadeOut(mensajes),
        FadeOut(encabezado), FadeIn(otro_encabezado, shift=DOWN * 0.2),
        run_time=0.8,
    )
    scene.play(*[FadeIn(v[0]) for v in logs], run_time=0.5)
    for ventana, glosa in zip(logs, glosas):
        teclear(scene, ventana, ritmo=0.22)
        scene.play(FadeIn(glosa, shift=DOWN * 0.1), run_time=0.5)
    scene.next_slide()
