from manim import *
from manim_chemistry import *
import sys
sys.path.append("../")
from helpers import *

slides = False
if slides:
    from manim_slides import Slide


class BohrAtomModel(Slide if slides else Scene):
    def construct(self):
        self.opbygning()
        self.slide_pause(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def opbygning(self):
        ECOL = GOLD
        PCOL = RED
        NCOL = GRAY
        OCOL = LIGHT_GRAY
        atom = BohrAtom(
            e=10, p=10, n=8,
            # level=6
            orbit_color=OCOL,
            electron_color=ECOL,
            proton_color=PCOL,
            neutron_color=NCOL
        )
        electrons = atom.get_electrons()
        nuclei = atom.get_nuclei()
        orbitals = atom.get_orbitals().set_style(stroke_width=1.5)
        print(*[n.get_color() for n in nuclei])
        # print([n for n in nuclei if n.get_color() == NCOL][0])
        self.play(
            LaggedStart(
                DrawBorderThenFill(nuclei),
                Create(orbitals),
                DrawBorderThenFill(electrons),
                lag_ratio=1
            ),
            run_time=9
        )
        self.slide_pause()
        self.play(
            atom.animate.shift(4*LEFT)
        )

        lcmap = {
            "Proton": PCOL,
            "Neutron": NCOL,
            "Elektron": ECOL,
            "Skal": OCOL
        }
        labels = VGroup(
            Tex("Proton", ", positivt ladet").set_color_by_tex_to_color_map(lcmap),
            Tex("Neutron", ", neutralt").set_color_by_tex_to_color_map(lcmap),
            Tex("Elektron", ", negativt ladet").set_color_by_tex_to_color_map(lcmap),
            Tex("Skal").set_color_by_tex_to_color_map(lcmap)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(UR)
        particles = VGroup(
            nuclei[0].copy(),
            nuclei[1].copy(),
            # [n for n in nuclei if n.get_color() != NCOL][0],
            # [n for n in nuclei if n.get_color() == NCOL][0],
            electrons[0][0].copy(),
            orbitals[0].copy()
        )
        # self.add(particles)
        for label, particle in zip(labels, particles):
            scale = 1
            if particle == particles[-1]:
                scale = 0.2
            self.play(
                LaggedStart(
                    particle.animate.scale(scale).next_to(label, LEFT),
                    Write(label, run_time=0.5),
                    lag_ratio=0.75
                )
            )
            self.slide_pause()

        self.play(
            *[FadeOut(m) for m in [*labels, *particles]],
            atom.animate.move_to(ORIGIN)
        )
        self.slide_pause()

        self.play(
            Rotate(electrons, 8*PI, about_point=ORIGIN),
            run_time=16
        )

        # self.play(
        #     # MoveAlongPath(moving_electron, orbitals[0])
        #     Rotate(moving_electron, PI/2, about_point=atom.get_center())
        # )