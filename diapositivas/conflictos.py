"""Diapositiva 16 — conflictos: qué son y cómo se salen.

Un conflicto no es un error de git ni un castigo: es git diciendo "aquí no
puedo decidir por ti". Solo pasa cuando dos ramas tocaron **las mismas líneas
del mismo archivo**; si una tocó el principio y otra el final, git las junta
solo y ni te enteras.

La pantalla clave es la del archivo con los marcadores, porque cuando aparecen
por primera vez asustan. Con los colores puestos —verde lo tuyo, morado lo que
viene de la otra rama— se leen de un vistazo, y una vez se lee, resolver es
elegir y borrar tres líneas.

La segunda pantalla es el procedimiento, y termina donde tiene que terminar:
``git merge --abort`` deja todo exactamente como estaba. Saber que existe es
lo que quita el miedo.
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

from animaciones import flecha, teclear
from componentes import terminal, texto
from componentes import titulo as hacer_titulo
from estilo import (
    CLARO,
    ERROR,
    OK,
    RAMA_FEATURE,
    SECUNDARIO,
)

ARCHIVO = (
    ("## Resultados", "txt"),
    ("<<<<<<< HEAD", "ok"),
    ("acierta un 87 %", "ok"),
    ("=======", "out"),
    ("acierta un 0.87", "alt"),
    (">>>>>>> experimento", "alt"),
)

# (fila del archivo, anotación, color)
LECTURAS = (
    (1, "lo tuyo: lo que hay en main", OK),
    (4, "lo que trae la otra rama", RAMA_FEATURE),
    (3, "la frontera entre los dos", SECUNDARIO),
)
X_LECTURA = 0.15

PASOS = (
    ("1", "git status", "te dice qué archivos están en conflicto"),
    ("2", "abre el archivo", "y decide qué se queda: uno, otro o los dos"),
    ("3", "borra los marcadores", "<<<<<<<   =======   >>>>>>>"),
    ("4", "git add informe.md", "así le dices a git que ya está resuelto"),
    ("5", "git commit", "git ya trae escrito el mensaje del merge"),
)

X_NUMERO = -6.2
X_PASO = -5.5
X_DETALLE = -2.3
Y_PRIMER_PASO = 1.55
PASO_FILA = 0.68


def construir(scene):
    encabezado = hacer_titulo("Cuando git no puede decidir")

    grito = texto("CONFLICT: merge conflict in informe.md", 17, color=ERROR)
    grito.move_to([0, 2.25, 0])

    fichero = terminal(ARCHIVO, tam=17, nombre="informe.md")
    fichero.move_to([-3.3, -0.75, 0])

    lecturas = VGroup()
    for indice, mensaje, color in LECTURAS:
        fila = fichero[1][indice]
        punta = flecha(
            [fichero[0][0].get_right()[0] + 0.1, fila.get_y(), 0],
            [X_LECTURA - 0.1, fila.get_y(), 0],
            color=color, buff=0, grosor=3,
        )
        etiqueta = texto(mensaje, 15, color=color)
        etiqueta.move_to([X_LECTURA, fila.get_y(), 0], LEFT)
        lecturas.add(VGroup(punta, etiqueta))

    cuando = texto(
        "solo pasa si las dos ramas tocaron las mismas líneas del mismo archivo",
        15, color=SECUNDARIO,
    ).to_edge(DOWN, buff=0.6)
    if cuando.width > 12.4:
        cuando.scale(12.4 / cuando.width)

    # ---------------------- Pantalla 1: el archivo marcado -----------------
    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(FadeIn(grito, shift=DOWN * 0.1), run_time=0.5)
    scene.play(FadeIn(fichero[0]), run_time=0.5)
    teclear(scene, fichero, ritmo=0.3)
    scene.play(
        LaggedStart(*[FadeIn(le, shift=RIGHT * 0.15) for le in lecturas],
                    lag_ratio=0.35),
        run_time=1.4,
    )
    scene.play(FadeIn(cuando), run_time=0.45)
    scene.next_slide()

    # ---------------------- Pantalla 2: cómo se sale -----------------------
    otro_encabezado = hacer_titulo("Resolverlo: cinco pasos")

    pasos = VGroup()
    for i, (numero, que, detalle) in enumerate(PASOS):
        y = Y_PRIMER_PASO - i * PASO_FILA
        n = texto(numero, 17, color=CLARO).move_to([X_NUMERO, y, 0], LEFT)
        cabeza = texto(que, 17, color=OK).move_to([X_PASO, y, 0], LEFT)
        cola = texto(detalle, 14, color=SECUNDARIO)
        cola.move_to([X_DETALLE, y, 0], LEFT)
        pasos.add(VGroup(n, cabeza, cola))

    salida = VGroup(
        texto("¿te has metido en un lío?", 16, color=CLARO),
        texto("git merge --abort", 20, color=ERROR),
        texto("deja todo exactamente como estaba antes del merge", 14,
              color=SECUNDARIO),
    ).arrange(DOWN, buff=0.18).move_to([0, -2.45, 0])

    scene.play(
        FadeOut(grito), FadeOut(fichero), FadeOut(lecturas), FadeOut(cuando),
        FadeOut(encabezado), FadeIn(otro_encabezado, shift=DOWN * 0.2),
        run_time=0.8,
    )
    scene.play(
        LaggedStart(*[FadeIn(p, shift=RIGHT * 0.15) for p in pasos],
                    lag_ratio=0.3),
        run_time=2.0,
    )
    scene.play(
        LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in salida],
                    lag_ratio=0.3),
        run_time=1.0,
    )
    scene.wait(0.3)

    scene.next_slide()
