import math

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


class SimpleCircuits(MovingCameraScene, Slide if slides else Scene):
    def construct(self):
        self.camera.background_color = DARKER_GRAY
        # title = Tex("Fældningsreaktioner").scale(2)
        # self.add(title)
        # self.slide_pause()
        # self.play(
        #     FadeOut(title),
        #     run_time=0.25
        # )
        self.component_definitions()
        self.wait(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def _make_power_source(self, stroke_width=2):
        power_source = VGroup()
        power_source.add(
            Line(
                0.5*LEFT, 0.5*RIGHT, stroke_width=stroke_width, stroke_opacity=1
            )
        )
        power_source.add(
            Line(
                0.25*DOWN, 0.25*UP, stroke_width=2*stroke_width, stroke_opacity=1
            ).move_to(power_source[0].get_end())
        )
        power_source.add(
            Line(
                0.5*DOWN, 0.5*UP, stroke_width=stroke_width, stroke_opacity=1
            ).move_to(power_source[1]).shift(0.25*RIGHT)
        )
        power_source.add(
            power_source[0].copy().next_to(power_source[2], RIGHT, buff=0)
        )
        power_source.move_to(ORIGIN)
        return power_source

    def _line_width_circle(self, stroke_width=2):
        output = VGroup()
        output.add(
            Line(
                0.5*LEFT, 0.5*RIGHT, stroke_width=stroke_width, stroke_opacity=1
            )
        )
        output.add(
            Circle(
                radius=0.5, stroke_width=1, stroke_opacity=stroke_width, stroke_color=WHITE
            ).next_to(output[0], RIGHT, buff=0)
        )
        output.add(
            output[0].copy().next_to(output[1], RIGHT, buff=0)
        )
        output.move_to(ORIGIN)
        return output

    def _make_amperemeter(self, stroke_width=2):
        amperemeter = self._line_width_circle(stroke_width=stroke_width)
        amperemeter.add(
            Text(
                "A", font_size=42
            ).move_to(amperemeter[1])
        )
        return amperemeter

    def _make_lightbulb(self, stroke_width=2):
        lightbulb = self._line_width_circle()
        r = lightbulb[1].get_radius()
        lightbulb.add(
            *[Line(
                r*LEFT, r*RIGHT, stroke_width=stroke_width, stroke_opacity=1
            ).move_to(lightbulb[1]).rotate(a*DEGREES) for a in (45, -45)]
        )
        return lightbulb

    def _make_breaker(self, stroke_width=2):
        breaker = VGroup()
        breaker.add(
            Line(
                0.5*LEFT, 0.5*RIGHT, stroke_width=stroke_width, stroke_opacity=1
            )
        )
        breaker.add(
            Line(
                breaker[0].get_end() + 0.25*UP, breaker[0].get_end() + 0.5*RIGHT,
                stroke_width=stroke_width, stroke_opacity=1
            )
        )
        breaker.add(
            Line(
                breaker[1].get_end(), breaker[1].get_end() + RIGHT, stroke_width=stroke_width, stroke_opacity=1
            )
        )
        breaker.move_to(ORIGIN)
        return breaker

    def component_definitions(self):
        power_source = self._make_power_source().to_edge(UL)
        self.add(power_source)

        amperemeter = self._make_amperemeter().to_edge(UR)
        self.add(amperemeter)

        lightbulb = self._make_lightbulb().to_edge(DL)
        self.add(lightbulb)

        breaker = self._make_breaker().to_edge(DR)
        self.add(breaker)


if __name__ == "__main__":
    classes = [
        SimpleCircuits,
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