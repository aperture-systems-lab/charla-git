"""Diapositiva 18 — ``git reset``: ¿hasta dónde deshace?

Casi todo el susto con ``reset`` viene de no saber hasta dónde llega cada
variante, así que aquí no se cuenta: se ve. Se reconstruye el mapa de carriles
que nace al final de ``tres_zonas`` —directorio de trabajo, staging,
repositorio— con un punto de partida que ya conoce todo el mundo: un commit
hecho, algo añadido y algo sin añadir.

Sobre ese mismo mapa se lanzan los tres resets uno detrás de otro, siempre el
mismo comando y siempre volviendo al punto de partida, para que lo único que
cambie de una pasada a otra sea la bandera. Las tres mueven la rama un commit
atrás —eso es ``reset``, y es lo que nunca cambia—; lo que cambia es qué hacen
con lo que ya tenías delante:

  * ``--soft`` no toca nada de lo tuyo y encima deja en staging lo que traía el
    commit deshecho: es un "me equivoqué de mensaje" y poco más.
  * ``--mixed`` (el que sale por defecto) vacía el staging, pero los cambios no
    se pierden: bajan al directorio de trabajo, sin añadir.
  * ``--hard`` es el único que borra de verdad, y solo se lleva lo que nunca
    llegó a estar en un commit.

Al final, la tabla de siempre como resumen: las tres banderas en filas, las
tres zonas en columnas y un vistazo que se lee en dos segundos.

Sigue en ``git_checkout`` (viajar al pasado) y ``git_reflog`` (la red debajo
del trapecio); las tres dicen lo mismo desde ángulos distintos: se puede
volver atrás.
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
    RoundedRectangle,
    Transform,
    VGroup,
)

from componentes import archivo, aspa, nodo_commit, puntero, texto, visto
from componentes import titulo as hacer_titulo
from estilo import (
    AMBAR,
    ERROR,
    OK,
    RAMA_MAIN,
    SECUNDARIO,
    STAGING,
    SUPERFICIE,
)

from .tres_zonas import X_CARRILES, carriles_zonas

# El mismo título de punta a punta: la diapositiva entera va del comando,
# y lo que cambia de una pantalla a otra ya lo dice el propio dibujo.
TITULO = "git reset"

# --- El mapa de carriles, bajado y recortado por abajo ---------------------
# Los carriles son los de ``tres_zonas`` (misma x, mismos iconos), pero aquí
# caen algo más abajo: sin la terminal debajo sobra sitio al pie, y bajarlos
# reparte el hueco en vez de dejar el dibujo apelotonado contra el título.
BAJADA_MAPA = 0.45
Y_CARRIL = -2.05          # hasta dónde llega la línea de cada carril
Y_FICHA = 0.0             # la fila donde espera lo que ya tenías
Y_BAJADA = -1.2           # donde cae lo que el reset saca del staging
Y_NUEVO = 0.27            # el commit que se va a deshacer
Y_VIEJO = -1.07           # al que retrocede la rama
RADIO = 0.3
Y_MARCA = -2.5            # el veredicto de cada carril, debajo de su línea
Y_ORDEN = -3.2

HASH_NUEVO = "9c1d"
HASH_VIEJO = "77ab"
ALTO_ARCHIVO = 0.46
TAM_FICHA = 13

# (bandera, color, qué le pasa a cada zona, dónde cae lo del commit).
# "retrocede" = la rama se mueve, y es lo único igual en las tres. Lo que hace
# cada una no se escribe en ningún sitio: se ve moverse, y lo dice quien habla.
RESETS = (
    ("--soft", SECUNDARIO, ("intacto", "intacto", "retrocede"), 1),
    ("--mixed", AMBAR, ("intacto", "vacia", "retrocede"), 0),
    ("--hard", ERROR, ("borra", "borra", "retrocede"), None),
)

# --- La tabla del resumen --------------------------------------------------
COLUMNAS = (
    ("directorio de trabajo", -2.9, SECUNDARIO),
    ("staging", 0.65, STAGING),
    ("repositorio", 3.95, RAMA_MAIN),
)
X_BANDERA = -6.4
Y_CABECERA = 1.25
Y_PRIMERA = 0.3
PASO_FILA = 0.95
Y_TABLA = -0.45           # el centro del hueco que deja el título


def _marca(estado, x, y):
    """El veredicto de una zona: intacta, vaciada, borrada o retrocediendo.

    Mismo cartelito en las pasadas y en la tabla del final, a propósito: el
    resumen no estrena lenguaje, repite el que se acaba de ver moverse.
    """
    if estado == "intacto":
        icono, etiqueta, color = visto(OK, tam=0.13), "intacto", OK
    elif estado == "vacia":
        icono, etiqueta, color = texto("↓", 20, color=STAGING), "se vacía", STAGING
    elif estado == "borra":
        icono, etiqueta, color = aspa(ERROR, tam=0.13), "se pierde", ERROR
    else:
        icono, etiqueta, color = texto("←", 20, color=RAMA_MAIN), "retrocede", RAMA_MAIN
    fila = VGroup(icono, texto(etiqueta, 14, color=color))
    return fila.arrange(RIGHT, buff=0.22).move_to([x, y, 0])


def _ficha(nombre, color, carril, y):
    """Un bulto de cambios plantado en un carril, dentro de su caja.

    La caja no es adorno: el carril es una línea gruesa que si no pasaría por
    encima del icono. Rellena del color de los nodos, lo tapa —el mismo truco
    que las paradas de ``tres_zonas``— y de paso agrupa icono y nombre en lo
    que son, una sola cosa.
    """
    contenido = VGroup(
        archivo(color=color, alto=ALTO_ARCHIVO),
        texto(nombre, TAM_FICHA, color=color),
    ).arrange(DOWN, buff=0.14)
    caja = RoundedRectangle(
        width=contenido.width + 0.5, height=contenido.height + 0.34,
        corner_radius=0.14, stroke_color=color, stroke_width=2.5,
    ).set_fill(SUPERFICIE, opacity=1.0)
    caja.move_to(contenido.get_center())
    return VGroup(caja, contenido).move_to([X_CARRILES[carril], y, 0])


def _historial():
    """Los dos commits del carril del repositorio, con la rama pegada al último.

    No hace falta dibujar la arista entre ellos: el propio carril es la línea
    del repositorio, y los une igual. Devuelve los punteros aparte, que son los
    que se mueven —y moverlos es todo lo que hace ``reset``—.
    """
    nuevo = nodo_commit(HASH_NUEVO, RAMA_MAIN, RADIO, 14)
    nuevo.move_to([X_CARRILES[2], Y_NUEVO, 0])
    viejo = nodo_commit(HASH_VIEJO, RAMA_MAIN, RADIO, 14)
    viejo.move_to([X_CARRILES[2], Y_VIEJO, 0])
    punteros = VGroup(
        puntero("HEAD", OK, 13), puntero("main", RAMA_MAIN, 13),
    ).arrange(DOWN, buff=0.12).next_to(nuevo, RIGHT, buff=0.28)
    return nuevo, viejo, punteros


def _partida():
    """Lo que hay antes de cada reset: dos cambios esperando, cada uno en su zona."""
    return VGroup(
        _ficha("sin añadir", ERROR, 0, Y_FICHA),
        _ficha("añadido", STAGING, 1, Y_FICHA),
    )


def construir(scene):
    encabezado = hacer_titulo(TITULO)
    pistas = carriles_zonas().shift(DOWN * BAJADA_MAPA)
    for pista, x in zip(pistas, X_CARRILES):
        pista[2].put_start_and_end_on(pista[2].get_start(), [x, Y_CARRIL, 0])

    # ---------------------- El punto de partida ----------------------------
    scene.play(FadeIn(encabezado, shift=DOWN * 0.2), run_time=0.6)
    scene.play(
        LaggedStart(*[FadeIn(pista[0], shift=DOWN * 0.15) for pista in pistas],
                    lag_ratio=0.25),
        run_time=0.8,
    )
    scene.play(
        LaggedStart(*[FadeIn(pista[1]) for pista in pistas], lag_ratio=0.25),
        *[Create(pista[2]) for pista in pistas],
        run_time=0.9,
    )

    nuevo, viejo, punteros = _historial()
    fichas = _partida()
    scene.play(
        LaggedStart(GrowFromCenter(viejo), GrowFromCenter(nuevo),
                    lag_ratio=0.4),
        run_time=0.9,
    )
    scene.play(FadeIn(punteros, shift=LEFT * 0.15), run_time=0.5)
    scene.play(
        LaggedStart(*[GrowFromCenter(f) for f in fichas], lag_ratio=0.3),
        run_time=0.9,
    )
    scene.next_slide()

    # ---------------------- Los tres, uno por uno --------------------------
    for bandera, color, estados, destino in RESETS:
        orden = texto(f"git reset {bandera} HEAD~1", 20, color=color)
        orden.move_to([0, Y_ORDEN, 0])
        scene.play(FadeIn(orden, shift=UP * 0.1), run_time=0.45)

        # Lo que hacen las tres: la rama suelta el último commit y retrocede.
        # El commit no se borra —se queda ahí, sin nadie que lo señale—, y por
        # eso se apaga en vez de desaparecer.
        marca_repo = _marca(estados[2], X_CARRILES[2], Y_MARCA)
        scene.play(
            punteros.animate.next_to(viejo, RIGHT, buff=0.28),
            nuevo.animate.set_opacity(0.28),
            FadeIn(marca_repo, shift=UP * 0.1),
            run_time=1.0,
        )

        # Y lo que cambia de una bandera a otra: qué pasa con lo que ya tenías
        # en cada carril, de izquierda a derecha y uno por uno.
        marcas = VGroup(marca_repo)
        aspas = VGroup()
        for i, estado in enumerate(estados[:2]):
            marca = _marca(estado, X_CARRILES[i], Y_MARCA)
            if estado == "intacto":
                efecto = Indicate(fichas[i], color=OK, scale_factor=1.08)
            elif estado == "vacia":
                # No se pierde: se desmarca y baja al carril de al lado.
                efecto = Transform(
                    fichas[i], _ficha("sin añadir", ERROR, 0, Y_BAJADA))
            else:
                cruz = aspa(ERROR, tam=0.34, grosor=7)
                cruz.move_to(fichas[i].get_center())
                aspas.add(cruz)
                efecto = LaggedStart(GrowFromCenter(cruz),
                                     fichas[i].animate.set_opacity(0.12),
                                     lag_ratio=0.4)
            scene.play(efecto, FadeIn(marca, shift=UP * 0.1), run_time=0.9)
            marcas.add(marca)

        # Lo que traía el commit deshecho tiene que caer en algún sitio, y ese
        # sitio es justo lo que distingue ``--soft`` de ``--mixed``.
        if destino is not None:
            bulto = nodo_commit("", RAMA_MAIN, 0.15).move_to(nuevo.get_center())
            scene.add(bulto)
            scene.play(
                bulto.animate.move_to(fichas[destino].get_center()),
                run_time=0.8,
            )
            scene.play(
                FadeOut(bulto, scale=0.3),
                Flash(fichas[destino], color=color, line_length=0.16,
                      num_lines=12, flash_radius=0.75),
                run_time=0.5,
            )

        scene.next_slide()

        # Y vuelta al punto de partida, para que la siguiente bandera se lea
        # contra lo mismo y no contra lo que dejó la anterior. Las fichas se
        # transforman en vez de cambiarse por otras: así se ve rebobinar lo que
        # el reset acababa de mover, y ninguna caja se funde sobre su carril.
        scene.play(
            FadeOut(orden), FadeOut(marcas), FadeOut(aspas),
            Transform(fichas, _partida()),
            punteros.animate.next_to(nuevo, RIGHT, buff=0.28),
            nuevo.animate.set_opacity(1.0),
            run_time=0.7,
        )

    # ---------------------- El resumen: la tabla ---------------------------
    cabeceras = VGroup(*[
        texto(nombre, 16, color=color).move_to([x, Y_CABECERA, 0])
        for nombre, x, color in COLUMNAS
    ])
    raya = Line([X_BANDERA - 0.2, Y_CABECERA - 0.4, 0],
                [4.95, Y_CABECERA - 0.4, 0],
                color=SECUNDARIO, stroke_width=2).set_stroke(opacity=0.4)

    filas = VGroup()
    for i, (bandera, color, estados, _destino) in enumerate(RESETS):
        y = Y_PRIMERA - i * PASO_FILA
        nombre = texto(f"git reset {bandera}", 17, color=color)
        nombre.move_to([X_BANDERA, y, 0], LEFT)
        marcas = VGroup(*[
            _marca(estado, x, y)
            for estado, (_, x, _c) in zip(estados, COLUMNAS)
        ])
        filas.add(VGroup(nombre, marcas))

    # Cada celda se coloca por su columna y su fila, que es lo cómodo para
    # escribirla pero deja el bloque escorado; se centra entero de una vez en
    # vez de ir cuadrando números a mano.
    VGroup(cabeceras, raya, filas).move_to([0, Y_TABLA, 0])

    scene.play(
        FadeOut(pistas), FadeOut(nuevo), FadeOut(viejo),
        FadeOut(punteros), FadeOut(fichas),
        run_time=0.8,
    )
    scene.play(
        LaggedStart(*[FadeIn(c, shift=DOWN * 0.1) for c in cabeceras],
                    lag_ratio=0.25),
        Create(raya), run_time=1.0,
    )
    for fila in filas:
        scene.play(FadeIn(fila[0], shift=RIGHT * 0.15), run_time=0.4)
        scene.play(
            LaggedStart(*[FadeIn(m, shift=UP * 0.1) for m in fila[1]],
                        lag_ratio=0.25),
            run_time=0.7,
        )
    scene.play(Indicate(filas[2][0], color=ERROR, scale_factor=1.12),
               run_time=0.6)
    scene.wait(0.3)

    scene.next_slide()
