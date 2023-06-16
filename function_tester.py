from manim import *
from helpers import *
import numpy as np

slides = False
if slides:
    from manim_slides import Slide


"""

class Keyword(Slide if slides else Scene):
    def construct(self):
        self.add(NumberPlane())
        keyword_overlay(self)
        slides_pause(self, 5)


class BezierSplineExample(Scene):
    def construct(self):
        p1 = np.array([0, 1, 0])
        p1b = p1 + [0, -0.5, 0]
        d1 = Dot(point=p1).set_color(BLUE)
        # l1 = Line(p1, p1b)
        p2 = np.array([-2, -1, 0])
        p2b = p2 + [0, 0.5, 0]
        d2 = Dot(point=p2).set_color(RED)
        # l2 = Line(p2b, p2)
        bezier = CubicBezier(p1, p1 + DOWN, p2 + UP, p2)
        self.play(
            LaggedStart(
                Create(d1),
                # Create(l1),
                Create(bezier),
                # Create(l2),
                Create(d2),
                lag_ratio=0.66
            ),
            run_time=2
        )
        xl_pause(self)
"""

class ShineTester(Scene):
    def construct(self):
        # line = Line(LEFT, UP, stroke_width=2, color=YELLOW)
        # line = VGroup(line, *add_shine(line, 10))
        # self.play(
        #     *[Create(shine) for shine in line],
        #     run_time=4
        # )
        #
        # circ = Circle(radius=2, color=BLUE, stroke_width=2).shift(DOWN).set_style(fill_opacity=0)
        # circ = VGroup(circ, *add_shine(circ, 10))
        # self.play(
        #     *[Create(shine) for shine in circ],
        #     run_time=4
        # )
        #
        # self.wait(1)
        # fade_out_all(self)

        plane = NumberPlane()
        graph = plane.plot(lambda x: x**2)
        self.add(plane)
        graph = VGroup(graph, *add_shine(graph, nlines=10))
        self.play(
            # Create(graph),
            DrawBorderThenFill(graph),
            run_time=2
        )
        self.wait(2)


class DrejeKnapTest(Scene):
    def construct(self):
        a_knap = DrejeKnap(range_min=-2, range_max=2, label="a", show_value=True, color=WHITE, accent_color=YELLOW)
        b_knap = DrejeKnap(range_min=-3, range_max=5, label="b", show_value=True, color=WHITE, accent_color=BLUE)
        a_tracker = a_knap.tracker
        b_tracker = b_knap.tracker
        a_knap.scale(1).to_edge(UL)
        b_knap.scale(1).next_to(a_knap, DOWN)
        self.add(a_knap, b_knap)

        slider = Slider(smin=-3, smax=5, label="b", color=BLUE).scale(1).to_edge(RIGHT)
        bb_tracker = slider.tracker
        self.add(slider)

        plane = NumberPlane(
            x_range=[-6.5, 6.5, 1],
            y_range=[-3.25, 3.25, 1],
            x_length=6.5,
            y_length=3.25,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.4
            }
        )
        graph = always_redraw(lambda:
            plane.plot(lambda x: a_tracker.get_value() * x + b_tracker.get_value())
        )
        self.add(plane, graph)
        for i in range(10):
            self.play(
                a_tracker.animate.set_value(a_knap.get_max()),
                b_tracker.animate.set_value(b_knap.get_max()),
                bb_tracker.animate.set_value(b_knap.get_max()),
                run_time=5
            )
            self.play(
                a_tracker.animate.set_value(a_knap.get_min()),
                b_tracker.animate.set_value(b_knap.get_min()),
                bb_tracker.animate.set_value(b_knap.get_min())
            )

