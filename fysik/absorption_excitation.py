import sys
sys.path.append("../")
from manim import *
from manim_chemistry import *
from helpers import *
import random

slides = False
if slides:
    from manim_slides import Slide


class AbsorptionExcitation(Slide if slides else Scene):
    def construct(self):
        self.absorption()
        # self.excitation()
        self.slide_pause(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def abs_animation(self, electron, to_orbital, photon_color=YELLOW):
        target_dot = electron.copy().move_to(
            to_orbital.point_at_angle(np.arctan(electron.get_center()[1]/electron.get_center()[0]))
        )
        photon = Dot(color=photon_color).scale(0.5).to_edge(UL, buff=-1)
        trace = TracedPath(photon.get_start, stroke_color=photon_color, dissipating_time=0.5)
        self.add(photon, trace)

        self.play(
            photon.animate.move_to(electron.get_center())
        )
        self.play(
            Flash(electron, color=photon_color),
            Indicate(electron, color=photon_color),
            FadeOut(photon)
        )
        self.play(
            electron.animate.become(target_dot)
        )
        self.remove(trace)

    def absorption(self):
        ECOL = GOLD_A
        PCOL = RED
        NCOL = GRAY
        OCOL = LIGHT_GRAY
        lcmap = {
            "Proton": PCOL, "proton": PCOL,
            "Neutron": NCOL, "neutron": NCOL,
            "Elektron": ECOL, "elektron": ECOL,
            "Skal": OCOL
        }

        atom = BohrAtom(
            e=1, p=1, n=0,
            level=6,
            orbit_color=OCOL,
            electron_color=ECOL,
            proton_color=PCOL,
            neutron_color=NCOL,
            sheen_factor=-0.25,
            separate_nuclei=True
        ).scale(0.5)
        electrons = atom.get_electrons()
        orbitals = atom.get_orbitals().set_style(stroke_width=1.5)
        # self.play(
        #     FadeIn(atom)
        # )

        colors = VISIBLE_LIGHT
        print(interpolate_visible_light(-5))
