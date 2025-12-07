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


class Cordoid(MovingCameraScene, Slide if slides else Scene):
    def construct(self):
        self.camera.background_color = DARKER_GRAY
        self.cordoid()

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def make_circle_and_points(self, num_points, radius=1):
        circle = Circle(radius=radius, stroke_color=WHITE, stroke_width=1)
        points = VGroup(
            *[
                Dot(
                    fill_color=BLUE, radius=0.05
                ).move_to(circle.point_at_angle(a)) for a in np.arange(0, 2*PI, 2*PI/num_points)
            ]
        )
        return circle, points

    def cordoid(self):
        num_points = 256
        circle, points = self.make_circle_and_points(num_points, radius=3)
        self.add(circle, points)
        lines = VGroup()
        # for i in range(2 * num_points):
        for i in range(num_points + 1):
            dot1 = points[i % num_points]
            dot2 = points[2 * i % num_points]
            line = Line(
                dot1, dot2, stroke_opacity=(0.1, 1, 0.1),
                # stroke_color=interpolate_color(WHITE, RED, i/num_points),
                stroke_color=three_way_interpolate(PURE_BLUE, WHITE, PURE_RED, i, num_points)
            )
            dot1.set_style(fill_color=RED)
            dot2.set_style(fill_color=RED)
            self.add(line)
            lines.add(line)
            self.wait(max(10/num_points, 2*_ONEFRAME))
            dot1.set_style(fill_color=BLUE)
            dot2.set_style(fill_color=BLUE)

        self.play(
            FadeOut(points),
            FadeOut(circle),
            run_time=0.25
        )
        self.wait(5)



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