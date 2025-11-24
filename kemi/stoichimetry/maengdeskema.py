import math

from manim import *
import sys

sys.path.append("../")
sys.path.append("../../")
import numpy as np
import subprocess
from helpers import *
from custom_classes import *
# from manim_chemistry import *

slides = True
if slides:
    from manim_slides import Slide

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
_ONEFRAME = 1/_FRAMERATE[q]


class MaengdeSkema(MovingCameraScene, Slide if slides else Scene):
    def construct(self):
        self.camera.background_color = DARKER_GRAY
        # title = Tex("Elektronegativitet").scale(2)
        # self.add(title)
        # self.slide_pause()
        # self.play(
        #     FadeOut(title),
        #     run_time=0.25
        # )
        # self.molmasse()
        self.skema()
        self.wait(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def molmasse(self):
        cmap = {"C": BLACK, "O": RED}
        # molekyle = Sumformel("CO2").shift(2*UP)
        # molekyle[0][0].set_color(cmap["C"])
        # molekyle[0][1].set_color(cmap["O"])
        tekst = Tex("CO$_2$ består af 1 ", "C", "-atom og 2 ", "O", "-atomer").to_edge(UP)
        tekst[1].set_color(cmap["C"])
        tekst[3].set_color(cmap["O"])
        atomare_molmasser = VGroup(
            Tex("Molmassen for ", "C", " er ", r"$12.01\frac{g}{mol}$"),
            Tex("Molmassen for ", "O", " er ", r"$16.00\frac{g}{mol}$"),
            Tex("Molmassen for ", "C", "O$_2$", " er ", r"$12.01\frac{g}{mol}$", " + ",
                r"$2\cdot 16.00\frac{g}{mol}$", " = ", r"$44.01\frac{g}{mol}$"),
        ).arrange(DOWN, aligned_edge=LEFT).next_to(tekst, DOWN)
        for t, c in zip(atomare_molmasser, cmap.values()):
            t[1].set_color(c),
            t[3].set_color(c)
        atomare_molmasser[-1][1].set_color(cmap["C"])
        atomare_molmasser[-1][2].set_color(cmap["O"])
        atomare_molmasser[-1][4].set_color(cmap["C"])
        atomare_molmasser[-1][6].set_color(cmap["O"])
        # atomare_molmasser[-1][-1].set_color(interpolate_color(cmap["C"], cmap["O"], 0.5)).set_stroke_color(WHITE)
        self.add(tekst, atomare_molmasser)

    def skema(self):
        reaktionsskema = VGroup(
            Sumformel("C6H12O6"), MathTex(r"\longrightarrow"),
            Sumformel("CO2", prefix="2"), MathTex("+"), Sumformel("C2H5OH", prefix="2")
        ).arrange(RIGHT, buff=0.75)
        # self.add(reaktionsskema)
        print(*reaktionsskema)
        self.play(
            Write(reaktionsskema),
            run_time=2
        )
        self.play(
            reaktionsskema.animate.shift(2*UP)
        )
        self.slide_pause()

        widths = [
            reaktionsskema[1].get_edge_center(DOWN)[0] - reaktionsskema[0].get_corner(DL)[0] + 0.5,
            reaktionsskema[3].get_edge_center(DOWN)[0] - reaktionsskema[1].get_edge_center(DOWN)[0],
            reaktionsskema[-1].get_corner(DR)[0] - reaktionsskema[3].get_edge_center(DOWN)[0] + 0.5,
        ]
        heights = [
            # 3 * reaktionsskema[0].height for _ in range(3)
            1.5 for _ in range(3)
        ]
        colors = (YELLOW, GREEN, BLUE)
        tabel_struktur = VGroup(
            *[
                VGroup(
                    *[
                        Rectangle(
                            width=w, height=h, stroke_color=c, stroke_width=0.875, fill_color=c, fill_opacity=0.075
                        ) for w in widths
                    ]
                ).arrange(RIGHT, buff=0) for h, c in zip(heights, colors)
            ]
        ).arrange(DOWN, buff=0.015).next_to(reaktionsskema, DOWN)
        row_labels = VGroup(
            *[
                Tex(t, color=c).scale(2).next_to(tab, LEFT) for t, c, tab in zip(
                    ("m", "M", "n"), colors, (tabel_struktur[0], tabel_struktur[1], tabel_struktur[2])
                )
            ]
        )
        # self.add(tabel_struktur, row_labels)
        self.play(
            LaggedStart(
                *[
                    LaggedStart(
                        *[DrawBorderThenFill(box) for box in line],
                        lag_ratio=0.1
                    ) for line in tabel_struktur
                ],
                lag_ratio=0.5
            ),
            run_time=2
        )
        self.slide_pause()

        self.play(
            Write(row_labels)
        )
        self.slide_pause()

        m_values = VGroup(
            *[
                DecimalNumber(
                    n, num_decimal_places=2, color=colors[0], unit="g"
                ).scale(0.85).next_to(tab, LEFT, buff=-0.9*tab.width) for n, tab in zip(
                    (180.18, 88.02, 92.16),
                    [*tabel_struktur[0]]
                )
            ]
        )
        # self.add(m_values)
        self.play(
            FadeIn(m_values[0], shift=m_values[0].get_center() - reaktionsskema[0].get_center()),
            Indicate(reaktionsskema[0], color=m_values[0].get_color())
        )
        self.slide_pause()

        # self.play(
        #     LaggedStart(
        #         FadeIn(m_values[1], shift=m_values[1].get_center() - reaktionsskema[2][1:].get_center()),
        #         FadeIn(m_values[2], shift=m_values[2].get_center() - reaktionsskema[4][1:].get_center()),
        #         lag_ratio=0.33
        #     ),
        #     LaggedStart(
        #         Indicate(reaktionsskema[2][1:], color=m_values[1].get_color()),
        #         Indicate(reaktionsskema[4][1:], color=m_values[2].get_color()),
        #         lag_ratio=0.33
        #     )
        # )
        # self.slide_pause()

        M_values = VGroup(
            *[
                VGroup(
                    DecimalNumber(n, num_decimal_places=2, color=colors[1]),
                    MathTex(r"\frac{g}{mol}", color=colors[1]),
                ).set(color=colors[1]).scale(0.85).arrange(RIGHT, buff=0.1).next_to(tab, LEFT, buff=-0.9*tab.width) for n, tab in zip(
                    (180.18, 44.01, 46.08),
                    [*tabel_struktur[1]]
                )
            ]
        )
        # self.add(M_values)
        self.play(
            LaggedStart(
                *[
                    AnimationGroup(
                        FadeIn(
                            M_values[i], shift=M_values[i].get_center() - reaktionsskema[2*i].get_center()
                        ),
                        Indicate(reaktionsskema[2*i][1], color=M_values[i].get_color())
                    ) for i in range(len(M_values))
                ],
                lag_ratio=0.5
            ),
            run_time=2
        )
        self.slide_pause()

        n_values = VGroup(
            *[
                DecimalNumber(
                    n, num_decimal_places=2, color=colors[2], unit="mol"
                ).scale(0.85).next_to(tab, LEFT, buff=-0.9*tab.width) for n, tab in zip(
                    (1.00, 2.00, 2.00),
                    [*tabel_struktur[2]]
                )
            ]
        )
        n_udregninger = VGroup(
            VGroup(
                m_values[0].copy(),
                Line(LEFT, RIGHT, stroke_width=0.75),
                M_values[0].copy()
            ).scale(0.75).arrange(DOWN, buff=0.1).next_to(n_values[0], LEFT).shift(0.25*DOWN)
        )
        self.add(n_values, n_udregninger)

        op_tracker = ValueTracker(0)
        hidden_index = always_redraw(lambda:
            Integer(
                1, color=colors[0], fill_opacity=op_tracker.get_value(), stroke_opacity=op_tracker.get_value(),
            ).next_to(reaktionsskema, LEFT, buff=0.1)
        )
        # hidden_index.add_updater(lambda t: hidden_index.animate.set(opacity=np.sin(t)**2))
        self.add(hidden_index)
        for _ in range(3):
            self.play(
                op_tracker.animate.set_value(1),
                rate_func=rate_functions.there_and_back
            )


class FormelMasse(MaengdeSkema):
    def construct(self):
        self.camera.background_color = DARK_GRAY
        title = Tex("Formelmasse").scale(2)
        play_title2(self, title, hidden_box_color=self.camera.background_color)
        elements = self.massetabel()
        self.eksempeludregning(elements)
        self.wait(5)

    def _tabel_label(
            self, label: str, mass: float, width: float = 1.0, height: float = 1.0, square_color: ManimColor = WHITE,
            text_color: ManimColor = WHITE,
    ):
        output = VGroup()
        output.add(
            Rectangle(
                width=width, height=height,
                stroke_color=square_color, stroke_width=0.75,
                fill_color=square_color, fill_opacity=0.2
            ).set_z_index(1)
        )
        output.add(
            Tex(
                label, color=text_color
            ).set_z_index(2).scale(0.75).next_to(output[0], DOWN, buff=0.1).shift(height * UP)
        )
        output.add(
            DecimalNumber(
                mass, num_decimal_places=2, color=text_color, unit="u"
            ).set_z_index(2).scale(0.625).next_to(output[0], UP, buff=0.1).shift(height * DOWN)
        )
        return output

    def massetabel(self, dry=False):
        masses = {
            'H': 1.01, 'He': 4.00,
            'Li': 6.94, 'Be': 9.01, 'B': 10.81, 'C': 12.01, 'N': 14.01, 'O': 16.00, 'F': 19.00, 'Ne': 20.18,
            'Na': 22.99, 'Mg': 24.31, 'Al': 26.98, 'Si': 28.09, 'P': 30.97, 'S': 32.07, 'Cl': 35.45, 'Ar': 39.95
        }
        coords = {
            'H': (0, 2, 0), 'He': (7.5, 2, 0),
            'Li': (0, 1, 0), 'Be': (1, 1, 0), 'B': (2.5, 1, 0), 'C': (3.5, 1, 0), 'N': (4.5, 1, 0), 'O': (5.5, 1, 0), 'F': (6.5, 1, 0), 'Ne': (7.5, 1, 0),
            'Na': (0, 0, 0), 'Mg': (1, 0, 0), 'Al': (2.5, 0, 0), 'Si': (3.5, 0, 0), 'P': (4.5, 0, 0), 'S': (5.5, 0, 0), 'Cl': (6.5, 0, 0), 'Ar': (7.5, 0, 0)
        }
        elements = VGroup(
            *[
                self._tabel_label(
                    label=atom, mass=masses[atom], square_color=c
                ).move_to(coords[atom]) for atom, c in zip(
                    masses.keys(), (GREEN_A, GREEN_A, *[GREEN_C for _ in range(8)], *[GREEN_E for _ in range(8)])
                )
            ]
        ).shift(4*LEFT).scale(1.5)
        # self.add(elements)

        forklarende_tekst = VGroup(
            Tex("vejer i gennemsnit").next_to(elements[0][1], RIGHT),
            Tex("vejer i gennemsnit").next_to(elements[1][2], LEFT)
        )
        if not dry:
            self.play(
                LaggedStart(
                    Write(elements[0][1]),
                    Write(forklarende_tekst[0]),
                    Write(elements[0][2]),
                    lag_ratio=0.95
                ),
                run_time=1
            )
            self.slide_pause()
            self.play(
                FadeOut(forklarende_tekst[0]),
                FadeIn(elements[0][0]),
                run_time=1
            )
            self.slide_pause()
            self.play(
                LaggedStart(
                    Write(elements[1][1]),
                    Write(forklarende_tekst[1]),
                    Write(elements[1][2]),
                    lag_ratio=0.95
                ),
                run_time=1
            )
            self.slide_pause()

            self.play(
                FadeOut(forklarende_tekst[1]),
                FadeIn(elements[1][0]),
                run_time=1
            )
            self.play(
                LaggedStart(
                    *[FadeIn(*e, lag_ratio=0.1) for e in elements[2:]],
                    lag_ratio=0.25
                ),
                run_time=5
            )
        overskrift = Tex("Formelmasse af nogle atomer").scale(1.5).move_to(between_mobjects(elements[0], elements[1]))
        if not dry:
            self.play(
                Write(overskrift),
                run_time=0.5
            )
            self.slide_pause()
        elements.add(overskrift)
        if dry:
            self.add(elements)
        return elements

    def eksempeludregning(self, elements):
        self.play(
            elements.animate.scale(1/2).to_edge(UL)
        )
        element_box = get_background_rect(
            elements, fill_color=BLACK, stroke_colour=GREEN
        )
        self.play(
            FadeIn(element_box),
            run_time=0.5
        )
        self.slide_pause()
        udregnings_tabel_struktur = VGroup(
            *[
                VGroup(
                    *[
                        Rectangle(
                            width=w, height=1, stroke_color=c, stroke_width=0.75, fill_color=c, fill_opacity=0.2
                        ).set_z_index(1) for w in (1, 3, 2)
                    ]
                ).arrange(RIGHT, buff=0.025) for c in (BLACK, BLUE, YELLOW, RED, BLACK)
            ]
        ).arrange(DOWN, buff=0.025).to_edge(UR)
        # self.add(udregnings_tabel_struktur)

        tabel_labels = VGroup(
            *[
                Tex(t).set_z_index(2).scale(0.75).next_to(
                    udregnings_tabel_struktur[0][i], UP, buff=0.1, aligned_edge=RIGHT
                ).shift(udregnings_tabel_struktur[0][i].height * DOWN) for i, t in enumerate(("Atom", "Udregning", "Masse"))
            ],
            Tex("Sum").set_z_index(2).next_to(
                    udregnings_tabel_struktur[-1][1], DOWN, buff=0.1, aligned_edge=RIGHT
                ).shift(udregnings_tabel_struktur[-1][1].height * UP)
        )
        # self.add(tabel_labels)

        eksempel_tekst = Tex("Eksempelmolekyle: Svovlsyre").to_edge(LEFT)
        eksempel_struktur = Sumformel("H2SO4").next_to(eksempel_tekst, DOWN, aligned_edge=RIGHT)
        eksempel_struktur[1][0][0].set_color(BLUE)
        eksempel_struktur[1][0][2].set_color(YELLOW)
        eksempel_struktur[1][0][3].set_color(RED)
        # self.add(eksempel_tekst, eksempel_struktur)
        self.play(
            Write(eksempel_tekst),
            Write(eksempel_struktur),
            run_time=0.5
        )
        self.slide_pause()

        eksempel_udregning = VGroup(
            VGroup(
                Tex("2 {{H}}").set_z_index(2).set_color_by_tex_to_color_map({"H": BLUE}).move_to(
                    udregnings_tabel_struktur[1][0]
                ),
                MathTex(rf"2\cdot", f"{elements[0][2].get_value()}", "u = ").set_z_index(2).next_to(
                    udregnings_tabel_struktur[1][1], LEFT, buff=0.1
                ).shift(udregnings_tabel_struktur[1][1].width * RIGHT),
                DecimalNumber(2*elements[0][2].get_value(), num_decimal_places=2, unit="u").set_z_index(2).next_to(
                    udregnings_tabel_struktur[1][2], LEFT, buff=0.1
                ).shift(udregnings_tabel_struktur[1][2].width * RIGHT)
            ),
            VGroup(
                Tex("1 {{S}}").set_color_by_tex_to_color_map({"S": YELLOW}).set_z_index(2).move_to(
                    udregnings_tabel_struktur[2][0]
                ),
                MathTex(rf"1\cdot", f"{elements[15][2].get_value()}", "u = ").set_z_index(2).next_to(
                    udregnings_tabel_struktur[2][1], LEFT, buff=0.1
                ).shift(udregnings_tabel_struktur[2][1].width * RIGHT),
                DecimalNumber(1*elements[15][2].get_value(), num_decimal_places=2, unit="u").set_z_index(2).next_to(
                    udregnings_tabel_struktur[2][2], LEFT, buff=0.1
                ).shift(udregnings_tabel_struktur[2][2].width * RIGHT)
            ),
            VGroup(
                Tex("4 {{O}}").set_color_by_tex_to_color_map({"O": RED}).set_z_index(2).move_to(
                    udregnings_tabel_struktur[3][0]
                ),
                MathTex(rf"4\cdot", f"{elements[7][2].get_value():.2f}", "u = ").set_z_index(2).next_to(
                    udregnings_tabel_struktur[3][1], LEFT, buff=0.1
                ).shift(udregnings_tabel_struktur[3][1].width * RIGHT),
                DecimalNumber(4*elements[7][2].get_value(), num_decimal_places=2, unit="u").set_z_index(2).next_to(
                    udregnings_tabel_struktur[3][2], LEFT, buff=0.1
                ).shift(udregnings_tabel_struktur[3][2].width * RIGHT)
            ),
            DecimalNumber(
                2*elements[0][2].get_value() + elements[15][2].get_value() + 4*elements[7][2].get_value(),
                num_decimal_places=2, unit="u"
            # ).next_to(udregnings_tabel_struktur[-1][-1], LEFT, buff=0.1, aligned_edge=UP).shift(
            #     udregnings_tabel_struktur[-1][-1].width * RIGHT
            # )
            ).set_z_index(2).next_to(tabel_labels[-1], RIGHT, aligned_edge=DOWN, buff=0.5)
        )
        # self.add(eksempel_udregning)
        self.play(
            Write(tabel_labels[0], run_time=0.5),
            FadeIn(udregnings_tabel_struktur[1][0]),
        )

        # H
        self.play(
            ReplacementTransform(eksempel_struktur[1][0][:2].copy(), eksempel_udregning[0][0]),
            Indicate(eksempel_struktur[1][0][:2], color=BLUE),
        )
        self.slide_pause()

        self.play(
            Write(tabel_labels[1], run_time=0.5),
            FadeIn(udregnings_tabel_struktur[1][1]),
        )
        self.play(
            ReplacementTransform(eksempel_udregning[0][0][0].copy(), eksempel_udregning[0][1][0]),
            Indicate(eksempel_udregning[0][0][0], color=BLUE),
        )
        self.slide_pause()

        self.play(
            ReplacementTransform(elements[0][2].copy(), eksempel_udregning[0][1][1]),
            FadeIn(eksempel_udregning[0][1][2]),
            Indicate(elements[0], color=BLUE)
        )
        self.slide_pause()

        self.play(
            Write(tabel_labels[2], run_time=0.5),
            FadeIn(udregnings_tabel_struktur[1][2]),
        )
        self.play(
            ReplacementTransform(eksempel_udregning[0][1][:2].copy(), eksempel_udregning[0][2]),
            Indicate(eksempel_udregning[0][1][:2], color=BLUE),
        )
        self.slide_pause()

        # S
        self.play(
            FadeIn(udregnings_tabel_struktur[2][0]),
            ReplacementTransform(eksempel_struktur[1][0][2].copy(), eksempel_udregning[1][0]),
            Indicate(eksempel_struktur[1][0][2], color=YELLOW),
        )
        self.slide_pause()

        self.play(
            FadeIn(udregnings_tabel_struktur[2][1]),
            ReplacementTransform(eksempel_udregning[1][0][0].copy(), eksempel_udregning[1][1][0]),
            Indicate(eksempel_udregning[1][0][0], color=YELLOW),
        )
        self.slide_pause()

        self.play(
            ReplacementTransform(elements[15][2].copy(), eksempel_udregning[1][1][1]),
            FadeIn(eksempel_udregning[1][1][2]),
            Indicate(elements[15], color=YELLOW)
        )
        self.slide_pause()

        self.play(
            FadeIn(udregnings_tabel_struktur[2][2]),
            ReplacementTransform(eksempel_udregning[1][1][:2].copy(), eksempel_udregning[1][2]),
            Indicate(eksempel_udregning[1][1][:2], color=YELLOW),
        )
        self.slide_pause()

        # O
        self.play(
            FadeIn(udregnings_tabel_struktur[3][0]),
            ReplacementTransform(eksempel_struktur[1][0][3:].copy(), eksempel_udregning[2][0]),
            Indicate(eksempel_struktur[1][0][3:], color=RED),
        )
        self.slide_pause()

        self.play(
            FadeIn(udregnings_tabel_struktur[3][1]),
            ReplacementTransform(eksempel_udregning[2][0][0].copy(), eksempel_udregning[2][1][0]),
            Indicate(eksempel_udregning[2][0][0], color=RED),
        )
        self.slide_pause()

        self.play(
            ReplacementTransform(elements[7][2].copy(), eksempel_udregning[2][1][1]),
            FadeIn(eksempel_udregning[2][1][2]),
            Indicate(elements[7], color=RED)
        )
        self.slide_pause()

        self.play(
            FadeIn(udregnings_tabel_struktur[3][2]),
            ReplacementTransform(eksempel_udregning[2][1][:2].copy(), eksempel_udregning[2][2]),
            Indicate(eksempel_udregning[2][1][:2], color=RED),
        )
        self.slide_pause()

        # sum
        self.play(
            Write(tabel_labels[3], run_time=0.5),
            ReplacementTransform(
                VGroup(
                    *[row[-1].copy() for row in eksempel_udregning[:3]]
                ),
                eksempel_udregning[3]
            )
        )
        self.slide_pause()

        opsummerende_tekst = VGroup(
            Tex("Svovlsyres formelmasse er derfor ", f"{eksempel_udregning[3].get_value()}u")
        ).to_edge(DOWN)
        self.play(
            FadeIn(opsummerende_tekst)
        )
        # self.slide_pause()


class FormelMasseThumbnail(FormelMasse):
    def construct(self):
        # self.camera.background_color = DARK_GRAY
        self.massetabel(dry=True)



if __name__ == "__main__":
    classes = [
        # MaengdeSkema,
        FormelMasse
    ]
    for cls in classes:
        class_name = cls.__name__
        command = rf"manim {sys.argv[0]} {class_name} -p --resolution={_RESOLUTION[q]} --frame_rate={_FRAMERATE[q]}"
        # if _bcol is not None:
        #     command += f" -c {_bcol} --background_color {_bcol}"
        scene_marker(rf"RUNNNING:    {command}")
        subprocess.run(command)
        if slides and q == "h":
            command = rf"manim-slides convert {class_name} {class_name}.html --one-file --offline"
            scene_marker(rf"RUNNNING:    {command}")
            subprocess.run(command)
            if class_name + "Thumbnail" in dir():
                command = rf"manim {sys.argv[0]} {class_name}Thumbnail -pq{q} -o {class_name}Thumbnail.png"
                scene_marker(rf"RUNNNING:    {command}")
                subprocess.run(command)