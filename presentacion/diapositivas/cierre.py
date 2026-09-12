"""Diapositiva 33 — cierre.

El mismo cierre que la charla de inauguración del semillero, contado con las
piezas de esta. Arriba el agradecimiento; en el centro **el historial entero**
—ya no el commit suelto de la portada, sino la rama que sale y vuelve—
corriendo de izquierda a derecha hasta desembocar en el QR; abajo, en cuatro
papeles, los cuatro dibujos que sostuvieron la charla, haciéndose solos: las
tres zonas, la cadena de commits, la rama que se fusiona y el viaje al remoto.

Cierra el círculo sin una sola frase que lo explique: lo que en la portada era
un grafo por explicar, aquí es un historial que se enciende solo y del que cada
pieza tiene ya nombre.

Y se queda vivo. El último tramo va en bucle (``next_slide(loop=True)``): una
oleada recorre el historial hasta latir en la tarjeta del QR, y los cuatro
papeles se mueven con ella. Una y otra vez mientras la gente escanea y
pregunta: el historial no se congela.

Las oleadas son ``ShowPassingFlash`` sobre copias de las aristas y no puntos
viajando: la luz recorriendo el cable se lee de un vistazo y no cuesta nada.
Y todo lo que se mueve en el bucle vuelve a su sitio —``there_and_back``,
``Indicate``, destellos sin rastro—, porque el bucle solo se cierra sin costura
si cada pieza acaba donde empezó.

Press Start 2P no trae acentos ni signos de apertura —le pasa lo mismo al
título de la portada—, así que el agradecimiento va en mayúsculas y sin ellos.
"""

import numpy as np
from manim import (
    DOWN,
    RIGHT,
    UP,
    AnimationGroup,
    Arrow,
    Create,
    FadeIn,
    Group,
    GrowFromCenter,
    Indicate,
    LaggedStart,
    Line,
    RoundedRectangle,
    ShowPassingFlash,
    Succession,
    VGroup,
    there_and_back,
)

from animaciones import pulso
from componentes import (
    arista,
    cajon,
    carpeta,
    discos,
    imagen,
    nodo_commit,
    puntero,
    texto,
)
from estilo import (
    BLANCO,
    CLARO,
    FONT_TITULO,
    OK,
    PRIMARIO,
    RAMA_FEATURE,
    RAMA_MAIN,
    SECUNDARIO,
    STAGING,
    SUPERFICIE,
)

# --- Cabecera --------------------------------------------------------------
# Una sola línea, a plena anchura. Sin subtítulo debajo: el historial llega
# alto con la pegatina de la rama, y un cierre no necesita explicar que se dan
# las gracias.
Y_GRACIAS = 3.18
TAM_GRACIAS = 48
ANCHO_MAX_GRACIAS = 10.4

# --- El historial, que desemboca en el QR ----------------------------------
# El grafo ocupa la mitad izquierda y el QR la derecha, los dos en la misma
# banda: el último commit apunta a la tarjeta, así que la charla entera acaba
# entrando en el formulario.
COL = (-6.15, -4.9, -3.65, -2.4, -1.15, 0.1)
Y_MAIN = 0.15
Y_FEATURE = 1.35
R = 0.26
BUFF_PUNTERO = 0.24

# --- El QR -----------------------------------------------------------------
X_QR = 4.25
Y_TARJETA = 0.55
LADO_TARJETA = 2.9
MARGEN_QR = 0.3          # zona de silencio: sin ella los lectores fallan
Y_PIE_QR = -1.35

# --- La tira de repaso -----------------------------------------------------
# Cuatro papeles, un dibujo por papel: cada uno es la imagen de una parte de
# la charla, en el color con el que se contó allí.
#
# Van sin rótulo a propósito. Acaban de verse una por una durante cinco horas,
# así que ponerles el nombre debajo es repetir lo que la silueta ya dice, y
# cuatro textos seguidos convierten la tira en una fila de botones.
Y_TIRA = -2.55
ANCHO_PAPEL, ALTO_PAPEL = 2.6, 1.30
BUFF_PAPEL = 0.32
ALTO_ICONO = 0.44        # los iconos de zona dentro de su papel
RADIO_MINI = 0.14        # los commits en miniatura

Y_FIRMA = -3.62


# --------------------------------------------------------------------------
# El historial
# --------------------------------------------------------------------------
def _historial():
    """El grafo de la portada, ya con todos sus nombres.

    Devuelve las aristas **en el orden en que las recorre la oleada** (de la
    izquierda a la derecha, y la rama en su sitio), que es lo que permite
    después encender el historial por tramos en vez de todo a la vez.
    """
    a = nodo_commit(color=RAMA_MAIN, radio=R).move_to([COL[0], Y_MAIN, 0])
    b = nodo_commit(color=RAMA_MAIN, radio=R).move_to([COL[1], Y_MAIN, 0])
    d = nodo_commit(color=RAMA_MAIN, radio=R).move_to([COL[4], Y_MAIN, 0])
    m = nodo_commit(color=RAMA_MAIN, radio=R).move_to([COL[5], Y_MAIN, 0])
    f1 = nodo_commit(color=RAMA_FEATURE, radio=R).move_to([COL[2], Y_FEATURE, 0])
    f2 = nodo_commit(color=RAMA_FEATURE, radio=R).move_to([COL[3], Y_FEATURE, 0])

    ab = arista(a, b, RAMA_MAIN, R)
    bd = arista(b, d, RAMA_MAIN, R)
    dm = arista(d, m, RAMA_MAIN, R)
    salida = arista(b, f1, RAMA_FEATURE, R)
    f1f2 = arista(f1, f2, RAMA_FEATURE, R)
    vuelta = arista(f2, m, RAMA_FEATURE, R)

    p_main = puntero("main", RAMA_MAIN, 13).next_to(m, DOWN, buff=BUFF_PUNTERO)
    p_rama = puntero("feature", RAMA_FEATURE, 13)
    p_rama.next_to(f2, UP, buff=BUFF_PUNTERO)

    nodos = VGroup(a, b, f1, f2, d, m)
    hilos = VGroup(ab, salida, f1f2, bd, vuelta, dm)
    return nodos, hilos, VGroup(p_main, p_rama), m


def _desemboque(ultimo):
    """La flecha que lleva el último commit hasta la tarjeta del QR."""
    borde = X_QR - LADO_TARJETA / 2
    tramo = (ultimo.get_center() + RIGHT * (R + 0.12),
             np.array([borde - 0.12, Y_MAIN, 0.0]))
    flecha = Arrow(
        *tramo, color=PRIMARIO, stroke_width=4, buff=0.0,
        max_tip_length_to_length_ratio=0.11,
    )
    # Riel invisible con el recorrido de la flecha: el destello va por aquí,
    # porque ``ShowPassingFlash`` sobre una ``Arrow`` arrastra la punta.
    return flecha, Line(*tramo)


# --------------------------------------------------------------------------
# La tira de repaso: los cuatro dibujos de la charla, en miniatura
# --------------------------------------------------------------------------
# Cada boceto devuelve sus piezas **en el orden en que se cuentan**, porque de
# ese orden sale la animación: ``_dibujarse`` las va soltando una a una, así
# que la lista es a la vez el dibujo y su guion. Las piezas marcadas con
# ``crece`` brotan del centro; las demás se trazan.
def _crece(mob):
    mob.crece = True
    return mob


def _mini(x, y, color):
    """Un commit del tamaño de la tira."""
    return _crece(nodo_commit(color=color, radio=RADIO_MINI).move_to([x, y, 0]))


def _boceto_zonas():
    """Las tres zonas: el directorio, el área de preparación y el repositorio."""
    iconos = VGroup(
        carpeta(ALTO_ICONO, SECUNDARIO),
        cajon(ALTO_ICONO, STAGING),
        discos(ALTO_ICONO, RAMA_MAIN),
    ).arrange(RIGHT, buff=0.30)
    for icono in iconos:
        _crece(icono)
    return iconos


def _boceto_cadena():
    """La cadena de commits: cada uno agarrado al anterior."""
    nodos = [_mini(x, 0, RAMA_MAIN) for x in (-0.72, 0.0, 0.72)]
    return VGroup(
        nodos[0], arista(nodos[0], nodos[1], RAMA_MAIN, RADIO_MINI),
        nodos[1], arista(nodos[1], nodos[2], RAMA_MAIN, RADIO_MINI),
        nodos[2],
    )


def _boceto_rama():
    """La rama que sale y vuelve: el rombo del merge."""
    a = _mini(-0.82, -0.22, RAMA_MAIN)
    m = _mini(0.82, -0.22, RAMA_MAIN)
    f = _mini(0.0, 0.30, RAMA_FEATURE)
    return VGroup(
        a, arista(a, m, RAMA_MAIN, RADIO_MINI), m,
        arista(a, f, RAMA_FEATURE, RADIO_MINI), f,
        arista(f, m, RAMA_FEATURE, RADIO_MINI),
    )


def _cajita(x, color):
    """Una máquina o un servidor, del tamaño de la tira."""
    return _crece(RoundedRectangle(
        width=0.86, height=0.52, corner_radius=0.1,
        stroke_color=color, stroke_width=2.6,
    ).set_fill(SUPERFICIE, opacity=1.0).move_to([x, 0, 0]))


def _boceto_remoto():
    """El viaje al remoto: sube una copia y baja otra."""
    aqui, alla = _cajita(-0.85, OK), _cajita(0.85, PRIMARIO)
    ida = Arrow([-0.36, 0.14, 0], [0.36, 0.14, 0], color=OK, buff=0,
                stroke_width=2.6, max_tip_length_to_length_ratio=0.22)
    vuelta = Arrow([0.36, -0.14, 0], [-0.36, -0.14, 0], color=PRIMARIO, buff=0,
                   stroke_width=2.6, max_tip_length_to_length_ratio=0.22)
    return VGroup(aqui, alla, ida, vuelta)


# --------------------------------------------------------------------------
# Y los cuatro, vivos: lo que hace cada dibujo cuando la tira entra en bucle
# --------------------------------------------------------------------------
# Nada de lo de aquí deja rastro: destellos y ``Indicate``, que vuelven solos.
def _vive_zonas(boceto):
    """El archivo viajando de zona en zona, como lo hace un commit."""
    return LaggedStart(*[
        Indicate(icono, color=color, scale_factor=1.14)
        for icono, color in zip(boceto, (SECUNDARIO, STAGING, RAMA_MAIN))
    ], lag_ratio=0.45)


def _vive_cadena(boceto):
    """La luz recorriendo la cadena, de un commit al siguiente."""
    return LaggedStart(*[
        pulso(boceto[i], CLARO, run_time=0.55, ancho=5) for i in (1, 3)
    ], lag_ratio=0.5)


def _vive_rama(boceto):
    """El ramal encendiéndose y desembocando en el merge."""
    return LaggedStart(
        pulso(boceto[3], RAMA_FEATURE, run_time=0.6, ancho=5),
        pulso(boceto[5], RAMA_FEATURE, run_time=0.6, ancho=5),
        Indicate(boceto[2], color=RAMA_MAIN, scale_factor=1.25),
        lag_ratio=0.45,
    )


def _vive_remoto(boceto):
    """Una copia sube y otra baja: eso es todo lo que hay entre dos repos."""
    _, _, ida, vuelta = boceto
    return Succession(
        pulso(ida, OK, run_time=0.55, ancho=5),
        pulso(vuelta, PRIMARIO, run_time=0.55, ancho=5),
    )


# (cómo se dibuja, cómo vive en el bucle)
REPASO = (
    (_boceto_zonas, _vive_zonas),
    (_boceto_cadena, _vive_cadena),
    (_boceto_rama, _vive_rama),
    (_boceto_remoto, _vive_remoto),
)


def _dibujarse(boceto, lag=0.3):
    """El boceto haciéndose solo, pieza a pieza y en el orden en que llegó."""
    return LaggedStart(*[
        GrowFromCenter(pieza) if getattr(pieza, "crece", False) else Create(pieza)
        for pieza in boceto
    ], lag_ratio=lag)


def _papel(dibujar):
    """Un papel de la tira: el boceto solo, centrado y sin rótulo."""
    fondo = RoundedRectangle(
        width=ANCHO_PAPEL, height=ALTO_PAPEL, corner_radius=0.14,
        stroke_color=SECUNDARIO, stroke_width=1.6,
    ).set_fill(CLARO, opacity=0.03)
    fondo.set_stroke(opacity=0.3)
    return VGroup(fondo, dibujar().move_to(fondo.get_center()))


# --------------------------------------------------------------------------
def construir(scene):
    # --- Cabecera ----------------------------------------------------------
    gracias = VGroup(
        texto("MUCHAS", TAM_GRACIAS, color=CLARO, font=FONT_TITULO),
        texto("GRACIAS", TAM_GRACIAS, color=PRIMARIO, font=FONT_TITULO),
    ).arrange(RIGHT, buff=0.5)
    if gracias.width > ANCHO_MAX_GRACIAS:
        gracias.scale(ANCHO_MAX_GRACIAS / gracias.width)
    gracias.move_to([0, Y_GRACIAS, 0])

    # --- El historial y su desemboque --------------------------------------
    nodos, hilos, punteros, ultimo = _historial()
    salida, riel = _desemboque(ultimo)

    # --- El QR, que hace de destino ----------------------------------------
    papel_qr = RoundedRectangle(
        width=LADO_TARJETA, height=LADO_TARJETA, corner_radius=0.2,
        stroke_color=PRIMARIO, stroke_width=3,
    ).set_fill(BLANCO, opacity=1.0).move_to([X_QR, Y_TARJETA, 0])
    codigo = imagen("qr_formulario")
    codigo.scale_to_fit_width(LADO_TARJETA - MARGEN_QR * 2)
    codigo.move_to(papel_qr.get_center())
    tarjeta = Group(papel_qr, codigo)

    pie_qr = VGroup(
        texto("Escanea el código", 15, color=CLARO),
        texto("Asistencia y material de la charla", 14, color=SECUNDARIO),
    ).arrange(DOWN, buff=0.12).move_to([X_QR, Y_PIE_QR, 0])

    # --- La tira de repaso y la firma --------------------------------------
    tira = VGroup(*[_papel(dibujar) for dibujar, _ in REPASO])
    tira.arrange(RIGHT, buff=BUFF_PAPEL).move_to([0, Y_TIRA, 0])

    firma = texto("Semillero de Data Science e IA  ·  Aperture", 15,
                  color=SECUNDARIO).move_to([0, Y_FIRMA, 0])

    # ---------------------- Animación --------------------------------------
    scene.play(FadeIn(gracias[0], shift=UP * 0.18), run_time=0.5)
    scene.play(FadeIn(gracias[1], shift=UP * 0.18), run_time=0.5)

    # El historial se arma como se armó la charla: los commits primero, la
    # rama después, y el merge al final.
    scene.play(
        LaggedStart(*[GrowFromCenter(n) for n in nodos], lag_ratio=0.3),
        run_time=1.1,
    )
    scene.play(
        LaggedStart(*[Create(h) for h in hilos], lag_ratio=0.25),
        run_time=1.1,
    )
    scene.play(FadeIn(punteros, shift=UP * 0.1), run_time=0.45)

    # Y el primer recorrido desemboca en el QR, que aparece al recibirlo.
    scene.play(
        LaggedStart(*[pulso(h, CLARO, run_time=0.7, ancho=7) for h in hilos],
                    lag_ratio=0.3),
        run_time=1.6,
    )
    scene.play(Create(salida), run_time=0.45)
    # La tarjeta primero y el código encima: encadenados, no en dos golpes.
    scene.play(
        LaggedStart(GrowFromCenter(papel_qr), FadeIn(codigo, scale=0.85),
                    lag_ratio=0.55),
        run_time=0.95,
    )
    scene.play(FadeIn(pie_qr, shift=UP * 0.1), run_time=0.4)

    # --- Lo que vimos hoy, en cuatro dibujos -------------------------------
    # Sin pausa antes de la tira: partir aquí congelaría media pantalla vacía.
    # Cada papel entra y se dibuja solo antes de que empiece el siguiente, así
    # que la tira se lee como cuatro dibujos haciéndose y no como cuatro
    # estampas apareciendo de golpe.
    scene.play(
        LaggedStart(*[
            Succession(FadeIn(fondo, shift=UP * 0.18), _dibujarse(boceto))
            for fondo, boceto in tira
        ], lag_ratio=0.42),
        run_time=2.8,
    )
    scene.play(FadeIn(firma, shift=UP * 0.1), run_time=0.4)

    # --- Y se queda vivo ---------------------------------------------------
    # Sin indicador en la última pausa: no queda nada que anunciar, y su
    # animación de entrada caería dentro del bucle, parpadeando en cada vuelta.
    # El armado desemboca directo en el bucle, sin clic intermedio: marcamos
    # con ``auto_next`` la diapositiva del armado —la que sigue abierta hasta
    # este ``next_slide``— para que manim-slides encadene sola con el bucle.
    if hasattr(scene, "_base_slide_config"):
        scene._base_slide_config.auto_next = True
    scene.next_slide(loop=True, indicador=False)
    # Los cuatro papeles se mueven con la oleada, escalonados de izquierda a
    # derecha: viven en su propia banda, así que no compiten con el historial
    # y el ojo puede recorrerlos mientras la luz cruza arriba.
    scene.play(
        LaggedStart(
            *[pulso(h, CLARO, run_time=0.7, ancho=7) for h in hilos],
            AnimationGroup(
                ShowPassingFlash(riel.copy().set_stroke(PRIMARIO, 5.0, 1.0),
                                 time_width=0.4),
                tarjeta.animate(rate_func=there_and_back).scale(1.045),
                lag_ratio=0.55,
            ),
            lag_ratio=0.3,
        ),
        LaggedStart(*[
            vivir(papel[1]) for (_, vivir), papel in zip(REPASO, tira)
        ], lag_ratio=0.22),
        run_time=2.6,
    )

    scene.next_slide(indicador=False)
