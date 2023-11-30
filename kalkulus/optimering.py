from manim import *
import sys
sys.path.append("../")
from helpers import *
import subprocess

slides = False
if slides:
    from manim_slides import Slide
q = "l"


class CylindersAreal(ThreeDScene, Slide if slides else Scene):
    def construct(self):
        self.set_camera_orientation(zoom=0.5)
        V = 330
        r = ValueTracker(4.0)
        cylinder = always_redraw(lambda:
            Cylinder(
                radius=r.get_value(),
                height=V/(PI*r.get_value()*r.get_value()),
                direction=UP
            )
        )
        self.add(cylinder)
        # self.play(DrawBorderThenFill(cylinder))
        self.wait()
        # self.play(
        #     r.animate.set_value(2.0)
        # )
        # self.wait()


if __name__ == "__main__":
    class_name = CylindersAreal.__name__
    command = rf"manim {sys.argv[0]} {class_name} -pq{q}"
    scene_marker(rf"RUNNNING:    {command}")
    subprocess.run(command)
