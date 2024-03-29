import sys
sys.path.append("../")
from manim import *
from manim_chemistry import *
from helpers import *
import random

slides = True
if slides:
    from manim_slides import Slide


class AbsorptionExcitation(Slide if slides else Scene):
    def construct(self):
        # self.absorption()
        # self.excitation()
        self.absorptionsspektrum()
        self.slide_pause(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def abs_animation(self, electron, to_orbital, photon_color=YELLOW):
        target_dot = electron.copy().move_to(
            to_orbital.point_at_angle(np.arctan(electron.get_center()[1]/electron.get_center()[0]))
        )
        photon = Dot(color=photon_color).scale(0.5).to_edge(UL, buff=-1)
        trace = TracedPath(photon.get_center, stroke_color=photon_color, dissipating_time=0.5)
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

    def exc_animation(self, electron, to_orbital, photon_color=YELLOW):
        target_dot = electron.copy().move_to(
            to_orbital.point_at_angle(np.arctan(electron.get_center()[1]/electron.get_center()[0]))
        )
        photon = Dot(color=photon_color).scale(0.5).move_to(electron)
        trace = TracedPath(photon.get_center, stroke_color=photon_color, dissipating_time=0.5)
        self.add(photon, trace)

        self.play(
            Flash(electron, color=photon_color),
            Indicate(electron, color=photon_color),
            FadeIn(photon)
        )
        self.play(
            photon.animate.to_edge(UR, buff=-1)
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
        self.play(
            FadeIn(atom)
        )

        # self.play(
        #     Indicate(orbitals[0]),
        #     Indicate(orbitals[1])
        # )
        self.abs_animation(electrons, orbitals[1])
        self.exc_animation(electrons, orbitals[0])

        # colors = VISIBLE_LIGHT
        # print(interpolate_visible_light(50))

    def absorptionsspektrum(self):
        balmer_colors = [
            interpolate_color(VISIBLE_LIGHT[650], VISIBLE_LIGHT[650], 0.628),
            interpolate_color(VISIBLE_LIGHT[480], VISIBLE_LIGHT[490], 0.614),
            interpolate_color(VISIBLE_LIGHT[430], VISIBLE_LIGHT[440], 0.405),
            interpolate_color(VISIBLE_LIGHT[410], VISIBLE_LIGHT[410], 0.173),
        ]
        intp_light = interpolate_visible_light(5)
        abs_wls = []
        ECOL = GOLD_A
        PCOL = RED
        NCOL = GRAY
        OCOL = LIGHT_GRAY

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
        orbitals = atom.get_orbitals().set_style(stroke_width=1.5)
        electron = atom.get_electrons()
        electron.move_to(
            orbitals[1].point_at_angle(np.arctan(electron.get_center()[1]/electron.get_center()[0]))
        )
        atoms = VGroup(*[atom.copy().scale(0.4) for _ in range(4)]).arrange(RIGHT)
        rainbow = VGroup(*[
            Line(
                start=9*LEFT, end=6*LEFT, stroke_color=intp_light[key], stroke_opacity=0.5
            ).shift(2*i/len(intp_light.keys()) * DOWN) for i, key in enumerate(intp_light.keys()) if key not in abs_wls
        ]).next_to(atoms[0][2], LEFT, buff=4)
        self.add(atoms, rainbow)
        electron = atoms[0].get_electrons()
        orbitals = atoms[0].get_orbitals()
        self.play(
            rainbow.animate.next_to(atoms[0][2], LEFT, buff=0),
            run_time=4,
            rate_func=rate_functions.linear
        )
        self.play(
            Flash(electron, color=balmer_colors[0]),
            Indicate(electron, color=balmer_colors[0]),
        )
        self.play(
            electron.animate.move_to(orbitals[2].point_at_angle(PI/2))
        )

        abs_wls.append(640)
        rainbow = VGroup(*[
            Line(
                start=LEFT, end=RIGHT, stroke_color=intp_light[key], stroke_opacity=0.5
            ).shift(i/len(intp_light.keys()) * DOWN) for i, key in enumerate(intp_light.keys()) if key not in abs_wls
        ]).scale(2).next_to(rainbow, RIGHT, buff=0)
        self.add(rainbow)


class RydbergBalmer(AbsorptionExcitation):
    def construct(self):
        title = Tex("Rydbergformlen og Balmerserien")
        play_title(self, title)
        photon_energies = self.rydberg_formel()
        self.balmer_serie(photon_energies)
        self.play(
            LaggedStart(
                *[FadeOut(m) for m in self.mobjects],
                lag_ratio=0.1
            ),
            run_time=2
        )
        play_title_reverse(self, title)

    def rydberg_formel(self):
        cmap = {
            "n": YELLOW, "m": YELLOW,
            r"R_H": RED, r"\lambda": color_gradient([RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE], 6)
        }
        balmer_colors = [
            interpolate_color(VISIBLE_LIGHT[650], VISIBLE_LIGHT[650], 0.628),
            interpolate_color(VISIBLE_LIGHT[480], VISIBLE_LIGHT[490], 0.614),
            interpolate_color(VISIBLE_LIGHT[430], VISIBLE_LIGHT[440], 0.405),
            interpolate_color(VISIBLE_LIGHT[410], VISIBLE_LIGHT[410], 0.173),
        ]
        # starter = VGroup(
        #     Tex("Rydbergs formel", " bruges til at udregne ", "bølgelængden"),
        #     Tex("af exciteret eller absorberet lys mellem ", "to energitilstande")
        # ).arrange(DOWN, aligned_edge=LEFT).to_edge(DL)
        # starter[0][0].set_color(cmap[r"R_H"])
        # starter[1][1].set_color(cmap["n"])
        formel = MathTex(
            r"{1\over\lambda}", r" = ", r"R_H", r" \left( ", r"{1\over n^2}", " -", r"{1\over m^2}", r" \right)",
            substrings_to_isolate=list(cmap.keys())
        ).set_color_by_tex_to_color_map(cmap)
        # self.play(
        #     Write(starter),
        #     run_time=2
        # )
        # self.slide_pause()
        # for i in formel:
        #     print(i)
        self.add(formel)
        # self.play(
        #     LaggedStart(
        #         ReplacementTransform(starter[0][0], formel[4]),
        #         ReplacementTransform(starter[0][2], formel[1]),
        #         ReplacementTransform(starter[1][1], formel[7]),
        #         ReplacementTransform(starter[1][1], formel[11]),
        #         ReplacementTransform(
        #             VGroup(starter[0][1], starter[1]),
        #             VGroup(formel[0], formel[2:4], formel[5:7], formel[8:11], formel[12:])
        #         ),
        #         lag_ratio=0.75
        #     ),
        #     run_time=5
        # )
        self.slide_pause()

        calc = VGroup(
            formel.copy(),
            MathTex(r"{1\over\lambda}", r" = ", r"1.097\times10^7 \text{m}^{-1}", r" \left( ", r"{1\over", " n^2}", " -", r"{1\over", " m^2}", r" \right)"),
            MathTex(r"{1\over\lambda}", r" = ", r"1.097\times10^7 \text{m}^{-1}", r" \left( ", r"{1\over", " 2^2}", " -", r"{1\over", " 3^2}", r" \right)"),
            MathTex(r"{1\over\lambda}", r" = ", r"1.097\times10^7 \text{m}^{-1}", r" \left( ", r"{1\over", " 4}", " -", r"{1\over", " 9}", r" \right)"),
            MathTex(r"{1\over\lambda}", r" = ", r"1.097\times10^7 \text{m}^{-1}", r" \left( ", r"{9\over", " 36}", " -", r"{4\over", " 36}", r" \right)"),
            MathTex(r"{1\over\lambda}", r" = ", r"1.097\times10^7 \text{m}^{-1}", r" \left( ", r"{9-4", r"\over", " 36}", r" \right)"),
            MathTex(r"{1\over\lambda}", r" = ", r"1.097\times10^7 \text{m}^{-1}", r" \left( ", r"{5", r"\over", " 36}", r" \right)"),
            MathTex(r"{1\over\lambda}", r" = ", r"1.097\times10^7 \text{m}^{-1}", r"\cdot", r"{5", r"\over", " 36}"),
            MathTex(r"{1\over\lambda}", r" = ", r"0.152\times10^7 \text{m}^{-1}"),
            MathTex(r"\lambda", r" = ", r"6.563\times10^{-7} \text{m}"),
            MathTex(r"\lambda", r" = ", r"656.3 \text{nm}"),
        )
        for i, c in enumerate(calc):
            c[0][-1].set_color(cmap[r"\lambda"])
            if i < 8:
                c[2].set_color(cmap[r"R_H"])
            if 0 < i < 4:
                c[5][0].set_color(cmap["n"])
                c[8][0].set_color(cmap["m"])
            if 4 <= i < 7:
                c[4:-1].set_color(interpolate_color(cmap["n"], cmap["m"], 0.5))
            if i == 7:
                c[4:].set_color(interpolate_color(cmap["n"], cmap["m"], 0.5))
            if i == 8:
                c[2:].set_color(interpolate_color(cmap[r"R_H"], interpolate_color(cmap["n"], cmap["m"], 0.5), 0.5))
            if i >= 9:
                c[2].set_color(balmer_colors[0])
        calc.add(MathTex(r"\lambda_{2\leftarrow3}", r" = ", r"656.3 \text{nm}"))
        calc[-1][0][0].set_color(cmap[r"\lambda"])
        calc[-1][-1].set_color(balmer_colors[0])

        self.remove(formel)
        for i, c in enumerate(calc):
            if i == 0:
                self.add(c)
            elif i in [1, 5, 7]:
                self.play(
                    TransformMatchingTex(calc[i-1], c)
                )
            else:
                self.play(
                    ReplacementTransform(calc[i-1], c)
                )
            self.slide_pause()

        photon_energies = VGroup(
            MathTex(r"\lambda_{2\leftarrow3}", r" = ", r"656.3 \text{nm}"),
            MathTex(r"\lambda_{2\leftarrow4}", r" = ", r"486.1 \text{nm}"),
            MathTex(r"\lambda_{2\leftarrow5}", r" = ", r"434.0 \text{nm}"),
            MathTex(r"\lambda_{2\leftarrow6}", r" = ", r"410.2 \text{nm}"),
        ).arrange(DOWN, aligned_edge=LEFT).next_to(c, DOWN, buff=0).shift(UP * c.get_height()).set_z_index(2)
        for en, col in zip(photon_energies, balmer_colors):
            en[0][0].set_color(cmap[r"\lambda"])
            en[-1].set_color(col)
        self.remove(c)
        self.add(photon_energies[0])
        self.play(
            LaggedStart(
                *[FadeIn(pe, shift=0.5*DOWN) for pe in photon_energies[1:]],
                lag_ratio=0.75
            ),
            run_time=2
        )
        self.slide_pause()
        self.play(
            photon_energies.animate.to_edge(DL)
        )
        srec = get_background_rect(
            photon_energies, stroke_colour=color_gradient(balmer_colors, 8), fill_color=BLACK, fill_opacity=0.8
        ).set_z_index(1)
        balmer_lab = Tex("Balmerserien").next_to(srec, UP, aligned_edge=LEFT, buff=0.1).set_color(
            color_gradient([interpolate_color(WHITE, bc, 0.25) for bc in balmer_colors], 8)
        )
        self.play(
            # DrawBorderThenFill(srec),
            FadeIn(srec),
            Write(balmer_lab),
            run_time=0.5
        )
        self.slide_pause()
        return VGroup(photon_energies, srec, balmer_lab)

    def balmer_serie(self, photon_energies):
        ECOL = GOLD_A
        PCOL = RED
        NCOL = GRAY
        OCOL = LIGHT_GRAY
        balmer_colors = [
            interpolate_color(VISIBLE_LIGHT[650], VISIBLE_LIGHT[650], 0.628),
            interpolate_color(VISIBLE_LIGHT[480], VISIBLE_LIGHT[490], 0.614),
            interpolate_color(VISIBLE_LIGHT[430], VISIBLE_LIGHT[440], 0.405),
            interpolate_color(VISIBLE_LIGHT[410], VISIBLE_LIGHT[410], 0.173),
        ]

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
        electron = atom.get_electrons()
        orbitals = atom.get_orbitals().set_style(stroke_width=1.5)
        electron.move_to(
            orbitals[1].point_at_angle(np.arctan(electron.get_center()[1]/electron.get_center()[0]))
        )
        backup_electron = electron.copy()
        self.play(
            FadeIn(atom)
        )
        # self.play(
        #     Indicate(orbitals[1:3], color=balmer_colors[0])
        # )
        self.slide_pause()
        orb_labels = VGroup(*[
            MathTex(rf"n={i+1}").scale(0.5).next_to(orb, DOWN, buff=0) for i, orb in enumerate(orbitals)
        ])
        self.play(
            LaggedStart(
                *[ShowPassingFlash(orb.copy().set_color(YELLOW), time_width=2, run_time=0.5) for orb in orbitals],
                lag_ratio=0.9
            ),
            LaggedStart(
                *[FadeIn(lab, shift=0.25*DOWN) for lab in orb_labels],
                lag_ratio=0.9
            ),
            run_time=9
        )
        self.slide_pause()

        for orb, bcol in zip(orbitals[2:7], balmer_colors):
            self.play(
                ShowPassingFlash(VGroup(orbitals[1], orb).copy().set_color(bcol), time_width=2),
                run_time=3
            )
            self.abs_animation(electron, orb, bcol)
            self.slide_pause()
            self.exc_animation(electron, orbitals[1], bcol)
            self.slide_pause()

