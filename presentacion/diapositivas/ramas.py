"""Diapositiva 14 — ramas: ``git branch`` y ``git switch``.

Misma forma que ``git_checkout`` y ``git_reflog``: la pantalla partida en dos
bandas que no se juntan.

  * **arriba, las ramas** — los commits y los cartelitos que los señalan;
  * **abajo, la terminal** — lo que se teclea y lo que git contesta.

Una rama no es una carpeta ni una copia: es una pegatina con un nombre pegada
a un commit, y ``HEAD`` es otra que dice en cuál estás tú. Crear una rama no
copia el proyecto, no duplica archivos y no tarda: **añade un nombre más
apuntando al commit en el que ya estabas**, y eso es exactamente lo que se ve
arriba —aparece un segundo cartelito sobre el mismo nodo— mientras la terminal
contesta con su ``Switched to a new branch``. Esa imagen es la que hace que la
gente pierda el respeto a ramificar.

A partir de ahí, cada ``commit`` mueve solo la pegatina en la que está HEAD:
la rama nueva avanza y ``main`` se queda clavado donde estaba. Y al volver, el
``git branch`` del final no es una lista más: el asterisco de ``* main`` es el
mismo HEAD que se acaba de ver moverse, así que cada línea enciende su
cartelito arriba.

La última pantalla es el reencuentro con ``checkout``: el mismo salto de rama,
tecleado con el comando de toda la vida y contestando exactamente lo mismo.
Ahí se cierra lo que quedó abierto en ``git_checkout`` —que hace demasiadas
cosas distintas— y se entiende por qué desde git 2.23 hay dos comandos
separados: ``switch`` para ramas y ``restore`` para archivos. Los dos funcionan;
el nuevo dice en su nombre lo que hace, y es el que conviene enseñar.

Para volver a la rama anterior sin escribir su nombre está ``git switch -``,
que se dice en voz alta y no necesita pantalla.
"""

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    FadeIn,
    FadeOut,
    Flash,
    GrowFromCenter,
    Indicate,
    LaggedStart,
    Line,
    VGroup,
)

from animaciones import teclear
from componentes import ALTO_BARRA, arista, linea_terminal, nodo_commit
from componentes import puntero, texto, ventana
from componentes import titulo as hacer_titulo
from estilo import OK, RAMA_FEATURE, RAMA_MAIN, SECUNDARIO

TITULO = "ramas"

# --- Arriba: las ramas -----------------------------------------------------
X_MAIN = (-5.2, -3.7, -2.2)
Y_MAIN = 0.9
X_RAMA = (-0.5, 1.0)
Y_RAMA = 2.1
RADIO = 0.36
TAM_HASH = 15
HASHES_MAIN = ("0e5f", "77ab", "9c1d")
HASHES_RAMA = ("a3c1", "b8e2")
NOMBRE_RAMA = "experimento"
TAM_PUNTERO = 15
BUFF_PUNTERO = 0.28       # del nodo a su cartelito, y del cartelito a HEAD

# --- El corte entre las dos mitades ----------------------------------------
Y_CORTE = 0.1
X_ROTULO = -6.35
Y_ROTULO = 1.5            # entre las dos filas: rotula la banda entera
TAM_ROTULO = 15

# --- Abajo: la terminal ----------------------------------------------------
ANCHO_CONSOLA = 7.0
ALTO_CONSOLA = 2.6
Y_CONSOLA = -1.9
MARGEN_CONSOLA = 0.5
TAM_SESION = 15
BUFF_SESION = 0.16
# Alto de la primera línea: fijo, para que al cambiar de tanda la sesión no
# suba y baje. Una terminal escribe desde arriba, tenga dos líneas o cinco.
Y_SESION = Y_CONSOLA + ALTO_CONSOLA / 2 - ALTO_BARRA - 0.25

# Una tanda por pantalla. La del medio son dos commits y nada más: cada línea
# hace nacer su nodo arriba, que es lo único que hay que ver.
SESIONES = (
    ((f"git switch -c {NOMBRE_RAMA}", "cmd"),
     (f"Switched to a new branch '{NOMBRE_RAMA}'", "ok")),
    (('git commit -m "prueba A"', "cmd"),
     ('git commit -m "prueba B"', "cmd")),
    (("git switch main", "cmd"),
     ("Switched to branch 'main'", "ok"),
     ("git branch", "cmd"),
     ("* main", "ok"),
     (f"  {NOMBRE_RAMA}", "out")),
    ((f"git checkout {NOMBRE_RAMA}", "cmd"),
     (f"Switched to branch '{NOMBRE_RAMA}'", "ok")),
)


def _marco_consola():
    """La ventana de la terminal, vacía y del tamaño de la tanda más larga."""
    return ventana(ANCHO_CONSOLA, ALTO_CONSOLA, "terminal", 14).move_to(
        [0, Y_CONSOLA, 0])


def _sesion(indice):
    """Las líneas de la tanda ``indice``, colocadas dentro de la ventana.

    Los espacios de la izquierda hay que reponerlos a mano: no dejan tinta, así
    que el ``arrange`` alinea por el primer carácter visible y la sangría de la
    salida de ``git branch`` se perdería —y es justo lo que hace que el nombre
    de la rama caiga bajo el de la actual, con el asterisco fuera—.
    """
    filas = VGroup(*[
        linea_terminal(c, t, TAM_SESION) for c, t in SESIONES[indice]
    ]).arrange(DOWN, buff=BUFF_SESION, aligned_edge=LEFT)
    unidad = linea_terminal("M", "out", TAM_SESION).width
    for fila, (contenido, _tipo) in zip(filas, SESIONES[indice]):
        sangria = len(contenido) - len(contenido.lstrip(" "))
        if sangria:
            fila.shift(RIGHT * unidad * sangria)
    filas.align_to([0, Y_SESION, 0], UP)
    return filas.align_to([-ANCHO_CONSOLA / 2 + MARGEN_CONSOLA, 0, 0], LEFT)


def construir(scene):
    encabezado = hacer_titulo(TITULO)

    # ---------------------- Las dos bandas ---------------------------------
    nodos = VGroup(*[
        nodo_commit(h, RAMA_MAIN, RADIO, TAM_HASH).move_to([x, Y_MAIN, 0])
        for x, h in zip(X_MAIN, HASHES_MAIN)
    ])
    aristas = VGroup(*[
        arista(nodos[i], nodos[i + 1], RAMA_MAIN, RADIO)
        for i in range(len(nodos) - 1)
    ])
    # Los cartelitos van siempre a la derecha de su commit, y HEAD a la derecha
    # del cartelito al que está pegado: así se lee "HEAD está en esta rama" sin
    # más explicación, y moverlo es toda la animación de ``switch``.
    p_main = puntero("main", RAMA_MAIN, TAM_PUNTERO)
    p_main.next_to(nodos[-1], RIGHT, buff=BUFF_PUNTERO)
    p_head = puntero("HEAD", OK, TAM_PUNTERO)
    p_head.next_to(p_main, RIGHT, buff=BUFF_PUNTERO)

    corte = Line([-6.6, Y_CORTE, 0], [6.6, Y_CORTE, 0],
                 color=SECUNDARIO, stroke_width=2).set_stroke(opacity=0.3)
    rotulo_ramas = texto("las ramas", TAM_ROTULO, color=SECUNDARIO)
    rotulo_ramas.move_to([X_ROTULO, Y_ROTULO, 0], LEFT)
    rotulo_consola = texto("la terminal", TAM_ROTULO, color=SECUNDARIO)
    rotulo_consola.move_to([X_ROTULO, Y_CONSOLA, 0], LEFT)
    marco_consola = _marco_consola()

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(
        LaggedStart(*[GrowFromCenter(n) for n in nodos], lag_ratio=0.25),
        FadeIn(rotulo_ramas, shift=RIGHT * 0.15), run_time=0.9,
    )
    scene.play(
        LaggedStart(*[Create(a) for a in aristas], lag_ratio=0.25),
        run_time=0.6,
    )
    scene.play(FadeIn(p_main, shift=LEFT * 0.1),
               FadeIn(p_head, shift=LEFT * 0.1), run_time=0.5)
    scene.play(Create(corte), FadeIn(rotulo_consola, shift=RIGHT * 0.15),
               run_time=0.6)
    scene.play(FadeIn(marco_consola), run_time=0.5)
    scene.next_slide()

    # ---------------------- 1. Crear la rama -------------------------------
    # No se copia nada: aparece un cartelito más sobre el mismo commit. El
    # flash es del nodo, no de la rama, para que se vea que es *ese* commit.
    sesion = _sesion(0)
    teclear(scene, VGroup(marco_consola, sesion), hasta=1, ritmo=0.32)

    p_rama = puntero(NOMBRE_RAMA, RAMA_FEATURE, TAM_PUNTERO)
    p_rama.next_to(nodos[-1], UP, buff=BUFF_PUNTERO)
    scene.play(FadeIn(p_rama, shift=DOWN * 0.12), run_time=0.5)
    scene.play(
        Flash(nodos[-1], color=RAMA_FEATURE, line_length=0.22, num_lines=14,
              flash_radius=RADIO + 0.35),
        run_time=0.6,
    )
    # Y HEAD se muda a la pegatina nueva: a partir de aquí los commits son suyos.
    scene.play(p_head.animate.next_to(p_rama, RIGHT, buff=BUFF_PUNTERO),
               run_time=0.8)
    teclear(scene, VGroup(marco_consola, sesion), desde=1, ritmo=0.32)
    scene.next_slide()

    # ---------------------- 2. Dos commits en la rama ----------------------
    scene.play(FadeOut(sesion), run_time=0.3)
    sesion = _sesion(1)

    anterior = nodos[-1]
    nuevos, ramales = VGroup(), VGroup()
    for i, (x, h) in enumerate(zip(X_RAMA, HASHES_RAMA)):
        teclear(scene, VGroup(marco_consola, sesion), desde=i, hasta=i + 1,
                ritmo=0.32)
        nodo = nodo_commit(h, RAMA_FEATURE, RADIO, TAM_HASH)
        nodo.move_to([x, Y_RAMA, 0])
        ramal = arista(anterior, nodo, RAMA_FEATURE, RADIO)
        scene.play(Create(ramal), GrowFromCenter(nodo), run_time=0.7)
        destino_rama = p_rama.copy().next_to(nodo, RIGHT, buff=BUFF_PUNTERO)
        destino_head = p_head.copy().next_to(destino_rama, RIGHT,
                                             buff=BUFF_PUNTERO)
        scene.play(
            p_rama.animate.move_to(destino_rama),
            p_head.animate.move_to(destino_head),
            run_time=0.5,
        )
        nuevos.add(nodo)
        ramales.add(ramal)
        anterior = nodo

    # main ni se ha enterado: sigue clavado en su commit.
    scene.play(Indicate(p_main, color=RAMA_MAIN, scale_factor=1.2),
               run_time=0.8)
    scene.next_slide()

    # ---------------------- 3. Volver, y ver las dos -----------------------
    scene.play(FadeOut(sesion), run_time=0.3)
    sesion = _sesion(2)
    teclear(scene, VGroup(marco_consola, sesion), hasta=1, ritmo=0.32)
    scene.play(p_head.animate.next_to(p_main, RIGHT, buff=BUFF_PUNTERO),
               run_time=0.9)
    teclear(scene, VGroup(marco_consola, sesion), desde=1, hasta=3, ritmo=0.32)

    # Y la lista no dice nada nuevo: cada línea es uno de los cartelitos de
    # arriba, y el asterisco es el HEAD que se acaba de ver moverse.
    for linea, cartel, color in ((3, p_main, RAMA_MAIN),
                                 (4, p_rama, RAMA_FEATURE)):
        teclear(scene, VGroup(marco_consola, sesion), desde=linea,
                hasta=linea + 1, ritmo=0.32)
        scene.play(Indicate(cartel, color=color, scale_factor=1.15),
                   run_time=0.5)
    scene.next_slide()

    # ---------------------- 4. Lo mismo, con checkout ----------------------
    # El comando de toda la vida hace este salto igual de bien, y contesta
    # exactamente lo mismo: se ve que ``switch`` no trae nada nuevo, solo
    # separa en dos lo que ``checkout`` hacía a la vez.
    scene.play(FadeOut(sesion), run_time=0.3)
    sesion = _sesion(3)
    teclear(scene, VGroup(marco_consola, sesion), hasta=1, ritmo=0.32)
    scene.play(p_head.animate.next_to(p_rama, RIGHT, buff=BUFF_PUNTERO),
               run_time=0.9)
    teclear(scene, VGroup(marco_consola, sesion), desde=1, ritmo=0.32)
    scene.wait(0.3)

    scene.next_slide()
