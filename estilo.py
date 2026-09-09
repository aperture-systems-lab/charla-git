"""Paleta, tipografía y constantes compartidas por toda la animación.

Único sitio con valores "mágicos": cambia aquí los colores o la fuente y se
re-tematiza la presentación entera. Ninguna diapositiva debe hardcodear hex
ni rutas de assets.

Charla: "Git y GitHub".
Marca: Semillero de Data Science e IA — Aperture.
"""

import os

# Importar registra las fuentes de marca (Press Start 2P + JetBrains Mono).
import fuentes  # noqa: F401

# --- Paleta (marca Aperture) ---------------------------------------------
FONDO = "#010409"        # fondo oscuro azulado (el mismo negro de GitHub)
PRIMARIO = "#29c4d9"     # cian: acento de marca (títulos, resaltados)
SECUNDARIO = "#8dbccd"   # azul acero: texto secundario, ejes, líneas
CLARO = "#eaf6fc"        # casi blanco: texto principal sobre el fondo oscuro
BLANCO = "#ffffff"       # blanco puro: solo para fondos de imagen (discos, QR)

# Colores de apoyo de la paleta (categorías, diagramas, énfasis)
AMBAR = "#caa655"
MORADO = "#ac94f1"
VERDE = "#48d0a5"
ROJO = "#e06c75"

# --- Roles de color de esta charla ---------------------------------------
# Git tiene tres o cuatro conceptos que se repiten en media presentación. Si
# cada uno lleva SIEMPRE el mismo color, los diagramas se leen sin leyenda:
# el ámbar es el staging en la diapositiva de las tres zonas y sigue siéndolo
# doce diapositivas después, en la del reset.
RAMA_MAIN = PRIMARIO     # la rama principal, y el repositorio "de verdad"
RAMA_FEATURE = MORADO    # cualquier rama de trabajo que sale de main
STAGING = AMBAR          # el área de preparación (y lo que está a medias)
OK = VERDE               # lo confirmado, lo que funciona, lo remoto que llegó
ERROR = ROJO             # conflictos, pérdidas, lo que no hay que hacer

# Alias cómodos (por si prefieres nombrarlos por su rol de color)
ACENTO = PRIMARIO
GRIS = SECUNDARIO

# Relleno de los nodos y cajas de diagrama: casi el fondo, pero no del todo,
# para que un nodo tape la malla decorativa que pasa por detrás.
SUPERFICIE = "#04121a"

# --- Tipografía ----------------------------------------------------------
FONT = "JetBrains Mono"          # cuerpo, texto general y TODO el código
FONT_TITULO = "Press Start 2P"   # títulos / display (pixel, retro)

# --- Rutas ---------------------------------------------------------------
RAIZ = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(RAIZ, "assets")  # imágenes de marca (.png, logos, iconos)

# --- Constantes de layout ------------------------------------------------
TAM_TITULO = 30          # tamaño del título de diapositiva (en FONT_TITULO)
