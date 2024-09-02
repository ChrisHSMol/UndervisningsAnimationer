from manim import *
import sys
sys.path.append("../")
from helpers import *
import subprocess
import random

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


class FangEnGraf(MovingCameraScene, Slide if slides else Scene):
    btransparent = False

    def construct(self):
        self.fangst()
        self.wait(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t=t, slides_bool=slides_bool)

    def fangst(self):
        xmin, xmax, xstep = -1, 11.5, 1
        ymin, ymax, ystep = -1, 8.5, 1
        width = 10
        plane = NumberPlane(
            x_range=[xmin, xmax, xstep],
            y_range=[ymin, ymax, ystep],
            x_length=width,
            y_length=width / 16 * 9,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 2,
                "stroke_opacity": 0.3
            },
            axis_config={"include_numbers": True}
        )
        self.add(plane)
        flying_graphs = VGroup(*[
            plane.plot(lambda x: a * x + b, x_range=[-20, 20]) for a, b in zip(
                (np.random.rand(6) - 0.5) * 6,
                np.random.rand(6) * 8,
            )
        ])
        self.add(flying_graphs[0])
        self.slide_pause()

        for i, graph in enumerate(flying_graphs[1:]):
            self.play(
                ReplacementTransform(flying_graphs[i], graph),
                run_time=2
            )
        # self.slide_pause()
        self.wait()

        p1 = Dot(plane.c2p(2, 3), z_index=5)
        first_lock_graph = plane.plot(lambda x: x + 1, x_range=[-20, 20], color=interpolate_color(WHITE, GREEN, 0.5))
        self.play(
            LaggedStart(
                ReplacementTransform(graph, first_lock_graph),
                FadeIn(p1),
                lag_ratio=0.95
            ),
            run_time=2
        )
        self.slide_pause()

        self.play(
            Rotate(first_lock_graph, about_point=p1.get_center(), angle=6*PI),
            run_time=10,
            # rate_func=rate_functions.linear
        )
        # self.slide_pause()
        self.wait()

        p2 = Dot(plane.c2p(4, 2), z_index=5)
        final_graph = plane.plot(lambda x: -0.5 * x + 4, x_range=[-20, 20], color=GREEN)
        self.play(
            LaggedStart(
                ReplacementTransform(first_lock_graph, final_graph),
                FadeIn(p2),
                lag_ratio=0.95
            ),
            run_time=2
        )
        self.slide_pause()


if __name__ == "__main__":
    cls = FangEnGraf
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

