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

slides = False
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


class Ioner(MovingCameraScene, Slide if slides else Scene):
    def construct(self):
        self.natrium_ion()

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def natrium_ion(self):
        na_neutral = BohrAtom(
            e=11, p=11, n=11
        ).scale(0.5)
        print(*na_neutral.get_electrons())
        self.add(na_neutral)
        # self.play(
        #     na_neutral.get_electrons()[0][0].animate.rotate(0.05*PI, about_point=[0, 0, 0], axis=[0, 0, 1]),
        #     na_neutral.get_electrons()[0][1].animate.rotate(0.95*PI, about_point=[0, 0, 0], axis=[0, 0, 1]),
        # )
        self.slide_pause()


if __name__ == "__main__":
    classes = [
        Ioner
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
            if class_name + "Thumbnail" in dir():
                command = rf"manim {sys.argv[0]} {class_name}Thumbnail -pq{q} -o {class_name}Thumbnail.png"
                scene_marker(rf"RUNNNING:    {command}")
                subprocess.run(command)

