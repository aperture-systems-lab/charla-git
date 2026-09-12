"""Portada: el cartel de la charla, con la identidad de marca Aperture.

Composición de cartel a página completa, en tres franjas: arriba el título en
Press Start 2P con su eco cian —el desplazamiento de color de los carteles de
recreativa— y el tema en una línea; en medio, el objeto del que va la charla
entera: un historial de commits que crece, se abre en una rama y vuelve a
cerrarse en un merge, con sus punteros ``main`` y ``feature``; abajo, la firma
del semillero junto al logo.

El historial es el mismo dibujo que reaparece en la diapositiva de ramas y en
el cierre, así que desde el primer minuto la gente ya ha visto el mapa. Va a lo
ancho y no en media pantalla a propósito: es el suelo sobre el que se apoya el
título, no una ilustración de acompañamiento.
"""

from manim import (
    DOWN,
    LEFT,
    PI,
    RIGHT,
    UP,
    Create,
    FadeIn,
    Flash,
    GrowFromCenter,
    Square,
    VGroup,
)

from animaciones import pulso
from componentes import (
    arista,
    logo_esquina,
    nodo_commit,
    puntero,
    separador,
    texto,
)
from estilo import (
    CLARO,
    FONT_TITULO,
    PRIMARIO,
    RAMA_FEATURE,
    RAMA_MAIN,
    SECUNDARIO,
)

# --- Rótulos ---------------------------------------------------------------
# El "Introducción a" va en JetBrains Mono y no en la fuente display: es la
# entradilla del título, y el contraste entre las dos fuentes es lo que hace
# que se lea como una sola frase con el peso en "GIT Y GITHUB".
ANTETITULO = "Introducción a"
TITULO = "GIT Y GITHUB"
SUBTITULO = "Control de versiones y trabajo en equipo"
FIRMA = "Semillero de Data Science e IA"

# --- Medidas del bloque de texto ------------------------------------------
TAM_TITULO_PORTADA = 46
ANCHO_MAX = 10.6         # ni el título ni el subtítulo se acercan al marco
ECO = RIGHT * 0.09 + DOWN * 0.09   # cuánto se separa la sombra cian del título

# --- Rejilla del historial (la banda central del cartel) ------------------
# La banda va por encima del tronco del grafo decorativo del fondo (y = -1.9 en
# el preset que le toca a esta diapositiva): si coincidieran, los puntos tenues
# del fondo caerían justo sobre la línea de ``main`` y se leerían como suciedad.
COL = (-4.4, -2.64, -0.88, 0.88, 2.64, 4.4)
Y_MAIN = -1.5
Y_FEATURE = -0.4
R = 0.3                  # radio de los nodos

# --- Pie de cartel ---------------------------------------------------------
Y_REGLA_PIE = -3.0


def _ajustar(mob, ancho=ANCHO_MAX):
    """Encoge un mobject si se pasa de ancho. Devuelve el propio mobject."""
    if mob.width > ancho:
        mob.scale(ancho / mob.width)
    return mob


def _regla_rombo(largo=1.9):
    """Filete decorativo con un rombo en medio, bajo el título."""
    rombo = Square(side_length=0.14, stroke_width=0)
    rombo.set_fill(PRIMARIO, opacity=1).rotate(PI / 4)
    return VGroup(
        separador(largo=largo, grosor=2),
        rombo,
        separador(largo=largo, grosor=2),
    ).arrange(RIGHT, buff=0.24)


def _cabecera():
    """Entradilla, título con su eco, filete y subtítulo."""
    antetitulo = texto(ANTETITULO, 22, color=SECUNDARIO)
    titulo = _ajustar(texto(TITULO, TAM_TITULO_PORTADA, color=CLARO,
                            font=FONT_TITULO))
    # Copia del título en cian por detrás: el título se ve doble, como en la
    # pantalla de un recreativo. Se coloca ya desplazada para que el bloque
    # mida lo que va a ocupar; la animación la trae desde debajo del título.
    eco = titulo.copy().set_color(PRIMARIO).set_opacity(0.45).shift(ECO)
    # Entradilla y título son una sola frase, así que van más juntos entre sí
    # que con el resto del bloque.
    cabeza = VGroup(antetitulo, VGroup(eco, titulo))
    cabeza.arrange(DOWN, buff=0.18)

    filete = _regla_rombo()
    subtitulo = _ajustar(texto(SUBTITULO, 18, color=SECUNDARIO))

    bloque = VGroup(cabeza, filete, subtitulo)
    bloque.arrange(DOWN, buff=0.34).to_edge(UP, buff=0.75)
    return antetitulo, titulo, eco, filete, subtitulo


def _pie_de_cartel():
    """Firma del semillero y logo, sobre un filete a todo lo ancho.

    El logo se crea con ``logo_esquina``, la misma fábrica que usa el indicador
    de avance: así el indicador cae exactamente encima y no se duplica.
    """
    logo = logo_esquina()
    firma = texto(FIRMA, 15, color=SECUNDARIO)
    firma.to_edge(LEFT, buff=0.75).set_y(logo.get_center()[1])

    # El filete va exactamente de un extremo a otro de la fila que tiene
    # debajo: empieza donde empieza la firma y acaba donde acaba el logo.
    izq, der = firma.get_left()[0], logo.get_right()[0]
    regla = separador(largo=(der - izq) / 2, grosor=2).set_opacity(0.3)
    regla.move_to([(izq + der) / 2, Y_REGLA_PIE, 0])
    return regla, firma, logo


def _historial(scene):
    """Dibuja el grafo de la banda central, paso a paso."""
    # --- Nodos --------------------------------------------------------------
    a = nodo_commit("a1", RAMA_MAIN, R).move_to([COL[0], Y_MAIN, 0])
    b = nodo_commit("b2", RAMA_MAIN, R).move_to([COL[1], Y_MAIN, 0])
    d = nodo_commit("d4", RAMA_MAIN, R).move_to([COL[4], Y_MAIN, 0])
    m = nodo_commit("m5", RAMA_MAIN, R).move_to([COL[5], Y_MAIN, 0])
    f1 = nodo_commit("f1", RAMA_FEATURE, R).move_to([COL[2], Y_FEATURE, 0])
    f2 = nodo_commit("f2", RAMA_FEATURE, R).move_to([COL[3], Y_FEATURE, 0])

    # --- Aristas ------------------------------------------------------------
    ab = arista(a, b, RAMA_MAIN, R)
    bd = arista(b, d, RAMA_MAIN, R)          # main sigue, por debajo de la rama
    dm = arista(d, m, RAMA_MAIN, R)
    salida = arista(b, f1, RAMA_FEATURE, R)  # la rama se abre
    f1f2 = arista(f1, f2, RAMA_FEATURE, R)
    vuelta = arista(f2, m, RAMA_FEATURE, R)  # y se cierra en el merge

    # --- Punteros -----------------------------------------------------------
    p_feature = puntero("feature", RAMA_FEATURE, 15)
    p_feature.next_to(f2, UP, buff=0.24)
    p_main = puntero("main", RAMA_MAIN, 15).next_to(m, DOWN, buff=0.24)

    # ---------------------- Animación ---------------------------------------
    scene.play(GrowFromCenter(a), run_time=0.4)
    scene.play(Create(ab), run_time=0.3)
    scene.play(GrowFromCenter(b), run_time=0.4)

    # Se abre la rama: primero la curva, que es la que cuenta la historia.
    scene.play(Create(salida), run_time=0.5)
    scene.play(GrowFromCenter(f1), run_time=0.35)
    scene.play(Create(f1f2), run_time=0.3)
    scene.play(GrowFromCenter(f2), run_time=0.35)
    scene.play(FadeIn(p_feature, shift=DOWN * 0.12), run_time=0.35)

    # Mientras tanto, main no se ha parado.
    scene.play(Create(bd), run_time=0.5)
    scene.play(GrowFromCenter(d), run_time=0.35)

    # Y las dos historias se juntan en un commit con dos padres.
    scene.play(Create(dm), Create(vuelta), run_time=0.6)
    scene.play(
        GrowFromCenter(m),
        Flash(m, color=RAMA_MAIN, line_length=0.22, num_lines=14,
              flash_radius=R + 0.35),
        run_time=0.6,
    )
    scene.play(FadeIn(p_main, shift=UP * 0.12), run_time=0.35)

    # Un repaso de luz por el camino completo: así se lee como un recorrido y
    # no como seis círculos sueltos.
    scene.play(
        pulso(ab, CLARO, 0.5), pulso(salida, CLARO, 0.6),
        pulso(f1f2, CLARO, 0.5), pulso(bd, CLARO, 0.9),
        pulso(vuelta, CLARO, 0.6), pulso(dm, CLARO, 0.5),
        run_time=1.1,
    )


def construir(scene):
    antetitulo, titulo, eco, filete, subtitulo = _cabecera()
    regla_pie, firma, logo = _pie_de_cartel()

    # --- Animación: primero el cartel, luego el historial -------------------
    scene.play(FadeIn(antetitulo, shift=DOWN * 0.1), run_time=0.4)
    # El eco entra pegado al título y se separa: el cartel "se enciende".
    eco.shift(-ECO)
    scene.play(FadeIn(eco, scale=1.05), FadeIn(titulo, scale=1.05),
               run_time=0.6)
    scene.play(eco.animate.shift(ECO), run_time=0.3)

    scene.play(
        Create(filete[0]), GrowFromCenter(filete[1]), Create(filete[2]),
        run_time=0.45,
    )
    scene.play(FadeIn(subtitulo, shift=UP * 0.1), run_time=0.45)

    _historial(scene)

    scene.play(Create(regla_pie), run_time=0.5)
    scene.play(FadeIn(firma, shift=UP * 0.08), FadeIn(logo), run_time=0.5)
    scene.wait(0.6)
    scene.next_slide()
