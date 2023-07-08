from manim import *
import sys
sys.path.append("../")
from helpers import *
import numpy as np

slides = False
if slides:
    from manim_slides import Slide


class ComplexTest(ThreeDScene):
    def construct(self):
        self.test3d()

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t=t, slides_bool=slides_bool)

    def test3d(self):
        plane = NumberPlane(
            x_range=[-12, 12, 2],
            y_range=[-1.5, 1.5, 0.25],
            x_length=12,
            y_length=12 / 32 * 9,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 0,
                "stroke_opacity": 0.3
            },
            # axis_config={"include_numbers": True}
        )

        phase_tracker = ValueTracker(0)
        wave_dots = always_redraw(lambda: VGroup(*[
            Dot(
                plane.c2p(x, np.sin(x * 2 * PI / 3 + phase_tracker.get_value())),
                color=interpolate_color(RED, BLUE, 0.5*(np.sin(x * 2 * PI / 3 + phase_tracker.get_value())+1)),
                radius=0.04
            ) for x in np.linspace(-6.5, 6.5, 61)
        ]))
        self.play(
            DrawBorderThenFill(plane),
            Create(wave_dots)
        )
        self.play(
            phase_tracker.animate.set_value(10),
            run_time=10,
            rate_func=rate_functions.linear
        )

        self.slide_pause()

        axes = ThreeDAxes(
            x_range=(0, 5, 1),
            y_range=(0, 5, 1),
            z_range=(-1, 1, 1)
        )
        x_label = axes.get_x_axis_label(Tex("x"))
        y_label = axes.get_y_axis_label(Tex("y")).shift(UP * 1.8)
        self.set_camera_orientation(
            phi=0,
            zoom=0.5
        )
        self.play(FadeIn(axes), FadeIn(x_label), FadeIn(y_label))

        def param_surface(u, v):
            x = u
            y = v
            z = np.sin(x) * np.cos(y)
            return z
        surface = Surface(
            lambda u, v: axes.c2p(u, v, param_surface(u, v)),
            v_range=[0, 5],
            u_range=[0, 5],
            )
        self.add(surface)
