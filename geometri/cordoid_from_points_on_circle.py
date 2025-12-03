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


class Cordoid(MovingCameraScene, Slide if slides else Scene):
    def construct(self):
        self.camera.background_color = DARKER_GRAY
        self.cordoid()

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def make_circle_and_points(self, num_points, radius=1):
        circle = Circle(radius=radius)
        points = VGroup(
            *[
                Dot(fill_color=BLACK).move_to(circle.point_at_angle(a)) for a in np.arange(0, 2*PI, num_points)
            ]
        )
        return VGroup(circle, points)

    def cordoid(self):
        num_points = 32
        circle, points = self.make_circle_and_points(num_points)
        self.add(circle, points)
        lines = VGroup()
        for i in range(2 * num_points):
            dot1 = points[i % num_points]
            dot2 = points[2 * i % num_points]
            line = Line(dot1, dot2)
            self.add(line)
            lines.add(line)
            self.wait()



if __name__ == "__main__":
    classes = [
        Cordoid
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