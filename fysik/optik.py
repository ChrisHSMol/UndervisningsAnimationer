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
from _manim_physics import *

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


class Snell(MovingCameraScene, Slide if slides else Scene):
    def construct(self):
        self.camera.background_color = DARKER_GRAY
        self.concave_lens()
        self.wait(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def concave_lens(self):
        focal_tracker = ValueTracker(1.0)
        width_tracker = ValueTracker(1.0)
        index_tracker = ValueTracker(1.33)
        lens = always_redraw(lambda:
            Lens(f=focal_tracker.get_value(), d=width_tracker.get_value(), n=index_tracker.get_value())
        )
        self.add(lens)

        n_rays = ValueTracker(3)
        light = always_redraw(lambda:
            VGroup(*[
                Ray(start=8*LEFT + y*UP, direction=RIGHT) for y in np.linspace(-2, 2, n_rays + 1)
            ])
        )
        self.add(light)


if __name__ == "__main__":
    classes = [
        Snell
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