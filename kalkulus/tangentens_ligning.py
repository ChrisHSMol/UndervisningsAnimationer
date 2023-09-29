from manim import *
import sys
sys.path.append("../")
from helpers import *

slides = False
if slides:
    from manim_slides import Slide


class TangentLigning(MovingCameraScene, Slide if slides else Scene):
    def construct(self):
        self.tangentens_ligning()
        self.slide_pause(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def tangentens_ligning(self):
        c = {"f": YELLOW, "t": RED}
        xmin, xmax = -8, 8
        plane = NumberPlane(
            x_range=[xmin, xmax, 1],
            y_range=[-3, 6, 1],
            x_length=self.camera.frame.get_width(),
            y_length=self.camera.frame.get_height(),
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.3
            }
        )

        f = plane.plot(
            lambda x: 0.2 * x**2 + x - 2,
            color=c["f"]
        )
        df = plane.plot(lambda x: 0.4 * x + 1)
        self.add(plane, f)

        x0 = ValueTracker(2)
        slope = always_redraw(lambda:
            plane.get_secant_slope_group(
                x=x0.get_value(),
                graph=f,
                dx=0.01,
                secant_line_color=RED,
                secant_line_length=2
            )
        )

        def slope_function(x, x0):
            return df.underlying_function(x0) * x + (f.underlying_function(x0) - df.underlying_function(x0)*x0)

        slope_func = always_redraw(lambda:
            plane.plot(lambda x: slope_function(x, x0.get_value()))
        )
        self.add(slope_func, slope)
        self.play(
            x0.animate.set_value(xmax),
            run_time=3
        )
        self.play(
            x0.animate.set_value(xmin),
            run_time=4
        )
