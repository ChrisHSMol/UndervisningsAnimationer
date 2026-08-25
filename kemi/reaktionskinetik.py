# Maxwell-Boltzmann formel:
# PDF: P(x)=np.sqrt(2/np.pi) * x**2 / a**3 * np.exp(-x**2 / (2*a**2))
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


class HastighedsFordeling(MovingCameraScene, Slide if slides else Scene):
    def construct(self):
        self.camera.background_color = DARKER_GRAY
        # title = Tex("Det lodrette kast").scale(2)
        # self.add(title)
        # self.slide_pause()
        # self.play(
        #     FadeOut(title),
        #     run_time=0.25
        # )
        self.maxwell_boltzmann()
        self.wait(5)

    def slide_pause(self, t=0.5, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def _cmap(self):
        cmap = {"tid": BLUE_C, "sted": GREEN, "hast": YELLOW, "acc": RED}
        return cmap

    def maxwell_boltzmann(self):
        # P(x) = np.sqrt(2 / np.pi) * x ** 2 / a ** 3 * np.exp(-x ** 2 / (2 * a ** 2))
        # f(v) = (m/(2pikBT))^3/2 * 4piv^2^* exp(-mv^2/(2kBT))
        eps = 1e-6
        _unit = 1.6605E-27 # kg
        kB = 1.380649E-23 # m^2 kg s^-2 K^-1
        T = ValueTracker(300) # K
        m = ValueTracker(20) * _unit
        plane = NumberPlane(
            x_range=(0, 3000+eps, 500),
            y_range=(0, 0.005+eps, 0.001),
            x_length=4.5*2,
            y_length=7.5,
            background_line_style={
                "stroke_color": LIGHTER_GRAY,
                "stroke_width": 1,
                "stroke_opacity": 0.3,
            },
            axis_config={
                "include_tip": True,
                "tip_shape": StealthTip,
                "tip_width": 0.2,
                "tip_height": 0.2
            },
        ).to_edge(RIGHT, buff=0.1)
        graph = always_redraw(lambda:
            plane.plot(
                lambda v: (m.get_value()/(2*np.pi*kB*T.get_value()))**(3/2) * 4*np.pi*v**2 * np.exp((-m.get_value()*v**2)/(2*kB*T.get_value())),
                x_range=(0, 3000)
            )
        )
        self.add(plane, graph)
        self.play(
            T.animate.set_value(0)
        )
        self.slide_pause()
        self.play(
            T.animate.set_value(1000),
            run_time=10
        )


if __name__ == "__main__":
    classes = [
        HastighedsFordeling,
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