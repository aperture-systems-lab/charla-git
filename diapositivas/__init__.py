"""Diapositivas agrupadas en mixins temáticos.

Cada diapositiva vive en su propio archivo como ``construir(scene)``; aquí se
agrupan en mixins que exponen métodos ``slide_<nombre>(self)`` para la clase
principal de ``main.py``. ``SlideBase`` aporta la limpieza de pantalla entre
diapositivas y el contador de avance.

Para añadir una diapositiva:
  1) crea ``diapositivas/<nombre>.py`` (copia ``_plantilla.py``);
  2) impórtalo abajo y añade ``slide_<nombre> = _slide(<nombre>.construir)``
     al mixin que corresponda;
  3) llámalo desde ``construct`` en ``main.py``.
"""

from manim import UP, FadeIn, FadeOut

from componentes import grafo_decorativo, logo_esquina

from . import (
    cerrar_rama,
    cierre,
    comandos_remotos,
    configuracion,
    conventional_commits,
    conflictos,
    el_problema,
    era_ia,
    flujos_de_trabajo,
    fork_y_pr,
    git_checkout,
    git_diff,
    git_ignore,
    git_init,
    git_reflog,
    git_reset,
    git_revert,
    historia,
    instalacion,
    la_terminal,
    local_remoto,
    log,
    merge,
    mensajes_commit,
    minecraft,
    portada,
    pronto_iniciamos,
    que_es_git,
    que_es_un_commit,
    ramas,
    rebase_y_cherry,
    siguientes_pasos,
    tres_zonas,
)


class SlideBase:
    """Estado y utilidades compartidas por todas las diapositivas.

    Va antes de ``Slide`` en la herencia de ``presentation``, así que su
    ``next_slide`` envuelve al de manim-slides: ninguna diapositiva tiene que
    acordarse del indicador de avance.
    """

    def indicador(self):
        """Logo de la esquina, creado una sola vez y reutilizado en cada pausa."""
        if getattr(self, "_indicador", None) is None:
            self._indicador = logo_esquina()
        return self._indicador

    def next_slide(self, *args, indicador=True, **kwargs):
        """Pausa marcando con el logo del semillero que la charla sigue.

        El logo entra como última animación de la diapositiva —así queda en el
        fotograma congelado de la pausa— y se retira nada más avanzar, para que
        no se quede encima del contenido siguiente.

        ``indicador=False`` cierra el tramo sin él. Hace falta en dos casos: en
        la última pausa de la charla, donde ya no queda nada que anunciar, y al
        cerrar un tramo en bucle, donde esa animación de entrada caería dentro
        del bucle y el logo parpadearía en cada vuelta.
        """
        if not indicador:
            super().next_slide(*args, **kwargs)
            return
        logo = self.indicador()
        self.play(FadeIn(logo, shift=UP * 0.1), run_time=0.3)
        super().next_slide(*args, **kwargs)
        self.remove(logo)

    def iniciar_slide(self):
        """Limpia la pantalla (salvo el marco) y estrena el fondo de historial.

        Cada diapositiva estrena un preset distinto de ``grafo_decorativo``, que
        rota con el número de diapositiva: el fondo va cambiando solo, sin que
        ninguna diapositiva tenga que ocuparse de él.
        """
        self._slide_actual = getattr(self, "_slide_actual", 0) + 1
        marco = getattr(self, "marco", None)
        fondo_viejo = getattr(self, "_fondo", None)
        resto = [m for m in self.mobjects if m is not marco and m is not fondo_viejo]
        for m in resto:
            m.clear_updaters()

        self._fondo = grafo_decorativo(self._slide_actual - 1)
        salidas = [FadeOut(m) for m in resto]
        if fondo_viejo is not None:
            salidas.append(FadeOut(fondo_viejo))
        self.play(*salidas, FadeIn(self._fondo))
        if marco is not None:
            self.add(marco)  # re-añadir lo trae al frente, por encima del grafo


def _slide(construir):
    """Adapta un ``construir(scene)`` a un método de diapositiva (limpia y delega)."""

    def metodo(self):
        self.iniciar_slide()
        construir(self)

    return metodo


# --- Mixins temáticos: agrupa las diapositivas por sección ------------------
class SlidesInicio:
    slide_pronto_iniciamos = _slide(pronto_iniciamos.construir)
    slide_portada = _slide(portada.construir)
    slide_el_problema = _slide(el_problema.construir)


class SlidesFundamentos:
    slide_que_es_git = _slide(que_es_git.construir)
    slide_minecraft = _slide(minecraft.construir)
    slide_historia = _slide(historia.construir)
    slide_era_ia = _slide(era_ia.construir)
    slide_la_terminal = _slide(la_terminal.construir)
    slide_instalacion = _slide(instalacion.construir)
    slide_configuracion = _slide(configuracion.construir)


class SlidesLocal:
    slide_git_init = _slide(git_init.construir)
    slide_tres_zonas = _slide(tres_zonas.construir)
    slide_que_es_un_commit = _slide(que_es_un_commit.construir)
    slide_log = _slide(log.construir)
    slide_mensajes_commit = _slide(mensajes_commit.construir)
    slide_conventional_commits = _slide(conventional_commits.construir)
    slide_git_ignore = _slide(git_ignore.construir)
    slide_git_diff = _slide(git_diff.construir)
    slide_git_reset = _slide(git_reset.construir)
    slide_git_checkout = _slide(git_checkout.construir)
    slide_git_revert = _slide(git_revert.construir)
    slide_git_reflog = _slide(git_reflog.construir)


class SlidesRamas:
    slide_ramas = _slide(ramas.construir)
    slide_merge = _slide(merge.construir)
    slide_conflictos = _slide(conflictos.construir)
    slide_cerrar_rama = _slide(cerrar_rama.construir)


class SlidesRemoto:
    slide_local_remoto = _slide(local_remoto.construir)
    slide_comandos_remotos = _slide(comandos_remotos.construir)
    slide_fork_y_pr = _slide(fork_y_pr.construir)


class SlidesFinal:
    slide_flujos_de_trabajo = _slide(flujos_de_trabajo.construir)
    slide_rebase_y_cherry = _slide(rebase_y_cherry.construir)
    slide_siguientes_pasos = _slide(siguientes_pasos.construir)
    slide_cierre = _slide(cierre.construir)
