import sys
sys.path.append("../")
from manim import *
from manim_chemistry import *
from helpers import *
import random

slides = False
if slides:
    from manim_slides import Slide


class BohrAtomModel(Slide if slides else Scene):
    def construct(self):
        # self.opbygning()
        self.grundstoffer()
        self.slide_pause(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def opbygning(self):
        ECOL = GOLD_A
        PCOL = RED
        NCOL = GRAY
        OCOL = LIGHT_GRAY
        atom = BohrAtom(
            e=10, p=10, n=8,
            # level=6
            orbit_color=OCOL,
            electron_color=ECOL,
            proton_color=PCOL,
            neutron_color=NCOL,
            sheen_factor=-0.25,
            separate_nuclei=True
        )
        electrons = atom.get_electrons()
        orbitals = atom.get_orbitals().set_style(stroke_width=1.5)
        protons = atom.get_protons()
        neutrons = atom.get_neutrons()

        zindices = [*[2*n for n in range(atom.p)], *[2*n+1 for n in range(atom.n)]]  # Even index for proton, odd index for neutron
        for n, z in zip([*protons, *neutrons], zindices):
            n.set_z_index(z)
        # for e in electrons:
        #     e.set_color(atom.electron_color).set_sheen(factor=100, direction=DR)

        for i, parts in enumerate([atom.get_protons(), atom.get_neutrons(), atom.get_electrons()]):
            if i == 2:
                self.play(
                    Create(orbitals)
                )
            self.play(
                LaggedStart(
                    *[FadeIn(p, run_time=0.2) for p in parts],
                    lag_ratio=1 / (len(parts))
                ),
                run_time=2
            )

        self.play(
            atom.animate.shift(4*LEFT)
        )
        self.slide_pause()

        lcmap = {
            "Proton": PCOL, "proton": PCOL,
            "Neutron": NCOL, "neutron": NCOL,
            "Elektron": ECOL, "elektron": ECOL,
            "Skal": OCOL
        }
        labels = VGroup(
            Tex("Proton", ", positivt ladet").set_color_by_tex_to_color_map(lcmap),
            Tex("Neutron", ", neutralt").set_color_by_tex_to_color_map(lcmap),
            Tex("Elektron", ", negativt ladet").set_color_by_tex_to_color_map(lcmap),
            Tex("Skal").set_color_by_tex_to_color_map(lcmap)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(UR)
        print(*atom)
        copied_particles = VGroup(
            protons[0].copy(),
            neutrons[0].copy(),
            electrons[0][0].copy(),
            orbitals[0].copy()
        )

        idle_opacity = 0.1
        self.play(
            protons.animate.set_opacity(idle_opacity),
            neutrons.animate.set_opacity(idle_opacity),
            electrons.animate.set_opacity(idle_opacity)
        )
        for i, particle in enumerate([protons[0], neutrons[0], electrons[0][0], Dot(radius=0)]):
            scale = 1 if i < 3 else 0.2
            self.play(particle.animate.set_opacity(1), run_time=1 if i < 3 else 0.01)
            self.play(
                LaggedStart(
                    copied_particles[i].animate.scale(scale).next_to(labels[i], LEFT),
                    Write(labels[i], run_time=0.5),
                    lag_ratio=0.75
                ),
                particle.animate.set_opacity(idle_opacity)
            )
            self.slide_pause()

        self.play(
            protons.animate.set_opacity(1),
            neutrons.animate.set_opacity(1),
            electrons.animate.set_opacity(1)
        )

        self.play(
            *[FadeOut(m) for m in [*labels, *copied_particles]],
            atom.animate.shift(DOWN)
            # atom.animate.move_to(ORIGIN)
        )
        self.slide_pause()

        scene_marker("atomkernens opbygning")
        proton_copies = protons.copy().scale(1).arrange(RIGHT).to_edge(UR)
        # electron_copies = electrons.copy().scale(0.75).arrange(RIGHT).next_to(proton_copies, DOWN)
        electron_copies = VGroup(*[
            e.copy() for orbs in electrons for e in orbs
        ]).scale(1).arrange(RIGHT).next_to(proton_copies, DOWN)
        neutron_copies = neutrons.copy().scale(1).arrange(RIGHT).next_to(electron_copies, DOWN)
        # for old, new in zip([protons, electrons, neutrons], [proton_copies, electron_copies, neutron_copies]):
        #     self.play(
        #         ReplacementTransform(
        #             old.copy(),
        #             new
        #         )
        #     )
        self.play(
            ReplacementTransform(protons.copy(), proton_copies)
        )
        self.play(
            ReplacementTransform(electrons.copy(), electron_copies)
        )
        neutralt_atom = VGroup(
            Tex("I et atom er der lige").set_color_by_tex_to_color_map(lcmap),
            Tex("mange ", "protoner", " og ", "elektroner").set_color_by_tex_to_color_map(lcmap)
        ).scale(0.825).arrange(DOWN, aligned_edge=RIGHT).next_to(
            VGroup(proton_copies, electron_copies), LEFT
        )
        self.play(
            Write(neutralt_atom)
        )
        self.slide_pause()

        self.play(
            ReplacementTransform(neutrons.copy(), neutron_copies)
        )
        antal_neutroner = Tex(
            "Antallet af ", "neutroner", " kan variere"
        ).set_color_by_tex_to_color_map(lcmap).scale(0.825).next_to(neutralt_atom, DOWN, aligned_edge=RIGHT, buff=0.2)
        self.play(
            Write(antal_neutroner)
        )
        self.slide_pause()

        ptable = PeriodicTable("../Elements_DK.csv").to_edge(DR)
        self.play(
            FadeIn(ptable)
        )
        self.slide_pause()

        fade_out_all(self)

    def grundstoffer(self):
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

        protoner = np.arange(10) + 1
        elektroner = protoner
        neutroner = [0, 2, 4, 5, 6, 6, 7, 8, 10, 10]

        text_protoner = VGroup(*[
            Tex("Protoner", f": {p}").set_color_by_tex_to_color_map(lcmap).to_edge(UR) for p in protoner
        ])
        text_elektroner = VGroup(*[
            Tex("Elektroner", f": {e}").set_color_by_tex_to_color_map(lcmap).next_to(
                text_protoner, DOWN, aligned_edge=RIGHT
            ) for e in elektroner
        ])
        text_neutroner = VGroup(*[
            Tex("Neutroner", f": {n}").set_color_by_tex_to_color_map(lcmap).next_to(
                text_elektroner, DOWN, aligned_edge=RIGHT
            ) for n in neutroner
        ])

        atomer = VGroup(*[
            BohrAtom(
                p=p, e=e, n=n,
                orbit_color=OCOL,
                electron_color=ECOL,
                proton_color=PCOL,
                neutron_color=NCOL,
                sheen_factor=-0.25,
            ) for p, e, n in zip(protoner, elektroner, neutroner)
        ]).shift(UP)
        grundstoffer = VGroup(*[
            MElementObject.from_csv_file_data(filename="../Elements_DK.csv", atomic_number=i+1) for i in range(10)
        ]).next_to(atomer, DOWN)
        self.play(
            FadeIn(atomer[0]),
            DrawBorderThenFill(grundstoffer[0]),
            Write(text_protoner[0]),
            Write(text_elektroner[0]),
            Write(text_neutroner[0])
        )
        prevs = [atomer[0], grundstoffer[0], text_protoner[0], text_elektroner[0], text_neutroner[0]]
        # prev_atom, prev_grun = atomer[0], grundstoffer[0]
        for atom, grun, tp, te, tn in zip(
                atomer[1:], grundstoffer[1:], text_protoner[1:], text_elektroner[1:], text_neutroner[1:]
        ):
            self.play(
                ReplacementTransform(prevs[0], atom),
                ReplacementTransform(prevs[1], grun),
                ReplacementTransform(prevs[2], tp),
                ReplacementTransform(prevs[3], te),
                ReplacementTransform(prevs[4], tn)
            )
            # prev_atom, prev_grun = atom, grun
            prevs = [atom, grun, tp, te, tn]



