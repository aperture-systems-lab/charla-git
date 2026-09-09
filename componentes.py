"""Fábricas de mobjects reutilizables (texto, terminal, nodos de commit…).

Todas son funciones puras: reciben parámetros y devuelven mobjects listos
para posicionar y animar desde las diapositivas. Aquí viven las piezas que
esta charla repite sin parar —la ventana de terminal, el nodo de commit, el
puntero de rama, el icono de archivo— para que ninguna diapositiva tenga que
dibujar un rectángulo redondeado a mano.
"""

import os

import numpy as np
from manim import (
    DOWN,
    DR,
    LEFT,
    NORMAL,
    ORIGIN,
    RIGHT,
    UP,
    Circle,
    CubicBezier,
    DashedVMobject,
    Dot,
    Ellipse,
    Group,
    ImageMobject,
    Line,
    ManimColor,
    Polygon,
    Rectangle,
    RoundedRectangle,
    Text,
    VGroup,
    VMobject,
    config,
)
from PIL import Image, ImageDraw, ImageOps

from estilo import (
    AMBAR,
    ASSETS,
    BLANCO,
    CLARO,
    ERROR,
    FONDO,
    FONT,
    OK,
    PRIMARIO,
    RAMA_FEATURE,
    RAMA_MAIN,
    SECUNDARIO,
    STAGING,
    SUPERFICIE,
    TAM_TITULO,
    VERDE,
)
from estilo import FONT_TITULO


def marco():
    """Borde decorativo del color de marca, del tamaño del frame."""
    return Rectangle(
        width=config.frame_width - 0.22,
        height=config.frame_height - 0.22,
        stroke_color=PRIMARIO,
        stroke_width=8,
        fill_opacity=0,
    )


# --- Fondo decorativo ------------------------------------------------------
# Presets del grafo de fondo: (commits, y del tronco, ramas, semilla, color,
# opacidad). El fondo de esta charla no es una malla neuronal sino lo que la
# charla explica: un historial con ramas que salen y vuelven.
PRESETS_GRAFO = (
    (9, 1.6, 2, 7, SECUNDARIO, 0.16),
    (12, -1.9, 3, 13, PRIMARIO, 0.13),
    (7, 2.2, 2, 21, SECUNDARIO, 0.18),
    (14, -1.4, 3, 34, SECUNDARIO, 0.11),
    (10, 1.1, 2, 55, PRIMARIO, 0.15),
)


def grafo_decorativo(indice=0):
    """Historial tenue —tronco, commits y ramas— para el fondo de una diapositiva.

    ``indice`` elige preset rotando (``indice % 5``): pásale el número de
    diapositiva y el fondo va variando solo. Es decorativo y va muy bajo de
    opacidad a propósito: nunca debe competir con el contenido.
    """
    n, y0, n_ramas, semilla, color, op = PRESETS_GRAFO[indice % len(PRESETS_GRAFO)]
    rng = np.random.default_rng(semilla)
    w = config.frame_width / 2 - 0.25
    xs = np.linspace(-w, w, n)
    grupo = VGroup()

    tronco = Line([xs[0], y0, 0], [xs[-1], y0, 0],
                  color=color, stroke_width=1.2, stroke_opacity=op)
    grupo.add(tronco)
    for x in xs:
        grupo.add(Dot([x, y0, 0], radius=0.05, color=color, fill_opacity=op * 2.0))

    # Cada rama sale de un commit, sube (o baja) y vuelve a entrar unos
    # commits más adelante: el dibujo de un merge, repetido y muy tenue.
    for _ in range(n_ramas):
        i = int(rng.integers(0, n - 3))
        j = min(i + int(rng.integers(2, 4)), n - 1)
        dy = float(rng.choice([-1.0, 1.0])) * float(rng.uniform(0.85, 1.7))
        salida, entrada = np.array([xs[i], y0, 0]), np.array([xs[j], y0, 0])
        cima = (salida + entrada) / 2 + np.array([0, dy, 0])
        curva = VMobject(color=color, stroke_width=1.2)
        curva.set_points_smoothly([salida, cima, entrada])
        curva.set_stroke(opacity=op)
        grupo.add(curva)
        for t in (0.35, 0.65):
            grupo.add(Dot(curva.point_from_proportion(t), radius=0.045,
                          color=color, fill_opacity=op * 2.0))
    return grupo


# --- Imágenes --------------------------------------------------------------
_EXTENSIONES = (".png", ".jpg", ".jpeg", ".webp", ".avif", ".gif", ".bmp")


def ruta_asset(nombre):
    """Ruta dentro de ``assets``; sin extensión conocida se asume ``.png``.

    Se compara contra una lista en vez de usar ``splitext`` porque aquí hay
    nombres con número de versión dentro: para ``splitext``, la "extensión" de
    ``mc/mc_1.16`` es ``.16``.
    """
    if not nombre.lower().endswith(_EXTENSIONES):
        nombre = f"{nombre}.png"
    return os.path.join(ASSETS, nombre)


def imagen(nombre, escala=1.0):
    """Carga ``assets/<nombre>`` como ImageMobject.

    Si ``nombre`` no trae extensión se asume ``.png``, así que
    ``imagen("logo")`` e ``imagen("foto.jpg")`` funcionan igual.
    """
    return ImageMobject(ruta_asset(nombre)).scale(escala)


def imagen_circular(nombre, diametro=3.2, relleno=BLANCO, ocupacion=0.86):
    """``assets/<nombre>`` compuesta sobre un disco liso y recortada en círculo.

    Devuelve un único ImageMobject que ya llega con los bordes redondos, así que
    no hay que taparle las esquinas con otro mobject encima. ``ocupacion`` es la
    fracción del disco que ocupa la imagen (el resto queda de margen).
    """
    original = Image.open(ruta_asset(nombre)).convert("RGBA")

    lado = max(original.size)
    foto = ImageOps.contain(
        original, (int(lado * ocupacion),) * 2, Image.LANCZOS
    )
    disco = Image.new("RGBA", (lado, lado), (*ManimColor(relleno).to_int_rgb(), 255))
    disco.alpha_composite(
        foto, ((lado - foto.width) // 2, (lado - foto.height) // 2)
    )

    # Máscara dibujada a 4x y reducida: el borde del círculo sale sin dientes.
    mascara = Image.new("L", (lado * 4, lado * 4), 0)
    ImageDraw.Draw(mascara).ellipse((0, 0, lado * 4 - 1, lado * 4 - 1), fill=255)
    disco.putalpha(mascara.resize((lado, lado), Image.LANCZOS))

    mob = ImageMobject(np.array(disco)).scale_to_fit_width(diametro)
    # El caché de escena de manim resume los arrays grandes recortándolos a su
    # esquina superior izquierda, que aquí siempre es blanca: sin esta marca en
    # el ``__dict__`` dos discos distintos tienen el mismo hash y al
    # re-renderizar se reutilizaría el vídeo antiguo.
    mob.receta_circular = (nombre, diametro, relleno, ocupacion)
    return mob


def imagen_recortada(nombre, ancho=2.0, radio=0.1):
    """``assets/<nombre>`` con las esquinas redondeadas.

    Para que una foto o un pantallazo no rompa el lenguaje de cajas redondeadas
    del resto de la charla. ``radio`` es la fracción del lado que se redondea.
    """
    original = Image.open(ruta_asset(nombre)).convert("RGBA")
    w, h = original.size

    # La máscara se dibuja a 4x y se reduce: las esquinas salen sin dientes.
    mascara = Image.new("L", (w * 4, h * 4), 0)
    ImageDraw.Draw(mascara).rounded_rectangle(
        (0, 0, w * 4 - 1, h * 4 - 1), radius=int(min(w, h) * 4 * radio), fill=255,
    )
    original.putalpha(mascara.resize((w, h), Image.LANCZOS))

    mob = ImageMobject(np.array(original)).scale_to_fit_width(ancho)
    mob.receta_recorte = (nombre, ancho, radio)   # ver nota en imagen_circular
    return mob


def fotografia(nombre, ancho=3.0, pie=None, giro=-0.045):
    """``assets/<nombre>`` montada como una foto revelada de las de antes.

    Papel blanco con margen, el de abajo más ancho que los otros tres —ahí va
    escrito el pie—, y una pizca de inclinación para que parezca puesta encima
    de la diapositiva en vez de pegada al fondo.
    """
    foto = imagen(nombre).scale_to_fit_width(ancho)
    margen = ancho * 0.055
    margen_pie = ancho * 0.2 if pie else margen
    papel = RoundedRectangle(
        width=ancho + 2 * margen,
        height=foto.height + margen + margen_pie,
        corner_radius=0.06, stroke_width=0,
    ).set_fill(BLANCO, opacity=1.0)

    foto.move_to(papel.get_top() + DOWN * (margen + foto.height / 2))
    grupo = Group(papel, foto)
    if pie:
        rotulo = texto(pie, ancho * 5.6, color=FONDO)
        rotulo.move_to(papel.get_bottom() + UP * margen_pie / 2)
        grupo.add(rotulo)
    return grupo.rotate(giro)


def logo_esquina(ancho=0.8, buff=0.3):
    """Logo del semillero en la esquina inferior derecha.

    Lo usan la portada y el cierre como firma, y ``SlideBase.next_slide`` como
    indicador de avance antes de cada pausa. Misma fábrica a propósito: en esas
    dos diapositivas el indicador cae exactamente encima del que ya estaba, así
    que no se duplica ni se desalinea aunque se cambien aquí las medidas.
    """
    logo = imagen("aperture-eye-cyan")
    return logo.scale_to_fit_width(ancho).to_corner(DR, buff=buff)


# --- Texto -----------------------------------------------------------------
def texto(contenido, tam, color=CLARO, weight=NORMAL, font=FONT, t2c=None):
    """Texto con la fuente del proyecto (``font`` permite sobreescribirla).

    Por defecto usa el color claro de marca, legible sobre el fondo oscuro.

    Ojo con ``tam``: Pango cuantiza el tamaño en tramos de seis puntos, así
    que 15 y 20 salen del mismo tamaño en pantalla y de 14 a 15 hay un salto
    del 48 %. Los tramos son 10-14, 15-20, 21-26, 27-32… Para que un texto se
    vea más grande hay que cruzar de tramo; subirlo de 16 a 18 no hace nada.

    ``t2c`` pinta trozos sueltos de la cadena. Las claves son expresiones
    regulares, así que para señalar una parte concreta conviene la forma por
    posición —``"[17:20]"``— y no la palabra: un ``$`` o un paréntesis dentro
    de la clave hace cosas raras. Lo usa :func:`linea_terminal` para el prompt
    y lo usan las diapositivas que despiezan un comando.
    """
    return Text(contenido, font=font, font_size=tam, color=color, weight=weight,
                t2c=t2c or {})


def parrafo(lineas, buff=0.15, alinear=ORIGIN):
    """Varias líneas apiladas. ``lineas`` es una lista de tuplas ``(txt, tam, ...)``."""
    textos = [texto(*linea) for linea in lineas]
    return VGroup(*textos).arrange(DOWN, buff=buff, aligned_edge=alinear)


def titulo(contenido):
    """Título de diapositiva anclado al borde superior.

    Mismo tratamiento que la pantalla de espera (``pronto_iniciamos``): fuente
    pixel en cian directamente sobre el fondo, sin tarjeta detrás. Si el título
    es largo se encoge para no comerse el marco.
    """
    t = texto(contenido, TAM_TITULO, color=PRIMARIO, font=FONT_TITULO)
    ancho_max = config.frame_width - 1.8
    if t.width > ancho_max:
        t.scale(ancho_max / t.width)
    return t.to_edge(UP, buff=0.6)


def vinetas(textos, tam=26, buff=0.45, color=PRIMARIO):
    """Lista de viñetas (punto de marca + texto), alineadas a la izquierda."""
    filas = VGroup()
    for contenido in textos:
        punto = Dot(radius=0.07, color=color)
        filas.add(VGroup(punto, texto(contenido, tam)).arrange(RIGHT, buff=0.25))
    return filas.arrange(DOWN, buff=buff, aligned_edge=LEFT)


def tarjeta(lineas, ancho_extra=0.7, alto_extra=0.4, color=PRIMARIO):
    """Tarjeta rellena de color de marca con texto oscuro encima.

    ``lineas``: lista de tuplas ``(texto, font_size, weight)``.
    """
    textos = VGroup(*[
        texto(t, fs, color=FONDO, weight=w) for t, fs, w in lineas
    ]).arrange(DOWN, buff=0.1)
    fondo = RoundedRectangle(
        corner_radius=0.14,
        width=textos.width + ancho_extra,
        height=textos.height + alto_extra,
        fill_color=color,
        fill_opacity=1.0,
        stroke_width=0,
    )
    return VGroup(fondo, textos)


def burbuja(autor, mensaje, color=SECUNDARIO, tam=16, adjunto=False,
            cola=None):
    """Mensaje de un chat de grupo: quién escribe, dentro de su globo.

    ``adjunto=True`` pone el icono de archivo delante del texto: son los
    mensajes que en realidad son "te paso mi versión del proyecto", que es
    justo la forma de trabajar que git vino a jubilar.

    ``cola=LEFT`` o ``cola=RIGHT`` le saca el pico por esa esquina de abajo,
    que es lo que hace que un rectángulo redondeado se lea como un chat.
    """
    quien = texto(autor, 13, color=color)
    cuerpo = texto(mensaje, tam, color=CLARO)
    if adjunto:
        cuerpo = VGroup(
            archivo(color=color, alto=0.32), cuerpo,
        ).arrange(RIGHT, buff=0.18)
    dentro = VGroup(quien, cuerpo).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
    globo = RoundedRectangle(
        width=dentro.width + 0.5, height=dentro.height + 0.32,
        corner_radius=0.18, stroke_color=color, stroke_width=2.5,
    ).set_fill(SUPERFICIE, opacity=1.0)

    piezas = [globo]
    if cola is not None:
        # El pico se dibuja en dos trozos para que no se vea la costura: un
        # parche del color del relleno que tapa el borde del globo entre los
        # dos puntos de anclaje, y encima la línea que continúa ese borde.
        fuera = -1.0 if cola[0] < 0 else 1.0
        x = globo.get_left()[0] if fuera < 0 else globo.get_right()[0]
        y = globo.get_bottom()[1]
        arriba, abajo = y + 0.38, y + 0.15
        punta = np.array([x + fuera * 0.16, y + 0.04, 0])
        dentro_x = x - fuera * 0.05
        piezas.append(Polygon(
            np.array([dentro_x, arriba, 0]), punta,
            np.array([dentro_x, abajo, 0]), stroke_width=0,
        ).set_fill(SUPERFICIE, opacity=1.0))
        borde = VMobject(color=color, stroke_width=2.5)
        borde.set_points_as_corners([
            np.array([x, arriba, 0]), punta, np.array([x, abajo, 0]),
        ])
        piezas.append(borde)

    piezas.append(dentro.move_to(globo.get_center()))
    return VGroup(*piezas)


def avatar(inicial, nombre=None, radio=0.5, color=SECUNDARIO):
    """Ficha de una persona: su inicial en un círculo y el nombre debajo.

    Los tamaños salen del radio, así que la ficha se escala entera cambiando
    un solo número. Sin ``nombre`` devuelve solo el círculo.
    """
    circulo = Circle(radius=radio, color=color, stroke_width=2.5)
    circulo.set_fill(SUPERFICIE, opacity=1.0)
    cara = VGroup(circulo, texto(inicial, radio * 50).move_to(circulo))
    if nombre is None:
        return cara
    return VGroup(cara, texto(nombre, radio * 33, color=color)).arrange(
        DOWN, buff=radio * 0.38)


def globo_mudo(ancho, alto=0.32, color=SECUNDARIO):
    """Un globo de chat sin texto: la silueta de un mensaje.

    Para las maquetas en las que no hace falta leer la conversación sino ver
    que es larga —un móvil de fondo, un hilo que sigue y sigue—.
    """
    return RoundedRectangle(
        width=ancho, height=alto, corner_radius=min(0.16, alto / 2),
        stroke_color=color, stroke_width=1.5,
    ).set_fill(SUPERFICIE, opacity=1.0).set_stroke(opacity=0.55)


def telefono(ancho=4.1, alto=6.0, color=SECUNDARIO, rotulo=None, sub=None,
             hora="9:41"):
    """Maqueta de móvil para enseñar una conversación en pantalla.

    Dibuja la carcasa, la pantalla, la isla del altavoz, la barra de estado
    —hora y batería—, la barra de la app con el nombre del chat y la barra de
    inicio de abajo. Nada de eso es información: es lo que hace que un montón
    de globos de texto se lea como un móvil y no como un diagrama.

    Devuelve ``VGroup(carcasa, lienzo)``: ``movil[1]`` es el hueco libre de la
    pantalla —lo que queda entre la barra de la app y la de inicio—, así que
    la diapositiva coloca ahí su contenido sin repetir ninguna medida.
    """
    radio = ancho * 0.12
    borde = 0.13
    cuerpo = RoundedRectangle(
        width=ancho, height=alto, corner_radius=radio,
        stroke_color=color, stroke_width=4,
    ).set_fill(FONDO, opacity=1.0)
    pantalla = RoundedRectangle(
        width=ancho - 2 * borde, height=alto - 2 * borde,
        corner_radius=radio - borde, stroke_width=0,
    ).set_fill(SUPERFICIE, opacity=0.6)

    arriba, abajo = pantalla.get_top()[1], pantalla.get_bottom()[1]
    izq, der = pantalla.get_left()[0], pantalla.get_right()[0]
    y_estado = arriba - 0.26

    # --- Barra de estado: isla, hora y batería -----------------------------
    isla = RoundedRectangle(
        width=ancho * 0.2, height=0.12, corner_radius=0.06, stroke_width=0,
    ).set_fill(FONDO, opacity=1.0).move_to([0, y_estado, 0])
    reloj = texto(hora, 11, color=color).move_to([izq + 0.36, y_estado, 0])
    pila = RoundedRectangle(width=0.3, height=0.15, corner_radius=0.05,
                            stroke_color=color, stroke_width=1.5)
    carga = RoundedRectangle(width=0.19, height=0.08, corner_radius=0.025,
                             stroke_width=0).set_fill(color, opacity=0.75)
    carga.align_to(pila, LEFT).shift(RIGHT * 0.045)
    pico = Line(UP * 0.03, DOWN * 0.03, color=color, stroke_width=2)
    pico.next_to(pila, RIGHT, buff=0.02)
    bateria = VGroup(pila, carga, pico).move_to([der - 0.4, y_estado, 0])
    adornos = VGroup(isla, reloj, bateria)

    # --- Barra de la app: con quién estás hablando -------------------------
    if rotulo:
        avatar = Dot(radius=0.12, color=color).set_fill(color, opacity=0.35)
        nombre = VGroup(texto(rotulo, 13, color=CLARO))
        if sub:
            nombre.add(texto(sub, 10, color=color))
        nombre.arrange(DOWN, buff=0.05, aligned_edge=LEFT)
        cabecera = VGroup(avatar, nombre).arrange(RIGHT, buff=0.16)
        adornos.add(cabecera.move_to([0, arriba - 0.8, 0]))

    y_division = arriba - 1.12
    adornos.add(Line([izq, y_division, 0], [der, y_division, 0],
                     color=color, stroke_width=1.5).set_stroke(opacity=0.4))
    adornos.add(RoundedRectangle(
        width=ancho * 0.32, height=0.07, corner_radius=0.035, stroke_width=0,
    ).set_fill(color, opacity=0.5).move_to([0, abajo + 0.22, 0]))

    # --- El hueco donde va la conversación ---------------------------------
    techo, suelo = y_division - 0.18, abajo + 0.45
    lienzo = Rectangle(width=der - izq - 0.24, height=techo - suelo,
                       stroke_width=0, fill_opacity=0)
    lienzo.move_to([0, (techo + suelo) / 2, 0])

    return VGroup(VGroup(cuerpo, pantalla, adornos), lienzo)


def barra(largo, alto=0.42, color=PRIMARIO, opacidad=1.0):
    """Barra horizontal de un gráfico, con las puntas redondeadas.

    El radio se recorta cuando la barra es más estrecha que el propio radio,
    que es lo que pasa con los valores pequeños de cualquier gráfico real: sin
    eso, manim dibuja una cápsula deforme en vez de una barrita.
    """
    largo = max(largo, 0.03)
    return RoundedRectangle(
        width=largo, height=alto, corner_radius=min(0.09, largo / 2),
        stroke_width=0,
    ).set_fill(color, opacity=opacidad)


# --- Terminal --------------------------------------------------------------
# El tipo de cada línea decide su color, y con eso basta para que una sesión
# de terminal se lea de un vistazo: lo que se teclea en claro, lo que responde
# git en gris, lo que sale bien en verde y lo que revienta en rojo.
_COLOR_TIPO = {
    "cmd": CLARO,
    "out": SECUNDARIO,
    "txt": CLARO,            # contenido de un archivo, no salida de git
    "ok": OK,
    "err": ERROR,
    "avi": AMBAR,
    "alt": RAMA_FEATURE,     # lo que trae la otra rama, en un conflicto
    "com": SECUNDARIO,
}


def linea_terminal(contenido, tipo="cmd", tam=17):
    """Una línea suelta de terminal, con el prompt y el comando coloreados.

    Los colores van por posición y no por palabra: las claves de texto de
    ``t2c`` son expresiones regulares, y un ``$`` o un ``.`` dentro de la clave
    hace cosas raras. Así que el ``$`` va en verde y el programa con su
    subcomando —``git commit``, ``gh repo``— en cian, calculando los índices
    sobre el propio string.
    """
    if tipo == "sep":                       # línea en blanco: solo ocupa alto
        hueco = Rectangle(width=0.01, height=tam * 0.011,
                          stroke_width=0, fill_opacity=0)
        hueco.es_separador = True           # ``teclear`` no intenta animarlo
        return hueco

    color = _COLOR_TIPO.get(tipo, CLARO)
    if tipo == "com":
        contenido = f"# {contenido}"

    t2c = {}
    if tipo == "cmd":
        contenido = f"$ {contenido}"
        t2c["[0:1]"] = OK
        partes = contenido.split()
        if len(partes) > 1:
            # "git commit" entero en cian; para otros programas, solo su nombre.
            largo = len(partes[1])
            if partes[1] in ("git", "gh") and len(partes) > 2:
                largo += 1 + len(partes[2])
            t2c[f"[2:{2 + largo}]"] = PRIMARIO

    linea = Text(contenido, font=FONT, font_size=tam, color=color, t2c=t2c)
    if tipo == "com":
        linea.set_opacity(0.7)
    return linea


ALTO_BARRA = 0.42        # alto de la barra de título de una ventana


def ventana(ancho, alto, nombre=None, tam=15, barra=True, color=PRIMARIO):
    """El marco de una ventana: caja, barra de título, semáforo y rótulo.

    Es el envoltorio que comparten la terminal, un archivo abierto y el
    navegador de la diapositiva de instalación. Devuelve un ``VGroup`` cuyo
    primer elemento es la caja, para colocar dentro lo que haga falta.
    """
    caja = RoundedRectangle(
        width=ancho, height=alto, corner_radius=0.16,
        stroke_color=color, stroke_width=3,
    ).set_fill(SUPERFICIE, opacity=1.0)
    chrome = VGroup(caja)
    if not barra:
        return chrome

    y_barra = caja.get_top()[1] - ALTO_BARRA
    division = Line(
        [caja.get_left()[0], y_barra, 0], [caja.get_right()[0], y_barra, 0],
        color=color, stroke_width=2,
    ).set_stroke(opacity=0.45)
    semaforo = VGroup(*[
        Dot(radius=0.055, color=c, fill_opacity=0.8)
        for c in (ERROR, AMBAR, VERDE)
    ]).arrange(RIGHT, buff=0.13)
    semaforo.move_to([caja.get_left()[0] + 0.42, y_barra + ALTO_BARRA / 2, 0])
    chrome.add(division, semaforo)
    if nombre:
        rotulo = texto(nombre, tam, color=SECUNDARIO)
        rotulo.move_to([caja.get_center()[0], y_barra + ALTO_BARRA / 2, 0])
        chrome.add(rotulo)
    return chrome


def terminal(lineas, tam=17, ancho=None, margen=0.55, buff=0.24, barra=True,
             nombre=None):
    """Ventana de terminal con sus líneas dentro, lista para revelar una a una.

    ``lineas``: lista de tuplas ``(contenido, tipo)`` con tipo en
    ``cmd`` (lo tecleado), ``out`` (respuesta de git), ``txt`` (contenido de un
    archivo), ``ok``, ``err``, ``avi`` (aviso), ``com`` (comentario) o ``sep``
    (línea en blanco).

    ``nombre`` escribe un rótulo en la barra de título. Sirve para las ventanas
    que no son una terminal sino un archivo abierto —``.gitignore``,
    ``README.md``—: el nombre va dentro de la barra y no encima de la caja,
    que es donde se comería el título de la diapositiva.

    Devuelve un ``VGroup(chrome, filas)``: ``ventana[1]`` son las filas, así
    que una diapositiva puede hacerlas aparecer de una en una mientras el
    marco de la ventana ya está en pantalla.
    """
    filas = VGroup(*[
        linea_terminal(c, t, tam) for c, t in lineas
    ]).arrange(DOWN, buff=buff, aligned_edge=LEFT)

    ancho = ancho or filas.width + margen * 2
    alto_barra = ALTO_BARRA if barra else 0.0
    alto = filas.height + margen * 2 + alto_barra

    chrome = ventana(ancho, alto, nombre, tam - 2, barra)
    filas.move_to(chrome[0].get_center() + DOWN * alto_barra / 2)
    filas.align_to(chrome[0].get_left() + RIGHT * margen, LEFT)
    return VGroup(chrome, filas)


# --- Piezas de un repositorio ---------------------------------------------
def nodo_commit(etiqueta="", color=PRIMARIO, radio=0.32, tam=15):
    """Un commit: círculo relleno con su hash corto dentro."""
    circulo = Circle(radius=radio, color=color, stroke_width=4)
    circulo.set_fill(SUPERFICIE, opacity=1.0)
    if not etiqueta:
        return VGroup(circulo)
    letras = texto(etiqueta, tam, color=color)
    if letras.width > radio * 1.7:
        letras.scale_to_fit_width(radio * 1.7)
    return VGroup(circulo, letras.move_to(circulo.get_center()))


def nodo_fantasma(etiqueta="", color=ERROR, radio=0.32, tam=15):
    """Un commit al que ya no apunta nadie: el mismo nodo, pero a trazos.

    Lo estrena ``git_amend`` para el commit que acaba de ser reemplazado, y
    vale para cualquier huérfano: el borde discontinuo dice "esto sigue en el
    repositorio pero se ha soltado de la rama" sin necesidad de rotularlo.

    El relleno va en un círculo aparte, con el borde encima, porque un trazo
    discontinuo son arcos sueltos y no cierran figura que rellenar.
    """
    relleno = Circle(radius=radio, stroke_width=0)
    relleno.set_fill(SUPERFICIE, opacity=1.0)
    borde = DashedVMobject(
        Circle(radius=radio, color=color, stroke_width=4),
        num_dashes=22, dashed_ratio=0.55,
    )
    nodo = VGroup(relleno, borde)
    if not etiqueta:
        return nodo
    letras = texto(etiqueta, tam, color=color)
    if letras.width > radio * 1.7:
        letras.scale_to_fit_width(radio * 1.7)
    return nodo.add(letras.move_to(nodo.get_center()))


def enlace(inicio, fin, color=PRIMARIO, grosor=3.5):
    """Une dos puntos como los une git.

    Si están a la misma altura sale una recta; si no, la ese de los grafos de
    git —horizontal al salir, horizontal al entrar, con los puntos de control
    en la x del medio—, que es lo que dibujan GitHub o ``git log --graph``.

    Es la versión por puntos de :func:`arista`, para cuando lo que se une no
    son nodos redondos sino cajas, tarjetas o bordes calculados a mano.
    """
    inicio, fin = np.array(inicio, dtype=float), np.array(fin, dtype=float)
    if abs(inicio[1] - fin[1]) < 0.01:
        return Line(inicio, fin, color=color, stroke_width=grosor)
    medio = (inicio[0] + fin[0]) / 2
    return CubicBezier(
        inicio,
        np.array([medio, inicio[1], 0]),
        np.array([medio, fin[1], 0]),
        fin,
        color=color, stroke_width=grosor,
    )


def arista(a, b, color=PRIMARIO, radio=0.32, grosor=3.5):
    """Une dos nodos de commit, de borde a borde."""
    return enlace(a.get_center() + RIGHT * radio,
                  b.get_center() + LEFT * radio, color, grosor)


def puntero(nombre, color=PRIMARIO, tam=16, relleno=0.16):
    """Etiqueta de rama o de ``HEAD``: el cartelito que apunta a un commit.

    En git una rama no es una copia de nada: es esto, un nombre pegado a un
    commit que se mueve solo. Por eso en los diagramas de la charla siempre va
    dibujada como una pegatina y nunca como una línea.
    """
    letras = texto(nombre, tam, color=color)
    caja = RoundedRectangle(
        width=letras.width + 0.3, height=letras.height + 0.22,
        corner_radius=0.08, stroke_color=color, stroke_width=2.5,
    ).set_fill(color, opacity=relleno)
    return VGroup(caja, letras.move_to(caja.get_center()))


def archivo(nombre="", color=SECUNDARIO, alto=0.7, tam=14):
    """Icono de archivo (hoja con la esquina doblada) y su nombre debajo."""
    ancho = alto * 0.78
    d = alto * 0.26                       # lado de la esquina doblada
    hoja = Polygon(
        [-ancho / 2, alto / 2, 0], [ancho / 2 - d, alto / 2, 0],
        [ancho / 2, alto / 2 - d, 0], [ancho / 2, -alto / 2, 0],
        [-ancho / 2, -alto / 2, 0],
        color=color, stroke_width=3,
    ).set_fill(color, opacity=0.10)
    doblez = Polygon(
        [ancho / 2 - d, alto / 2, 0], [ancho / 2, alto / 2 - d, 0],
        [ancho / 2 - d, alto / 2 - d, 0],
        color=color, stroke_width=2.5,
    ).set_fill(color, opacity=0.25)
    icono = VGroup(hoja, doblez)
    if not nombre:
        return icono
    etiqueta = texto(nombre, tam, color=color).next_to(icono, DOWN, buff=0.14)
    return VGroup(icono, etiqueta)


# La foto va montada como los retratos de la charla (ver :func:`fotografia`):
# papel blanco con tres márgenes finos, el de abajo más ancho, y una pizca de
# inclinación para que parezca puesta encima y no pegada al fondo. Esta está
# dibujada en vez de ser un .png porque se tiñe —cián el commit nuevo, gris los
# viejos, ámbar el que recuperas— y porque se transforma en otras cosas.
ANCHO_PAPEL = 0.98
MARGEN_PAPEL = 0.055
PIE_PAPEL = 0.19         # el margen de abajo, el ancho: la barbilla del papel
ALTO_IMAGEN = 0.66       # casi cuadrada, con la barbilla debajo: una foto
ALTO_HOJA = 0.44         # el archivo retratado, dentro de la imagen
GIRO_PAPEL = -0.05


def foto_proyecto(escala=1.0, color=SECUNDARIO, vacia=False):
    """El proyecto entero revelado como una foto: eso es un commit.

    Lo retratado es el archivo del proyecto, así que es el mismo dibujo a
    cualquier tamaño: grande sobre la carpeta cuando se hace el commit y en
    miniatura encima de cada nodo del historial. Siempre se reconoce.

    ``vacia=True`` dibuja el hueco a rayas en vez del archivo: es la foto de
    un commit anterior, de cuando ese archivo todavía no existía. Puestas en
    fila, las dos versiones cuentan solas que cada commit retrata un estado
    distinto del proyecto.
    """
    ancho_imagen = ANCHO_PAPEL - 2 * MARGEN_PAPEL
    papel = RoundedRectangle(
        width=ANCHO_PAPEL,
        height=ALTO_IMAGEN + MARGEN_PAPEL + PIE_PAPEL,
        corner_radius=0.05, stroke_width=0,
    ).set_fill(BLANCO, opacity=1.0)
    imagen = RoundedRectangle(
        width=ancho_imagen, height=ALTO_IMAGEN, corner_radius=0.03,
        stroke_width=0,
    ).set_fill(SUPERFICIE, opacity=1.0)
    imagen.move_to(papel.get_top() + DOWN * (MARGEN_PAPEL + ALTO_IMAGEN / 2))

    # El archivo, o su hueco. La silueta es la de :func:`archivo`, la misma
    # que se ve en la carpeta: la foto retrata lo que había allí.
    hoja = archivo("", color, ALTO_HOJA)
    if vacia:
        hoja = DashedVMobject(
            hoja[0].set_fill(opacity=0), num_dashes=22, dashed_ratio=0.55,
        ).set_stroke(color, width=2.5, opacity=0.5)
    hoja.move_to(imagen.get_center())

    # Un brillo en diagonal por la esquina, que es lo que hace que un papel
    # parezca un papel y no un rectángulo blanco.
    izq, der = imagen.get_left()[0], imagen.get_right()[0]
    arriba, abajo = imagen.get_top()[1], imagen.get_bottom()[1]
    brillo = Polygon(
        [izq, arriba, 0], [izq + ancho_imagen * 0.36, arriba, 0],
        [izq + ancho_imagen * 0.12, abajo, 0], [izq, abajo, 0],
        stroke_width=0,
    ).set_fill(BLANCO, opacity=0.07)

    # Y en la barbilla, la raya del pie escrito a mano.
    pie = Line(
        [-ancho_imagen * 0.22, 0, 0], [ancho_imagen * 0.22, 0, 0],
        color=color, stroke_width=2.2,
    ).set_stroke(opacity=0.45)
    pie.move_to(papel.get_bottom() + UP * PIE_PAPEL / 2)

    return VGroup(papel, imagen, brillo, hoja, pie).rotate(GIRO_PAPEL).scale(
        escala)


def zona(nombre, color=PRIMARIO, ancho=3.4, alto=2.6, tam=17, discontinua=True):
    """Caja rotulada para las tres zonas de git (trabajo, staging, repositorio).

    Devuelve ``VGroup(caja, rotulo)``: ``zona[0]`` es la caja, útil para
    colocar cosas dentro con ``move_to`` o ``next_to``.
    """
    caja = RoundedRectangle(
        width=ancho, height=alto, corner_radius=0.18,
        stroke_color=color, stroke_width=3,
    ).set_fill(color, opacity=0.05)
    if discontinua:
        borde = DashedVMobject(
            caja.copy().set_fill(opacity=0), num_dashes=42, dashed_ratio=0.6,
        )
        caja = VGroup(caja.set_stroke(opacity=0), borde)
    rotulo = texto(nombre, tam, color=color).next_to(caja, UP, buff=0.18)
    return VGroup(caja, rotulo)


# --- Las mismas zonas, en carriles -----------------------------------------
# La otra forma de dibujar las tres zonas: en vez de cajas apiladas, un carril
# vertical por zona con su icono arriba. Las cajas cuentan bien un viaje de una
# vez; los carriles aguantan lo que viene después, porque dejan el eje vertical
# entero para el tiempo (los commits que van cayendo) y el horizontal para los
# comandos que mueven cosas de un carril a otro.
def carpeta(alto=0.9, color=SECUNDARIO):
    """Icono de carpeta abierta: el directorio de trabajo."""
    ancho = alto * 1.22
    tapa = Polygon(
        [-ancho / 2, -alto / 2, 0], [-ancho / 2, alto / 2, 0],
        [-ancho * 0.10, alto / 2, 0], [-ancho * 0.02, alto / 2 - alto * 0.18, 0],
        [ancho / 2, alto / 2 - alto * 0.18, 0], [ancho / 2, -alto / 2, 0],
        color=color, stroke_width=3,
    ).set_fill(color, opacity=0.06)
    frente = Polygon(
        [-ancho / 2, -alto / 2, 0], [ancho / 2, -alto / 2, 0],
        [ancho / 2, alto * 0.14, 0], [-ancho / 2, -alto * 0.02, 0],
        color=color, stroke_width=3,
    ).set_fill(color, opacity=0.16)
    return VGroup(tapa, frente)


def cajon(alto=0.9, color=STAGING):
    """Icono del staging: la caja donde se apartan las piezas del próximo commit.

    El visto va del color de la zona y no en verde a propósito: lo que hay aquí
    está marcado para entrar, que no es lo mismo que estar guardado.
    """
    ancho = alto * 1.16
    caja = RoundedRectangle(
        width=ancho, height=alto * 0.9, corner_radius=alto * 0.1,
        stroke_color=color, stroke_width=3,
    ).set_fill(SUPERFICIE, opacity=1.0)
    lado = alto * 0.18
    piezas = VGroup(*[
        Rectangle(width=lado, height=lado, color=color, stroke_width=2)
        .set_fill(color, opacity=0.35)
        for _ in range(4)
    ]).arrange_in_grid(rows=2, buff=lado * 0.4)
    piezas.move_to(caja.get_center() + LEFT * ancho * 0.12)
    sello = VGroup(
        Circle(radius=alto * 0.2, color=color, stroke_width=3)
        .set_fill(SUPERFICIE, opacity=1.0),
        visto(color=color, tam=alto * 0.1, grosor=4),
    ).move_to(caja.get_corner(DR))
    return VGroup(caja, piezas, sello)


def discos(alto=0.9, color=RAMA_MAIN, n=3):
    """Pila de discos (el icono de "esto es una base de datos"): el repositorio."""
    ancho = alto * 1.02
    alto_disco = ancho * 0.34
    salto = (alto - alto_disco) / (n - 1)
    ys = [alto / 2 - alto_disco / 2 - i * salto for i in range(n)]
    paredes = VGroup(*[
        Line([lado * ancho / 2, ys[0], 0], [lado * ancho / 2, ys[-1], 0],
             color=color, stroke_width=3)
        for lado in (-1, 1)
    ])
    # De abajo arriba: cada disco tapa con su relleno al que tiene debajo, que
    # es lo que hace que la pila se lea como una pila y no como tres elipses.
    tapas = VGroup(*[
        Ellipse(width=ancho, height=alto_disco, color=color, stroke_width=3)
        .set_fill(SUPERFICIE, opacity=1.0).move_to([0, y, 0])
        for y in reversed(ys)
    ])
    return VGroup(paredes, tapas)


def carriles(zonas, xs, y_icono=2.25, y_rotulo=1.45, y_linea=(1.08, -3.15),
             tam=19, grosor=7):
    """Un carril vertical por zona: icono arriba, nombre debajo y su línea.

    ``zonas`` son tuplas ``(icono, nombre, color)`` y ``xs`` la x de cada
    carril. Devuelve un ``VGroup`` de ``VGroup(icono, rotulo, linea)``: la
    línea (``carriles[i][2]``) es de la que cuelga todo lo que venga después
    —commits, flechas de comandos—, así que pídela por índice en vez de volver
    a calcular la x a mano.
    """
    grupo = VGroup()
    for (icono, nombre, color), x in zip(zonas, xs):
        rotulo = texto(nombre, tam, color=color).move_to([x, y_rotulo, 0])
        linea = Line([x, y_linea[0], 0], [x, y_linea[1], 0],
                     color=color, stroke_width=grosor)
        grupo.add(VGroup(icono.move_to([x, y_icono, 0]), rotulo, linea))
    return grupo


# --- Dibujos -------------------------------------------------------------
def robot(alto=1.6, color=SECUNDARIO):
    """Un robot de dibujo: antena, cabeza con dos ojos y cuerpo con brazos.

    Todas las medidas salen de ``alto``, así que se escala entero cambiando un
    solo número. En esta charla es "el bot" que rastrea claves publicadas.
    """
    u = alto / 8.0                     # la unidad de la que sale todo lo demás
    cabeza = RoundedRectangle(
        width=u * 4.4, height=u * 3.4, corner_radius=u * 0.7,
        stroke_color=color, stroke_width=3,
    ).set_fill(SUPERFICIE, opacity=1.0)
    ojos = VGroup(*[
        Dot(radius=u * 0.42, color=color) for _ in range(2)
    ]).arrange(RIGHT, buff=u * 1.3).move_to(cabeza)

    antena = Line(cabeza.get_top(), cabeza.get_top() + UP * u,
                  color=color, stroke_width=3)
    bombilla = Dot(antena.get_end(), radius=u * 0.42, color=color)

    cuerpo = RoundedRectangle(
        width=u * 5.4, height=u * 3.2, corner_radius=u * 0.6,
        stroke_color=color, stroke_width=3,
    ).set_fill(SUPERFICIE, opacity=1.0).next_to(cabeza, DOWN, buff=u * 0.35)
    brazos = VGroup(*[
        Line(cuerpo.get_edge_center(lado), cuerpo.get_edge_center(lado) + lado * u * 1.1,
             color=color, stroke_width=3)
        for lado in (LEFT, RIGHT)
    ])
    return VGroup(antena, bombilla, cabeza, ojos, cuerpo, brazos)


def descarga(alto=1.4, color=PRIMARIO):
    """El icono de descargar de toda la vida: flecha abajo sobre su bandeja."""
    u = alto / 3.0
    asta = Line(UP * u * 1.5, DOWN * u * 0.15, color=color, stroke_width=9)
    punta = Polygon(
        [-u * 0.8, -u * 0.1, 0], [u * 0.8, -u * 0.1, 0], [0, -u * 1.15, 0],
        stroke_width=0,
    ).set_fill(color, opacity=1.0)
    bandeja = VMobject(color=color, stroke_width=9)
    bandeja.set_points_as_corners([
        [-u * 1.5, -u * 0.85, 0], [-u * 1.5, -u * 1.65, 0],
        [u * 1.5, -u * 1.65, 0], [u * 1.5, -u * 0.85, 0],
    ])
    return VGroup(asta, punta, bandeja)


def billete(ancho=1.9, color=OK):
    """Un billete de dibujo: papel, filete interior y el símbolo en medio."""
    alto = ancho * 0.46
    papel = RoundedRectangle(
        width=ancho, height=alto, corner_radius=alto * 0.14,
        stroke_color=color, stroke_width=3,
    ).set_fill(SUPERFICIE, opacity=1.0)
    filete = RoundedRectangle(
        width=ancho - alto * 0.3, height=alto - alto * 0.3,
        corner_radius=alto * 0.1, stroke_color=color, stroke_width=1.5,
    ).set_stroke(opacity=0.55)
    simbolo = texto("$", alto * 40, color=color).move_to(papel)
    return VGroup(papel, filete, simbolo)


# --- Adornos ---------------------------------------------------------------
def aspa(color=ERROR, tam=0.14, grosor=5):
    """Un ✗ dibujado con dos líneas (no depende de que la fuente lo tenga)."""
    return VGroup(
        Line(LEFT * tam + DOWN * tam, RIGHT * tam + UP * tam,
             color=color, stroke_width=grosor),
        Line(LEFT * tam + UP * tam, RIGHT * tam + DOWN * tam,
             color=color, stroke_width=grosor),
    )


def visto(color=OK, tam=0.14, grosor=5):
    """Un ✓ dibujado, pareja de :func:`aspa`."""
    return VGroup(
        Line(np.array([-tam * 1.15, 0.0, 0]), np.array([-tam * 0.3, -tam, 0]),
             color=color, stroke_width=grosor),
        Line(np.array([-tam * 0.3, -tam, 0]), np.array([tam * 1.3, tam * 1.2, 0]),
             color=color, stroke_width=grosor),
    )


def separador(largo=4.6, grosor=3, color=PRIMARIO):
    """Línea horizontal fina del color de marca (para cierres, divisiones)."""
    return Line(LEFT * largo, RIGHT * largo, color=color, stroke_width=grosor)


def enmarcar(mob, margen=0.12, color=PRIMARIO):
    """Rectángulo redondeado del color de marca alrededor de un mobject."""
    return RoundedRectangle(
        width=mob.width + margen, height=mob.height + margen,
        corner_radius=0.14, stroke_color=color, stroke_width=5, fill_opacity=0,
    ).move_to(mob.get_center())
