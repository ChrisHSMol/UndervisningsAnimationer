import math

from manim import *
import sys

sys.path.append("../")
sys.path.append("../../")
import numpy as np
import subprocess
from helpers import *
from manim_chemistry import *
from custom_classes import *

slides = False
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


class AtomPrikformel(MovingCameraScene, Slide if slides else Scene):
    def construct(self):
        self.bohr_atom()

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def bohr_atom(self):
        atomer = VGroup(
            *[
                BohrAtom(
                    e=i+1, p=i+1, n=neu
                ) for i, neu in enumerate([1, 4, 7, 9, 10, 12, 14, 16, 19, 21])
            ]
        )#.scale(0.3).arrange_in_grid(rows=3)
        # self.add(atomer)
        for atom in atomer:
            self.add(atom)
            self.slide_pause()
            self.remove(atom)


class KovalenteBindinger(AtomPrikformel):
    def construct(self):
        self.camera.background_color = WHITE
        self.prikformler()

    def prikformler(self):
        h1 = Prikformel(
            atom_label="H",
            number_of_valence_electrons=1,
            rotation=-PI/2,
            label_color=BLACK
        ).shift(LEFT)
        h2 = Prikformel(
            atom_label="H",
            number_of_valence_electrons=1,
            rotation=PI/2,
            label_color=BLACK
        ).shift(RIGHT)
        h1_nuc, h1_elec = h1
        h2_nuc, h2_elec = h2
        h1_elec.next_to(h1_nuc, UP)
        h2_elec.next_to(h2_nuc, UP)
        self.add(h1, h2)
        self.slide_pause()

        self.play(
            LaggedStart(
                h1_elec.animate.next_to(h1_nuc, RIGHT),
                h2_elec.animate.next_to(h2_nuc, LEFT),
                lag_ratio=0.25
            ),
            run_time=2
        )
        self.slide_pause()

        self.play(
            h1_elec.animate.set_color(BLUE).next_to(h1_nuc, RIGHT, aligned_edge=UP),
            h1_nuc.animate.set_color(BLUE),
            h2_elec.animate.set_color(RED).next_to(h2_nuc, LEFT, aligned_edge=DOWN),
            h2_nuc.animate.set_color(RED)
        )
        self.slide_pause()

        self.play(
            h1.animate.shift(0.45*RIGHT),
            h2.animate.shift(0.45*LEFT)
        )
        self.slide_pause()

        self.play(
            h1_elec.animate.set_color(RED),
        )
        self.play(
            h1_elec.animate.set_color(BLUE),
            h2_elec.animate.set_color(BLUE),
        )
        self.play(
            h2_elec.animate.set_color(RED),
        )
        self.slide_pause()

        p = Prikformel(
            atom_label="P",
            number_of_valence_electrons=5,
            rotation=0,
            label_color=BLACK
        ).to_edge(RIGHT)
        p[1][1].shift(0.15*DOWN)
        p[1][2].shift(0.15*LEFT)
        p[1][3].shift(0.15*UP)
        self.add(p)
        self.slide_pause()


if __name__ == "__main__":
    classes = [
        # AtomPrikformel,
        KovalenteBindinger,
    ]
    for cls in classes:
        class_name = cls.__name__
        command = rf"manim {sys.argv[0]} {class_name} -p --resolution={_RESOLUTION[q]} --frame_rate={_FRAMERATE[q]}"
        scene_marker(rf"RUNNNING:    {command}")
        subprocess.run(command)
        if slides and q == "h":
            command = rf"manim-slides convert {class_name} {class_name}.html --one-file --offline"
            scene_marker(rf"RUNNNING:    {command}")
            subprocess.run(command)
            if class_name+"Thumbnail" in dir():
                command = rf"manim {sys.argv[0]} {class_name}Thumbnail -pq{q} -o {class_name}Thumbnail.png"
                scene_marker(rf"RUNNNING:    {command}")
                subprocess.run(command)

