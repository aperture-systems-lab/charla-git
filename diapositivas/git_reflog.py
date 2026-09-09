"""Diapositiva 20 — ``git reflog``: la red debajo del trapecio.

Cierra el tramo que abren ``git_reset`` y ``git_checkout``, y usa la misma
forma que ``git_checkout``: la pantalla partida en dos bandas que no se juntan.

  * **arriba, la rama** — la cadena de commits con ``HEAD`` y ``main``;
  * **abajo, la terminal** — lo que se teclea y lo que git contesta.

Aquí el historial no aparece hecho: se hace delante. Se teclean cuatro
``commit`` uno detrás de otro y con cada uno nace su commit arriba y la rama
avanza —una sesión de trabajo normal, la de cualquiera—, y solo entonces llega
el ``reset --hard HEAD~2`` que parece comerse los dos últimos: se apagan, la
rama retrocede, y ahí está el susto.

Ese orden es todo el truco de la diapositiva. Cuando después sale ``git
reflog``, la lista no es una salida rara que hay que descifrar: **cada línea es
uno de los comandos que se acaban de ver**, en orden inverso, y por eso se lee
sola. Las dos que corresponden a los commits huérfanos encienden su nodo en
ámbar; las de los que nunca salieron de la rama solo parpadean.

Y el remate: con el hash que acaba de leer, otro ``reset --hard`` los devuelve.
Git apunta cada movimiento de HEAD y guarda esas anotaciones treinta días; con
eso en la cabeza, experimentar deja de dar miedo, que es justo con lo que hay
que salir de este tramo.
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
    Line,
    Transform,
    VGroup,
)

from animaciones import teclear
from componentes import ALTO_BARRA, linea_terminal, nodo_commit, puntero, texto
from componentes import titulo as hacer_titulo
from componentes import ventana
from estilo import AMBAR, OK, RAMA_MAIN, SECUNDARIO

TITULO = "git reflog"

# --- Arriba: la rama -------------------------------------------------------
X_CADENA = (-4.6, -1.55, 1.55, 4.6)
Y_CADENA = 2.15
RADIO = 0.38
TAM_HASH = 15
HASHES = ("0e5f", "77ab", "9c1d", "3f2a")
PERDIDOS = (2, 3)         # los que el reset deja sin nadie que los señale
ATRAS = 1                 # a dónde retrocede la rama
TAM_PUNTERO = 15
BUFF_PUNTERO = 0.3
APAGADO = 0.3             # lo que queda de un commit huérfano

# --- El corte entre las dos mitades ----------------------------------------
Y_CORTE = 0.35
X_ROTULO = -6.35
TAM_ROTULO = 15

# --- Abajo: la terminal ----------------------------------------------------
ANCHO_CONSOLA = 8.0
ALTO_CONSOLA = 3.05
Y_CONSOLA = -1.9
MARGEN_CONSOLA = 0.5
TAM_SESION = 15
BUFF_SESION = 0.16
# Alto de la primera línea: fijo, para que al cambiar de tanda la sesión no
# suba y baje. Una terminal escribe desde arriba, tenga dos líneas o seis.
Y_SESION = Y_CONSOLA + ALTO_CONSOLA / 2 - ALTO_BARRA - 0.25

# --- La sesión, en tres tandas ---------------------------------------------
# La primera es la clave de todo: se ve *hacerse* el historial —cuatro commits,
# uno por línea— antes de que el reset se lo lleve, así que cuando salga el
# reflog cada línea de la lista será uno de estos comandos y no habrá nada que
# descifrar. El ``git log --oneline`` sale dos veces a propósito, y es el
# testigo de la diapositiva: primero para enseñar que los de delante ya no
# aparecen, y al final para enseñar que han vuelto.
SESIONES = (
    (('git commit -m "primer commit"', "cmd"),
     ('git commit -m "añade el análisis"', "cmd"),
     ('git commit -m "corrige la tabla 2"', "cmd"),
     ('git commit -m "reescribe conclusiones"', "cmd")),
    (("git reset --hard HEAD~2", "cmd"),
     ("HEAD is now at 77ab21", "avi"),
     ("git log --oneline", "cmd"),
     ("77ab21 añade el análisis", "out"),
     ("0e5f33 primer commit", "out")),
    (("git reflog", "cmd"),
     ("77ab21 HEAD@{0}: reset: moving to HEAD~2", "out"),
     ("3f2a1b HEAD@{1}: commit: reescribe conclusiones", "ok"),
     ("9c1d04 HEAD@{2}: commit: corrige la tabla 2", "ok"),
     ("77ab21 HEAD@{3}: commit: añade el análisis", "out"),
     ("0e5f33 HEAD@{4}: commit (initial): primer commit", "out")),
    (("git reset --hard 3f2a1b", "cmd"),
     ("git log --oneline", "cmd"),
     ("3f2a1b reescribe conclusiones", "ok"),
     ("9c1d04 corrige la tabla 2", "ok"),
     ("77ab21 añade el análisis", "out"),
     ("0e5f33 primer commit", "out")),
)
COMMITS = 4               # la primera tanda: un commit por línea
QUEDAN = (1, 0)           # los que sí salen en el log después del reset

# Qué hace cada línea del reflog (tanda 2) al aparecer (índice de línea →
# índice de nodo). Los dos huérfanos se encienden en ámbar —siguen ahí—, y los
# que nunca salieron de la rama solo parpadean: también están apuntados, pero
# no hay nada que rescatar en ellos.
ENCIENDE = {2: 3, 3: 2}
PARPADEA = {4: 1, 5: 0}


def _nodo(indice, color=RAMA_MAIN):
    """Un commit de la cadena, en su sitio y del color que toque."""
    nodo = nodo_commit(HASHES[indice], color, RADIO, TAM_HASH)
    return nodo.move_to([X_CADENA[indice], Y_CADENA, 0])


def _marco_consola():
    """La ventana de la terminal, vacía y del tamaño de la tanda más larga.

    Se crea una vez y se queda: lo que cambia son las líneas de dentro
    (``_sesion``), no la ventana, así que la terminal no baila.
    """
    return ventana(ANCHO_CONSOLA, ALTO_CONSOLA, "terminal", 14).move_to(
        [0, Y_CONSOLA, 0])


def _sesion(indice):
    """Las líneas de la tanda ``indice``, colocadas dentro de la ventana.

    Devuelve solo las filas: para teclearlas hay que pasarle a ``teclear`` el
    par ``VGroup(marco, filas)``, que es la forma que tiene una ``terminal``.
    """
    filas = VGroup(*[
        linea_terminal(c, t, TAM_SESION) for c, t in SESIONES[indice]
    ]).arrange(DOWN, buff=BUFF_SESION, aligned_edge=LEFT)
    filas.align_to([0, Y_SESION, 0], UP)
    return filas.align_to([-ANCHO_CONSOLA / 2 + MARGEN_CONSOLA, 0, 0], LEFT)


def construir(scene):
    encabezado = hacer_titulo(TITULO)

    # ---------------------- Las dos bandas, todavía vacías -----------------
    nodos = VGroup(*[_nodo(i) for i in range(len(HASHES))])
    aristas = VGroup(*[
        Line(nodos[i].get_center() + RIGHT * RADIO,
             nodos[i + 1].get_center() + LEFT * RADIO,
             color=RAMA_MAIN, stroke_width=4)
        for i in range(len(nodos) - 1)
    ])
    punteros = VGroup(
        puntero("HEAD", OK, TAM_PUNTERO), puntero("main", RAMA_MAIN, TAM_PUNTERO),
    ).arrange(DOWN, buff=0.12).next_to(nodos[0], DOWN, buff=BUFF_PUNTERO)

    corte = Line([-6.6, Y_CORTE, 0], [6.6, Y_CORTE, 0],
                 color=SECUNDARIO, stroke_width=2).set_stroke(opacity=0.3)
    rotulo_rama = texto("la rama", TAM_ROTULO, color=SECUNDARIO)
    rotulo_rama.move_to([X_ROTULO, Y_CADENA, 0], LEFT)
    rotulo_consola = texto("la terminal", TAM_ROTULO, color=SECUNDARIO)
    rotulo_consola.move_to([X_ROTULO, Y_CONSOLA, 0], LEFT)
    marco_consola = _marco_consola()

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(
        FadeIn(rotulo_rama, shift=RIGHT * 0.15), Create(corte),
        FadeIn(rotulo_consola, shift=RIGHT * 0.15), run_time=0.7,
    )
    scene.play(FadeIn(marco_consola), run_time=0.5)

    # ---------------------- 1. El primer commit ----------------------------
    sesion = _sesion(0)
    teclear(scene, VGroup(marco_consola, sesion), hasta=1, ritmo=0.32)
    scene.play(GrowFromCenter(nodos[0]), run_time=0.5)
    scene.play(FadeIn(punteros, shift=UP * 0.1), run_time=0.45)
    scene.next_slide()

    # ---------------------- 2. Y los demás, uno por línea ------------------
    # Cada commit nace donde le toca y la rama avanza con él: una sesión de
    # trabajo cualquiera, que es justo lo que hay que reconocer luego.
    for i in range(1, COMMITS):
        teclear(scene, VGroup(marco_consola, sesion), desde=i, hasta=i + 1,
                ritmo=0.32)
        scene.play(
            GrowFromCenter(nodos[i]), Create(aristas[i - 1]),
            punteros.animate.next_to(nodos[i], DOWN, buff=BUFF_PUNTERO),
            run_time=0.7,
        )
    scene.next_slide()

    # ---------------------- 3. El susto ------------------------------------
    # Se teclea, y solo después se mueve el dibujo: así el comando y lo que
    # hace no se pisan, y da tiempo a leer las dos bandas por separado.
    scene.play(FadeOut(sesion), run_time=0.3)
    sesion = _sesion(1)
    teclear(scene, VGroup(marco_consola, sesion), hasta=1, ritmo=0.32)
    scene.play(
        punteros.animate.next_to(nodos[ATRAS], DOWN, buff=BUFF_PUNTERO),
        *[nodos[i].animate.set_opacity(APAGADO) for i in PERDIDOS],
        *[aristas[i - 1].animate.set_stroke(opacity=APAGADO)
          for i in PERDIDOS],
        run_time=1.1,
    )
    # Y el log parece confirmarlo: de los cuatro solo quedan dos, y los de
    # delante no salen por ningún lado.
    teclear(scene, VGroup(marco_consola, sesion), desde=1, ritmo=0.32)
    scene.play(
        *[Indicate(nodos[i], color=RAMA_MAIN, scale_factor=1.12)
          for i in QUEDAN],
        run_time=0.7,
    )
    scene.next_slide()

    # ---------------------- 4. La red --------------------------------------
    # Aquí se cobra el rato anterior: la lista es la sesión que se acaba de
    # ver, del revés. Cada línea enciende el commit del que habla.
    scene.play(FadeOut(sesion), run_time=0.3)
    sesion = _sesion(2)
    teclear(scene, VGroup(marco_consola, sesion), hasta=2, ritmo=0.3)
    for linea in range(2, len(SESIONES[2])):
        teclear(scene, VGroup(marco_consola, sesion), desde=linea,
                hasta=linea + 1, ritmo=0.3)
        if linea in ENCIENDE:
            nodo = ENCIENDE[linea]
            scene.play(
                Transform(nodos[nodo], _nodo(nodo, AMBAR)),
                Flash(nodos[nodo], color=AMBAR, line_length=0.2, num_lines=14,
                      flash_radius=RADIO + 0.35),
                run_time=0.6,
            )
        else:
            scene.play(
                Indicate(nodos[PARPADEA[linea]], color=RAMA_MAIN,
                         scale_factor=1.12),
                run_time=0.5,
            )
    scene.next_slide()

    # ---------------------- 5. La vuelta -----------------------------------
    scene.play(FadeOut(sesion), run_time=0.3)
    sesion = _sesion(3)
    teclear(scene, VGroup(marco_consola, sesion), hasta=1, ritmo=0.3)
    scene.play(
        punteros.animate.next_to(nodos[-1], DOWN, buff=BUFF_PUNTERO),
        *[Transform(nodos[i], _nodo(i)) for i in PERDIDOS],
        *[aristas[i - 1].animate.set_stroke(opacity=1.0) for i in PERDIDOS],
        run_time=1.1,
    )
    scene.play(
        Flash(nodos[-1], color=OK, line_length=0.22, num_lines=16,
              flash_radius=RADIO + 0.4),
        run_time=0.6,
    )
    # El mismo log de antes, y ahora salen los cuatro: no era un rescate raro,
    # el historial está como estaba.
    teclear(scene, VGroup(marco_consola, sesion), desde=1, ritmo=0.32)
    scene.wait(0.3)

    scene.next_slide()
