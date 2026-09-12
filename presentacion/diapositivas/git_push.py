"""Diapositiva 22b — ``git push``: subir lo que ya está confirmado.

El remoto ya está enlazado; esto es el viaje de ida. La diapositiva no enseña
una sesión de terminal sino **la línea despiezada**, porque el lío de ``push``
no es lo que hace sino sus tres apéndices: la gente copia ``git push -u origin
main`` de un tutorial y arrastra el ``-u`` para siempre sin saber qué hace.

  * ``-u`` es ``--set-upstream``: enlaza tu rama con la del remoto. Se pone
    **una vez por rama** y a partir de ahí ``git push`` a secas ya sabe a
    dónde va;
  * ``origin`` es el apodo de la diapositiva anterior;
  * ``main`` es la rama que subes, no "el proyecto".

El comando va en claro y solo las tres piezas llevan color, que es lo que las
empareja con su explicación: si ``git push`` fuera cian —lo normal en las
terminales de la charla— chocaría con el cian de ``main``, y el color dejaría
de significar nada.

Y el remate, que es el error más común de los primeros días: ``push`` sube
commits. Lo que sigue sin confirmar no viaja, por mucho que esté guardado en
el editor.
"""

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    FadeIn,
    VGroup,
)

from componentes import linea_terminal, texto
from componentes import titulo as hacer_titulo
from estilo import AMBAR, CLARO, OK, RAMA_MAIN, SECUNDARIO

TITULO = "git push"

ORDEN = "git push -u origin main"
TAM_ORDEN = 21
Y_ORDEN = 2.05

# (trozo tal cual sale en la línea, qué es, color)
PIEZAS = (
    ("-u", "la primera vez: enlaza tu main con el suyo", AMBAR),
    ("origin", "a qué remoto lo mandas", OK),
    ("main", "qué rama subes", RAMA_MAIN),
)
X_PIEZA, X_QUE_ES = -4.8, -3.1
Y_PIEZAS = 0.85
PASO_PIEZA = 0.95
TAM_QUE_ES = 17

DESPUES = "a partir de ahí, así de corto:"
ORDEN_CORTA = "git push"
Y_DESPUES = -2.25
BUFF_DESPUES = 0.45

REMATE = "push sube commits: lo que no has confirmado no viaja"


def _orden_despiezada():
    """La línea entera, con cada pieza de su color.

    Las claves de ``t2c`` son expresiones regulares, así que las piezas van
    por posición —``"[11:13]"``— calculada sobre la cadena que se dibuja, ya
    con el prompt delante: un ``-`` o un ``$`` dentro de la clave haría cosas
    raras.
    """
    completa = f"$ {ORDEN}"
    t2c = {"[0:1]": OK}
    for trozo, _, color in PIEZAS:
        i = completa.index(trozo)
        t2c[f"[{i}:{i + len(trozo)}]"] = color
    return texto(completa, TAM_ORDEN, color=CLARO, t2c=t2c)


def construir(scene):
    encabezado = hacer_titulo(TITULO)
    linea = _orden_despiezada().move_to([0, Y_ORDEN, 0])

    piezas = VGroup()
    for i, (trozo, que_es, color) in enumerate(PIEZAS):
        y = Y_PIEZAS - i * PASO_PIEZA
        piezas.add(VGroup(
            texto(trozo, TAM_ORDEN, color=color).move_to([X_PIEZA, y, 0], LEFT),
            texto(que_es, TAM_QUE_ES, color=SECUNDARIO).move_to(
                [X_QUE_ES, y, 0], LEFT),
        ))

    despues = VGroup(
        texto(DESPUES, TAM_QUE_ES, color=SECUNDARIO),
        linea_terminal(ORDEN_CORTA, "cmd", TAM_ORDEN),
    ).arrange(RIGHT, buff=BUFF_DESPUES).move_to([0, Y_DESPUES, 0])

    remate = texto(REMATE, 15, color=OK).to_edge(DOWN, buff=0.62)

    # ------------------------------ montaje --------------------------------
    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(FadeIn(linea, shift=RIGHT * 0.15), run_time=0.7)
    for pieza in piezas:
        scene.play(FadeIn(pieza, shift=RIGHT * 0.12), run_time=0.55)
    scene.play(FadeIn(despues, shift=DOWN * 0.1), run_time=0.6)
    scene.play(FadeIn(remate), run_time=0.45)
    scene.wait(0.3)

    scene.next_slide()
