import sys
sys.path.append("../")
from manim import *
# from manim_chemistry import *
from custom_classes import BohrAtom
from helpers import *
import random
import subprocess
from manim_slides import Slide

slides = True

q = "h"
_RESOLUTION = {
    "ul": "426,240",
    "l": "854,480",
    "h": "1920,1080"
}
_FRAMERATE = {
    "ul": 5,
    "l": 15,
    "h": 60
}


class AbsorptionExcitation(Scene if not slides else Slide):
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
        self.slide_pause()
        play_title2(self, title)
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
        # self.add(formel)
        self.play(
            Write(formel),
            run_time=0.5
        )
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
            MathTex(r"{1\over\lambda}", r" = ", r"1.097\times10^7 \text{m}^{-1}", r" \left( ", r"{1\over", " n^2}", " -", r"{1\over", " m^2}", r" \right)", " ", " ", " ", " "),
            MathTex(r"{1\over\lambda}", r" = ", r"1.097\times10^7 \text{m}^{-1}", r" \left( ", r"{1\over", " 2^2}", " -", r"{1\over", " 3^2}", r" \right)", " ", " ", " ", " "),
            MathTex(r"{1\over\lambda}", r" = ", r"1.097\times10^7 \text{m}^{-1}", r" \left( ", r"{1\over", " 4}", " -", r"{1\over", " 9}", r" \right)", " ", " ", " ", " "),
            MathTex(r"{1\over\lambda}", r" = ", r"1.097\times10^7 \text{m}^{-1}", r" \left( ", r"{9\over", " 36}", " -", r"{4\over", " 36}", r" \right)", " ", " ", " ", " "),
            MathTex(r"{1\over\lambda}", r" = ", r"1.097\times10^7 \text{m}^{-1}", r" \left( ", r"{9-4", r"\over", " 36}", r" \right)", " ", " ", " ", " ", " ", " "),
            MathTex(r"{1\over\lambda}", r" = ", r"1.097\times10^7 \text{m}^{-1}", r" \left( ", r"{5", r"\over", " 36}", r" \right)", " ", " ", " ", " ", " ", " "),
            MathTex(r"{1\over\lambda}", r" = ", r"1.097\times10^7 \text{m}^{-1}", r"\cdot", r"{5", r"\over", " 36}", " ", " ", " ", " ", " ", " ", " "),
            MathTex(r"{1\over\lambda}", r" = ", r"0.152\times10^7 \text{m}^{-1}", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "),
            MathTex(r"\lambda", r" = ", r"6.563\times10^{-7} \text{m}", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "),
            MathTex(r"\lambda", r" = ", r"656.3 \text{nm}", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "),
        )
        for n in calc:
            print(len(n))
        [calc[i][0][2].set_color(cmap[r"\lambda"]) for i in [1, 2, 3, 4, 5, 6, 7, 8]]
        [calc[i][0].set_color(cmap[r"\lambda"]) for i in [9, 10]]
        [calc[i][2].set_color(cmap[r"R_H"]) for i in [1, 2, 3, 4, 5, 6, 7]]
        [calc[i][5][0].set_color(cmap["n"]) for i in [1, 2, 3]]
        # calc[4][5].set_color(cmap["n"])
        calc[4][4:9].set_color(interpolate_color(cmap["n"], cmap["m"], 0.5))
        [calc[i][4:7].set_color(interpolate_color(cmap["n"], cmap["m"], 0.5)) for i in [5, 6, 7]]
        [calc[i][8][0].set_color(cmap["m"]) for i in [1, 2, 3]]
        # calc[4][8].set_color(cmap["m"])
        calc[8][2].set_color(interpolate_color(cmap[r"R_H"], interpolate_color(cmap["n"], cmap["m"], 0.5), 0.5))
        [calc[i][2].set_color(balmer_colors[0]) for i in [9, 10]]

        # for i, c in enumerate(calc):
        #     c[0][-1].set_color(cmap[r"\lambda"])
        #     if i < 8:
        #         c[2].set_color(cmap[r"R_H"])
        #     if 0 < i < 4:
        #         c[5][0].set_color(cmap["n"])
        #         c[8][0].set_color(cmap["m"])
        #     if 4 <= i < 7:
        #         c[4:-1].set_color(interpolate_color(cmap["n"], cmap["m"], 0.5))
        #     if i == 7:
        #         c[4:].set_color(interpolate_color(cmap["n"], cmap["m"], 0.5))
        #     if i == 8:
        #         c[2:].set_color(interpolate_color(cmap[r"R_H"], interpolate_color(cmap["n"], cmap["m"], 0.5), 0.5))
        #     if i >= 9:
        #         c[2].set_color(balmer_colors[0])
        calc.add(MathTex(r"\lambda", r"_{2\leftarrow3}", r" = ", r"656.3 \text{nm}", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "))
        calc[-1][0][0].set_color(cmap[r"\lambda"])
        calc[-1][3].set_color(balmer_colors[0])

        self.remove(formel)
        for i, c in enumerate(calc):
            if i == 0:
                self.add(c)
            # elif i in [1, 5, 7]:
            #     self.play(
            #         TransformMatchingTex(calc[i-1], c)
            #     )
            else:
                self.play(
                    ReplacementTransform(calc[i-1], c, transform_mismatches=True)
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


class RydbergBalmerThumbnail(RydbergBalmer):
    def construct(self):
        title = Tex("Rydbergformlen og Balmerserien")
        self.slide_pause()
        play_title2(self, title)
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
        # self.add(formel)
        self.play(
            Write(formel),
            run_time=0.5
        )
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
            MathTex(r"{1\over\lambda}", r" = ", r"1.097\times10^7 \text{m}^{-1}", r" \left( ", r"{1\over", " n^2}", " -", r"{1\over", " m^2}", r" \right)", " ", " ", " ", " "),
            MathTex(r"{1\over\lambda}", r" = ", r"1.097\times10^7 \text{m}^{-1}", r" \left( ", r"{1\over", " 2^2}", " -", r"{1\over", " 3^2}", r" \right)", " ", " ", " ", " "),
            MathTex(r"{1\over\lambda}", r" = ", r"1.097\times10^7 \text{m}^{-1}", r" \left( ", r"{1\over", " 4}", " -", r"{1\over", " 9}", r" \right)", " ", " ", " ", " "),
            MathTex(r"{1\over\lambda}", r" = ", r"1.097\times10^7 \text{m}^{-1}", r" \left( ", r"{9\over", " 36}", " -", r"{4\over", " 36}", r" \right)", " ", " ", " ", " "),
            MathTex(r"{1\over\lambda}", r" = ", r"1.097\times10^7 \text{m}^{-1}", r" \left( ", r"{9-4", r"\over", " 36}", r" \right)", " ", " ", " ", " ", " ", " "),
            MathTex(r"{1\over\lambda}", r" = ", r"1.097\times10^7 \text{m}^{-1}", r" \left( ", r"{5", r"\over", " 36}", r" \right)", " ", " ", " ", " ", " ", " "),
            MathTex(r"{1\over\lambda}", r" = ", r"1.097\times10^7 \text{m}^{-1}", r"\cdot", r"{5", r"\over", " 36}", " ", " ", " ", " ", " ", " ", " "),
            MathTex(r"{1\over\lambda}", r" = ", r"0.152\times10^7 \text{m}^{-1}", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "),
            MathTex(r"\lambda", r" = ", r"6.563\times10^{-7} \text{m}", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "),
            MathTex(r"\lambda", r" = ", r"656.3 \text{nm}", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "),
        )
        for n in calc:
            print(len(n))
        [calc[i][0][2].set_color(cmap[r"\lambda"]) for i in [1, 2, 3, 4, 5, 6, 7, 8]]
        [calc[i][0].set_color(cmap[r"\lambda"]) for i in [9, 10]]
        [calc[i][2].set_color(cmap[r"R_H"]) for i in [1, 2, 3, 4, 5, 6, 7]]
        [calc[i][5][0].set_color(cmap["n"]) for i in [1, 2, 3]]
        # calc[4][5].set_color(cmap["n"])
        calc[4][4:9].set_color(interpolate_color(cmap["n"], cmap["m"], 0.5))
        [calc[i][4:7].set_color(interpolate_color(cmap["n"], cmap["m"], 0.5)) for i in [5, 6, 7]]
        [calc[i][8][0].set_color(cmap["m"]) for i in [1, 2, 3]]
        # calc[4][8].set_color(cmap["m"])
        calc[8][2].set_color(interpolate_color(cmap[r"R_H"], interpolate_color(cmap["n"], cmap["m"], 0.5), 0.5))
        [calc[i][2].set_color(balmer_colors[0]) for i in [9, 10]]

        # for i, c in enumerate(calc):
        #     c[0][-1].set_color(cmap[r"\lambda"])
        #     if i < 8:
        #         c[2].set_color(cmap[r"R_H"])
        #     if 0 < i < 4:
        #         c[5][0].set_color(cmap["n"])
        #         c[8][0].set_color(cmap["m"])
        #     if 4 <= i < 7:
        #         c[4:-1].set_color(interpolate_color(cmap["n"], cmap["m"], 0.5))
        #     if i == 7:
        #         c[4:].set_color(interpolate_color(cmap["n"], cmap["m"], 0.5))
        #     if i == 8:
        #         c[2:].set_color(interpolate_color(cmap[r"R_H"], interpolate_color(cmap["n"], cmap["m"], 0.5), 0.5))
        #     if i >= 9:
        #         c[2].set_color(balmer_colors[0])
        calc.add(MathTex(r"\lambda", r"_{2\leftarrow3}", r" = ", r"656.3 \text{nm}", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "))
        calc[-1][0][0].set_color(cmap[r"\lambda"])
        calc[-1][3].set_color(balmer_colors[0])

        self.remove(formel)
        for i, c in enumerate(calc):
            if i == 0:
                self.add(c)
            # elif i in [1, 5, 7]:
            #     self.play(
            #         TransformMatchingTex(calc[i-1], c)
            #     )
            else:
                self.play(
                    ReplacementTransform(calc[i-1], c, transform_mismatches=True)
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


class Spektra(MovingCameraScene, Scene if not slides else Slide):
    btransparent = False

    def construct(self):
        self.absorption()

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def absorption(self):
        H_farver = [
            interpolate_color(VISIBLE_LIGHT[650], VISIBLE_LIGHT[650], 0.628),
            interpolate_color(VISIBLE_LIGHT[480], VISIBLE_LIGHT[490], 0.614),
            interpolate_color(VISIBLE_LIGHT[430], VISIBLE_LIGHT[440], 0.405),
            interpolate_color(VISIBLE_LIGHT[410], VISIBLE_LIGHT[410], 0.173),
        ]
        He_farver = [
            interpolate_color(VISIBLE_LIGHT[650], VISIBLE_LIGHT[650], 0.0),
            interpolate_color(VISIBLE_LIGHT[580], VISIBLE_LIGHT[590], 0.8),
            interpolate_color(VISIBLE_LIGHT[500], VISIBLE_LIGHT[510], 0.2),
            interpolate_color(VISIBLE_LIGHT[490], VISIBLE_LIGHT[500], 0.2),
            interpolate_color(VISIBLE_LIGHT[470], VISIBLE_LIGHT[480], 0.1),
            interpolate_color(VISIBLE_LIGHT[440], VISIBLE_LIGHT[450], 0.7),
            interpolate_color(VISIBLE_LIGHT[430], VISIBLE_LIGHT[440], 0.9),
            interpolate_color(VISIBLE_LIGHT[410], VISIBLE_LIGHT[410], 0.0),
        ]

        H_lambda = [656, 486, 434, 410]
        He_lambda = [668, 588, 502, 492, 471, 447, 439, 403]
        fuldt_spektrum = [l for l in np.arange(400, 671, 1)]
        H_linjer = VGroup(*[
            Rectangle(
                width=1, height=25, fill_color=c, fill_opacity=1, stroke_width=0
            ).shift(l*RIGHT) for c, l in zip(H_farver, H_lambda)
        ])
        He_linjer = VGroup(*[
            Rectangle(
                width=1, height=25, fill_color=c, fill_opacity=1, stroke_width=0
            ).shift(l*RIGHT) for c, l in zip(He_farver, He_lambda)
        ])
        fuld_linjer = VGroup(*[
            Rectangle(
                width=1, height=25, fill_opacity=1, stroke_width=0, fill_color=interpolate_color(
                    VISIBLE_LIGHT[10*np.floor(l/10)], VISIBLE_LIGHT[10*np.ceil(l/10)], (l - 10*np.floor(l/10))/10
                )
            ).shift(l * RIGHT) for l in fuldt_spektrum if l not in H_lambda + He_lambda
        ])

        titles = VGroup(
            Tex("Synligt lys", "", "", "", "", font_size=800).next_to(fuld_linjer, UP, aligned_edge=LEFT),
            Tex("Synligt lys", " minus ", "Hydrogen", "", "", font_size=800).next_to(fuld_linjer, UP, aligned_edge=LEFT),
            Tex("Synligt lys", " minus ", "Hydrogen", " og ", "Helium", font_size=800).next_to(fuld_linjer, UP, aligned_edge=LEFT),
            Tex("Hydrogen", "", "", font_size=800).next_to(fuld_linjer, UP, aligned_edge=LEFT).shift(50*DOWN),
            Tex("", "", "Helium", font_size=800).next_to(fuld_linjer, UP, aligned_edge=LEFT).shift(100*DOWN),
            Tex("Hydrogen", " + ", "Helium", font_size=800).next_to(fuld_linjer, UP, aligned_edge=LEFT).shift(75*DOWN)
        )

        self.camera.frame.set(
            width=300
        ).move_to(VGroup(fuld_linjer, H_linjer, He_linjer)).shift(50*DOWN)
        # self.add(fuld_linjer)
        # self.wait(0.5)
        # self.add(H_linjer)
        # self.wait(0.5)
        # self.add(He_linjer)
        # self.wait(0.5)
        self.add(fuld_linjer, H_linjer, He_linjer, titles[0])
        self.slide_pause()

        self.play(
            H_linjer.animate.shift(50*DOWN),
            FadeIn(titles[3], shift=50*DOWN),
            TransformMatchingTex(titles[0], titles[1], transform_mismatches=False)
        )
        self.slide_pause()

        self.play(
            He_linjer.animate.shift(100*DOWN),
            FadeIn(titles[4], shift=100*DOWN),
            TransformMatchingTex(titles[1], titles[2], transform_mismatches=False)
        )
        self.slide_pause()

        self.play(
            H_linjer.animate.shift(25*DOWN),
            He_linjer.animate.shift(25*UP),
            TransformMatchingTex(VGroup(titles[3], titles[4]), titles[5], transform_mismatches=False)
        )
        self.slide_pause()


class SpektraThumbnail(MovingCameraScene):

    def construct(self):
        H_farver = [
            interpolate_color(VISIBLE_LIGHT[650], VISIBLE_LIGHT[650], 0.628),
            interpolate_color(VISIBLE_LIGHT[480], VISIBLE_LIGHT[490], 0.614),
            interpolate_color(VISIBLE_LIGHT[430], VISIBLE_LIGHT[440], 0.405),
            interpolate_color(VISIBLE_LIGHT[410], VISIBLE_LIGHT[410], 0.173),
        ]
        He_farver = [
            interpolate_color(VISIBLE_LIGHT[650], VISIBLE_LIGHT[650], 0.0),
            interpolate_color(VISIBLE_LIGHT[580], VISIBLE_LIGHT[590], 0.8),
            interpolate_color(VISIBLE_LIGHT[500], VISIBLE_LIGHT[510], 0.2),
            interpolate_color(VISIBLE_LIGHT[490], VISIBLE_LIGHT[500], 0.2),
            interpolate_color(VISIBLE_LIGHT[470], VISIBLE_LIGHT[480], 0.1),
            interpolate_color(VISIBLE_LIGHT[440], VISIBLE_LIGHT[450], 0.7),
            interpolate_color(VISIBLE_LIGHT[430], VISIBLE_LIGHT[440], 0.9),
            interpolate_color(VISIBLE_LIGHT[410], VISIBLE_LIGHT[410], 0.0),
        ]

        H_lambda = [656, 486, 434, 410]
        He_lambda = [668, 588, 502, 492, 471, 447, 439, 403]
        fuldt_spektrum = [l for l in np.arange(400, 671, 1)]
        H_linjer = VGroup(*[
            Rectangle(
                width=1, height=25, fill_color=c, fill_opacity=1, stroke_width=0
            ).shift(l*RIGHT) for c, l in zip(H_farver, H_lambda)
        ])
        He_linjer = VGroup(*[
            Rectangle(
                width=1, height=25, fill_color=c, fill_opacity=1, stroke_width=0
            ).shift(l*RIGHT) for c, l in zip(He_farver, He_lambda)
        ])
        fuld_linjer = VGroup(*[
            Rectangle(
                width=1, height=25, fill_opacity=1, stroke_width=0, fill_color=interpolate_color(
                    VISIBLE_LIGHT[10*np.floor(l/10)], VISIBLE_LIGHT[10*np.ceil(l/10)], (l - 10*np.floor(l/10))/10
                )
            ).shift(l * RIGHT) for l in fuldt_spektrum if l not in H_lambda + He_lambda
        ])

        titles = VGroup(
            # Tex("Synligt lys", "", "", "", "", font_size=800).next_to(fuld_linjer, UP, aligned_edge=LEFT),
            # Tex("Synligt lys", " minus ", "Hydrogen", "", "", font_size=800).next_to(fuld_linjer, UP, aligned_edge=LEFT),
            Tex("Synligt lys", " minus ", "Hydrogen", " og ", "Helium", font_size=800).next_to(fuld_linjer, UP, aligned_edge=LEFT),
            # Tex("Hydrogen", "", "", font_size=800).next_to(fuld_linjer, UP, aligned_edge=LEFT).shift(50*DOWN),
            # Tex("", "", "Helium", font_size=800).next_to(fuld_linjer, UP, aligned_edge=LEFT).shift(100*DOWN),
            Tex("Hydrogen", " + ", "Helium", font_size=800).next_to(fuld_linjer, UP, aligned_edge=LEFT).shift(75*DOWN)
        )

        self.camera.frame.set(
            width=300
        ).move_to(VGroup(fuld_linjer, H_linjer, He_linjer)).shift(25*DOWN)
        # self.add(fuld_linjer)
        # self.wait(0.5)
        # self.add(H_linjer)
        # self.wait(0.5)
        # self.add(He_linjer)
        # self.wait(0.5)
        self.add(fuld_linjer, H_linjer.shift(75*DOWN), He_linjer.shift(75*DOWN), titles)
        # self.slide_pause()

        title = Tex("Absorptions", "- og ", "emissions", "spektre", font_size=1600).next_to(
            titles, UP, aligned_edge=LEFT
        ).shift(20*UP)
        title[0].set_color(YELLOW)
        title[2].set_color(BLUE)
        self.add(title)


class RedShift(MovingCameraScene, Scene if not slides else Slide):
    def construct(self):
        self.slide_pause()
        self.absorption()
        fade_out_all(self)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def _absorption(self):
        plane = NumberLine(
            x_range=[350, 750, 50],
            # y_range=[0, 2],
            length=400,
            # y_length=75,
            # axis_config={"include_numbers": True, "font_size": 288}
            stroke_width=50,
            include_numbers=True,
            font_size=800,
        ).set_z_index(4)
        plane_lines = VGroup(*[
            DashedLine(start=plane.n2p(i), end=plane.n2p(i) + 210 * UP, stroke_width=25) for i in
            np.linspace(350, 750, 9)
        ])
        self.add(plane, plane_lines)

        H_lambda_ref = [656.34, 486.17, 434.08, 410.21]
        H_farver_ref = [
            interpolate_color(
                VISIBLE_LIGHT[10 * np.floor(l / 10)],
                VISIBLE_LIGHT[10 * np.ceil(l / 10)],
                (l - 10 * np.floor(l / 10)) / 10
            ) for l in H_lambda_ref
        ]
        # H_farver_ref = [
        #     interpolate_color(VISIBLE_LIGHT[650], VISIBLE_LIGHT[660], 0.628),
        #     interpolate_color(VISIBLE_LIGHT[480], VISIBLE_LIGHT[490], 0.614),
        #     interpolate_color(VISIBLE_LIGHT[430], VISIBLE_LIGHT[440], 0.405),
        #     interpolate_color(VISIBLE_LIGHT[400], VISIBLE_LIGHT[410], 0.173),
        # ]

        z_faktorer = {"Andromeda": 0.00103, "A2147": 0.035}
        # z_faktorer = {"Andromeda": 0.0203}
        H_lambda_fjern = {
            k: [l * (1 + z) for l in H_lambda_ref] for k, z in z_faktorer.items()
        }
        H_farver_fjern = {
            # k: [interpolate_color(
            #     VISIBLE_LIGHT[10*np.floor(l*(1+z)/10)],
            #     VISIBLE_LIGHT[10*np.ceil(l*(1+z)/10)],
            #     (l*(1+z) - 10*np.floor(l*(1+z)/10))/10
            # ) for l in H_lambda] for k, z in z_faktorer.items()
            k: [interpolate_color(
                VISIBLE_LIGHT[10 * np.floor(l / 10)],
                VISIBLE_LIGHT[10 * np.ceil(l / 10)],
                (l - 10 * np.floor(l / 10)) / 10
            ) for l in H_lambda_fjern[k]] for k in z_faktorer.keys()
        }
        print(H_farver_fjern, H_farver_ref)

        H_linjer_ref = VGroup(*[
            Rectangle(
                width=1, height=50, fill_color=c, fill_opacity=1, stroke_width=0
            ).move_to(plane.n2p(l)).shift(70 * UP) for c, l in zip(H_farver_ref, H_lambda_ref)
        ])
        H_linjer_fjern = {
            k: VGroup(*[
                Rectangle(
                    width=1, height=50, fill_color=c, fill_opacity=1, stroke_width=0
                ).move_to(plane.n2p(l)).shift(140 * UP) for c, l in zip(H_farver_fjern[k], H_lambda_fjern[k])
            ]) for k in z_faktorer.keys()
        }

        H_labels_ref = VGroup(*[
            Tex(f"{plane.p2n(l.get_center()):.2f}nm", font_size=600).next_to(l, DOWN) for l in H_linjer_ref
        ])
        H_labels_fjern = {
            k: VGroup(*[
                Tex(f"{plane.p2n(l.get_center()):.2f}nm", font_size=600).next_to(l, DOWN) for l in H_linjer_fjern[k]
            ]) for k in z_faktorer.keys()
        }

        data_labels = VGroup(
            Tex("Hydrogen, ref", font_size=800).next_to(plane_lines[0], DR).shift(H_linjer_ref[0].get_y() * UP),
            Tex("Hydrogen, A2147", font_size=800).next_to(plane_lines[0], DR).shift(
                H_linjer_fjern["A2147"][0].get_y() * UP)
        )
        self.add(data_labels)
        # titles = VGroup(
        #     Tex("Synligt lys", "", "", font_size=800).next_to(fuld_linjer, UP, aligned_edge=LEFT),
        #     Tex("Synligt lys", " minus ", "Hydrogen", font_size=800).next_to(fuld_linjer, UP, aligned_edge=LEFT),
        #     Tex("Hydrogen", "", "", font_size=800).next_to(fuld_linjer, UP, aligned_edge=LEFT).shift(50*DOWN),
        # )
        #
        self.camera.frame.set(
            # width=300
            # ).move_to(VGroup(H_linjer_ref, H_linjer_fjern["A2147"]))
            width=450,
            # height=125
        ).move_to(plane).shift(100 * UP)
        self.add(H_linjer_ref, H_linjer_fjern["A2147"])
        self.wait()
        # H_linjer_ref.shift(25*UP)
        # H_labels_ref.shift(25*UP)
        # H_linjer_fjern["A2147"].shift(25*DOWN)
        # H_labels_fjern["A2147"].shift(25*DOWN)
        self.add(H_labels_ref, H_labels_fjern["A2147"])
        self.wait()

    def absorption(self):
        self.camera.frame.set(
            width=16
        )
        plane = NumberLine(
            x_range=[350, 750, 50],
            # y_range=[0, 2],
            length=8,
            # y_length=75,
            # axis_config={"include_numbers": True, "font_size": 288}
            stroke_width=2,
            include_numbers=True,
            font_size=40,
        ).set_z_index(4).shift(3*DOWN)
        x_labels = plane.get_ticks()
        plane_lines = VGroup(*[
            DashedLine(start=plane.n2p(i), end=plane.n2p(i) + 6*UP, stroke_width=1) for i in np.linspace(350, 750, 9)
        ])
        # self.add(plane, plane_lines)
        self.play(
            LaggedStart(
                # *[DrawBorderThenFill(m) for m in [*plane, *plane_lines]],
                # *[Write(m) for m in x_labels],
                DrawBorderThenFill(plane),
                DrawBorderThenFill(plane_lines),
                Write(x_labels),
                lag_ratio=0.1
            ),
            run_time=0.5
        )
        # self.add(plane, x_labels)

        H_lambda_ref = [656.34, 486.17, 434.08, 410.21]
        H_farver_ref = [
            interpolate_color(
                VISIBLE_LIGHT[10*np.floor(l/10)],
                VISIBLE_LIGHT[10*np.ceil(l/10)],
                (l - 10*np.floor(l/10))/10
            ) for l in H_lambda_ref
        ]

        z_faktorer = {"Andromeda": 0.00103, "A2147": 0.035}
        H_lambda_fjern = {
            k: [l * (1 + z) for l in H_lambda_ref] for k, z in z_faktorer.items()
        }
        H_farver_fjern = {
            k: [interpolate_color(
                VISIBLE_LIGHT[10*np.floor(l/10)],
                VISIBLE_LIGHT[10*np.ceil(l/10)],
                (l - 10*np.floor(l/10))/10
            ) for l in H_lambda_fjern[k]] for k in z_faktorer.keys()
        }

        # H_linjer_ref = VGroup(*[
        #     Rectangle(
        #         width=1, height=50, fill_color=c, fill_opacity=1, stroke_width=0
        #     ).move_to(plane.n2p(l)).shift(70*UP) for c, l in zip(H_farver_ref, H_lambda_ref)
        # ])
        H_linjer_ref = VGroup(*[
            Line(
                start=plane.n2p(l)+0.5*UP, end=plane.n2p(l)+2.5*UP, stroke_color=c, stroke_width=3
            ) for c, l in zip(H_farver_ref, H_lambda_ref)
        ])
        # H_linjer_fjern = {
        #     k: VGroup(*[
        #         Rectangle(
        #             width=1, height=50, fill_color=c, fill_opacity=1, stroke_width=0
        #         ).move_to(plane.n2p(l)).shift(140*UP) for c, l in zip(H_farver_fjern[k], H_lambda_fjern[k])
        #     ]) for k in z_faktorer.keys()
        # }
        H_linjer_fjern = {
            k: VGroup(*[
                Line(
                    start=plane.n2p(l)+3.5*UP, end=plane.n2p(l)+5.5*UP, stroke_color=c, stroke_width=3
                ) for c, l in zip(H_farver_fjern[k], H_lambda_fjern[k])
            ]) for k in z_faktorer.keys()
        }

        H_labels_ref = VGroup(*[
            Tex(f"{plane.p2n(l.get_center()):.2f}nm", font_size=24).next_to(l, UP, buff=b) for l, b in zip(
                H_linjer_ref, [0, 0, 0.25, 0]
            )
        ])
        H_labels_fjern = {
            k: VGroup(*[
                Tex(f"{plane.p2n(l.get_center()):.2f}nm", font_size=24).next_to(l, UP, buff=b) for l, b in zip(
                H_linjer_fjern[k], [0, 0, 0.25, 0]
            )
            ]) for k in z_faktorer.keys()
        }

        data_labels = VGroup(
            Tex("Hydrogen, ref", font_size=24).next_to(plane_lines[0], DL, aligned_edge=DOWN).shift(1.5*UP),
            Tex("Hydrogen, A2147", font_size=24).next_to(plane_lines[0], DL, aligned_edge=DOWN).shift(4.5*UP)
        )
        self.play(
            LaggedStart(
                *[Write(m) for m in data_labels],
                *[Create(m) for m in [*H_linjer_ref, *H_linjer_fjern["A2147"]]],
                lag_ratio=0.1
            ),
            run_time=0.5
        )
        # self.add(data_labels)
        # self.add(H_linjer_ref, H_linjer_fjern["A2147"])
        self.slide_pause()

        self.play(
            LaggedStart(
                *[Write(m) for m in [*H_labels_ref, *H_labels_fjern["A2147"]]],
                lag_ratio=0.1
            ),
            run_time=0.5
        )
        # self.add(H_labels_ref, H_labels_fjern["A2147"])
        self.slide_pause()

        opgave = VGroup(
            Tex("Find ud af, hvordan spektret fra A2147"),
            Tex("er opstået ud fra referencen.")
        ).arrange(DOWN, aligned_edge=RIGHT).next_to(plane_lines[4], UP)
        self.play(
            Write(opgave),
            run_time=0.5
        )
        # self.add(opgave)
        self.slide_pause()

        z_tracker = ValueTracker(z_faktorer["A2147"])
        # z_tracker = ValueTracker(0)
        H_linjer_tracker = always_redraw(lambda:
            VGroup(*[
                Line(
                    start=plane.n2p(l * (1+z_tracker.get_value()))+3.5*UP,
                    end=plane.n2p(l * (1+z_tracker.get_value()))+5.5*UP,
                    stroke_width=3,
                    stroke_color=interpolate_color(
                        VISIBLE_LIGHT[10*np.floor(l * (1+z_tracker.get_value())/10)],
                        VISIBLE_LIGHT[10*np.ceil(l * (1+z_tracker.get_value())/10)],
                        (l * (1+z_tracker.get_value()) - 10*np.floor(l * (1+z_tracker.get_value())/10))/10
                    )
                ) for l in H_lambda_ref
            ])
        )
        self.play(
            LaggedStart(
                *[FadeOut(m) for m in [data_labels, H_labels_ref, H_labels_fjern["A2147"], H_linjer_fjern["A2147"]]],
                *[FadeIn(m) for m in H_linjer_tracker],
                lag_ratio=0.1
            ),
            run_time=0.5
        )
        self.remove(H_linjer_tracker)
        # self.remove(data_labels, H_labels_ref, H_labels_fjern["A2147"], H_linjer_fjern["A2147"])
        self.add(H_linjer_tracker)
        self.slide_pause()

        self.play(
            z_tracker.animate.set_value(0),
            run_time=1
        )
        self.slide_pause()

        z_label = always_redraw(lambda:
            VGroup(
                MathTex("z = "),
                DecimalNumber(z_tracker.get_value(), num_decimal_places=5)
            ).arrange(RIGHT).next_to(plane_lines[-1], DR, aligned_edge=DOWN).shift(4.5*UP)
        )
        # self.add(z_label)
        self.play(
            Write(z_label)
        )
        self.play(
            z_tracker.animate.set_value(z_faktorer["A2147"]),
            run_time=5
        )
        self.slide_pause()


if __name__ == "__main__":
    cls = Spektra
    class_name = cls.__name__
    # transparent = cls.btransparent
    command = rf"manim {sys.argv[0]} {class_name} -p --resolution={_RESOLUTION[q]} --frame_rate={_FRAMERATE[q]}"
    # if transparent:
    #     command += " --transparent --format=webm"
    scene_marker(rf"RUNNNING:    {command}")
    # subprocess.run(command)
    if slides and q == "h":
        command = rf"manim-slides convert {class_name} {class_name}.html"
        scene_marker(rf"RUNNNING:    {command}")
        # subprocess.run(command)
        if class_name+"Thumbnail" in dir():
            command = rf"manim {sys.argv[0]} {class_name}Thumbnail -pq{q} -o {class_name}Thumbnail.png"
            scene_marker(rf"RUNNNING:    {command}")
            subprocess.run(command)
