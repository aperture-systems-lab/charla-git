"""Diapositiva 7 — la terminal: dónde estás y cómo te mueves.

Va justo antes de instalar git porque de aquí en adelante todo se teclea, y
con público que nunca ha salido del explorador de archivos conviene dedicarle
tres minutos. Tres actos:

  1. Por qué tecleando y no a botonazos: la misma encuesta que cerró
     ``historia`` pregunta también *cómo* se usa el control de versiones, y
     ocho de cada diez contestan que por línea de comandos.
  2. Dónde estás: el árbol de carpetas con la carpeta actual marcada, las
     dos rutas relativas que salen en todos los comandos —``.`` es esta
     carpeta y ``..`` la de arriba— y, debajo, la ruta absoluta de la misma
     carpeta.
  3. Cómo te mueves: ``pwd``, ``ls``, ``mkdir`` y ``cd``, tecleados en orden y
     con lo que hace cada uno al lado.

Fuente:
  * Stack Overflow Developer Survey 2022 — "Version control"
    (https://survey.stackoverflow.co/2022/#technology-version-control), la
    misma página de la que sale la gráfica de ``historia``: es la otra
    pregunta, la de cómo interactúan con el control de versiones. Respuesta
    múltiple, así que los porcentajes no suman 100.

La gráfica lleva el mismo tratamiento que la de ``historia`` —una sola serie,
de mayor a menor, acento de marca en la respuesta que importa y gris recesivo
en el resto— justamente para que se reconozca: es la misma encuesta.
"""

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    FadeIn,
    FadeOut,
    GrowFromEdge,
    LaggedStart,
    Transform,
    VGroup,
)

from animaciones import flecha
from componentes import barra, puntero, terminal, texto
from componentes import titulo as hacer_titulo
from estilo import CLARO, PRIMARIO, SECUNDARIO

TITULO_GRAFICA = "¿Y cómo lo usan?"
TITULO_ARBOL = "Rutas y carpetas"
TITULO_COMANDOS = "Comandos básicos"

# --- Acto 1: la gráfica ----------------------------------------------------
# Stack Overflow Developer Survey 2022 — "Version control", la pregunta de con
# qué interactúan con el control de versiones. Las etiquetas van traducidas y
# acortadas para que quepan: en la encuesta son "version control hosting
# service web GUI" (la web de GitHub) y "dedicated version control GUI
# application" (una app aparte, tipo GitHub Desktop).
INTERACCION = (
    ("línea de comandos", 83.57),
    ("editor de código", 54.49),
    ("la web del servicio", 28.44),
    ("app de escritorio", 26.37),
)
X_ETIQUETA = -2.8        # borde derecho de los nombres
X_BARRA = -2.5           # donde arrancan todas las barras
LARGO_100 = 7.4          # cuánto mide el 100 %
ALTO_TRAZO = 0.6
Y_PRIMERA_BARRA = 1.9
PASO_BARRA = 1.25
FUENTE = "Stack Overflow Developer Survey 2022"
Y_FUENTE = -2.95

# --- Acto 2: el árbol ------------------------------------------------------
# Ninguna línea empieza por espacio: el dibujo se sostiene con los propios
# palotes del árbol, que es lo que mantiene las ramas a plomo.
ARBOL = (
    ("proyectos/", CLARO),
    ("├── charla-git/", PRIMARIO),
    ("│   ├── datos/", SECUNDARIO),
    ("│   ├── main.py", SECUNDARIO),
    ("│   └── README.md", SECUNDARIO),
    ("└── notas/", SECUNDARIO),
)
AQUI = 1                 # la línea en la que estás parado
TAM_ARBOL = 32
# Los renglones van pegados a propósito: si se separan, los palotes del
# árbol dejan de tocarse y el dibujo se rompe.
BUFF_ARBOL = 0.06
X_ARBOL = -6.2           # borde izquierdo del árbol
Y_ARBOL = 0.0
# Los dos atajos, cada uno a la altura de la línea a la que apunta.
ATAJOS = (
    ("..", "la carpeta de arriba", 0),
    (".", "esta carpeta, la de ahora", AQUI),
)
LARGO_FLECHA = 1.1
X_GLOSA = 0.3            # columna fija: las glosas arrancan todas a la misma x
# Debajo del árbol, la misma carpeta escrita como la contesta ``pwd``. Los dos
# atajos de arriba son rutas relativas —significan una cosa u otra según dónde
# estés parado—; esta es la absoluta, la que sale del disco y vale desde
# cualquier sitio. Y es el puente con el acto siguiente, donde la terminal
# contesta exactamente esto.
RUTA_PIE = "ruta absoluta:"
RUTA = "/c/Users/carmen/proyectos/charla-git"
Y_RUTA = -2.7

# --- Acto 3: los comandos --------------------------------------------------
# Los cuatro se enseñan de uno en uno: cada paso estrena su pegatina en la
# columna de la izquierda y sus líneas en la terminal, y ahí se para. Las
# pegatinas ya vistas se quedan, así que al final la pantalla es la chuleta.
SESION = (
    ("pwd", "cmd"),
    ("/c/Users/carmen/proyectos", "out"),
    ("ls", "cmd"),
    ("charla-git/  notas/", "out"),
    ("mkdir git-101", "cmd"),
    ("ls", "cmd"),
    ("charla-git/  git-101/  notas/", "ok"),   # ahí está: verde, ya existe
    ("cd git-101", "cmd"),
    ("cd ..", "cmd"),
)
GLOSAS = (
    ("pwd", "¿dónde estoy?"),
    ("ls", "¿qué hay aquí?"),
    ("mkdir", "crear una carpeta"),
    ("cd", "moverte"),
)
# Un paso por pausa: (pegatina que se estrena, hasta qué línea llega la
# terminal, qué carpeta pasa a marcar la barra de título de la ventana).
PASOS = (
    (0, 2, None),
    (1, 4, None),
    (2, 7, None),
    (3, 8, "proyectos/git-101"),   # entras: la barra lo dice y se pone cian
    (None, 9, "proyectos"),        # y con cd .. vuelves a donde estabas
)
CARPETA = "proyectos"    # lo que marca la barra de título al empezar
X_FICHA = -6.4           # borde izquierdo de las pegatinas
X_QUE_HACE = -4.6        # columna del texto, a la derecha de la pegatina
BUFF_GLOSAS = 0.85
X_SESION = 2.9
Y_SESION = 0.0
TAM_SESION = 19
NOTA = "en el cmd de Windows, ls se llama dir"
Y_NOTA = -3.05


def _grafica():
    """Las cuatro respuestas, de mayor a menor, y la fuente debajo."""
    filas = VGroup()
    for i, (nombre, porcentaje) in enumerate(INTERACCION):
        y = Y_PRIMERA_BARRA - i * PASO_BARRA
        destacado = i == 0          # la terminal; el resto se lee como contexto
        color = PRIMARIO if destacado else SECUNDARIO
        etiqueta = texto(nombre, 21, color=CLARO if destacado else SECUNDARIO)
        etiqueta.move_to([X_ETIQUETA, y, 0], RIGHT)
        trazo = barra(LARGO_100 * porcentaje / 100, ALTO_TRAZO, color,
                      1.0 if destacado else 0.55)
        trazo.move_to([X_BARRA, y, 0], LEFT)
        valor = texto(f"{porcentaje:.2f} %".replace(".", ","), 21,
                      color=CLARO if destacado else SECUNDARIO)
        valor.next_to(trazo, RIGHT, buff=0.22)
        filas.add(VGroup(etiqueta, trazo, valor))

    fuente = texto(FUENTE, 17, color=SECUNDARIO).set_opacity(0.7)
    fuente.move_to([0, Y_FUENTE, 0])
    return filas, fuente


def _arbol():
    """El árbol de carpetas, con la carpeta actual en el color de marca."""
    lineas = VGroup(*[
        texto(contenido, TAM_ARBOL, color=color) for contenido, color in ARBOL
    ]).arrange(DOWN, buff=BUFF_ARBOL, aligned_edge=LEFT)
    return lineas.move_to([X_ARBOL, Y_ARBOL, 0], LEFT)


def _ruta():
    """La misma carpeta del árbol, escrita entera desde la raíz del disco."""
    linea = VGroup(
        texto(RUTA_PIE, 20, color=SECUNDARIO),
        texto(RUTA, 20, color=PRIMARIO),
    ).arrange(RIGHT, buff=0.3)
    return linea.move_to([X_ARBOL, Y_RUTA, 0], LEFT)


def _atajos(lineas):
    """``.`` y ``..``, cada uno con su flecha a la línea que nombra.

    Las flechas arrancan todas de la misma x y mueren pegadas al final de su
    línea, que es distinta en cada caso: así se ve a cuál apunta cada una sin
    dibujar guías.
    """
    x_salida = lineas.get_right()[0] + 0.25 + LARGO_FLECHA
    filas = VGroup()
    for simbolo, glosa, indice in ATAJOS:
        color = PRIMARIO if indice == AQUI else CLARO
        y = lineas[indice].get_center()[1]
        punta = flecha([x_salida, y, 0],
                       [lineas[indice].get_right()[0] + 0.2, y, 0],
                       color=color, buff=0.05)
        ficha = puntero(simbolo, color, 24).move_to([x_salida + 0.2, y, 0], LEFT)
        que_es = texto(glosa, 22, color=color).move_to([X_GLOSA, y, 0], LEFT)
        filas.add(VGroup(punta, ficha, que_es))
    return filas


def _comandos():
    """La sesión de terminal y, a su izquierda, qué hace cada comando."""
    # Renglones apretados: son nueve, y una terminal de verdad tampoco los
    # separa. La barra de título lleva la carpeta en la que estás.
    sesion = terminal(SESION, tam=TAM_SESION, nombre=CARPETA, margen=0.5,
                      buff=0.16)
    sesion.move_to([X_SESION, Y_SESION, 0])

    glosas = VGroup()
    for comando, que_hace in GLOSAS:
        ficha = puntero(comando, PRIMARIO, 24).move_to([X_FICHA, 0, 0], LEFT)
        glosas.add(VGroup(
            ficha, texto(que_hace, 22).move_to([X_QUE_HACE, 0, 0], LEFT),
        ))
    glosas.arrange(DOWN, buff=BUFF_GLOSAS, aligned_edge=LEFT)
    glosas.move_to([X_FICHA, Y_SESION, 0], LEFT)

    nota = texto(NOTA, 17, color=SECUNDARIO).set_opacity(0.7)
    nota.move_to([X_FICHA, Y_NOTA, 0], LEFT)
    return sesion, glosas, nota


def construir(scene):
    # ---------------------- Acto 1: la encuesta ----------------------------
    encabezado = hacer_titulo(TITULO_GRAFICA)
    filas, fuente = _grafica()

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    for etiqueta, trazo, valor in filas:
        scene.play(
            FadeIn(etiqueta, shift=RIGHT * 0.1),
            GrowFromEdge(trazo, LEFT),
            run_time=0.55,
        )
        scene.play(FadeIn(valor, shift=LEFT * 0.1), run_time=0.25)
    scene.play(FadeIn(fuente), run_time=0.5)
    scene.next_slide()

    # ---------------------- Acto 2: el árbol -------------------------------
    encabezado_arbol = hacer_titulo(TITULO_ARBOL)
    lineas = _arbol()
    atajos = _atajos(lineas)
    ruta = _ruta()

    scene.play(
        FadeOut(filas), FadeOut(fuente),
        FadeOut(encabezado), FadeIn(encabezado_arbol, shift=DOWN * 0.2),
        run_time=0.8,
    )
    # El árbol se dibuja de arriba abajo, como lo escribiría el propio comando.
    scene.play(
        LaggedStart(*[FadeIn(linea, shift=RIGHT * 0.12) for linea in lineas],
                    lag_ratio=0.3),
        run_time=1.3,
    )
    for fila in atajos:
        scene.play(FadeIn(fila, shift=LEFT * 0.12), run_time=0.6)
    scene.play(FadeIn(ruta, shift=UP * 0.1), run_time=0.5)
    scene.next_slide()

    # ---------------------- Acto 3: los comandos ---------------------------
    encabezado_comandos = hacer_titulo(TITULO_COMANDOS)
    sesion, glosas, nota = _comandos()
    carpeta = sesion[0][3]          # el rótulo de la barra de título

    scene.play(
        FadeOut(lineas), FadeOut(atajos), FadeOut(ruta),
        FadeOut(encabezado_arbol),
        FadeIn(encabezado_comandos, shift=DOWN * 0.2),
        run_time=0.8,
    )
    scene.play(FadeIn(sesion[0]), run_time=0.5)

    # Un comando por pausa: su pegatina y sus líneas, y a esperar.
    desde = 0
    for paso, (glosa, hasta, destino) in enumerate(PASOS):
        entradas = [
            FadeIn(fila, shift=RIGHT * 0.12) for fila in sesion[1][desde:hasta]
        ]
        if glosa is not None:
            entradas.append(FadeIn(glosas[glosa], shift=RIGHT * 0.12))
        scene.play(LaggedStart(*entradas, lag_ratio=0.6),
                   run_time=0.45 * len(entradas) + 0.3)
        if destino is not None:
            # Moverse se ve en la barra de título, igual que en tu terminal.
            rotulo = texto(destino, TAM_SESION - 2,
                           color=PRIMARIO if destino != CARPETA else SECUNDARIO)
            scene.play(Transform(carpeta, rotulo.move_to(carpeta)),
                       run_time=0.5)
        desde = hasta
        if paso < len(PASOS) - 1:
            scene.next_slide()

    scene.play(FadeIn(nota), run_time=0.5)
    scene.wait(0.3)

    scene.next_slide()
