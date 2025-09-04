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


class AstroAnalemma(MovingCameraScene, Slide if slides else Scene):
    def construct(self):
        self.analemma_contributions()

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def analemma_ecliptic(self, x, interpolator=1.0):
        # return -7.659 * np.sin(6.24004077 + 0.01720197 * (365.25 * (2025 - 2020) + x))
        # return -7.659 * np.sin(0.01720197*x + 37.63364)
        return -7.659 * (np.sin(0.01720197*x + 37.63364)*interpolator + np.sin(0*x)*(1-interpolator))

    def analemma_speed(self, x, interpolator=1.0):
        # return 9.863 * np.sin(2 * (6.24004077 + 0.01720197*(365.25*(2025-2020)+x)) + 3.5932)
        # return 9.863 * np.sin(0.03440394*x + 78.90348)
        return 9.863 * (np.sin(0.03440394*x + 78.90348)*interpolator + np.sin(0*x)*(1-interpolator))

    def analemma_combined(self, x, inter_tilt=1.0, inter_ecce=1.0):
        return self.analemma_ecliptic(x, interpolator=inter_tilt) + self.analemma_speed(x, interpolator=inter_ecce)

    def analemma_y(self, x):
        return (23 + 27/60) * np.sin(x*360/365.25)

    def declination_sun(self, x, a=PI, tilt_modifier=1.0):
        # return 23.5 * np.sin(x/365.25 * (-1)**((2*x)//365.25))
        return tilt_modifier * 23.5 * np.sin(a*x/360)

    def analemma_graph(self, t, a=PI, inter_tilt=1.0, inter_ecce=1.0):
        return (
            self.analemma_combined(t, inter_tilt=inter_tilt, inter_ecce=inter_ecce),
            # self.analemma_y(t),
            self.declination_sun(t, a=a, tilt_modifier=inter_tilt),
            0
        )

    def apparent_solar_time(self, t):
        return np.acos(np.cos(2*np.pi*t/365)/np.sqrt(np.cos(2*np.pi*t/365)**2 + np.sin(2*np.pi*t/365)**2 * np.cos(23.5*DEGREES)**2))

    def noon(self, t):
        return np.asin(np.sin(2*np.pi*t/365)*np.sin(23.5*DEGREES)) + 50*DEGREES

    def analemma_contributions(self):
        plane = NumberPlane(
            x_range=[0, 360.1, 30],
            y_range=[-20.1, 20.1, 5],
            x_length=8,
            y_length=4,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.3
            },
            axis_config={
                "include_numbers": True,
                "include_ticks": True,
                "font_size": 24,
                "line_to_number_buff": 0.15
            },
            x_axis_config={
                "label_direction": DOWN,
            },
            y_axis_config={
                "label_direction": LEFT,
            }
        ).to_edge(UL)
        axes_titles = VGroup(
            Tex("Dag").move_to(plane.c2p(375, 0)).scale(0.5),
            Tex("EOT").move_to(plane.c2p(0, 23)).scale(0.5)
        )
        tilt_interpolator = ValueTracker(1.0)
        ecce_interpolator = ValueTracker(1.0)
        analemma_y = plane.plot(
            self.analemma_y,
        )
        # self.add(plane, analemma_y)
        analemma_ecliptic = always_redraw(lambda: plane.plot(
            # lambda x: -7.659 * np.sin(6.24004077 + 0.01720197*(365.25*(2025-2020)+x)),
            lambda x: self.analemma_ecliptic(x, interpolator=tilt_interpolator.get_value()),
            color=BLUE
        ))
        analemma_speed = always_redraw(lambda: plane.plot(
            # lambda x: 9.863 * np.sin(2 * (6.24004077 + 0.01720197*(365.25*(2025-2020)+x)) + 3.5932),
            lambda x: self.analemma_speed(x, interpolator=ecce_interpolator.get_value()),
            color=YELLOW
        ))
        analemma_combined = always_redraw(lambda: plane.plot(
            # lambda x: analemma_ecliptic.underlying_function(x) + analemma_speed.underlying_function(x),
            lambda x: self.analemma_combined(x, inter_tilt=tilt_interpolator.get_value(), inter_ecce=ecce_interpolator.get_value()),
            color=GREEN
        ))
        graph_texts = VGroup(
            *[
                VGroup(
                    Line(LEFT, RIGHT, stroke_color=c),
                    Tex(t)
                ).scale(0.5).arrange(RIGHT) for c, t in zip(
                    [BLUE, YELLOW, GREEN], ["Eccentricitet", "Aksehældning", "EOT"]
                )
            ]
        ).arrange(DOWN, aligned_edge=LEFT).next_to(plane, RIGHT, aligned_edge=UP)
        self.add(plane, analemma_ecliptic, analemma_speed, analemma_combined, graph_texts, axes_titles)
        # self.slide_pause(5)

        plane_analemma = NumberPlane(
            x_range=[-20, 20, 5],
            y_range=[-25, 25, 5],
            x_length=4,
            y_length=4,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.3
            },
            axis_config={
                "include_numbers": True,
                "include_ticks": True,
                "font_size": 24,
                "line_to_number_buff": 0.15
            },
            x_axis_config={
                "label_direction": DOWN,
            },
            y_axis_config={
                "label_direction": LEFT,
            }
        ).to_edge(DR, buff=0.5)
        analemma_axes_titles = VGroup(
            Tex("EOT").move_to(plane_analemma.c2p(25, 0)).scale(0.5),
            MathTex(r"\delta").move_to(plane_analemma.c2p(0, 30)).scale(0.5)
        )
        # analemma = ParametricFunction(
        #     self.analemma_graph,
        #     t_range=(0, 360, 30),
        # ).move_to(plane_analemma)
        n_dots = 36
        analemma = always_redraw(lambda: VGroup(
            *[
                Dot(
                    radius=0.05, color=interpolate_color(WHITE, RED, t/n_dots)
                ).move_to(plane_analemma.c2p(*self.analemma_graph(
                    t * 365/n_dots, inter_tilt=tilt_interpolator.get_value(), inter_ecce=ecce_interpolator.get_value()
                ))) for t in range(n_dots)
            ]
        ))
        self.add(plane_analemma)#, analemma)
        # for dot in analemma:
        #     self.add(dot)
        #     self.wait(0.1)
        self.add(analemma, analemma_axes_titles)
        self.play(
            tilt_interpolator.animate.set_value(0.001),
            run_time=5
        )
        # self.slide_pause()
        self.wait()
        self.play(
            tilt_interpolator.animate.set_value(1),
        )
        self.play(
            ecce_interpolator.animate.set_value(0.001),
            run_time=5
        )
        # self.slide_pause()
        self.wait()
        self.play(
            ecce_interpolator.animate.set_value(1),
        )
        # self.slide_pause(5)
        self.wait()


if __name__ == "__main__":
    classes = [
        AstroAnalemma,
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
