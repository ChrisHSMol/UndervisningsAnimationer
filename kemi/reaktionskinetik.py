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
import scipy
import subprocess
from helpers import *
from custom_classes import *
# from manim_chemistry import *

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
_ONEFRAME = 1/_FRAMERATE[q]


class HastighedsFordeling(MovingCameraScene, Slide if slides else Scene):
    def construct(self):
        self.camera.background_color = DARKER_GRAY
        title = Tex(r"Maxwell-Boltzmanns \\hastighedsfordeling").scale(2)
        self.add(title)
        self.slide_pause()
        self.play(
            FadeOut(title),
            run_time=0.25
        )
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
        T_min, T_max = 10, 5000
        m_brom, m_chlor = 79.9, 35.45
        eps = 1e-6
        _unit = 1.6605E-27 # kg
        kB = 1.380649E-23 # m^2 kg s^-2 K^-1
        T = ValueTracker(30) # K
        m = ValueTracker(m_brom) * _unit # starter på Brom
        plane = NumberPlane(
            x_range=(0, 3000+eps, 500),
            y_range=(0, 0.005+eps, 0.001),
            x_length=11,
            y_length=6,
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
        ) # .to_edge(RIGHT, buff=0.1)
        # axis_labels = VGroup(*[
        #     MathTex(
        #         lab, color=c, font_size=36
        #     ).move_to(plane.c2p(coord)).set_z_index(plane.get_z_index()+5)
        #     for lab, c, coord in zip(
        #         ["v~[m/s]", "p"], [(3, 0.25), (0.25, 6.25)]
        #     )
        # ])
        axis_labels = VGroup(
            MathTex("v~[m/s]", font_size=36).next_to(plane[2], RIGHT, aligned_edge=DOWN),
            MathTex("p", font_size=36).next_to(plane[3], UP, aligned_edge=LEFT)
        )
        tickmarks = {
            "x": VGroup(*[Line(
                start=plane.c2p(x, 0.0001), end=plane.c2p(x, -0.0001),
                color=WHITE, stroke_width=0.75
            ) for x in np.arange(0, 3000, 500)]).set_z_index(4),
            "y": VGroup(*[Line(
                start=plane.c2p(100, y), end=plane.c2p(100, y),
                color=WHITE, stroke_width=0.75
            ) for y in np.arange(0, 0.005, 0.001)]).set_z_index(4),
        }
        ticks = {
            "x": VGroup(*[DecimalNumber(
                number=x, num_decimal_places=0, include_sign=x < 0,
                color=WHITE, font_size=24 if x != 0 else 0.01
            ).set_z_index(4).next_to(
                tm, DOWN, buff=0.2
            ) for x, tm in zip(np.arange(0, 3000, 500), tickmarks["x"])]),
            "y": VGroup(*[DecimalNumber(
                number=y, num_decimal_places=3, include_sign=y < 0,
                color=WHITE, font_size=24 if y != 0 else 0.01
            ).set_z_index(4).next_to(
                tm, LEFT, buff=0.5
            ) for y, tm in zip(np.arange(0, 0.005+eps, 0.001), tickmarks["y"])]),
        }
        tick_bgs = VGroup(
            *[
                SurroundingRectangle(
                m, stroke_width=0, fill_opacity=1, fill_color=DARKER_GRAY, buff=0.025
                ) for m in ticks["x"]
            ],
            *[
                SurroundingRectangle(
                m, stroke_width=0, fill_opacity=1, fill_color=DARKER_GRAY, buff=0.025
                ) for m in ticks["y"]
            ],
            *[
                SurroundingRectangle(
                m, stroke_width=0, fill_opacity=1, fill_color=DARKER_GRAY, buff=0.025
                ) for m in axis_labels
            ]
        )
        self.play(
            LaggedStart(
                DrawBorderThenFill(plane),
                LaggedStart(
                    *[Write(l) for l in axis_labels],
                    *[Create(l) for l in tickmarks.values()],
                    *[Write(l) for l in ticks.values()],
                    lag_ratio=0.1
                ),
                lag_ratio=0.5
            ),
            run_time=3
        )
        self.slide_pause()
        graph = always_redraw(lambda:
            plane.plot(
                lambda v: (m.get_value()/(2*np.pi*kB*T.get_value()))**(3/2) * 4*np.pi*v**2 * np.exp((-m.get_value()*v**2)/(2*kB*T.get_value())),
                x_range=(0, 3000),
                color=interpolate_color(BLUE, RED, T.get_value()/(T_max-T_min))
            )
        )
        temperatur_tekst = always_redraw(lambda:
            VGroup(
                Tex("T = "),
                DecimalNumber(
                    T.get_value(), num_decimal_places=0,
                    color=interpolate_color(BLUE, RED, T.get_value()/(T_max-T_min)),
                    unit="K"
                ),
            ).arrange(RIGHT).move_to(plane.c2p(1500, 0.00525))
        )
        masse_tekst = always_redraw(lambda:
            VGroup(
                Tex("m = "),
                DecimalNumber(
                    m.get_value()/_unit, num_decimal_places=2,
                    color=YELLOW,
                    unit="amu"
                ),
            ).arrange(RIGHT).next_to(temperatur_tekst, DOWN, aligned_edge=LEFT)
        )
        # self.add(plane, graph)
        # self.add(axis_labels, *ticks.values(), *tickmarks.values())
        # self.add(temperatur_tekst, masse_tekst)
        self.play(
            LaggedStart(
                Create(graph, run_time=2),
                Write(temperatur_tekst),
                Write(masse_tekst),
                lag_ratio=0.25
            )
        )
        # self.play(
        #     T.animate.set_value(3*T_min)
        # )
        # self.slide_pause()
        # self.play(
        #     T.animate.set_value(T_max),
        #     run_time=10
        # )
        self.slide_pause()
        self.play(
            T.animate.set_value(273)
        )
        self.slide_pause()

        self.play(
            T.animate.set_value(1000),
            run_time=2
        )
        self.slide_pause()

        andel_cutoff_tracker = ValueTracker(1000) # m/s
        andel_areal = always_redraw(lambda:
            plane.get_riemann_rectangles(
                graph, x_range=(andel_cutoff_tracker.get_value(), 3000), dx=10, fill_opacity=0.75,
                stroke_width=0, color=GREEN, show_signed_area=True
            )
        )
        andel_tal = always_redraw(lambda:
            DecimalNumber(
                1 - (scipy.special.erf(andel_cutoff_tracker.get_value()*np.sqrt(m.get_value()/(2*kB*T.get_value()))) - andel_cutoff_tracker.get_value()*np.sqrt(2*m.get_value()/(kB*T.get_value())) * np.exp((-m.get_value()*andel_cutoff_tracker.get_value()**2)/(2*kB*T.get_value()))),
                color=GREEN
            ).move_to(plane.c2p(2500, 0.0015))
        ) # bliver ikke tilføjet, da resultatet går udenfor intervallet [0;1]
        # self.add(andel_areal)
        self.play(
            LaggedStart(
                *[
                    FadeIn(m) for m in andel_areal
                ],
                lag_ratio=0.01
            ),
            run_time=1
        )
        self.remove(andel_areal)
        self.add(andel_areal)
        self.slide_pause()
        self.play(
            T.animate.set_value(T_max)
        )
        self.slide_pause()
        self.play(
            T.animate.set_value(1000)
        )
        self.slide_pause()

        self.play(
            m.animate.set_value(m_chlor*_unit)
        )
        self.slide_pause()


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