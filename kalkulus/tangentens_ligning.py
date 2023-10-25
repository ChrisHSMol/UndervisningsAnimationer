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
        col = {"f": YELLOW, "t": BLUE, "dot": RED}
        xmin, xmax = -8, 8
        plane = NumberPlane(
            x_range=[xmin, xmax, 1],
            y_range=[-27, 27, 3],
            x_length=self.camera.frame.get_width(),
            y_length=self.camera.frame.get_height(),
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.3
            }
        )

        a0, a1, a2, a3 = 0.1, 0, -2, 0
        f = plane.plot(
            # lambda x: a * x**2 + b*x + c,
            lambda x: a0 * x**3 + a1 * x**2 + a2 * x + a3,
            color=col["f"]
        )
        # df = plane.plot(lambda x: 2*a * x + b)
        df = plane.plot(lambda x: 3 * a0 * x**2 + 2 * a1 * x + a2)
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
            rf"{a0} \cdot x^3" if a0 != 0 else "",
            "+" if a1 > 0 else "",
            rf"{a1} \cdot x^2" if a1 != 0 else "",
            "+" if a2 > 0 else "",
            rf"{a2} \cdot x" if a2 != 0 else "",
            "+" if a3 > 0 else "",
            rf"{a3}" if a3 != 0 else "",
            color=col["f"]
        ).to_edge(UL)
        dflab = always_redraw(lambda:
            MathTex(
                # "f'(x)=",
                "T(x)=",
                # rf"{df.underlying_function(x0.get_value()):.2f} \cdot x" if a != 0 else "",
                # rf"{f.underlying_function(x0.get_value()) - 2*a*x0.get_value():.2f}",
                rf"{df.underlying_function(x0.get_value()):.2f} \cdot x" if a0 != 0 else "",
                "+" if f.underlying_function(x0.get_value()) - df.underlying_function(x0.get_value())*x0.get_value() >= 0 else "",
                rf"{f.underlying_function(x0.get_value()) - df.underlying_function(x0.get_value())*x0.get_value():.2f}",
                color=col["t"]
            ).next_to(moving_point, UP)
        )

        def slope_function(x, x0):
            return df.underlying_function(x0) * x + (f.underlying_function(x0) - df.underlying_function(x0)*x0)

        slope_func = always_redraw(lambda:
            plane.plot(lambda x: slope_function(x, x0.get_value()), color=col["t"]),
        )
        intercept = always_redraw(lambda:
            Dot(plane.c2p(0, slope_func.underlying_function(0)), color=col["dot"])
        )
        intercept_lab = always_redraw(lambda:
            MathTex(rf"y={slope_func.underlying_function(0):.2f}", color=col["dot"]).next_to(intercept, RIGHT, buff=0.1)
        )
        self.add(slope_func, slope, flab, dflab, moving_point, intercept, intercept_lab)
        for x in (-5, 5, 0):
            self.play(
                x0.animate.set_value(0.9*x),
                run_time=np.abs(x0.get_value() - x)
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
