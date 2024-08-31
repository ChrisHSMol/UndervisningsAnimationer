from manim import *
import sys
sys.path.append("../")
from helpers import *
import subprocess
import random

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


class GeometriskUdvikling(ThreeDScene, Slide if slides else Scene):
    btransparent = False

    def construct(self):
        self.dimensionel_udvikling()
        self.wait(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t=t, slides_bool=slides_bool)

    def dimensionel_udvikling(self):
        points = VGroup(*[
            Dot(color=c).shift(LEFT).set_z_index(2-i) for i, c in enumerate([GREEN, RED])
        ])
        trace = TracedPath(points[1].get_center, color=color_gradient([GREEN, RED], 5)).set_z_index(0)
        self.add(points[0], trace)
        self.play(
            points[1].animate.shift(2*RIGHT)
        )


if __name__ == "__main__":
    cls = GeometriskUdvikling
    class_name = cls.__name__
    transparent = cls.btransparent
    command = rf"manim {sys.argv[0]} {class_name} -p --resolution={_RESOLUTION[q]} --frame_rate={_FRAMERATE[q]}"
    # if transparent:
    #     command += " --transparent --format=webm"
    scene_marker(rf"RUNNNING:    {command}")
    subprocess.run(command)
    if slides and q == "h":
        command = rf"manim-slides convert {class_name} {class_name}.html"
        scene_marker(rf"RUNNNING:    {command}")
        subprocess.run(command)
        if class_name+"Thumbnail" in dir():
            command = rf"manim {sys.argv[0]} {class_name}Thumbnail -pq{q} -o {class_name}Thumbnail.png"
            scene_marker(rf"RUNNNING:    {command}")
            subprocess.run(command)

