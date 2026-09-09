"""Diapositiva 27 — flujos de trabajo, y el de un proyecto de datos.

Seis pantallas, y las seis son un dibujo. Aquí no hay nada que leer: lo que hay
que ver está en la forma, y cada pantalla se apoya en la anterior.

1. **El workflow normal**: ``main`` abajo y dos ramas que salen y vuelven, con
   nombres de verdad.
2. **Qué cambia en datos**: al lado, lo que entra en un commit de código y lo
   que entra en un experimento —``train.py``, y además los datos, el modelo y
   el resultado—. Ahí se ve solo lo que git no está versionando.
3. **Los cuatro elementos**, en pirámide y de abajo arriba, porque cada uno se
   apoya en el de abajo.
4. **El flujo de un experimento**, en diagrama de decisión: de dónde sales, las
   dos formas de probar, y qué pasa según si mejoras o no.
5. **Secuencial** y 6. **paralela**: ese mismo diagrama traducido a git, una
   pantalla entera para cada uno, con el accuracy dentro de cada commit.

Los tres grafos comparten dibujo: carriles punteados, una pegatina por carril
arriba, y caminos en ángulo recto en vez de curvas. Es el lenguaje de los
diagramas de git flow de toda la vida, y hace que las tres pantallas se lean
como variaciones de la misma figura y no como tres dibujos distintos.

Fuente: DagsHub, *Git Flow for Data Science*
        https://dagshub.com/blog/git-flow-for-data-science/
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    DashedLine,
    FadeIn,
    FadeOut,
    GrowFromCenter,
    LaggedStart,
    Polygon,
    RoundedRectangle,
    VGroup,
    VMobject,
)

from componentes import archivo, discos, nodo_commit, puntero, robot, texto
from componentes import titulo as hacer_titulo
from estilo import (
    AMBAR,
    CLARO,
    ERROR,
    OK,
    RAMA_FEATURE,
    RAMA_MAIN,
    SECUNDARIO,
    SUPERFICIE,
)

RADIO = 0.3
TAM_ACC = 12               # el accuracy, dentro del commit
ANCHO_MAX = 12.4

# --- Lo que comparten los tres grafos --------------------------------------
X_GRAFO = (-5.9, 5.9)      # de dónde a dónde llegan los carriles
X_V0, X_V1 = -5.3, 5.3
Y_CHIPS = 2.5
X_CHIPS = (-4.3, 0.0, 4.3)
TAM_CHIP = 16
GROSOR = 4
RADIO_CODO = 0.3           # cuánto se redondean las esquinas de un camino

# --- Pantalla 1: el workflow normal ----------------------------------------
Y_MAIN = -2.1
Y_RAMAS = (1.5, 0.1)
# Un color por rama: con dos ramas del mismo morado hay que ir siguiendo
# el cable para saber cuál es cuál.
RAMAS = (("agente-rag", RAMA_FEATURE), ("tool-calling", OK))
X_NODOS_RAMA = ((-1.6, 2.6), (-2.6, -0.3, 2.0))
# La de fuera despega del propio v0 y la de dentro un poco más allá: las dos
# quedan encajadas una dentro de otra y ancladas al mismo commit, como en los
# diagramas de git flow de toda la vida.
X_SALIDA_RAMA = (X_V0, -4.2)
# La de arriba no vuelve: se queda abierta, que es lo que pasa con la mitad de
# las ramas de un equipo en cualquier momento dado. Solo baja a main la de
# dentro, que es la que ya está revisada.
X_VUELTA_RAMA = (None, 3.4)

# --- Pantalla 2: qué cabe en un commit y qué en un experimento -------------
# Los dos paneles no miden lo mismo a propósito: uno tiene un hueco y el otro
# cuatro, y ese ancho distinto ya cuenta media diapositiva antes de mirar
# dentro. Los iconos y sus nombres van a la misma altura en los cinco huecos:
# colgando cada nombre de su icono, salían escalonados según lo alto que fuera
# el dibujo.
X_PANEL = (-4.7, 2.0)
ANCHO_PANEL = (3.4, 8.8)
ALTO_PANEL = 3.8
Y_PANEL = -0.75
Y_TITULO_PANEL = 1.55
Y_ICONO = -0.5
Y_PIE_ICONO = -1.5
ALTO_ICONO = 1.25
PANELES = ("un cambio de código", "un experimento")
X_PIEZAS = (-1.3, 0.9, 3.1, 5.3)   # los cuatro huecos del panel de la derecha
METRICA = "acc 0.87"

# --- Pantalla 3: los cuatro elementos, en triángulo rectángulo ------------
# El triángulo se apoya en su lado vertical y crece hacia la derecha, así que
# los cuatro pisos quedan alineados por la izquierda y a la derecha queda sitio
# para lo único que hace falta: qué es cada uno, en un renglón.
X_TRI = -6.5               # el lado vertical, donde se apoya todo
X_TRI_BASE = 0.2           # hasta dónde llega la base, el piso más ancho
Y_TRI = -2.75
ALTO_CAPA = 1.25
HUECO = 0.14
X_EXPLICA = 1.1
Y_TRI_CIMA = Y_TRI + 4 * ALTO_CAPA
# (nombre, qué es, color)
ELEMENTOS = (
    ("versionar datos y modelos",
     "el .csv y el .pkl también tienen versión", RAMA_MAIN),
    ("encapsular el experimento",
     "código, datos, modelo y resultado, juntos", OK),
    ("aislar en su rama",
     "cada prueba en la suya, sin pisarse", RAMA_FEATURE),
    ("Data Science Pull Request",
     "se revisa entero, no solo el diff", AMBAR),
)

# --- Pantalla 4: el flujo de un experimento, en decisiones -----------------
# De izquierda a derecha, como se lee: sales de una rama, pruebas de una de las
# dos formas, y según si mejora o no acabas arriba o abajo. En vertical no
# cabía sin encoger la letra hasta lo ilegible.
ALTO_CAJA = 0.9
# El eje del diagrama no va en el centro del marco sino en el centro de lo que
# queda bajo el título, que es el hueco que de verdad hay libre.
Y_FLUJO = -0.45
Y_RAMAL = 1.15             # cuánto se abren las dos opciones de cada bifurcación
# (líneas, x, y, ancho, color)
CAJAS_FLUJO = (
    (("crea la rama", "del experimento"), -5.2, Y_FLUJO, 2.4, RAMA_FEATURE),
    (("secuencial", "un commit por prueba"), -1.6, Y_FLUJO + Y_RAMAL, 3.0,
     AMBAR),
    (("paralela", "una rama por prueba"), -1.6, Y_FLUJO - Y_RAMAL, 3.0,
     RAMA_FEATURE),
    (("DSPR y merge a main",), 5.15, Y_FLUJO + Y_RAMAL, 3.1, OK),
    (("te quedas en main",), 5.15, Y_FLUJO - Y_RAMAL, 3.1, ERROR),
)
# Entre caja y caja quedan casi 0.9 de hueco a propósito: es lo que necesita el
# codo para girar sin que la curva se coma la punta.
X_ROMBO = 1.9
SEMI_ROMBO = (1.0, 0.58)
PREGUNTA = "¿mejora main?"
ELEGIR = "elige el mejor"

# --- Pantallas 5 y 6: los dos git flow -------------------------------------
Y_SEC = (1.1, -0.4, -2.2)          # experimento, mejor, main
X_SEC_PRUEBAS = (-3.2, -1.4, 0.4, 2.2)
ACC_SEC = ("0.81", "0.84", "0.87", "0.83")
MEJOR_SEC = 2
X_SEC_SALIDA = -4.6
X_SEC_VUELTA = 4.2         # dónde baja a main la rama de la mejor prueba

Y_PAR = (1.9, 0.7, -0.5, -2.3)     # sub A, sub B (y experimento), sub C, main
X_PAR_EXP = -3.0
X_PAR_SALIDA = -4.6
X_PAR_BIFURCA = -1.5
X_PAR_SUBS = 1.2
ACC_PAR = ("0.79", "0.84", "0.87")
MEJOR_PAR = 2
X_PAR_VUELTA = 3.9


def _nodo(x, y, color, acc=""):
    """Un commit. Con ``acc``, lleva su métrica dentro: ahí no hay duda de a
    qué prueba pertenece el número, que es lo que pasaba con el rótulo al lado.
    """
    return nodo_commit(acc, color, RADIO, TAM_ACC).move_to([x, y, 0])


def _ajustar(mob, ancho=ANCHO_MAX):
    if mob.width > ancho:
        mob.scale(ancho / mob.width)
    return mob


def _carril(y):
    """La guía punteada de un carril, de lado a lado."""
    linea = DashedLine([X_GRAFO[0], y, 0], [X_GRAFO[1], y, 0],
                       color=SECUNDARIO, stroke_width=2, dash_length=0.16)
    return linea.set_stroke(opacity=0.3)


def _chips(nombres):
    """La leyenda de arriba: una pegatina por carril, repartidas a lo ancho."""
    return VGroup(*[
        puntero(nombre, color, TAM_CHIP).move_to([x, Y_CHIPS, 0])
        for (nombre, color), x in zip(nombres, X_CHIPS)
    ])


def _camino(puntos, color, grosor=GROSOR, radio=RADIO_CODO):
    """Un tramo de historia, en ángulo recto y con las esquinas redondeadas.

    Cada codo se corta ``radio`` antes y se cierra con una bézier que pasa por
    la esquina: la curva sale sola y el camino sigue leyéndose como el trazo
    de un diagrama de git, no como una diagonal.
    """
    # Fuera los puntos repetidos: un tramo de longitud cero deja el codo sin
    # dirección —una división por cero— y el camino entero sale roto. Pasa en
    # cuanto una rama sale y llega a la misma altura.
    pts = []
    for punto in (np.array(p, dtype=float) for p in puntos):
        if not pts or np.linalg.norm(punto - pts[-1]) > 1e-6:
            pts.append(punto)
    if len(pts) < 2:
        return VMobject(color=color, stroke_width=grosor)
    trazo = VMobject(color=color, stroke_width=grosor)
    trazo.start_new_path(pts[0])
    for anterior, esquina, siguiente in zip(pts, pts[1:], pts[2:]):
        entra, sale = esquina - anterior, siguiente - esquina
        largo_entra, largo_sale = np.linalg.norm(entra), np.linalg.norm(sale)
        r = min(radio, largo_entra / 2, largo_sale / 2)
        trazo.add_line_to(esquina - entra / largo_entra * r)
        trazo.add_quadratic_bezier_curve_to(esquina,
                                            esquina + sale / largo_sale * r)
    trazo.add_line_to(pts[-1])
    return trazo


def _flecha_codo(inicio, fin, color, grosor=3, punta=0.22):
    """Conector de diagrama: sale en horizontal, gira con el codo redondeado y
    entra en horizontal, con la punta pegada al destino.

    En diagonal recta el diagrama parecía un esquema de flechas sueltas; con el
    codo se lee como un circuito, que es lo que es.
    """
    (x0, y0), (x1, y1) = inicio[:2], fin[:2]
    medio = (x0 + x1) / 2
    camino = _camino(
        [[x0, y0, 0], [medio, y0, 0], [medio, y1, 0], [x1 - punta, y1, 0]],
        color, grosor, radio=min(RADIO_CODO, abs(y1 - y0) / 2 or RADIO_CODO),
    )
    cabeza = Polygon(
        [x1, y1, 0], [x1 - punta, y1 + punta * 0.6, 0],
        [x1 - punta, y1 - punta * 0.6, 0],
        color=color, stroke_width=0,
    ).set_fill(color, opacity=1.0)
    return VGroup(camino, cabeza)


def _v(x, y, nombre, hacia_dentro=RIGHT):
    """Un commit de main con su versión encima, corrida hacia el centro.

    Encima y no debajo porque por debajo de main no hay nada que estorbe, pero
    por arriba sí: dejando el nombre ahí, pegado al codo de la rama que
    despega, el pie del dibujo queda limpio.
    """
    nodo = _nodo(x, y, RAMA_MAIN)
    etiqueta = texto(nombre, 14, color=SECUNDARIO)
    etiqueta.next_to(nodo, UP, buff=0.18).shift(hacia_dentro * 0.34)
    return VGroup(nodo, etiqueta)


# --- Piezas de la pantalla 2 -----------------------------------------------
def _pieza(icono, nombre, color, x):
    """Un componente del proyecto: su icono arriba y su nombre debajo, los dos
    a la altura fija de la fila."""
    return VGroup(
        icono.move_to([x, Y_ICONO, 0]),
        texto(nombre, 14, color=color).move_to([x, Y_PIE_ICONO, 0]),
    )


def _tarjeta_metrica():
    """El resultado del experimento, que es lo que de verdad se compara."""
    letras = texto(METRICA, 16, color=OK)
    caja = RoundedRectangle(
        width=letras.width + 0.6, height=0.8, corner_radius=0.16,
        stroke_color=OK, stroke_width=2.5,
    ).set_fill(SUPERFICIE, opacity=1.0)
    return VGroup(caja, letras.move_to(caja))


def _panel(indice):
    """El cajón de uno de los dos casos, con su título encima."""
    x = X_PANEL[indice]
    caja = RoundedRectangle(
        width=ANCHO_PANEL[indice], height=ALTO_PANEL, corner_radius=0.2,
        stroke_color=SECUNDARIO, stroke_width=2.5,
    ).set_fill(SUPERFICIE, opacity=1.0).move_to([x, Y_PANEL, 0])
    caja.set_stroke(opacity=0.55)
    titulo = texto(PANELES[indice], 17, color=CLARO)
    return caja, titulo.move_to([x, Y_TITULO_PANEL, 0])


# --- Piezas de la pantalla 3 -----------------------------------------------
def _borde(y):
    """Dónde cae la hipotenusa a esa altura."""
    return X_TRI + (X_TRI_BASE - X_TRI) * (Y_TRI_CIMA - y) / (4 * ALTO_CAPA)


def _capa(indice):
    """Un piso del triángulo y, a su derecha, qué es en un renglón."""
    nombre, explicacion, color = ELEMENTOS[indice]
    y0 = Y_TRI + indice * ALTO_CAPA
    y1 = y0 + ALTO_CAPA - HUECO
    if indice == len(ELEMENTOS) - 1:
        y1 = Y_TRI_CIMA
        vertices = ([X_TRI, y0, 0], [_borde(y0), y0, 0], [X_TRI, y1, 0])
    else:
        vertices = ([X_TRI, y0, 0], [_borde(y0), y0, 0],
                    [_borde(y1), y1, 0], [X_TRI, y1, 0])
    # Dos polígonos iguales: el de abajo tapa la malla del fondo y el de
    # encima pone el tinte de su color, que en un solo mobject no se puede.
    forma = VGroup(
        Polygon(*vertices, stroke_width=0).set_fill(SUPERFICIE, opacity=1.0),
        Polygon(*vertices, color=color, stroke_width=3)
        .set_fill(color, opacity=0.12),
    )
    rotulo = VGroup(
        texto(nombre, 17, color=color),
        texto(explicacion, 14, color=SECUNDARIO),
    ).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
    rotulo.move_to([X_EXPLICA, (y0 + y1) / 2, 0], LEFT)
    return VGroup(forma, rotulo)


# --- Piezas de la pantalla 4 -----------------------------------------------
def _caja_flujo(indice):
    """Una caja del diagrama de decisión, con las esquinas redondeadas."""
    lineas, x, y, ancho, color = CAJAS_FLUJO[indice]
    caja = RoundedRectangle(
        width=ancho, height=ALTO_CAJA, corner_radius=0.18,
        stroke_color=color, stroke_width=2.5,
    ).set_fill(SUPERFICIE, opacity=1.0).move_to([x, y, 0])
    tamanos = (14,) if len(lineas) == 1 else (15, 12)
    colores = (color,) if len(lineas) == 1 else (color, SECUNDARIO)
    rotulo = VGroup(*[
        texto(t, tam, color=c) for t, tam, c in zip(lineas, tamanos, colores)
    ]).arrange(DOWN, buff=0.08).move_to(caja)
    return VGroup(caja, rotulo)


def _rombo():
    """La decisión: ¿el mejor experimento mejora lo que hay en main?"""
    ancho, alto = SEMI_ROMBO
    figura = Polygon(
        [0, alto, 0], [ancho, 0, 0], [0, -alto, 0], [-ancho, 0, 0],
        color=AMBAR, stroke_width=2.5,
    ).set_fill(SUPERFICIE, opacity=1.0).move_to([X_ROMBO, Y_FLUJO, 0])
    return VGroup(figura, texto(PREGUNTA, 13, color=AMBAR).move_to(figura))


def construir(scene):
    # ---------------------- Pantalla 1: el workflow normal -----------------
    encabezado = hacer_titulo("workflow normal")

    chips = _chips((("main", RAMA_MAIN), *RAMAS))
    carriles = VGroup(*[_carril(y) for y in (*Y_RAMAS, Y_MAIN)])
    v0 = _v(X_V0, Y_MAIN, "v0")
    v1 = _v(X_V1, Y_MAIN, "v1", LEFT)
    linea_main = _camino([[X_V0 + RADIO, Y_MAIN, 0],
                          [X_V1 - RADIO, Y_MAIN, 0]], RAMA_MAIN)

    ramas = VGroup()
    for i, y in enumerate(Y_RAMAS):
        color = RAMAS[i][1]
        nodos = VGroup(*[_nodo(x, y, color) for x in X_NODOS_RAMA[i]])
        # Si despega desde v0, arranca en el borde del commit y no en su
        # centro, que si no le cruza el círculo por dentro.
        y_arranque = Y_MAIN + (RADIO if X_SALIDA_RAMA[i] == X_V0 else 0)
        vuelta = X_VUELTA_RAMA[i]
        puntos = [[X_SALIDA_RAMA[i], y_arranque, 0], [X_SALIDA_RAMA[i], y, 0]]
        if vuelta is None:
            puntos.append([X_NODOS_RAMA[i][-1], y, 0])
        else:
            puntos += [[vuelta, y, 0], [vuelta, Y_MAIN, 0]]
        camino = _camino(puntos, color)
        ramas.add(VGroup(camino, nodos))

    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(FadeIn(carriles), FadeIn(chips, shift=DOWN * 0.1), run_time=0.7)
    scene.play(Create(linea_main), FadeIn(v0), FadeIn(v1), run_time=0.8)
    for rama in ramas:
        scene.play(Create(rama[0]), run_time=0.8)
        scene.play(
            LaggedStart(*[GrowFromCenter(n) for n in rama[1]], lag_ratio=0.3),
            run_time=0.7,
        )
    scene.wait(0.3)
    scene.next_slide()

    # ---------------------- Pantalla 2: qué cambia en datos ----------------
    encabezado_datos = hacer_titulo("y en un proyecto de datos")

    caja_izq, titulo_izq = _panel(0)
    caja_der, titulo_der = _panel(1)
    codigo = _pieza(archivo(color=RAMA_MAIN, alto=ALTO_ICONO), "train.py",
                    RAMA_MAIN, X_PANEL[0])
    piezas = VGroup(
        _pieza(archivo(color=RAMA_MAIN, alto=ALTO_ICONO), "train.py",
               RAMA_MAIN, X_PIEZAS[0]),
        _pieza(discos(ALTO_ICONO, AMBAR), "datos.csv", AMBAR, X_PIEZAS[1]),
        _pieza(robot(ALTO_ICONO, RAMA_FEATURE), "modelo.pkl", RAMA_FEATURE,
               X_PIEZAS[2]),
        _pieza(_tarjeta_metrica(), "resultado", OK, X_PIEZAS[3]),
    )
    izquierda = VGroup(caja_izq, titulo_izq, codigo)

    scene.play(
        FadeOut(carriles), FadeOut(chips), FadeOut(linea_main),
        FadeOut(v0), FadeOut(v1), FadeOut(ramas),
        FadeOut(encabezado), FadeIn(encabezado_datos, shift=DOWN * 0.2),
        run_time=0.8,
    )
    scene.play(FadeIn(izquierda, shift=RIGHT * 0.15), run_time=0.8)
    scene.play(FadeIn(caja_der), FadeIn(titulo_der), run_time=0.6)
    # Las cuatro piezas entran una a una: la primera es la misma de la
    # izquierda, y las otras tres son justo lo que git no está viendo.
    scene.play(
        LaggedStart(*[FadeIn(pieza, shift=UP * 0.15) for pieza in piezas],
                    lag_ratio=0.35),
        run_time=1.8,
    )
    scene.wait(0.3)
    scene.next_slide()

    # ---------------------- Pantalla 3: los cuatro elementos ---------------
    encabezado_piramide = hacer_titulo("los cuatro elementos")
    piramide = VGroup(*[_capa(i) for i in range(len(ELEMENTOS))])

    scene.play(
        FadeOut(izquierda), FadeOut(caja_der), FadeOut(titulo_der),
        FadeOut(piezas), FadeOut(encabezado_datos),
        FadeIn(encabezado_piramide, shift=DOWN * 0.2),
        run_time=0.8,
    )
    # De abajo arriba, que es el orden en el que se construye de verdad: sin
    # datos versionados no hay nada que encapsular, y sin encapsular no hay
    # pull request que revisar.
    for capa in piramide:
        scene.play(Create(capa[0]), FadeIn(capa[1], shift=UP * 0.1),
                   run_time=0.55)
    scene.next_slide()

    # ---------------------- Pantalla 4: el flujo, en decisiones ------------
    encabezado_flujo = hacer_titulo("el flujo de un experimento")

    inicio = _caja_flujo(0)
    secuencial, paralela = _caja_flujo(1), _caja_flujo(2)
    dspr, quedarse = _caja_flujo(3), _caja_flujo(4)
    rombo = _rombo()

    flechas = VGroup(
        _flecha_codo(inicio[0].get_right(), secuencial[0].get_left(),
                     SECUNDARIO),
        _flecha_codo(inicio[0].get_right(), paralela[0].get_left(),
                     SECUNDARIO),
        _flecha_codo(secuencial[0].get_right(), rombo[0].get_left(),
                     SECUNDARIO),
        _flecha_codo(paralela[0].get_right(), rombo[0].get_left(),
                     SECUNDARIO),
        _flecha_codo(rombo[0].get_right(), dspr[0].get_left(), OK),
        _flecha_codo(rombo[0].get_right(), quedarse[0].get_left(), ERROR),
    )
    # El sí y el no van pegados al tramo vertical de su codo, no al final de la
    # flecha: ahí es donde el camino se parte en dos y donde se mira.
    x_respuesta = (rombo[0].get_right()[0] + dspr[0].get_left()[0]) / 2 - 0.38
    rotulos = VGroup(
        texto(ELEGIR, 12, color=SECUNDARIO).next_to(rombo, UP, buff=0.22),
        texto("sí", 13, color=OK).move_to([x_respuesta, Y_FLUJO + 0.55, 0]),
        texto("no", 13, color=ERROR).move_to([x_respuesta, Y_FLUJO - 0.55, 0]),
    )

    scene.play(
        FadeOut(piramide), FadeOut(encabezado_piramide),
        FadeIn(encabezado_flujo, shift=DOWN * 0.2),
        run_time=0.8,
    )
    scene.play(FadeIn(inicio, shift=RIGHT * 0.15), run_time=0.6)
    scene.play(Create(flechas[0]), Create(flechas[1]), run_time=0.5)
    scene.play(FadeIn(secuencial, shift=RIGHT * 0.12),
               FadeIn(paralela, shift=RIGHT * 0.12), run_time=0.7)
    scene.play(Create(flechas[2]), Create(flechas[3]),
               FadeIn(rotulos[0]), run_time=0.6)
    scene.play(GrowFromCenter(rombo), run_time=0.6)
    scene.play(Create(flechas[4]), Create(flechas[5]),
               FadeIn(rotulos[1:]), run_time=0.7)
    scene.play(FadeIn(dspr, shift=RIGHT * 0.12),
               FadeIn(quedarse, shift=RIGHT * 0.12), run_time=0.7)
    scene.wait(0.3)
    scene.next_slide()

    # ---------------------- Pantalla 5: secuencial -------------------------
    encabezado_sec = hacer_titulo("secuencial")

    y_exp, y_mejor, y_main = Y_SEC
    chips_sec = _chips((("main", RAMA_MAIN), ("experimento", AMBAR),
                        ("mejor", OK)))
    carriles_sec = VGroup(*[_carril(y) for y in Y_SEC])
    v0s = _v(X_V0, y_main, "v0")
    v1s = _v(X_V1, y_main, "v1", LEFT)
    linea_main_sec = _camino([[X_V0 + RADIO, y_main, 0],
                              [X_V1 - RADIO, y_main, 0]], RAMA_MAIN)

    x_mejor = X_SEC_PRUEBAS[MEJOR_SEC]
    camino_exp = _camino([
        [X_SEC_SALIDA, y_main, 0], [X_SEC_SALIDA, y_exp, 0],
        [X_SEC_PRUEBAS[-1] + 0.7, y_exp, 0],
    ], AMBAR)
    pruebas = VGroup(*[
        _nodo(x, y_exp, OK if i == MEJOR_SEC else AMBAR, acc)
        for i, (x, acc) in enumerate(zip(X_SEC_PRUEBAS, ACC_SEC))
    ])
    # El mismo commit, ya en su rama: lleva su número, que si no es un círculo
    # vacío colgando de un cable.
    nodo_mejor = _nodo(x_mejor, y_mejor, OK, ACC_SEC[MEJOR_SEC])
    # Baja a su carril, corre por él y solo entonces entra en main: así la rama
    # se ve como una rama y no como un cable recto de arriba abajo.
    camino_mejor = _camino([
        [x_mejor, y_exp - RADIO, 0], [x_mejor, y_mejor - RADIO, 0],
    ], OK)
    # Acaba donde se junta con main y no encima de v1: si sigue hasta el nodo,
    # la línea se le mete dentro del círculo y queda un pegote.
    camino_vuelta = _camino([
        [x_mejor + RADIO, y_mejor, 0], [X_SEC_VUELTA, y_mejor, 0],
        [X_SEC_VUELTA, y_main, 0],
    ], OK)

    scene.play(
        FadeOut(inicio), FadeOut(secuencial), FadeOut(paralela),
        FadeOut(rombo), FadeOut(quedarse), FadeOut(dspr),
        FadeOut(flechas), FadeOut(rotulos),
        FadeOut(encabezado_flujo), FadeIn(encabezado_sec, shift=DOWN * 0.2),
        run_time=0.8,
    )
    scene.play(FadeIn(carriles_sec), FadeIn(chips_sec, shift=DOWN * 0.1),
               run_time=0.7)
    scene.play(Create(linea_main_sec), FadeIn(v0s), FadeIn(v1s), run_time=0.8)
    scene.play(Create(camino_exp), run_time=0.8)
    scene.play(
        LaggedStart(*[GrowFromCenter(n) for n in pruebas], lag_ratio=0.3),
        run_time=1.3,
    )
    # La que gana se lee en el número, y de ella sale la rama que vuelve.
    scene.play(Create(camino_mejor), GrowFromCenter(nodo_mejor), run_time=0.8)
    scene.play(Create(camino_vuelta), run_time=0.9)
    scene.wait(0.3)
    scene.next_slide()

    # ---------------------- Pantalla 6: paralela ---------------------------
    encabezado_par = hacer_titulo("paralela")

    y_a, y_b, y_c, y_main_par = Y_PAR
    chips_par = _chips((("main", RAMA_MAIN), ("experimento", AMBAR),
                        ("sub-experimento", RAMA_FEATURE)))
    carriles_par = VGroup(*[_carril(y) for y in Y_PAR])
    v0p = _v(X_V0, y_main_par, "v0")
    v1p = _v(X_V1, y_main_par, "v1", LEFT)
    linea_main_par = _camino([[X_V0 + RADIO, y_main_par, 0],
                              [X_V1 - RADIO, y_main_par, 0]], RAMA_MAIN)

    camino_exp_par = _camino([
        [X_PAR_SALIDA, y_main_par, 0], [X_PAR_SALIDA, y_b, 0],
        [X_PAR_BIFURCA, y_b, 0],
    ], AMBAR)
    nodo_exp = _nodo(X_PAR_EXP, y_b, AMBAR)
    subs = VGroup(*[
        _nodo(X_PAR_SUBS, y, OK if i == MEJOR_PAR else RAMA_FEATURE, acc)
        for i, (y, acc) in enumerate(zip((y_a, y_b, y_c), ACC_PAR))
    ])
    ramales = VGroup(*[
        _camino([[X_PAR_BIFURCA, y_b, 0], [X_PAR_BIFURCA, y, 0],
                 [X_PAR_SUBS, y, 0]],
                OK if i == MEJOR_PAR else RAMA_FEATURE)
        for i, y in enumerate((y_a, y_b, y_c))
    ])
    camino_mejor_par = _camino([
        [X_PAR_SUBS + RADIO, y_c, 0], [X_PAR_VUELTA, y_c, 0],
        [X_PAR_VUELTA, y_main_par, 0],
    ], OK)

    scene.play(
        FadeOut(carriles_sec), FadeOut(chips_sec), FadeOut(linea_main_sec),
        FadeOut(v0s), FadeOut(v1s), FadeOut(camino_exp), FadeOut(pruebas),
        FadeOut(camino_mejor), FadeOut(camino_vuelta),
        FadeOut(nodo_mejor),
        FadeOut(encabezado_sec), FadeIn(encabezado_par, shift=DOWN * 0.2),
        run_time=0.8,
    )
    scene.play(FadeIn(carriles_par), FadeIn(chips_par, shift=DOWN * 0.1),
               run_time=0.7)
    scene.play(Create(linea_main_par), FadeIn(v0p), FadeIn(v1p), run_time=0.8)
    scene.play(Create(camino_exp_par), GrowFromCenter(nodo_exp), run_time=0.9)
    scene.play(
        LaggedStart(*[Create(r) for r in ramales], lag_ratio=0.3),
        run_time=1.2,
    )
    scene.play(
        LaggedStart(*[GrowFromCenter(n) for n in subs], lag_ratio=0.3),
        run_time=1.0,
    )
    scene.play(Create(camino_mejor_par), run_time=1.0)
    scene.wait(0.3)

    scene.next_slide()
