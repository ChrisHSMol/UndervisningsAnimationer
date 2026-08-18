import math
import random

from manim import *
import sys

from manim_chemistry import ChemicalFormula

sys.path.append("../")
sys.path.append("../../")
import numpy as np
import pandas as pd
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


class LodretKast(MovingCameraScene, Slide if slides else Scene):
    def construct(self):
        self.camera.background_color = DARKER_GRAY
        # title = Tex("Fældningsreaktioner").scale(2)
        # self.add(title)
        # self.slide_pause()
        # self.play(
        #     FadeOut(title),
        #     run_time=0.25
        # )
        self.experimental_setup()
        # self.stedfunktion()
        # self.hastighedsfunktion()
        # self.accelerationsfunktion()
        self.wait(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def _cmap(self):
        return {"tid": BLUE_A, "sted": GREEN, "hast": YELLOW, "acc": RED}

    def experimental_setup(self):
        t_start = -1
        # Simulation setup
        t = ValueTracker(-1)  # s
        g = 9.82  # m/s^2
        m = 1.0  # kg
        h_max = 1.0  # m
        sigY = 1e-2  # m
        v0 = 10  # m/s
        s0 = 0.1  # m

        t_done = 2 * v0/g
        t_slut = np.ceil(t_done)

        cmap = self._cmap()
        sensor = Rectangle(
            width=4, height=0.25, stroke_width=0.25, fill_opacity=1, fill_color=BLUE
        ).to_edge(DL)
        svg_path = r"..\SVGs\basketball.svg"
        ball = SVGMobject(svg_path).scale(0.75).next_to(sensor, UP, buff=s0)
        ball_ref = ball.copy()
        # self.play(
        #     DrawBorderThenFill(ball),
        #     run_time=0.5
        # )
        # self.slide_pause()
        self.add(sensor, ball)

        def sted_raw(time, a=g, v=v0, s=s0):
            return -0.5 * a * time ** 2 + v * time + s

        def sted(time, a=g, v=v0, s=s0):
            return np.max([sted_raw(time, a=a, v=v, s=s), s])

        def sted_measured(time, a=g, v=v0, s=s0):
            return sted(time, a=a, v=v, s=s) + random.gauss(mu=0.0, sigma=sigY)

        def disp(time, a=g, h0=h_max):  # Displacement
            return h0 - 0.5 * a * time ** 2 if time <= 1 else h0 - 0.5 * a * (2 - time) ** 2

        def vf(time, a=g):  # final velocity
            return a * time if time <= 1 else a * (2 - time)

        def epot(time, mass=m, a=g):
            return disp(time) * mass * a

        ball.add_updater(
            lambda mob:
            mob.move_to(ball_ref.get_center() + sted(t.get_value()) * UP)
        )
        h_brace = always_redraw(lambda:
            BraceBetweenPoints(
                point_1=sensor.get_top() + RIGHT,
                point_2=ball.get_bottom() + RIGHT,
                direction=RIGHT,
                color=cmap["sted"]
            )
        )
        h_text = always_redraw(lambda:
            DecimalNumber(
                sted_measured(t.get_value()),
                num_decimal_places=2,
                include_sign=False,
                color=cmap["sted"],
                unit=" m"
            ).next_to(h_brace, RIGHT)
        )
        self.add(h_brace, h_text)
        self.play(
            t.animate.set_value(t_slut),
            run_time=t_slut-t_start,
            rate_func=linear,
        )

        plane = NumberPlane(
            x_range=(t_start, t_slut, 0.25),
            y_range=(-1, 6, 0.5),
            x_length=7,
            y_length=7,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.4
            }
        ).to_edge(DR, buff=0.55)
        stedpunkter = VGroup(
            *[
                Dot(
                    radius=0.05, stroke_width=0, fill_opacity=1, fill_color=cmap["sted"]
                ).move_to(plane.c2p(_t, sted_measured(_t))) for _t in np.linspace(t_start, t_slut, 50)
            ]
        )
        # stedgraf = always_redraw(lambda: plane.plot(
        #     lambda x: sted_measured(t.get_value()),
        # ))
        self.add(plane, stedpunkter)
        t.set_value(-1)

        self.play(
            t.animate.set_value(t_slut),
            LaggedStart(
                *[FadeIn(dot) for dot in stedpunkter],
                lag_ratio=(t_slut-t_start)/len(stedpunkter)
            ),
            run_time=t_slut-t_start,
            rate_func=linear,
        )

        stedgraf = plane.plot(lambda x: sted_raw(x), color=cmap["sted"])
        self.add(stedgraf)


if __name__ == "__main__":
    classes = [
        LodretKast,
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