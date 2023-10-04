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
        col = {"f": YELLOW, "t": RED}
        xmin, xmax = -8, 8
        plane = NumberPlane(
            x_range=[xmin, xmax, 1],
            y_range=[-9, 9, 1],
            x_length=self.camera.frame.get_width(),
            y_length=self.camera.frame.get_height(),
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.3
            }
        )

        a, b, c = 0.1, 0, 1
        f = plane.plot(
            lambda x: a * x**2 + b*x + c,
            color=col["f"]
        )
        df = plane.plot(lambda x: 2*a * x + b)
        self.add(plane, f)

        x0 = ValueTracker(0)
        slope = always_redraw(lambda:
            plane.get_secant_slope_group(
                x=x0.get_value(),
                graph=f,
                dx=0.01,
                secant_line_color=col["t"],
                secant_line_length=2
            )
        )
        moving_point = always_redraw(lambda:
            Dot(plane.c2p(x0.get_value(), f.underlying_function(x0.get_value())), color=col["t"])
        )
        flab = MathTex(
            "f(x) = ",
            rf"{a} \cdot x^2" if a != 0 else "",
            rf"{b} \cdot x" if b != 0 else "",
            rf"{c}" if c != 0 else "",
            color=col["f"]
        ).to_edge(UR)
        dflab = always_redraw(lambda:
            MathTex(
                "f'(x)=",
                rf"{df.underlying_function(x0.get_value()):.2f} \cdot x" if a != 0 else "",
                rf"{f.underlying_function(x0.get_value()) - 2*a*x0.get_value():.2f}",
                color=col["t"]
            ).next_to(moving_point, UP)
        )

        def slope_function(x, x0):
            return df.underlying_function(x0) * x + (f.underlying_function(x0) - df.underlying_function(x0)*x0)

        slope_func = always_redraw(lambda:
            plane.plot(lambda x: slope_function(x, x0.get_value()), color=col["t"]),
        )
        intercept = always_redraw(lambda:
            Dot(plane.c2p(0, slope_func.underlying_function(0)))
        )
        self.add(slope_func, slope, flab, dflab, moving_point, intercept)
        for x in (xmin, xmax, 0):
            self.play(
                x0.animate.set_value(0.9*x),
                run_time=5
            )
            self.slide_pause()
        # self.play(
        #     x0.animate.set_value(xmax),
        #     run_time=3
        # )
        # self.play(
        #     x0.animate.set_value(xmin),
        #     run_time=4
        # )
