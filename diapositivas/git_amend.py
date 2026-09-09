"""Diapositiva 19 — ``git commit --amend``: rehacer el último commit.

Va justo detrás de ``git_revert`` y hace de bisagra con ``git_reflog``, así que
usa la misma forma que sus dos vecinas: la pantalla partida en dos bandas que
no se juntan.

  * **arriba, la rama** — la cadena de commits con ``main`` y ``HEAD``;
  * **abajo, el último commit** — lo que lleva dentro: su mensaje y sus
    archivos. Sin etiquetas, que el color ya lo dice: cian lo que entró en el
    commit, rojo lo que se quedó fuera, ámbar lo que está en el staging
    esperando al próximo.

El caso es el de todos los días: acabas de commitear y en el mismo segundo ves
que el mensaje lleva una errata y que un archivo se quedó fuera. ``amend``
arregla las dos cosas de una vez.

Y el detalle que no se puede callar, porque es el que causa los sustos: amend
**no edita** el commit. Un commit no se toca nunca; lo que hace es cocinar otro
—con otro hash— y dejar la rama apuntando a ese. El viejo no desaparece: se
suelta de la rama y se queda flotando, dibujado a trazos y con su cartelito de
*reemplazado*.

Ahí se corta, con el commit viejo colgando en pantalla, porque de ese dibujo
salen solas las dos cosas que hay que decir en voz alta: que amend solo se hace
mientras el commit no haya salido de tu máquina —si ya está en GitHub, lo tuyo
es ``revert``, la diapositiva anterior— y que el viejo sigue estando en el
reflog, que es la siguiente.
"""

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    DashedLine,
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

from componentes import (
    archivo,
    arista,
    aspa,
    enmarcar,
    nodo_commit,
    nodo_fantasma,
    puntero,
    texto,
)
from componentes import titulo as hacer_titulo
from estilo import AMBAR, CLARO, ERROR, OK, RAMA_MAIN, SECUNDARIO

TITULO = "git commit --amend"

# --- Arriba: la rama -------------------------------------------------------
# Tres commits y ni uno más: la cadena no crece —esa es la gracia de amend—,
# así que no hace falta un hueco a la derecha. Lo que sí hace falta es aire
# encima del último, que es a donde sube el commit reemplazado.
X_CADENA = (-4.3, -1.75, 0.8)
Y_CADENA = 0.75
Y_FANTASMA = 2.3          # el commit viejo, ya sin rama que lo sujete
RADIO = 0.38
TAM_HASH = 15
HASHES = ("0e5f", "77ab", "9c1d")
NUEVO = "b41e"            # otro commit es otro hash, y de ahí sale todo lo demás
TAM_PUNTERO = 15
BUFF_PUNTERO = 0.34
TAM_SELLO = 15

# --- El corte entre las dos mitades ----------------------------------------
Y_CORTE = -0.35
X_ROTULO = -6.35
TAM_ROTULO = 15

# --- Abajo: el último commit -----------------------------------------------
# La errata va marcada por posición y no por palabra: las claves de ``t2c`` son
# expresiones regulares (ver ``componentes.texto``).
MENSAJE_MALO = '"corrgie la tabla 2"'
MENSAJE_BUENO = '"corrige la tabla 2"'
ERRATA = {"[1:8]": ERROR}
TAM_MENSAJE = 21
Y_MENSAJE = -1.05
Y_ROTULO_ABAJO = -1.7

ARCHIVOS = ("informe.md", "datos.csv")
FUERA = 1                 # el que se quedó sin añadir
X_ARCHIVOS = (-1.5, 1.5)
Y_ARCHIVOS = -2.2
ALTO_ARCHIVO = 0.62
TAM_NOMBRE = 14

# --- El pie: solo el comando -----------------------------------------------
TAM_ORDEN = 20
Y_ORDEN = -3.1


def _orden(contenido, color=CLARO):
    """El comando que se acaba de teclear, al pie de la diapositiva."""
    return texto(contenido, TAM_ORDEN, color=color).move_to([0, Y_ORDEN, 0])


def _mensaje(contenido, color=CLARO, t2c=None):
    """El mensaje del commit, entre comillas y en el centro de la banda."""
    return texto(contenido, TAM_MENSAJE, color=color,
                 t2c=t2c).move_to([0, Y_MENSAJE, 0])


def _archivo(indice, color):
    """Un archivo del commit: su icono, su nombre y nada más."""
    icono = archivo(ARCHIVOS[indice], color=color, alto=ALTO_ARCHIVO,
                    tam=TAM_NOMBRE)
    return icono.move_to([X_ARCHIVOS[indice], Y_ARCHIVOS, 0])


def _sello():
    """El cartelito del commit reemplazado: un aspa y la palabra, enmarcadas."""
    fila = VGroup(aspa(ERROR, tam=0.11, grosor=4),
                  texto("reemplazado", TAM_SELLO, color=ERROR))
    fila.arrange(RIGHT, buff=0.2)
    return VGroup(enmarcar(fila, margen=0.36, color=ERROR), fila)


def _relevo(fantasma, nuevo):
    """El hilo a trazos que dice quién sustituye a quién."""
    linea = DashedLine(
        fantasma.get_bottom() + DOWN * 0.12,
        nuevo.get_top() + UP * 0.26,
        color=AMBAR, stroke_width=3.5, dash_length=0.13,
    )
    return linea.add_tip(tip_length=0.24, tip_width=0.22)


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
    # Los cartelitos van a la derecha del commit, y HEAD a la derecha del
    # cartelito: arriba no cabe nada, que ese sitio es del commit que sube.
    p_main = puntero("main", RAMA_MAIN, TAM_PUNTERO)
    p_main.next_to(nodos[-1], RIGHT, buff=BUFF_PUNTERO)
    p_head = puntero("HEAD", OK, TAM_PUNTERO)
    p_head.next_to(p_main, RIGHT, buff=0.22)

    corte = Line([-6.6, Y_CORTE, 0], [6.6, Y_CORTE, 0],
                 color=SECUNDARIO, stroke_width=2).set_stroke(opacity=0.3)
    rotulo_rama = texto("la rama", TAM_ROTULO, color=SECUNDARIO)
    rotulo_rama.move_to([X_ROTULO, Y_CADENA, 0], LEFT)
    rotulo_commit = texto("el último commit", TAM_ROTULO, color=SECUNDARIO)
    rotulo_commit.move_to([X_ROTULO, Y_ROTULO_ABAJO, 0], LEFT)

    mensaje = _mensaje(MENSAJE_MALO, t2c=ERRATA)
    contenido = VGroup(_archivo(0, RAMA_MAIN), _archivo(FUERA, ERROR))
    cruz = aspa(ERROR, tam=0.2, grosor=6)
    cruz.move_to(contenido[FUERA][0].get_center())

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(
        LaggedStart(*[GrowFromCenter(n) for n in nodos], lag_ratio=0.25),
        FadeIn(rotulo_rama, shift=RIGHT * 0.15), run_time=0.9,
    )
    scene.play(
        LaggedStart(*[Create(a) for a in aristas], lag_ratio=0.25),
        run_time=0.5,
    )
    scene.play(FadeIn(p_main, shift=LEFT * 0.1),
               FadeIn(p_head, shift=LEFT * 0.1), run_time=0.5)
    scene.play(Create(corte), FadeIn(rotulo_commit, shift=RIGHT * 0.15),
               run_time=0.6)
    scene.play(FadeIn(mensaje, shift=UP * 0.1), run_time=0.5)
    scene.play(
        LaggedStart(*[GrowFromCenter(f) for f in contenido], lag_ratio=0.3),
        run_time=0.7,
    )
    # Los dos destrozos del commit, a la vez: la errata en rojo dentro del
    # mensaje y el archivo que nunca llegó a entrar.
    scene.play(GrowFromCenter(cruz),
               Indicate(mensaje, color=ERROR, scale_factor=1.06), run_time=0.7)
    scene.next_slide()

    # ---------------------- Lo que faltaba, al staging ---------------------
    add = _orden(f"git add {ARCHIVOS[FUERA]}")
    scene.play(FadeIn(add, shift=UP * 0.1), run_time=0.45)
    scene.play(
        FadeOut(cruz, scale=1.5),
        Transform(contenido[FUERA], _archivo(FUERA, AMBAR)),
        run_time=0.7,
    )
    scene.next_slide()

    # ---------------------- El amend ---------------------------------------
    # Ni se edita ni se borra nada: el commit viejo se suelta de la rama y sube,
    # y en su hueco nace otro con otro hash. La rama no se ha movido de sitio;
    # lo que hay debajo del cartelito es otro commit.
    orden = _orden(f"git commit --amend -m {MENSAJE_BUENO}")
    scene.play(FadeOut(add), FadeIn(orden, shift=UP * 0.1), run_time=0.6)

    fantasma = nodo_fantasma(HASHES[-1], ERROR, RADIO, TAM_HASH)
    fantasma.move_to([X_CADENA[-1], Y_FANTASMA, 0])
    scene.play(Transform(nodos[-1], fantasma), FadeOut(aristas[-1]),
               run_time=0.9)

    nuevo = nodo_commit(NUEVO, OK, RADIO, TAM_HASH)
    nuevo.move_to([X_CADENA[-1], Y_CADENA, 0])
    hilo = arista(nodos[-2], nuevo, OK, RADIO)
    relevo = _relevo(fantasma, nuevo)
    sello = _sello().next_to(fantasma, RIGHT, buff=0.5)

    scene.play(Create(hilo), GrowFromCenter(nuevo), run_time=0.7)
    scene.play(
        Create(relevo),
        FadeIn(sello, shift=LEFT * 0.15),
        Flash(nuevo, color=OK, line_length=0.22, num_lines=16,
              flash_radius=RADIO + 0.4),
        run_time=0.9,
    )
    # Y abajo, el commit rehecho: el mensaje sin la errata y el archivo dentro.
    scene.play(
        Transform(mensaje, _mensaje(MENSAJE_BUENO)),
        Transform(contenido[FUERA], _archivo(FUERA, RAMA_MAIN)),
        Indicate(p_main, color=RAMA_MAIN, scale_factor=1.12),
        Indicate(p_head, color=OK, scale_factor=1.12),
        run_time=0.9,
    )
    # Y un último guiño al commit que se ha quedado colgando: se enciende en
    # ámbar, que es el color con el que la diapositiva siguiente —el reflog—
    # rescata a los huérfanos.
    scene.play(Indicate(nodos[-1], color=AMBAR, scale_factor=1.15),
               run_time=0.8)

    scene.next_slide()
