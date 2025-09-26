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


class ElektronegativitetTabel(ThreeDScene, Slide if slides else Scene):
    def construct(self):
        self.camera.background_color = DARK_GRAY
        title = Tex("Elektronegativitet").scale(2)
        self.next_slide(loop=True)
        self.add(title)
        self.play(
            Indicate(title, scale_factor=1.05, color=interpolate_color(RED_D, WHITE, 0.75))
        )
        self.next_slide(loop=False)
        self.play(
            FadeOut(title),
            run_time=0.25
        )
        self.elektronegativitet()
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
            *[dot_labels[i].animate.set_opacity(1.0) for i in periods[0]]
        )
        self.slide_pause()

        for iper, period in enumerate(periods[1:]):
            self.play(
                *[dots[i].animate.set_opacity(0.2) for i in periods[iper]],
                *[dot_labels[i].animate.set_opacity(0.2) for i in periods[iper]],
                *[dots[i].animate.set_opacity(1.0) for i in period],
                *[dot_labels[i].animate.set_opacity(1.0) for i in period],
            )
            self.slide_pause()

        self.play(
            *[dots[i].animate.set_opacity(1.0) for i in range(Z_max)],
            *[dot_labels[i].animate.set_opacity(1.0) for i in range(Z_max)]
        )
        self.slide_pause()

        self.play(
            *[dots[i].animate.set_opacity(0.2) for i in range(Z_max) if i not in groups[0]],
            *[dot_labels[i].animate.set_opacity(0.2) for i in range(Z_max) if i not in groups[0]]
        )
        self.slide_pause()

        for igr, group in enumerate(groups[1:]):
            self.play(
                *[dots[i].animate.set_opacity(0.2) for i in groups[igr]],
                *[dot_labels[i].animate.set_opacity(0.2) for i in groups[igr]],
                *[dots[i].animate.set_opacity(1.0) for i in group],
                *[dot_labels[i].animate.set_opacity(1.0) for i in group],
            )
            self.slide_pause()

        self.play(
            *[dots[i].animate.set_opacity(1.0) for i in range(Z_max)],
            *[dot_labels[i].animate.set_opacity(1.0) for i in range(Z_max)]
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