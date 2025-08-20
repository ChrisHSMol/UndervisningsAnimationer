import math

from manim import *
import sys

sys.path.append("../")
sys.path.append("../../")
import numpy as np
import subprocess
from helpers import *
from custom_classes import Prikformel

slides = True
if slides:
    from manim_slides import Slide

q = "l"
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


class KovalenteBindinger(MovingCameraScene, Slide if slides else Scene):
    def construct(self):
        self.prikformler()

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def prikformler(self):
        h1 = Prikformel(
            atom_label="H",
            number_of_valence_electrons=1,
            rotation=-PI/2,
            label_color=RED
        ).shift(LEFT)
        h2 = Prikformel(
            atom_label="H",
            number_of_valence_electrons=1,
            rotation=PI/2,
            label_color=BLUE
        ).shift(RIGHT)
        self.add(h1, h2)
        # self.add(Circle())
        self.wait(1)
        self.play(
            h1.animate.shift(0.55*RIGHT),
            h2.animate.shift(0.55*LEFT)
        )
        self.wait(1)

        h1_electrons = h1[1]
        h2_electrons = h2[1]
        self.play(
            h1_electrons.animate.set_color(BLUE),
        )
        self.play(
            h1_electrons.animate.set_color(RED),
            h2_electrons.animate.set_color(RED),
        )
        self.play(
            h2_electrons.animate.set_color(BLUE),
        )



if __name__ == "__main__":
    classes = [
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

