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


# class ElektronegativitetTabel(ThreeDScene, Slide if slides else Scene):
class ElektronegativitetTabel(MovingCameraScene, Slide if slides else Scene):
    def construct(self):
        self.camera.background_color = DARK_GRAY
        title = Tex("Elektronegativitet").scale(2)
        if slides:
            self.next_slide(loop=True)
        self.add(title)
        self.play(
            Indicate(title, scale_factor=1.05, color=interpolate_color(RED_D, WHITE, 0.75))
        )
        if slides:
            self.next_slide(loop=False)
        self.play(
            FadeOut(title),
            run_time=0.25
        )
        self.elektronegativitet()
        self.partiel_ladning()
        self.wait(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def make_electronegativity_table(self):
        # data = np.loadtxt("electronegativity.csv", delimiter=",")
        data = []
        with open("elektronegativitet.txt", "r") as inFile:
            # print(inFile)
            for line in inFile:
                line = line.strip().split(",")
                n = line[0]
                v = line[1]
                if v == "no data":
                    v = 0
                data.append([n, float(v)])
        # data = np.array(data)
        return data

    def elektronegativitet(self):
        data = self.make_electronegativity_table()
        Z_max = 36
        width, height = 12, 5
        plane = NumberPlane(
            x_range=[0, Z_max+0.1, 1],
            y_range=[0, 4.1, 0.5],
            x_length=width,
            y_length=height,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 0.5,
                "stroke_opacity": 0.25
            },
            axis_config={"include_numbers": True},
            x_axis_config={"label_direction": DOWN},
            y_axis_config={"label_direction": LEFT}
        ).set_z_index(2)
        ax_labs = VGroup(
            plane.get_x_axis_label(Tex("Atomnummer")).next_to(plane, DOWN, aligned_edge=RIGHT),
            plane.get_y_axis_label(Tex("EN")).next_to(plane, UP, aligned_edge=LEFT),
        )
        self.add(plane, ax_labs)

        periods = [
            np.arange(0, 2),
            np.arange(2, 10),
            np.arange(10, 18),
            np.arange(18, Z_max),
        ]
        periode_tekst = VGroup(
            *[
                Tex(f"Periode {i+1}") for i in range(len(periods))
            ]
        ).next_to(plane, UP, aligned_edge=RIGHT)
        groups = [
            [0, 2, 10, 18],
            [3, 11, 19],
            [20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
            [4, 12, 30],
            [5, 13, 31],
            [6, 14, 32],
            [7, 15, 33],
            [8, 16, 34],
        ]
        gruppe_tekst = VGroup(
            *[
                Tex(f"Gruppe {n}") if n>0 else Tex("(Dem vi ignorerer)") for n in (1, 2, 0, 3, 4, 5, 6, 7)
            ]
        ).next_to(plane, UP, aligned_edge=RIGHT)

        dots = VGroup(
            *[
                Dot(
                    color=interpolate_color(WHITE, RED, y[1]/2), radius=0.05 if y[1]>0 else 0
                ).set_z_index(3).set_opacity(0).move_to(
                    plane.c2p(i+1, y[1])
                ) for i, y in enumerate(data[:Z_max])
            ]
        )
        dot_labels = VGroup(
            *[
                Tex(n[0]).set_z_index(3).set_opacity(0).scale(0.5).next_to(
                    dots[i], DOWN, buff=0.1
                ) for i, n in enumerate(data[:Z_max]) #if n[0] not in ("He", "Ne", "Ar") #if n[0] in [
                    # "H", "Li", "Na", "K", "Rb", "Cs", "Ra", "Be", "B", "C", "N", "O", "F"
                # ]
            ]
        )
        [dot_labels[i].scale(0) for i in (1, 9, 17)]
        period_lines = VGroup(
            *[
                DashedLine(
                    start=plane.c2p(x, 0), end=plane.c2p(x, 4.1), stroke_width=0.5
                ).set_z_index(3) for x in (2.5, 10.5, 18.5, 36.5, 54.5, 86.5) if x < Z_max
            ]
        )
        period_labels = VGroup(
            *[
                Tex(f"Periode {i+1}").scale(min(0.75, i+0.25)).move_to(plane.c2p(x, 4)) for i, x in enumerate(
                    (1.25, 6.5, 14.5, 27.5, 45.5, 70.5, 92.5)
                ) if x < Z_max
            ]
        )
        # underlying_gradient = Rectangle(
        #     width=width, height=height, stroke_width=0, fill_opacity=1, fill_color=color_gradient((WHITE, RED), 2)
        # ).move_to(plane)
        underlying_gradient = VGroup(
            *[
                Rectangle(
                    width=width, height=height/25, stroke_width=0, fill_opacity=0.2,
                    fill_color=interpolate_color(WHITE, RED, (i+1)/25)
                ) for i in range(25)
            ]
        ).arrange(UP, buff=0).move_to(plane.c2p(Z_max/2, 2.05))
        self.add(dots, dot_labels)
        # self.add(period_lines, period_labels, underlying_gradient)

        self.play(
            *[dots[i].animate.set_opacity(1.0) for i in periods[0]],
            *[dot_labels[i].animate.set_opacity(1.0) for i in periods[0]],
            FadeIn(periode_tekst[0], shift=RIGHT)
        )
        self.slide_pause()

        for iper, period in enumerate(periods[1:]):
            self.play(
                *[dots[i].animate.set_opacity(0.2) for i in periods[iper]],
                *[dot_labels[i].animate.set_opacity(0.2) for i in periods[iper]],
                *[dots[i].animate.set_opacity(1.0) for i in period],
                *[dot_labels[i].animate.set_opacity(1.0) for i in period],
                FadeOut(periode_tekst[iper], shift=RIGHT),
                FadeIn(periode_tekst[iper+1], shift=RIGHT)
            )
            self.slide_pause()

        self.play(
            *[dots[i].animate.set_opacity(1.0) for i in range(Z_max)],
            *[dot_labels[i].animate.set_opacity(1.0) for i in range(Z_max)],
            FadeOut(periode_tekst[-1], shift=RIGHT)
        )
        self.slide_pause()

        self.play(
            *[dots[i].animate.set_opacity(0.2) for i in range(Z_max) if i not in groups[0]],
            *[dot_labels[i].animate.set_opacity(0.2) for i in range(Z_max) if i not in groups[0]],
            FadeIn(gruppe_tekst[0], shift=DOWN)
        )
        self.slide_pause()

        for igr, group in enumerate(groups[1:]):
            self.play(
                *[dots[i].animate.set_opacity(0.2) for i in groups[igr]],
                *[dot_labels[i].animate.set_opacity(0.2) for i in groups[igr]],
                *[dots[i].animate.set_opacity(1.0) for i in group],
                *[dot_labels[i].animate.set_opacity(1.0) for i in group],
                FadeOut(gruppe_tekst[igr], shift=DOWN),
                FadeIn(gruppe_tekst[igr+1], shift=DOWN)
            )
            self.slide_pause()

        self.play(
            *[dots[i].animate.set_opacity(1.0) for i in range(Z_max)],
            *[dot_labels[i].animate.set_opacity(1.0) for i in range(Z_max)],
            FadeOut(gruppe_tekst[-1], shift=DOWN)
        )
        self.slide_pause()
        self.remove(*self.mobjects)

    def partiel_ladning(self):
        data = self.make_electronegativity_table()
        Z_max = 36
        width, height = 12, 5
        plane = NumberPlane(
            x_range=[0, Z_max+0.1, 1],
            y_range=[0, 4.1, 0.5],
            x_length=width,
            y_length=height,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 0.5,
                "stroke_opacity": 0.25
            },
            axis_config={"include_numbers": True},
            x_axis_config={"label_direction": DOWN},
            y_axis_config={"label_direction": LEFT}
        ).set_z_index(2)
        ax_labs = VGroup(
            plane.get_x_axis_label(Tex("Atomnummer")).next_to(plane, DOWN, aligned_edge=RIGHT),
            plane.get_y_axis_label(Tex("EN")).next_to(plane, UP, aligned_edge=LEFT),
        )
        dots = VGroup(
            *[
                Dot(
                    color=interpolate_color(WHITE, RED, y[1]/2), radius=0.05 if y[1]>0 else 0
                ).set_z_index(3).move_to(
                    plane.c2p(i+1, y[1])
                ) for i, y in enumerate(data[:Z_max])
            ]
        )
        dot_labels = VGroup(
            *[
                Tex(n[0]).set_z_index(3).scale(0.5).next_to(
                    dots[i], DOWN, buff=0.1
                ) for i, n in enumerate(data[:Z_max])
            ]
        )
        self.add(plane, ax_labs, dots, dot_labels)

        self.camera.frame.save_state()
        self.play(
            self.camera.frame.animate.set(
                width=20
            ),
            run_time=1
        )
        self.play(
            self.camera.frame.animate.shift(2.5*DR),
            run_time=1
        )
        self.slide_pause()

        nacl_molecule = Molecule2D(
            {"Na": [-0.5, 0, 0, 0], "Cl": [0.5, 0, 0, 0]},
        ).scale(2).next_to(plane, DOWN, aligned_edge=LEFT, buff=2)
        en_values = VGroup(
            *[
                DecimalNumber(
                    number=y[1],
                    num_decimal_places=2,
                    color=interpolate_color(WHITE, RED, y[1]/2)
                ).next_to(nacl_molecule, DOWN, aligned_edge=(-1)**i*LEFT) for i, y in enumerate((data[10], data[16]))
            ]
        )
        # self.add(nacl_molecule, en_values)
        self.play(
            DrawBorderThenFill(nacl_molecule)
        )
        self.slide_pause()

        self.play(
            LaggedStart(
                Indicate(VGroup(dots[10], dot_labels[10]), scale_factor=2),
                Indicate(VGroup(dots[16], dot_labels[16]), scale_factor=2),
                lag_ratio=0.5
            )
        )
        self.play(
            LaggedStart(
                ReplacementTransform(dots[10].copy(), en_values[0]),
                ReplacementTransform(dots[16].copy(), en_values[1]),
                lag_ratio=0.8
            ),
            run_time=2
        )
        self.slide_pause()

        udregning = VGroup(
            MathTex(r"\Delta EN_{NaCl}", " = ", r"EN_{Na}", " - ", r"EN_{Cl}"),
            MathTex(r"\Delta EN_{NaCl}", " = ", en_values[1].get_value(), " - ", en_values[0].get_value()),
            MathTex(r"\Delta EN_{NaCl}", " = ", f"{en_values[1].get_value() - en_values[0].get_value():.2f}")
        ).arrange(DOWN, aligned_edge=LEFT).next_to(nacl_molecule, RIGHT, buff=3).shift(DOWN)
        [i[0][0].set_color(BLUE) for i in udregning]
        [i[0][3:5].set_color(nacl_molecule[0][0][0].get_fill_color()) for i in udregning]
        udregning[0][2][2:].set_color(nacl_molecule[0][0][0].get_fill_color())
        udregning[1][2].set_color(nacl_molecule[0][0][0].get_fill_color())
        [i[0][5:].set_color(nacl_molecule[0][1][0].get_fill_color()) for i in udregning]
        udregning[0][4][2:].set_color(nacl_molecule[0][1][0].get_fill_color())
        udregning[1][4].set_color(nacl_molecule[0][1][0].get_fill_color())
        # symbolforklaring = Tex(r"\Delta (Delta) betyder \"\ae ndring\"").next_to(udregning, UP, aligned_edge=LEFT)
        # symbolforklaring[0].set_color(BLUE)
        # self.add(udregning)
        self.play(
            Write(udregning[0])
        )
        self.slide_pause()

        self.play(
            ReplacementTransform(udregning[0].copy(), udregning[1]),
            run_time=2
        )
        self.slide_pause()

        self.play(
            ReplacementTransform(udregning[1].copy(), udregning[2]),
            run_time=2
        )
        self.slide_pause()


if __name__ == "__main__":
    classes = [
        ElektronegativitetTabel,
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