"""Diapositiva 6 — ¿tiene sentido aprender git ahora que la IA escribe todo?

La respuesta, contada como lo que le pasa a alguien de verdad:

  1. Le pregunta a un chatbot cómo subir su proyecto. La IA contesta bien: los
     tres comandos son exactamente los que hacen falta.
  2. Los ejecuta. Y ``git add .`` significa "todo lo que hay en la carpeta",
     incluido el ``.env`` con la clave de la API. Eso la IA no se lo preguntó,
     porque no era su trabajo saber qué hay en esa carpeta.
  3. El repositorio es público. Los bots que rastrean claves en GitHub tardan
     minutos, y la factura la paga él.
  4. La conclusión: los comandos los da cualquier IA en dos segundos. Lo que
     no da es el criterio de qué subir y qué no, que es justo donde está el
     desastre. Y aquí el error no se deshace: una clave publicada ya está
     publicada aunque borres el commit.

Es la diapositiva que justifica el resto de la charla, así que va después de
la historia y antes de los comandos.
"""

from manim import (
    Circle,
    DOWN,
    Line,
    PI,
    LEFT,
    RIGHT,
    UP,
    Create,
    FadeIn,
    FadeOut,
    Flash,
    GrowFromCenter,
    LaggedStart,
    VGroup,
)

from animaciones import pulso, teclear
from componentes import (
    archivo,
    aspa,
    billete,
    burbuja,
    puntero,
    robot,
    separador,
    terminal,
    texto,
    visto,
    zona,
)
from componentes import titulo as hacer_titulo
from estilo import AMBAR, CLARO, ERROR, OK, PRIMARIO, SECUNDARIO

TITULO = "¿Y en la era de la IA?"

# --- Acto 1: la pregunta y la respuesta correcta ---------------------------
PREGUNTA = "¿cómo subo mi proyecto a GitHub?"
RESPUESTA = (
    ("git add .", "cmd"),
    ('git commit -m "primer commit"', "cmd"),
    ("git push", "cmd"),
)
X_PREGUNTA, Y_PREGUNTA = 6.3, 1.85      # borde derecho de la burbuja
X_RESPUESTA, Y_RESPUESTA = -6.4, -0.9   # borde izquierdo de la ventana

# --- Acto 2: qué significa el punto de "git add ." -------------------------
ARCHIVOS = (
    ("main.py", SECUNDARIO),
    ("README.md", SECUNDARIO),
    (".env", ERROR),
)
X_ARCHIVOS = -3.35
Y_ARCHIVOS = -0.15
ALTO_ARCHIVO = 1.15
SECRETO = "OPENAI_API_KEY=sk-proj-8fK2vQ…"

# --- Acto 3: la factura ----------------------------------------------------
# El dibujo ya dice de qué va cada cifra, así que no llevan pie.
CIFRAS = (
    ("8 min", AMBAR, "robot"),
    ("-4.200 USD", ERROR, "billete"),
)

# --- Acto 4: la conclusión, a dos columnas ---------------------------------
# A la izquierda lo que la IA resuelve —teclear— y a la derecha lo que no:
# decidir qué entra y qué no. Lo segundo va dibujado, no escrito.
COMANDOS = (
    ("git add .", "cmd"),
    ('git commit -m "..."', "cmd"),
    ("git push", "cmd"),
)
CRIBA = (
    ("main.py", SECUNDARIO, True),
    ("README.md", SECUNDARIO, True),
    (".env", ERROR, False),
)
X_IZQUIERDA, X_DERECHA = -3.5, 3.4
Y_COLUMNAS = 0.15
BUFF_CRIBA = 0.5
X_NOMBRE, X_MARCA = 0.8, 3.7      # columnas dentro de cada fila de la criba
PIES = (("los comandos", SECUNDARIO), ("el criterio", PRIMARIO))
Y_PIE = -2.3


def _acto_chat():
    """La pregunta del alumno y la respuesta —correcta— del asistente."""
    pregunta = burbuja("tú", PREGUNTA, SECUNDARIO, tam=24, cola=RIGHT)
    pregunta.move_to([X_PREGUNTA, Y_PREGUNTA, 0], RIGHT)
    respuesta = terminal(RESPUESTA, tam=24, nombre="asistente")
    respuesta.move_to([X_RESPUESTA, Y_RESPUESTA, 0], LEFT)
    # El veredicto va como chulo y no como frase: se lee de un vistazo.
    chulo = VGroup(
        Circle(radius=0.62, color=OK, stroke_width=5),
        visto(OK, tam=0.3, grosor=9),
    )
    chulo.next_to(respuesta, RIGHT, buff=1.1)
    return pregunta, respuesta, chulo


def _acto_carpeta():
    """Los tres archivos de la carpeta y lo que el punto se lleva por delante."""
    iconos = VGroup(*[
        VGroup(archivo(nombre, color, alto=ALTO_ARCHIVO, tam=22))
        for nombre, color in ARCHIVOS
    ]).arrange(RIGHT, buff=0.9).move_to([X_ARCHIVOS, Y_ARCHIVOS, 0])

    caja = zona("git add .", PRIMARIO, ancho=iconos.width + 1.2,
                alto=iconos.height + 1.1, tam=26)
    caja.move_to(iconos)

    # El aviso cuelga por fuera de la caja, no encima de su borde.
    env = iconos[-1]
    aviso = puntero("tu API key", ERROR, 22)
    aviso.next_to(caja, DOWN, buff=0.35).set_x(env.get_center()[0])
    secreto = terminal([(SECRETO, "err")], tam=19, nombre=".env")
    secreto.next_to(caja, RIGHT, buff=0.7)
    return iconos, caja, env, aviso, secreto


def _acto_factura(anclaje):
    """Las dos cifras del desastre, cada una con su dibujo al lado."""
    filas = VGroup()
    for cifra, color, dibujo in CIFRAS:
        estampa = robot(1.8, AMBAR) if dibujo == "robot" else billete(2.2)
        filas.add(VGroup(
            estampa, texto(cifra, 50, color=color),
        ).arrange(RIGHT, buff=0.6))
    filas.arrange(DOWN, buff=1.8, aligned_edge=LEFT)
    filas.next_to(anclaje, RIGHT, buff=0.65)
    return filas


def _fila_criba(nombre, color, pasa):
    """Un archivo y su veredicto: entra o no entra."""
    icono = archivo(color=color, alto=0.9)
    marca = visto(OK, tam=0.22, grosor=7) if pasa else aspa(ERROR, 0.22, 7)
    return VGroup(
        icono,
        texto(nombre, 26, color=color).move_to([X_NOMBRE, 0, 0], LEFT),
        marca.move_to([X_MARCA, 0, 0]),
    )


def _acto_conclusion():
    """Lo que la IA teclea por ti, y lo que tienes que decidir tú.

    Sin una sola frase: a la izquierda los comandos resueltos, a la derecha la
    criba que nadie te da hecha, y la ficha de cada columna poniéndoles nombre.
    """
    comandos = terminal(COMANDOS, tam=26, nombre="asistente")
    comandos.move_to([X_IZQUIERDA, Y_COLUMNAS, 0])

    criba = VGroup(*[
        _fila_criba(*fila) for fila in CRIBA
    ]).arrange(DOWN, buff=BUFF_CRIBA, aligned_edge=LEFT)
    criba.move_to([X_DERECHA, Y_COLUMNAS, 0])

    # El filete mide lo que la columna más alta de las dos.
    division = separador(largo=max(comandos.height, criba.height) / 2,
                         grosor=2)
    division.set_opacity(0.3).rotate(PI / 2).move_to([0, Y_COLUMNAS, 0])

    fichas = VGroup(*[
        puntero(etiqueta, color, 26).move_to([x, Y_PIE, 0])
        for (etiqueta, color), x in zip(PIES, (X_IZQUIERDA, X_DERECHA))
    ])
    return comandos, criba, division, fichas


def construir(scene):
    encabezado = hacer_titulo(TITULO)
    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)

    # ---------------------- Acto 1: le pregunta a la IA --------------------
    pregunta, respuesta, chulo = _acto_chat()
    scene.play(FadeIn(pregunta, shift=UP * 0.15, scale=0.95), run_time=0.7)
    scene.play(FadeIn(respuesta[0]), run_time=0.5)
    teclear(scene, respuesta, ritmo=0.5)
    scene.play(GrowFromCenter(chulo), run_time=0.6)
    scene.next_slide()

    # ---------------------- Acto 2: y lo ejecuta ---------------------------
    iconos, caja, env, aviso, secreto = _acto_carpeta()
    scene.play(FadeOut(pregunta), FadeOut(respuesta), FadeOut(chulo),
               run_time=0.6)
    scene.play(
        LaggedStart(*[FadeIn(i, shift=UP * 0.15) for i in iconos],
                    lag_ratio=0.3),
        run_time=1.1,
    )
    # El punto: la caja se traga los tres, no los dos que él tenía en la cabeza.
    scene.play(Create(caja), run_time=0.8)
    scene.play(
        Flash(env, color=ERROR, line_length=0.35, num_lines=18,
              flash_radius=0.9),
        run_time=0.7,
    )
    scene.play(FadeIn(aviso, shift=UP * 0.12), run_time=0.5)
    scene.play(FadeIn(secreto[0]), run_time=0.5)
    teclear(scene, secreto, ritmo=0.5)
    scene.next_slide()

    # ---------------------- Acto 3: la factura -----------------------------
    repo = zona("GitHub · público", SECUNDARIO, ancho=5.4, alto=4.0, tam=24)
    repo.move_to([-4.0, -0.25, 0])
    copia = secreto.copy().scale(0.9).move_to(repo[0])
    factura = _acto_factura(repo)

    scene.play(
        FadeOut(iconos), FadeOut(caja), FadeOut(aviso),
        secreto.animate.scale(0.9).move_to(repo[0]),
        Create(repo),
        run_time=1.0,
    )
    # El robo: la clave se va, y no vuelve.
    scene.play(pulso(repo[0][1], ERROR, 0.9, ancho=8), run_time=0.9)
    # El bot llega...
    bot, cifra_bot = factura[0]
    scene.play(FadeIn(bot, shift=LEFT * 0.4), run_time=0.6)
    scene.play(FadeIn(cifra_bot, scale=0.9), run_time=0.55)

    # ...y el dinero se borra: una barra lo recorre y el billete se apaga.
    plata, cifra_plata = factura[1]
    scene.play(FadeIn(plata, shift=UP * 0.15), run_time=0.5)
    barrido = Line(plata.get_left(), plata.get_right())
    scene.play(
        plata.animate.set_opacity(0.12),
        pulso(barrido, ERROR, 0.9, ancho=14, franja=0.5),
        run_time=0.9,
    )
    scene.play(FadeIn(cifra_plata, scale=0.9), run_time=0.5)
    scene.play(
        Flash(cifra_plata, color=ERROR, line_length=0.3, num_lines=16,
              flash_radius=1.1),
        run_time=0.6,
    )
    scene.next_slide()

    # ---------------------- Acto 4: la conclusión --------------------------
    comandos, criba, division, fichas = _acto_conclusion()
    scene.play(
        FadeOut(repo), FadeOut(secreto), FadeOut(factura), FadeOut(copia),
        run_time=0.7,
    )
    # Primero lo fácil: los comandos, que ya están resueltos.
    scene.play(FadeIn(comandos[0]), run_time=0.5)
    teclear(scene, comandos, ritmo=0.35)
    scene.play(FadeIn(fichas[0], shift=UP * 0.12), run_time=0.5)
    scene.play(Create(division), run_time=0.5)

    # Y luego lo que no: decidir qué entra.
    scene.play(
        LaggedStart(*[FadeIn(f, shift=RIGHT * 0.15) for f in criba],
                    lag_ratio=0.4),
        run_time=1.2,
    )
    scene.play(FadeIn(fichas[1], shift=UP * 0.12), run_time=0.5)
    scene.wait(0.3)

    scene.next_slide()
