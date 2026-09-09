"""Diapositiva 18b — ``git revert``: deshacer sin borrar.

Misma forma que ``git_checkout``: la pantalla partida en dos bandas que no se
juntan.

  * **arriba, la rama** — la cadena de commits con ``HEAD`` y ``main``;
  * **abajo, tu carpeta ahora** — los archivos que verías si abrieras la
    carpeta en este instante. Sin etiquetas: el color es el estado, rojo el
    que tiene el fallo y verde el que ya está bien.

Va justo detrás de ``git_reset`` y contra él: los dos deshacen, pero uno mueve
la rama hacia atrás y el otro no toca nada de lo que ya está. ``revert`` no
borra el commit que salió mal, **añade uno nuevo que hace justo lo contrario**.
El historial crece en vez de encoger y el error se queda escrito, que es
exactamente lo que quieres cuando el commit ya está en GitHub y otra persona lo
tiene bajado.

Y la prueba de que no se ha borrado nada no se dice, se hace: al final se viaja
con ``checkout`` al commit revertido y **sus archivos siguen ahí**, rotos como
estaban. El fallo no se ha ido del historial; encima de él hay otro commit que
lo deshace. Se vuelve al presente y la carpeta está otra vez bien.
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
    Transform,
    VGroup,
)

from componentes import archivo, arista, nodo_commit, puntero, texto
from componentes import titulo as hacer_titulo
from estilo import AMBAR, CLARO, ERROR, OK, RAMA_MAIN, SECUNDARIO

TITULO = "git revert"

# --- Arriba: la rama -------------------------------------------------------
# Cinco huecos: los cuatro commits que ya había y el que va a nacer al final.
X_CADENA = (-4.8, -2.4, 0.0, 2.4, 4.8)
Y_CADENA = 1.35
RADIO = 0.38
TAM_HASH = 15
HASHES = ("0e5f", "77ab", "9c1d", "3f2a")
CULPABLE = 2              # el commit que metió el fallo
HASH_REVERT = "r7b2"
TAM_PUNTERO = 15
BUFF_PUNTERO = 0.42

# --- El corte entre las dos mitades ----------------------------------------
Y_CORTE = -0.4
X_ROTULO = -6.35
TAM_ROTULO = 15

# --- Abajo: tu carpeta -----------------------------------------------------
# Solo nombre y color: el color es todo lo que hay que leer.
ARCHIVOS = ("informe.md", "conclusiones.md", "datos.csv")
TOCADO = 0                # el único que rompió el commit culpable
X_ARCHIVOS = (-2.8, 0.2, 3.0)
Y_ARCHIVOS = -1.7
ALTO_ARCHIVO = 0.7
TAM_NOMBRE = 14

# --- El pie: solo el comando -----------------------------------------------
TAM_ORDEN = 20
Y_ORDEN = -3.05


def _archivo(indice, color):
    """Un archivo de la carpeta: su icono, su nombre y nada más."""
    icono = archivo(ARCHIVOS[indice], color=color, alto=ALTO_ARCHIVO,
                    tam=TAM_NOMBRE)
    return icono.move_to([X_ARCHIVOS[indice], Y_ARCHIVOS, 0])


def _orden(contenido, color=CLARO):
    """El comando que se acaba de teclear, al pie de la diapositiva."""
    return texto(contenido, TAM_ORDEN, color=color).move_to([0, Y_ORDEN, 0])


def _head(nodo, color):
    """HEAD, plantado encima de un commit y del color que toque."""
    return puntero("HEAD", color, TAM_PUNTERO).next_to(nodo, UP,
                                                       buff=BUFF_PUNTERO)


def construir(scene):
    encabezado = hacer_titulo(TITULO)

    # ---------------------- Las dos bandas ---------------------------------
    nodos = VGroup(*[
        nodo_commit(h, RAMA_MAIN, RADIO, TAM_HASH).move_to([x, Y_CADENA, 0])
        for x, h in zip(X_CADENA, HASHES)
    ])
    aristas = VGroup(*[
        arista(nodos[i], nodos[i + 1], RAMA_MAIN, RADIO)
        for i in range(len(nodos) - 1)
    ])
    p_main = puntero("main", RAMA_MAIN, TAM_PUNTERO)
    p_main.next_to(nodos[-1], DOWN, buff=BUFF_PUNTERO)
    p_head = _head(nodos[-1], OK)

    corte = Line([-6.6, Y_CORTE, 0], [6.6, Y_CORTE, 0],
                 color=SECUNDARIO, stroke_width=2).set_stroke(opacity=0.3)
    rotulo_rama = texto("la rama", TAM_ROTULO, color=SECUNDARIO)
    rotulo_rama.move_to([X_ROTULO, Y_CADENA, 0], LEFT)
    rotulo_carpeta = texto("tu carpeta ahora", TAM_ROTULO, color=SECUNDARIO)
    rotulo_carpeta.move_to([X_ROTULO, Y_ARCHIVOS, 0], LEFT)

    carpeta = VGroup(_archivo(0, ERROR), _archivo(1, RAMA_MAIN),
                     _archivo(2, RAMA_MAIN))

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(
        LaggedStart(*[GrowFromCenter(n) for n in nodos], lag_ratio=0.25),
        FadeIn(rotulo_rama, shift=RIGHT * 0.15), run_time=0.9,
    )
    scene.play(
        LaggedStart(*[Create(a) for a in aristas], lag_ratio=0.25),
        run_time=0.6,
    )
    scene.play(FadeIn(p_main, shift=UP * 0.1), FadeIn(p_head, shift=DOWN * 0.1),
               run_time=0.5)
    scene.play(Create(corte), FadeIn(rotulo_carpeta, shift=RIGHT * 0.15),
               run_time=0.6)
    scene.play(
        LaggedStart(*[GrowFromCenter(f) for f in carpeta], lag_ratio=0.25),
        run_time=0.9,
    )
    # Un solo aviso, y de los que hacen falta: ese commit es el que dejó el
    # archivo en rojo.
    scene.play(Indicate(nodos[CULPABLE], color=ERROR, scale_factor=1.2),
               run_time=0.8)
    scene.next_slide()

    # ---------------------- El revert --------------------------------------
    # No se toca el commit malo: nace uno nuevo al final que hace lo contrario.
    orden = _orden(f"git revert {HASHES[CULPABLE]}")
    scene.play(FadeIn(orden, shift=UP * 0.1), run_time=0.45)

    revert = nodo_commit(HASH_REVERT, OK, RADIO, TAM_HASH)
    revert.move_to([X_CADENA[-1], Y_CADENA, 0])
    hilo = arista(nodos[-1], revert, OK, RADIO)
    scene.play(Create(hilo), GrowFromCenter(revert), run_time=0.8)

    destino_main = p_main.copy().next_to(revert, DOWN, buff=BUFF_PUNTERO)
    scene.play(
        p_main.animate.move_to(destino_main),
        Transform(p_head, _head(revert, OK)),
        Flash(revert, color=OK, line_length=0.22, num_lines=16,
              flash_radius=RADIO + 0.4),
        run_time=0.9,
    )
    # Y abajo, lo que se buscaba: el archivo vuelve a estar bien.
    scene.play(Transform(carpeta[TOCADO], _archivo(TOCADO, OK)), run_time=0.8)
    scene.next_slide()

    # ---------------------- La prueba: el fallo sigue ahí ------------------
    # Se viaja al commit revertido y su carpeta sale tal cual estaba, rota. No
    # se ha borrado nada: encima hay otro commit que lo deshace, y ya está.
    vuelta_atras = _orden(f"git checkout {HASHES[CULPABLE]}", color=AMBAR)
    scene.play(FadeOut(orden), FadeIn(vuelta_atras, shift=UP * 0.1),
               run_time=0.6)
    scene.play(Transform(p_head, _head(nodos[CULPABLE], AMBAR)), run_time=1.0)
    scene.play(Transform(carpeta[TOCADO], _archivo(TOCADO, ERROR)),
               run_time=0.8)
    scene.next_slide()

    # ---------------------- Y de vuelta al presente ------------------------
    vuelta = _orden("git checkout main", color=OK)
    scene.play(FadeOut(vuelta_atras), FadeIn(vuelta, shift=UP * 0.1),
               run_time=0.6)
    scene.play(Transform(p_head, _head(revert, OK)), run_time=1.0)
    scene.play(
        Transform(carpeta[TOCADO], _archivo(TOCADO, OK)),
        Flash(revert, color=OK, line_length=0.2, num_lines=14,
              flash_radius=RADIO + 0.35),
        run_time=0.8,
    )
    scene.wait(0.3)

    scene.next_slide()
