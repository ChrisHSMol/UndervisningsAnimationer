import sys
sys.path.append("../")
from manim import *
from helpers import *

slides = False
if slides:
    from manim_slides import Slide


class TrigFunktioner(Slide if slides else Scene):
    def construct(self):
        self.trig_funktioner()
        self.slide_pause(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def trig_funktioner(self):
        unit_circle = Circle(radius=1, color=WHITE).to_edge(UL).set_z_index(2)
        sin_plane = NumberPlane(
            x_range=[0, 6*PI, 1],
            y_range=[-1.1, 1.1, 0.2],
            x_length=1.5*PI,
            y_length=2.2*unit_circle.radius,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.4
            }
        ).set_z_index(2).next_to(unit_circle, RIGHT)
        cos_plane = NumberPlane(
            x_range=[0, 6*PI, 1],
            y_range=[-1.1, 1.1, 0.2],
            x_length=1.5*PI,
            y_length=2.2*unit_circle.radius,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.4
            }
        ).rotate(-PI/2).set_z_index(2).next_to(unit_circle, DOWN)
        self.add(unit_circle, sin_plane, cos_plane)

        time_tracker = ValueTracker(0)
        moving_dot = always_redraw(lambda:
            Dot(
                unit_circle.point_at_angle(time_tracker.get_value()),
                color=GREEN
            ).set_z_index(3)
        )
        lines = always_redraw(lambda:
            VGroup(
                Line(
                    start=moving_dot.get_center(),
                    end=sin_plane.c2p(0, np.sin(time_tracker.get_value())),
                    color=BLUE
                ).set_z_index(1),
                Line(
                    start=moving_dot.get_center(),
                    end=cos_plane.c2p(0, np.cos(time_tracker.get_value())),
                    color=YELLOW
                ).set_z_index(1)
            )
        )
        sin_plot = always_redraw(lambda:
            sin_plane.plot(
                lambda x: np.sin(time_tracker.get_value() - x),
                color=BLUE,
                x_range=[0, min(6*PI, time_tracker.get_value())]
            )
        )
        cos_plot = always_redraw(lambda:
            cos_plane.plot(
                lambda x: np.cos(time_tracker.get_value() - x),
                color=YELLOW,
                x_range=[0, min(6*PI, time_tracker.get_value())]
            )
        )
        self.add(moving_dot, lines, sin_plot, cos_plot)
        target_time = 10*PI
        self.play(
            time_tracker.animate.set_value(target_time),
            run_time=target_time,
            rate_func=rate_functions.linear
        )
        self.slide_pause()

        # self.play(
        #     FadeOut(lines, unit_circle, moving_dot)
        # )
        sin_plane_copy = always_redraw(lambda: sin_plane.copy().scale(2).move_to(ORIGIN).shift(DR))
        cos_plane_copy = always_redraw(lambda: cos_plane.copy().rotate(PI/2).scale(2).move_to(ORIGIN).shift(DR))
        sin_plot_copy = always_redraw(lambda: sin_plot.copy().scale(2).move_to(ORIGIN).shift(DR))
        cos_plot_copy = always_redraw(lambda: cos_plot.copy().rotate(PI/2).scale(2).move_to(ORIGIN).shift(DR))
        self.play(
            LaggedStart(
                # VGroup(sin_plane.copy(), sin_plot.copy()).animate.scale(2).move_to(ORIGIN).shift(DR),
                # VGroup(cos_plot.copy(), cos_plane.copy()).animate.rotate(PI/2).scale(2).move_to(ORIGIN).shift(DR),
                AnimationGroup(
                    ReplacementTransform(sin_plane.copy(), sin_plane_copy),
                    ReplacementTransform(sin_plot.copy(), sin_plot_copy),
                ),
                AnimationGroup(
                    ReplacementTransform(cos_plane.copy(), cos_plane_copy),
                    ReplacementTransform(cos_plot.copy(), cos_plot_copy),
                ),
                lag_ratio=0.95
            ),
            run_time=4
        )
        self.play(
            time_tracker.animate.set_value(14*PI),
            run_time=4*PI
        )

