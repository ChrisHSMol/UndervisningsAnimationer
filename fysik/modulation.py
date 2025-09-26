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

q = "ul"
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


class Modulation(MovingCameraScene, Slide if slides else Scene):
    def construct(self):
        # self.vigtige_begreber()
        self.am_modulering()
        self.fm_modulering()

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def message_function(self, x):
        # return (np.sin(0.5*x - 2) + 1) * np.exp(-0.05*x) * 2
        return x

    def am_modulering(self):
        message_amp_tracker = ValueTracker(1)
        message_lambda_tracker = ValueTracker(8)
        message_phase_tracker = ValueTracker(0)
        carrier_amp_tracker = ValueTracker(1)
        carrier_lambda_tracker = ValueTracker(2)
        carrier_phase_tracker = ValueTracker(0)
        planes = VGroup(*[
            NumberPlane(
                x_range=[-32, 32, 1],
                y_range=[-3, 3, 1],
                x_length=16,
                y_length=3,
                background_line_style={
                    "stroke_color": TEAL,
                    "stroke_width": 1,
                    "stroke_opacity": 0.3
                }
            ) for _ in range(3)
        ]).arrange(DOWN, buff=0).scale(0.9)
        labels = VGroup(*[
            Tex(t, color=c).next_to(
                plane, UP, aligned_edge=LEFT
            ).shift(DOWN+0.5*RIGHT).set_z_index(3) for t, c, plane in zip(
                ["Besked", "Bærer", "Signal"], [BLUE, YELLOW, GREEN], planes
            )
        ])
        message_wave = always_redraw(lambda: planes[0].plot(
            lambda x: message_amp_tracker.get_value() * np.sin(
                2*self.message_function(x)*PI/message_lambda_tracker.get_value() + message_phase_tracker.get_value()
            ),
            color=BLUE
        ))
        carrier_wave = always_redraw(lambda: planes[1].plot(
            lambda x: carrier_amp_tracker.get_value() * np.sin(2*x*PI/carrier_lambda_tracker.get_value() + carrier_phase_tracker.get_value()),
            color=YELLOW
        ))
        am_wave = always_redraw(lambda: planes[2].plot(
            # lambda x: message_wave.underlying_function(x) + carrier_wave.underlying_function(x),
            lambda x: (message_wave.underlying_function(x)+1) * carrier_wave.underlying_function(x),
            color=GREEN
        ))
        # message_wave_copy = always_redraw(lambda: message_wave.copy().set_style(stroke_opacity=0.5).move_to(am_wave))
        message_wave_copy = always_redraw(lambda:
            planes[2].plot(lambda x: message_wave.underlying_function(x) + 1, color=BLUE, stroke_opacity=0.5)
        )
        self.add(planes, message_wave, carrier_wave, am_wave, message_wave_copy, labels)
        self.slide_pause()

        self.play(
            carrier_lambda_tracker.animate.set_value(1),
            run_time=5,
            # rate_func=rate_functions.linear
        )
        self.slide_pause()
        self.play(
            carrier_lambda_tracker.animate.set_value(4),
            run_time=5,
            # rate_func=rate_functions.linear
        )
        self.slide_pause()
        self.play(
            carrier_lambda_tracker.animate.set_value(2),
            run_time=5,
            # rate_func=rate_functions.linear
        )
        self.slide_pause()

        self.play(
            message_lambda_tracker.animate.set_value(16),
            run_time=5
        )
        self.slide_pause()

        self.play(
            message_lambda_tracker.animate.set_value(32),
            run_time=5
        )
        self.slide_pause()

        self.play(
            message_lambda_tracker.animate.set_value(8),
            run_time=5
        )
        self.slide_pause()
        self.remove(planes, message_wave, carrier_wave, am_wave, message_wave_copy, labels)

    def fm_modulering(self):
        message_amp_tracker = ValueTracker(1)
        message_lambda_tracker = ValueTracker(8)
        message_phase_tracker = ValueTracker(0)
        carrier_amp_tracker = ValueTracker(1)
        carrier_lambda_tracker = ValueTracker(2)
        carrier_phase_tracker = ValueTracker(0)
        planes = VGroup(*[
            NumberPlane(
                x_range=[-32, 32, 1],
                y_range=[-3, 3, 1],
                x_length=16,
                y_length=3,
                background_line_style={
                    "stroke_color": TEAL,
                    "stroke_width": 1,
                    "stroke_opacity": 0.3
                }
            ) for _ in range(3)
        ]).arrange(DOWN, buff=0).scale(0.9)
        labels = VGroup(*[
            Tex(t, color=c).next_to(
                plane, UP, aligned_edge=LEFT
            ).shift(DOWN+0.5*RIGHT).set_z_index(3) for t, c, plane in zip(
                ["Besked", "Bærer", "Signal"], [BLUE, YELLOW, GREEN], planes
            )
        ])
        message_wave = always_redraw(lambda: planes[0].plot(
            lambda x: message_amp_tracker.get_value() * np.sin(
                2*self.message_function(x)*PI/message_lambda_tracker.get_value() + message_phase_tracker.get_value()
            ),
            color=BLUE
        ))
        carrier_wave = always_redraw(lambda: planes[1].plot(
            lambda x: carrier_amp_tracker.get_value() * np.sin(2*x*PI/carrier_lambda_tracker.get_value() + carrier_phase_tracker.get_value()),
            color=YELLOW
        ))
        fm_wave = always_redraw(lambda: planes[2].plot(
            # lambda x: message_wave.underlying_function(x) + carrier_wave.underlying_function(x),
            # lambda x: np.sin(
            #     2*x*PI/((carrier_lambda_tracker.get_value())+1) * message_wave.underlying_function(x)
            #     np.sin(2*x*PI/(carrier_lambda_tracker.get_value() * message_lambda_tracker.get_value()))
            # lambda x: carrier_lambda_tracker.get_value() * np.sin(2*x*PI/carrier_lambda_tracker.get_value() * 0.5*(
            #         np.sin(2*x*PI/message_lambda_tracker.get_value() + message_phase_tracker.get_value()) * message_amp_tracker.get_value() + 1
            # )
            lambda x: np.sin(
                4*x*x*PI*PI/(((carrier_lambda_tracker.get_value())+1) * message_wave.underlying_function(x))
            ),
            color=GREEN
        ))
        # message_wave_copy = always_redraw(lambda: message_wave.copy().set_style(stroke_opacity=0.5).move_to(fm_wave))
        message_wave_copy = always_redraw(lambda:
            planes[2].plot(lambda x: message_wave.underlying_function(x)+1, color=BLUE, stroke_opacity=0.5)
        )
        self.add(planes, message_wave, carrier_wave, fm_wave, message_wave_copy, labels)
        self.slide_pause()

        self.play(
            message_lambda_tracker.animate.set_value(32),
            run_time=5
        )
        self.slide_pause()

        self.play(
            message_lambda_tracker.animate.set_value(8),
            run_time=5
        )
        self.slide_pause()

        self.play(
            carrier_lambda_tracker.animate.set_value(4),
            run_time=5
        )
        self.slide_pause()

        self.play(
            carrier_lambda_tracker.animate.set_value(1),
            run_time=5
        )
        self.slide_pause()


if __name__ == "__main__":
    classes = [
        Modulation
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
