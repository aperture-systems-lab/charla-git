"""Diapositiva 15 — ``git merge``: los dos casos.

Misma forma que ``ramas``: la pantalla partida en dos bandas que no se juntan.

  * **arriba, las ramas** — los commits y los cartelitos que los señalan;
  * **abajo, la terminal** — lo que se teclea y lo que git contesta.

Merge se explica mal cuando se cuenta como una sola cosa, porque git hace dos
cosas muy distintas según lo que haya pasado en ``main`` mientras tanto, y aquí
se ven las dos sobre el mismo dibujo, una detrás de otra.

**Caso 1, main no se movió.** La rama se hace delante, como en ``git_reflog``:
se teclea el ``switch -c`` y los dos ``commit``, y los commits nuevos salen
arriba, en su carril, que es como los dibuja cualquiera. Y entonces llega el
truco de la diapositiva: al hacer el merge esos dos commits **bajan** a la
línea de main. No había nada que mezclar —la rama era main y dos pasos más—,
así que la línea estaba recta desde el principio y solo hacía falta deslizar la
pegatina. Por eso no aparece ningún commit nuevo ni se abre ningún editor: la
maniobra entera es que la línea se endereza y el cartel se desliza.

**Caso 2, main sí avanzó.** Las dos historias se separaron y ya no hay línea
que enderezar: git fabrica un commit nuevo con **dos padres**, uno por cada
rama. Es el único commit del historial que apunta hacia atrás dos veces, y es
lo que deja el rombo que se ve en GitHub. Las dos aristas se encienden al
final, una por padre, para que se vea de dónde viene cada una.

Lo que hay que recordar antes de teclear no se escribe en ningún sitio: se ve.
Las dos veces hace falta un ``git switch main`` primero, y las dos veces se ve
a ``HEAD`` mudarse al cartelito de la rama que recibe antes de que el merge
pueda hacer nada.
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
    LaggedStart,
    Line,
    Transform,
    VGroup,
)

from animaciones import pulso, teclear
from componentes import ALTO_BARRA, arista, linea_terminal, nodo_commit
from componentes import puntero, texto, ventana
from componentes import titulo as hacer_titulo
from estilo import CLARO, OK, RAMA_FEATURE, RAMA_MAIN, SECUNDARIO

TITULO = "git merge"

# --- Arriba: las ramas -----------------------------------------------------
# Dos carriles: el de main abajo y el de la rama de trabajo encima. Los
# cartelitos van siempre al mismo sitio —main debajo de su commit, la rama
# encima del suyo— y HEAD a la derecha del cartelito al que está pegado.
Y_BASE = 0.7
Y_ALTA = 1.85
RADIO = 0.33
TAM_HASH = 14
TAM_PUNTERO = 15
BUFF_PUNTERO = 0.28

# Caso 1: main se queda con dos commits y la rama pone otros dos encima.
X_FF_MAIN = (-4.8, -3.0)
X_FF_RAMA = (-1.2, 0.6)
HASHES_FF_MAIN = ("0e5f", "77ab")
HASHES_FF_RAMA = ("a3c1", "b8e2")

# Caso 2: la horquilla, con main avanzado por su cuenta.
X_BASE = (-5.0, -3.3, -1.6)
X_ALTA = (-1.6, 0.1)
X_MERGE = 1.9
RADIO_MERGE = 0.38
HASHES_BASE = ("0e5f", "77ab", "c4f0")
HASHES_ALTA = ("a3c1", "b8e2")
HASH_MERGE = "m9d3"

# La rama de trabajo, la misma en los dos casos: así lo único que cambia de uno
# a otro es lo que haya hecho main mientras tanto, que es de lo que va todo.
RAMA = "experimento"

# --- El corte entre las dos mitades ----------------------------------------
Y_CORTE = -0.55
X_ROTULO = -6.35
Y_ROTULO = 1.28           # en el hueco entre las dos filas
TAM_ROTULO = 15

# --- Abajo: la terminal ----------------------------------------------------
ANCHO_CONSOLA = 7.4
ALTO_CONSOLA = 2.3
Y_CONSOLA = -2.1
MARGEN_CONSOLA = 0.5
TAM_SESION = 15
BUFF_SESION = 0.16
Y_SESION = Y_CONSOLA + ALTO_CONSOLA / 2 - ALTO_BARRA - 0.25

# La primera tanda hace la rama delante de todos —una línea, un commit—, y las
# otras dos son los merges. Las dos empiezan igual, con el ``switch`` a la rama
# que recibe: esa repetición es la que enseña la regla sin enunciarla.
SESIONES = (
    ((f"git switch -c {RAMA}", "cmd"),
     ('git commit -m "arregla el pie"', "cmd"),
     ('git commit -m "y el margen"', "cmd")),
    (("git switch main", "cmd"),
     ("Switched to branch 'main'", "ok"),
     (f"git merge {RAMA}", "cmd")),
    (("git switch main", "cmd"),
     ("Switched to branch 'main'", "ok"),
     (f"git merge {RAMA}", "cmd")),
)


def _marco_consola():
    """La ventana de la terminal, vacía y del tamaño de la tanda más larga."""
    return ventana(ANCHO_CONSOLA, ALTO_CONSOLA, "terminal", 14).move_to(
        [0, Y_CONSOLA, 0])


def _sesion(indice):
    """Las líneas de la tanda ``indice``, colocadas dentro de la ventana."""
    filas = VGroup(*[
        linea_terminal(c, t, TAM_SESION) for c, t in SESIONES[indice]
    ]).arrange(DOWN, buff=BUFF_SESION, aligned_edge=LEFT)
    filas.align_to([0, Y_SESION, 0], UP)
    return filas.align_to([-ANCHO_CONSOLA / 2 + MARGEN_CONSOLA, 0, 0], LEFT)


def _mudar(scene, p_head, cartel, run_time=0.9):
    """HEAD se muda al cartelito de otra rama: eso es todo lo que hace switch."""
    scene.play(p_head.animate.next_to(cartel, RIGHT, buff=BUFF_PUNTERO),
               run_time=run_time)


def _plantar(scene, cartel, p_head, nodo, direccion=UP, run_time=0.5):
    """Un cartelito se planta en otro commit, con HEAD detrás si va con él.

    Los destinos se calculan antes de animar: si HEAD mirase dónde está el
    cartelito *ahora*, se quedaría en el sitio viejo y se solaparían.
    """
    destino = cartel.copy().next_to(nodo, direccion, buff=BUFF_PUNTERO)
    animaciones = [cartel.animate.move_to(destino)]
    if p_head is not None:
        detras = p_head.copy().next_to(destino, RIGHT, buff=BUFF_PUNTERO)
        animaciones.append(p_head.animate.move_to(detras))
    scene.play(*animaciones, run_time=run_time)


def construir(scene):
    encabezado = hacer_titulo(TITULO)

    corte = Line([-6.6, Y_CORTE, 0], [6.6, Y_CORTE, 0],
                 color=SECUNDARIO, stroke_width=2).set_stroke(opacity=0.3)
    rotulo_ramas = texto("las ramas", TAM_ROTULO, color=SECUNDARIO)
    rotulo_ramas.move_to([X_ROTULO, Y_ROTULO, 0], LEFT)
    rotulo_consola = texto("la terminal", TAM_ROTULO, color=SECUNDARIO)
    rotulo_consola.move_to([X_ROTULO, Y_CONSOLA, 0], LEFT)
    marco_consola = _marco_consola()

    # ---------------------- El repo de partida -----------------------------
    nodos = VGroup(*[
        nodo_commit(h, RAMA_MAIN, RADIO, TAM_HASH).move_to([x, Y_BASE, 0])
        for x, h in zip(X_FF_MAIN, HASHES_FF_MAIN)
    ])
    aristas = VGroup(arista(nodos[0], nodos[1], RAMA_MAIN, RADIO))
    p_main = puntero("main", RAMA_MAIN, TAM_PUNTERO)
    p_main.next_to(nodos[-1], DOWN, buff=BUFF_PUNTERO)
    p_head = puntero("HEAD", OK, TAM_PUNTERO)
    p_head.next_to(p_main, RIGHT, buff=BUFF_PUNTERO)

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(
        LaggedStart(*[GrowFromCenter(n) for n in nodos], lag_ratio=0.25),
        FadeIn(rotulo_ramas, shift=RIGHT * 0.15), run_time=0.9,
    )
    scene.play(Create(aristas[0]), run_time=0.5)
    scene.play(FadeIn(p_main, shift=UP * 0.1), FadeIn(p_head, shift=LEFT * 0.1),
               run_time=0.5)
    scene.play(Create(corte), FadeIn(rotulo_consola, shift=RIGHT * 0.15),
               run_time=0.6)
    scene.play(FadeIn(marco_consola), run_time=0.5)
    scene.next_slide()

    # ---------------------- La rama, hecha delante -------------------------
    # Los commits nuevos salen arriba, en su carril: así es como los dibuja
    # todo el mundo, y así es como hay que verlos antes de que bajen.
    sesion = _sesion(0)
    teclear(scene, VGroup(marco_consola, sesion), hasta=1, ritmo=0.32)
    p_rama = puntero(RAMA, RAMA_FEATURE, TAM_PUNTERO)
    p_rama.next_to(nodos[-1], UP, buff=BUFF_PUNTERO)
    scene.play(FadeIn(p_rama, shift=DOWN * 0.12), run_time=0.5)
    _mudar(scene, p_head, p_rama, run_time=0.7)

    anterior = nodos[-1]
    rama_nodos, rama_aristas = VGroup(), VGroup()
    for i, (x, h) in enumerate(zip(X_FF_RAMA, HASHES_FF_RAMA)):
        teclear(scene, VGroup(marco_consola, sesion), desde=i + 1, hasta=i + 2,
                ritmo=0.32)
        nodo = nodo_commit(h, RAMA_FEATURE, RADIO, TAM_HASH)
        nodo.move_to([x, Y_ALTA, 0])
        ramal = arista(anterior, nodo, RAMA_FEATURE, RADIO)
        scene.play(Create(ramal), GrowFromCenter(nodo), run_time=0.7)
        _plantar(scene, p_rama, p_head, nodo)
        rama_nodos.add(nodo)
        rama_aristas.add(ramal)
        anterior = nodo
    scene.next_slide()

    # ---------------------- El merge que no lo es --------------------------
    # main no se ha movido, así que no hay nada que mezclar: los dos commits
    # bajan a la línea de siempre —estaba recta desde el principio— y la
    # pegatina se desliza hasta el final.
    scene.play(FadeOut(sesion), run_time=0.3)
    sesion = _sesion(1)
    teclear(scene, VGroup(marco_consola, sesion), hasta=1, ritmo=0.32)
    _mudar(scene, p_head, p_main)
    teclear(scene, VGroup(marco_consola, sesion), desde=1, hasta=3, ritmo=0.32)

    bajados = VGroup(*[
        n.copy().move_to([x, Y_BASE, 0])
        for n, x in zip(rama_nodos, X_FF_RAMA)
    ])
    rectas = VGroup(
        arista(nodos[-1], bajados[0], RAMA_FEATURE, RADIO),
        arista(bajados[0], bajados[1], RAMA_FEATURE, RADIO),
    )
    scene.play(
        *[Transform(n, d) for n, d in zip(rama_nodos, bajados)],
        *[Transform(a, r) for a, r in zip(rama_aristas, rectas)],
        p_rama.animate.next_to(bajados[-1], UP, buff=BUFF_PUNTERO),
        run_time=1.1,
    )
    scene.play(*[pulso(a, RAMA_MAIN, 0.7) for a in rama_aristas], run_time=0.9)
    _plantar(scene, p_main, p_head, rama_nodos[-1], direccion=DOWN,
             run_time=1.0)
    scene.next_slide()

    # ---------------------- Caso 2: las dos avanzaron ----------------------
    base = VGroup(*[
        nodo_commit(h, RAMA_MAIN, RADIO, TAM_HASH).move_to([x, Y_BASE, 0])
        for x, h in zip(X_BASE, HASHES_BASE)
    ])
    alta = VGroup(*[
        nodo_commit(h, RAMA_FEATURE, RADIO, TAM_HASH).move_to([x, Y_ALTA, 0])
        for x, h in zip(X_ALTA, HASHES_ALTA)
    ])
    hilos = VGroup(
        arista(base[0], base[1], RAMA_MAIN, RADIO),
        arista(base[1], base[2], RAMA_MAIN, RADIO),
        arista(base[1], alta[0], RAMA_FEATURE, RADIO),
        arista(alta[0], alta[1], RAMA_FEATURE, RADIO),
    )
    q_main = puntero("main", RAMA_MAIN, TAM_PUNTERO)
    q_main.next_to(base[-1], DOWN, buff=BUFF_PUNTERO)
    q_rama = puntero(RAMA, RAMA_FEATURE, TAM_PUNTERO)
    q_rama.next_to(alta[-1], UP, buff=BUFF_PUNTERO)
    q_head = puntero("HEAD", OK, TAM_PUNTERO)
    q_head.next_to(q_rama, RIGHT, buff=BUFF_PUNTERO)

    scene.play(
        FadeOut(nodos), FadeOut(aristas), FadeOut(rama_nodos),
        FadeOut(rama_aristas), FadeOut(p_main), FadeOut(p_rama),
        FadeOut(p_head), FadeOut(sesion), run_time=0.6,
    )
    scene.play(
        LaggedStart(*[GrowFromCenter(n) for n in [*base, *alta]],
                    lag_ratio=0.22),
        run_time=1.1,
    )
    scene.play(
        LaggedStart(*[Create(h) for h in hilos], lag_ratio=0.22),
        run_time=0.9,
    )
    scene.play(FadeIn(q_main, shift=UP * 0.1), FadeIn(q_rama, shift=DOWN * 0.1),
               FadeIn(q_head, shift=LEFT * 0.1), run_time=0.5)
    scene.next_slide()

    # Aquí sí hay que fabricar algo: un commit con dos padres.
    sesion = _sesion(2)
    teclear(scene, VGroup(marco_consola, sesion), hasta=1, ritmo=0.32)
    _mudar(scene, q_head, q_main)
    teclear(scene, VGroup(marco_consola, sesion), desde=1, hasta=3, ritmo=0.32)

    m = nodo_commit(HASH_MERGE, RAMA_MAIN, RADIO_MERGE, TAM_HASH)
    m.move_to([X_MERGE, Y_BASE, 0])
    padres = VGroup(arista(base[-1], m, RAMA_MAIN, RADIO),
                    arista(alta[-1], m, RAMA_FEATURE, RADIO))
    scene.play(Create(padres[0]), Create(padres[1]), run_time=0.8)
    scene.play(
        GrowFromCenter(m),
        Flash(m, color=RAMA_MAIN, line_length=0.25, num_lines=16,
              flash_radius=RADIO_MERGE + 0.35),
        run_time=0.8,
    )
    _plantar(scene, q_main, q_head, m, direccion=DOWN, run_time=0.8)
    # Y las dos flechas hacia atrás, una por rama: eso es el commit de merge.
    scene.play(*[pulso(p, CLARO, 0.8) for p in padres], run_time=1.0)
    scene.wait(0.3)

    scene.next_slide()
