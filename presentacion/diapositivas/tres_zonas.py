"""Diapositiva 10 — las tres zonas.

La diapositiva más importante de la charla. Casi todo lo que confunde de git
—por qué hay que hacer ``add`` antes de ``commit``, qué significa "staged", por
qué ``git status`` habla de dos listas distintas— se cae solo en cuanto se ve
que hay **tres sitios** y que cada comando baja cosas de uno al siguiente:

    directorio de trabajo  --add-->  staging  --commit-->  repositorio

Va en vertical y de arriba abajo a propósito: así el recorrido es una caída,
y una caída se entiende sin leer nada. Por eso aquí no hay frases: en pantalla
solo están los nombres de las tres zonas, los dos comandos pegados a sus
flechas y el sello del final. Lo demás lo cuenta el movimiento.

Dos detalles que se animan porque explicarlos por escrito cuesta un párrafo:

  * ``git add`` no se lleva el archivo de tu carpeta. Baja una **copia** al
    staging —marcada en ámbar— y el original se queda donde estaba, atenuado.
  * ``git commit`` funde lo que hay en staging en **un solo punto** del
    historial, y el staging se queda vacío para la siguiente tanda.

Viene detrás de ``git_init``, que es donde ha nacido el ``.git`` en el que
acaban los commits de esta.

Y termina girando el dibujo: las tres cajas apiladas se estiran hasta ser tres
carriles verticales, uno por zona. Las cajas cuentan bien un viaje de una vez,
pero se quedan sin sitio en cuanto hay historial; el carril deja el eje
vertical entero para el tiempo y el horizontal para los comandos. Ese es el
mapa que heredan las diapositivas siguientes, que lo reconstruyen llamando a
``carriles_zonas``.

Sobre ese mapa se hace el recorrido una última vez, ya sin abstracciones: un
archivo con nombre —``i-use-arch.btw``— saltando de carril en carril, y debajo
la terminal con la sesión tal cual se teclea. Ahí es donde entra ``git
status``: después de cada comando se vuelve a lanzar, y lo que contesta es
exactamente en qué carril está el archivo. Esa es toda la explicación del
comando —no cuenta nada nuevo, lee este dibujo en voz alta—, y de paso los tres
que hay que saber quedan juntos y en orden: ``status``, ``add``, ``commit``.
"""

from manim import (
    BOLD,
    DOWN,
    LEFT,
    RIGHT,
    UP,
    AnimationGroup,
    Create,
    FadeIn,
    FadeOut,
    Flash,
    LaggedStart,
    ReplacementTransform,
    RoundedRectangle,
    Transform,
    VGroup,
)

from animaciones import flecha, pulso, teclear
from componentes import (
    ALTO_BARRA,
    archivo,
    cajon,
    carpeta,
    carriles,
    discos,
    linea_terminal,
    nodo_commit,
    tarjeta,
    texto,
    ventana,
    zona,
)
from componentes import titulo as hacer_titulo
from estilo import ERROR, OK, RAMA_MAIN, SECUNDARIO, STAGING, SUPERFICIE

TITULO = "Las tres zonas"

# --- Las tres cajas, apiladas ----------------------------------------------
# (nombre, color de rol, borde discontinuo). El staging va con el borde roto
# porque es el único de los tres que está de paso: se vacía en cada commit.
ZONAS = (
    ("directorio de trabajo", SECUNDARIO, False),
    ("staging", STAGING, True),
    ("repositorio", RAMA_MAIN, False),
)
ANCHO_ZONA = 9.4
ALTO_ZONA = 1.3
Y_ZONAS = (1.95, -0.1, -2.15)     # el hueco entre cajas es el de las flechas
TAM_ROTULO = 21
BUFF_ROTULO = 0.45                # del borde izquierdo de la caja al nombre

# --- Lo que baja de una a otra ---------------------------------------------
PASOS = (("git add", STAGING), ("git commit", RAMA_MAIN))
TAM_COMANDO = 19
N_ARCHIVOS = 3
ALTO_ARCHIVO = 0.72
BUFF_ARCHIVOS = 0.5
X_ARCHIVOS = 2.3                  # a la derecha del nombre, dentro de la caja
FANTASMA = 0.25                   # lo que queda del original tras el add
SELLO = "guardado"
X_SELLO = 4.15

# --- El mismo mapa, ya en carriles -----------------------------------------
# Los tres carriles, centrados en el frame: el del staging cae justo en el eje
# y los otros dos a la misma distancia, así que el dibujo queda simétrico y
# sobra sitio a los dos lados para las flechas de las diapositivas siguientes.
X_CARRILES = (-3.4, 0.0, 3.4)
TAM_CARRIL = 19
ALTO_ICONO = 0.92

# --- El recorrido final, con un archivo de verdad y la terminal debajo ------
EJEMPLO = "i-use-arch.btw"
MENSAJE = "flexeando arch"
HASH = "7d3e"
Y_CARRIL_CORTO = -1.35            # los carriles se recogen para dejar sitio
Y_EJEMPLO = -0.12                 # la fila por la que el archivo salta
ALTO_EJEMPLO = 0.6
RADIO_NODO = 0.3                  # el commit ocupa lo mismo que el icono
TAM_EJEMPLO = 15
BUFF_PARADA = 0.16                # del icono a su nombre, dentro de la caja
MARGEN_PARADA = (0.5, 0.4)        # lo que la caja sobra por los lados y arriba

# El color del archivo en cada carril, que es lo único que hace falta decir:
# rojo si git ni lo sigue, ámbar cuando está apartado para el commit y cian
# cuando ya es un commit. Lo que significa cada uno lo cuenta la terminal.
COLOR_PARADA = (ERROR, STAGING, RAMA_MAIN)

# La sesión, un paso por pantalla: el comando que toca y lo que contesta git.
# No crece hacia abajo —no hay sitio, y nadie lee diez líneas en una charla—,
# así que cada paso estrena las suyas. ``git status`` se repite en todos a
# propósito: es la costumbre que hay que pegar, mirar dónde estás después de
# cada cosa que haces.
SESION = (
    (("git status", "cmd"),
     ("Untracked files:", "out"),
     (f"      {EJEMPLO}", "err")),
    ((f"git add {EJEMPLO}", "cmd"),
     ("git status", "cmd"),
     ("Changes to be committed:", "out"),
     (f"      new file:   {EJEMPLO}", "ok")),
    ((f'git commit -m "{MENSAJE}"', "cmd"),
     (f"[main {HASH}] {MENSAJE}", "out"),
     ("git status", "cmd"),
     ("nothing to commit, working tree clean", "ok")),
)
ANCHO_CONSOLA = 8.0
ALTO_CONSOLA = 2.15
Y_CONSOLA = -2.62
MARGEN_CONSOLA = 0.5
TAM_SESION = 15
BUFF_SESION = 0.17
# Alto de la primera línea: fija, para que al cambiar de paso la sesión no
# suba y baje. Una terminal escribe desde arriba, tenga tres líneas o cuatro.
Y_SESION = Y_CONSOLA + ALTO_CONSOLA / 2 - ALTO_BARRA - 0.2


def _zonas():
    """Las tres cajas, con el nombre dentro y pegado a la izquierda.

    ``zona`` cuelga el rótulo por encima de la caja, que es lo que quiere una
    diapositiva con las zonas en fila; aquí van apiladas y no cabe, así que el
    nombre se mete dentro y el resto de la caja queda libre para los archivos.
    """
    cajas = []
    for (nombre, color, discontinua), y in zip(ZONAS, Y_ZONAS):
        caja = zona(nombre, color, ANCHO_ZONA, ALTO_ZONA, TAM_ROTULO,
                    discontinua)
        caja[0].move_to([0, y, 0])
        caja[1].move_to(
            caja[0].get_left() + RIGHT * (caja[1].width / 2 + BUFF_ROTULO))
        cajas.append(caja)
    return cajas


def _puentes(cajas):
    """Las dos flechas de bajada, cada una con su comando al lado."""
    puentes = VGroup()
    for (comando, color), arriba, abajo in zip(PASOS, cajas, cajas[1:]):
        punta = flecha([0, arriba[0].get_bottom()[1], 0],
                       [0, abajo[0].get_top()[1], 0],
                       color=color, buff=0.08, grosor=4)
        etiqueta = texto(comando, TAM_COMANDO, color=color)
        etiqueta.next_to(punta, RIGHT, buff=0.3)
        puentes.add(VGroup(punta, etiqueta))
    return puentes


def _archivos():
    """Tres archivos sin nombre: aquí lo que importa es por dónde pasan."""
    iconos = VGroup(*[
        archivo(color=SECUNDARIO, alto=ALTO_ARCHIVO) for _ in range(N_ARCHIVOS)
    ]).arrange(RIGHT, buff=BUFF_ARCHIVOS)
    return iconos.move_to([X_ARCHIVOS, Y_ZONAS[0], 0])


def carriles_zonas():
    """Las tres zonas como carriles verticales, colocadas y listas para usar.

    Nacen al final de esta diapositiva, pero son de todas: cualquier otra que
    quiera este mapa lo importa de aquí (``from diapositivas.tres_zonas import
    carriles_zonas``) en vez de repetir las x, los iconos y los nombres. Así
    los carriles caen siempre en el mismo sitio y la charla entera se lee como
    un solo dibujo que va creciendo.
    """
    iconos = (
        carpeta(ALTO_ICONO, SECUNDARIO),
        cajon(ALTO_ICONO, STAGING),
        discos(ALTO_ICONO, RAMA_MAIN),
    )
    zonas = [(icono, nombre, color)
             for icono, (nombre, color, _) in zip(iconos, ZONAS)]
    return carriles(zonas, X_CARRILES, tam=TAM_CARRIL)


def _parada(indice, color=None, fantasma=False):
    """El archivo plantado en el carril ``indice``, dentro de su propia caja.

    La caja no es adorno: el carril es una línea gruesa que si no pasaría por
    encima del icono y del nombre. Rellena con el color de los nodos, los tapa
    y de paso los agrupa en lo que son, una sola cosa —este archivo, aquí—.

    En el último carril el archivo ya no es un archivo sino un commit, así que
    la caja lleva dentro el nodo; como mide lo mismo, la caja no cambia de
    tamaño al pasar de una parada a la siguiente.

    ``color`` fuerza otro color (el archivo ya guardado, que no debe nada) y
    ``fantasma`` deja solo la marca de que el original sigue en su carpeta.
    """
    color = COLOR_PARADA[indice] if color is None else color
    pieza = (nodo_commit(HASH, color, RADIO_NODO, TAM_EJEMPLO - 1)
             if indice == len(X_CARRILES) - 1
             else archivo(color=color, alto=ALTO_EJEMPLO))
    contenido = VGroup(
        pieza, texto(EJEMPLO, TAM_EJEMPLO, color=color),
    ).arrange(DOWN, buff=BUFF_PARADA)
    caja = RoundedRectangle(
        width=contenido.width + MARGEN_PARADA[0],
        height=contenido.height + MARGEN_PARADA[1],
        corner_radius=0.14, stroke_color=color, stroke_width=2.5,
    ).set_fill(SUPERFICIE, opacity=1.0)
    caja.move_to(contenido.get_center())
    if fantasma:
        contenido.set_opacity(FANTASMA)
        caja.set_stroke(opacity=FANTASMA)
    return VGroup(caja, contenido).move_to([X_CARRILES[indice], Y_EJEMPLO, 0])


def _marco_consola():
    """La ventana de la terminal, vacía y del tamaño del paso más largo.

    Se crea una vez y se queda: lo que cambia en cada paso son las líneas de
    dentro (``_sesion``), no la ventana, así que la terminal no baila.
    """
    return ventana(ANCHO_CONSOLA, ALTO_CONSOLA, "terminal", 14).move_to(
        [0, Y_CONSOLA, 0])


def _sesion(indice):
    """Las líneas del paso ``indice``, colocadas dentro de la ventana.

    Devuelve solo las filas: para teclearlas hay que pasarle a ``teclear`` el
    par ``VGroup(marco, filas)``, que es la forma que tiene una ``terminal``.
    """
    filas = VGroup(*[
        linea_terminal(c, t, TAM_SESION) for c, t in SESION[indice]
    ]).arrange(DOWN, buff=BUFF_SESION, aligned_edge=LEFT)
    filas.align_to([0, Y_SESION, 0], UP)
    return filas.align_to([-ANCHO_CONSOLA / 2 + MARGEN_CONSOLA, 0, 0], LEFT)


def construir(scene):
    encabezado = hacer_titulo(TITULO)
    cajas = _zonas()
    puentes = _puentes(cajas)

    # ---------------------- El mapa ----------------------------------------
    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(
        LaggedStart(*[Create(caja[0]) for caja in cajas], lag_ratio=0.35),
        run_time=1.4,
    )
    scene.play(
        LaggedStart(*[FadeIn(caja[1], shift=RIGHT * 0.15) for caja in cajas],
                    lag_ratio=0.3),
        run_time=0.9,
    )
    scene.play(
        LaggedStart(*[FadeIn(p, shift=DOWN * 0.15) for p in puentes],
                    lag_ratio=0.4),
        run_time=1.0,
    )
    scene.next_slide()

    # ---------------------- git add: baja una copia ------------------------
    ficheros = _archivos()
    scene.play(
        LaggedStart(*[FadeIn(f, shift=UP * 0.12) for f in ficheros],
                    lag_ratio=0.25),
        run_time=0.9,
    )

    # La copia cae en vertical y se pone ámbar; el original se queda en su
    # sitio, apagado. Ese es todo el chiste de ``add``, y así no hace falta
    # contarlo: el archivo no se ha ido a ninguna parte.
    copias = ficheros.copy()
    scene.add(copias)
    scene.play(
        LaggedStart(*[
            copia.animate.move_to(
                [copia.get_center()[0], Y_ZONAS[1], 0]).set_color(STAGING)
            for copia in copias
        ], lag_ratio=0.3),
        ficheros.animate.set_opacity(FANTASMA),
        pulso(puentes[0][0], STAGING, run_time=1.2, ancho=9),
        run_time=1.4,
    )
    scene.next_slide()

    # ---------------------- git commit: los funde en uno -------------------
    commit = nodo_commit("a1c9", RAMA_MAIN, 0.42, 16)
    commit.move_to([X_ARCHIVOS, Y_ZONAS[2], 0])
    sello = tarjeta([(SELLO, 22, BOLD)], color=OK).rotate(-0.16)
    sello.move_to([X_SELLO, Y_ZONAS[2], 0])

    scene.play(
        ReplacementTransform(copias, commit),
        pulso(puentes[1][0], RAMA_MAIN, run_time=1.0, ancho=9),
        run_time=1.1,
    )
    # El sello cae de golpe, como un tampón, y los archivos de arriba vuelven
    # a su color: siguen ahí, y ya están guardados.
    scene.play(
        Flash(commit, color=RAMA_MAIN, line_length=0.28, num_lines=18,
              flash_radius=0.9),
        FadeIn(sello, scale=1.9),
        ficheros.animate.set_opacity(1.0),
        run_time=0.7,
    )
    scene.wait(0.3)
    scene.next_slide()

    # ---------------------- Lo mismo, girado a carriles --------------------
    # Cada caja se estira hasta ser la línea de su zona, y lo que estaba de
    # arriba abajo pasa a estar de izquierda a derecha. No cambia nada de lo
    # dicho: cambia el sitio libre. Con las zonas en carriles, el eje vertical
    # queda entero para el tiempo, que es lo que hace falta a partir de aquí.
    pistas = carriles_zonas()
    scene.play(
        FadeOut(puentes), FadeOut(ficheros), FadeOut(commit), FadeOut(sello),
        run_time=0.5,
    )
    scene.play(
        LaggedStart(*[
            AnimationGroup(
                ReplacementTransform(caja[0], pista[2]),
                ReplacementTransform(caja[1], pista[1]),
            )
            for caja, pista in zip(cajas, pistas)
        ], lag_ratio=0.25),
        run_time=1.4,
    )
    scene.play(
        LaggedStart(*[FadeIn(pista[0], shift=DOWN * 0.15) for pista in pistas],
                    lag_ratio=0.25),
        run_time=0.9,
    )
    scene.next_slide()

    # ---------------------- El recorrido, ya con nombre y terminal ---------
    # Aquí se junta todo. Los carriles se recogen para dejar sitio abajo, y en
    # el hueco entra la terminal: a partir de ahora manda lo que se teclea.
    # Cada comando empuja el archivo al carril siguiente y ``git status``, que
    # se lanza después de cada uno, contesta en cuál está. No hace falta
    # explicar el comando: se ve que está leyendo este dibujo en voz alta.
    scene.play(
        *[pista[2].animate.put_start_and_end_on(
            pista[2].get_start(), [x, Y_CARRIL_CORTO, 0])
          for pista, x in zip(pistas, X_CARRILES)],
        run_time=0.6,
    )

    marco_consola = _marco_consola()
    ejemplo = _parada(0)

    # Nace en rojo en el carril de tu carpeta: existe, pero git no lo sigue.
    scene.play(FadeIn(marco_consola), FadeIn(ejemplo, shift=UP * 0.12),
               run_time=0.6)
    sesion = _sesion(0)
    teclear(scene, VGroup(marco_consola, sesion), ritmo=0.3)
    scene.next_slide()

    # ``git add``: se teclea, salta el archivo, y solo entonces contesta el
    # status. Ese orden es el que hace que el comando no haya que explicarlo.
    copia = ejemplo.copy()
    scene.add(copia)
    scene.play(FadeOut(sesion), run_time=0.3)
    sesion = _sesion(1)
    teclear(scene, VGroup(marco_consola, sesion), hasta=1, ritmo=0.3)
    scene.play(
        Transform(copia, _parada(1)),
        Transform(ejemplo, _parada(0, fantasma=True)),
        run_time=1.0,
    )
    teclear(scene, VGroup(marco_consola, sesion), desde=1, ritmo=0.3)
    scene.next_slide()

    # ``git commit``: lo del staging se funde en un punto del historial y el
    # original vuelve a su color. Ya no debe nada, y el status se queda mudo.
    guardado = _parada(2)
    scene.play(FadeOut(sesion), run_time=0.3)
    sesion = _sesion(2)
    teclear(scene, VGroup(marco_consola, sesion), hasta=1, ritmo=0.3)
    scene.play(ReplacementTransform(copia, guardado), run_time=1.0)
    scene.play(
        Flash(guardado[1][0], color=RAMA_MAIN, line_length=0.28, num_lines=18,
              flash_radius=0.9),
        Transform(ejemplo, _parada(0, color=SECUNDARIO)),
        run_time=0.6,
    )
    teclear(scene, VGroup(marco_consola, sesion), desde=1, ritmo=0.3)
    scene.wait(0.3)

    scene.next_slide()
