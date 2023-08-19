import sys
sys.path.append("../")
from manim import *
from helpers import *

slides = True
if slides:
    from manim_slides import Slide


class TrigFunktioner(MovingCameraScene, Slide if slides else None):
    def construct(self):
        self.enhedscirkel()
        # self.trig_funktioner()
        self.wait(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def enhedscirkel(self):
        self.camera.frame.save_state()
        ac = RED
        plane = NumberPlane(
            x_range=[-1.5, 1.5, 0.25],
            y_range=[-1.5, 1.5, 0.25],
            x_length=3,
            y_length=3,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 0.5,
                # "stroke_opacity": 0.4,
                "stroke_opacity": 0.1
            },
            # axis_config={"include_numbers": True, "numbers_to_include": [-1, -0.5, 0, 0.5, 1]}
        ).set_z_index(2)
        plane_rec = get_background_rect(plane, stroke_colour=ac, buff=0)
        # unit_circle = Circle(radius=1, color=WHITE).move_to(plane.c2p(0, 0))
        unit_circle = Circle().from_three_points(
            plane.c2p(1, 0), plane.c2p(0, 1), plane.c2p(-1, 0)
        ).set_color(WHITE).set_stroke(width=0.5).set_z_index(3)
        tickmarks = {
            "x": VGroup(*[Line(
                start=plane.c2p(x, 0.05), end=plane.c2p(x, -0.05), color=WHITE, stroke_width=0.75
            ) for x in np.arange(-1, 1.1, 0.5)]).set_z_index(4),
            "y": VGroup(*[Line(
                start=plane.c2p(0.05, y), end=plane.c2p(-0.05, y), color=WHITE, stroke_width=0.75
            ) for y in np.arange(-1, 1.1, 0.5)]).set_z_index(4),
        }
        ticks = {
            "x": VGroup(*[DecimalNumber(
                number=x, num_decimal_places=1, include_sign=x < 0, color=WHITE, font_size=8 if x != 0 else 0.01
            ).next_to(
                tm.get_center(), DL if x < 0 else DR, buff=0.05
            ) for x, tm in zip(np.arange(-1, 1.1, 0.5), tickmarks["x"])]).set_z_index(4),
            "y": VGroup(*[DecimalNumber(
                number=y, num_decimal_places=1, include_sign=y < 0, color=WHITE, font_size=8
            ).next_to(
                tm.get_center(), DL, buff=0.05
            ) for y, tm in zip(np.arange(-1, 1.1, 0.5), tickmarks["y"])]).set_z_index(4)
        }

        self.play(
            LaggedStart(
                Create(plane_rec),
                DrawBorderThenFill(plane, lag_ratio=0.0),
                Create(unit_circle),
                self.camera.frame.animate.set(height=1.1 * plane.height),
                *[Create(tickmarks[d], lag_ratio=0.5) for d in tickmarks.keys()],
                lag_ratio=0.25
            ),
            run_time=2
        )
        self.slide_pause()

        self.play(
            *[Write(ticks[d], lag_ratio=0.1) for d in ticks.keys()],
            run_time=0.5
        )
        self.slide_pause()

        theta = ValueTracker(0)  # Rad
        radius_line = always_redraw(lambda: Line(
            start=plane.c2p(0, 0), end=unit_circle.point_at_angle(theta.get_value()), color=ac, stroke_width=1.5
        ).set_z_index(5))
        radius_text = Tex(f"radius = 1", font_size=12).next_to(plane_rec, RIGHT, buff=0.05, aligned_edge=UP)
        edge_point = always_redraw(lambda:
            Dot(radius=0.02, point=unit_circle.point_at_angle(theta.get_value()), color=GREEN).set_z_index(5)
        )
        hline = always_redraw(lambda: Line(
            start=plane.c2p(0, edge_point.get_y()), end=edge_point.get_center(), color=BLUE, stroke_width=1
        ).set_z_index(radius_line.get_z_index() - 1))
        vline = always_redraw(lambda: Line(
            start=plane.c2p(edge_point.get_x(), 0), end=edge_point.get_center(), color=YELLOW, stroke_width=1
        ).set_z_index(radius_line.get_z_index() - 1))
        self.play(
            GrowFromPoint(radius_line, plane.c2p(0, 0))
        )
        self.play(
            theta.animate.set_value(TAU),
            run_time=2,
        )
        self.play(
            ReplacementTransform(radius_line.copy(), radius_text),
            radius_line.copy().animate.scale(0.5).next_to(radius_text, DOWN, aligned_edge=LEFT, buff=0.05),
        )
        self.slide_pause()

        self.play(
            plane[2].animate.set_color(YELLOW).set(stroke_width=0.75),
            plane[3].animate.set_color(BLUE).set(stroke_width=0.75),
            DrawBorderThenFill(edge_point)
        )
        self.add(hline, vline)
        self.play(
            self.camera.frame.animate.move_to(plane.c2p(1, 0)),
            run_time=2
        )
        self.slide_pause()

        self.play(
            theta.animate.set_value(2*TAU),
            run_time=TAU
        )
        theta.set_value(0)
        self.slide_pause()

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

