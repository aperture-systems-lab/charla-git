from manim import ManimColor
from manim_slides import Slide

from componentes import marco
from diapositivas import (
    SlideBase,
    SlidesFinal,
    SlidesFundamentos,
    SlidesInicio,
    SlidesLocal,
    SlidesRamas,
    SlidesRemoto,
)
from estilo import FONDO


class presentation(
    SlidesInicio,
    SlidesFundamentos,
    SlidesLocal,
    SlidesRamas,
    SlidesRemoto,
    SlidesFinal,
    SlideBase,
    Slide,
):
    def construct(self):
        self._slide_actual = 0
        self.camera.background_color = ManimColor(FONDO)
        self.marco = marco()
        self.add(self.marco)

        self.slide_pronto_iniciamos()
        # self.slide_portada()
        # self.slide_el_problema()
        # self.slide_que_es_git()
        # self.slide_minecraft()
        # self.slide_historia()
        # self.slide_era_ia()
        # self.slide_la_terminal()
        # self.slide_instalacion()
        # self.slide_configuracion()
        # self.slide_git_init()
        # self.slide_tres_zonas()
        # self.slide_que_es_un_commit()
        # self.slide_log()
        # self.slide_mensajes_commit()
        # self.slide_conventional_commits()
        # self.slide_git_ignore()
        # self.slide_git_checkout()
        # self.slide_git_reset()
        # self.slide_git_revert()
        # self.slide_git_reflog()
        # self.slide_ramas()
        # self.slide_merge()
        # self.slide_rebase_y_cherry()
        # self.slide_cerrar_rama()
        # self.slide_local_remoto()
        # self.slide_fork_y_pr()
        # self.slide_flujos_de_trabajo()
        # self.slide_siguientes_pasos()
        # self.slide_cierre()

        # self.slide_git_diff() 
        # self.slide_conflictos() 
        # self.slide_comandos_remotos()
                