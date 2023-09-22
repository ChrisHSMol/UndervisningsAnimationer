from manim import *
import sys
sys.path.append("../")
from helpers import *

slides = False
if slides:
    from manim_slides import Slide


class RegneRegler(MovingCameraScene, Slide if slides else Scene):
    def construct(self):
        # self.addition()
        # self.subtraktion()
        self.multiplikation()
        self.slide_pause(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def addition(self):
        c = {"f": YELLOW, "g": BLUE, "h": GREEN}
        xmin, xmax = -8, 8
        plane = NumberPlane(
            x_range=[xmin, xmax, 1],
            y_range=[-3, 9, 1],
            x_length=self.camera.frame.get_width(),
            y_length=self.camera.frame.get_height(),
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.3
            }
        )
        planes = VGroup(
            *[plane.copy().scale(0.25) for _ in range(3)]
        ).arrange(RIGHT, buff=1).shift(UP)

        f = planes[0].plot(
            lambda x: 0.2 * x**2,
            color=c["f"]
        )
        g = planes[1].plot(
            lambda x: 0.5*x,
            color=c["g"]
        )
        h = planes[2].plot(
            lambda x: f.underlying_function(x) + g.underlying_function(x),
            color=c["h"]
        )
        func_labels = VGroup(
            MathTex("f(x)=0.2x^2", color=c["f"]).next_to(planes[0], UP, buff=0.1),
            MathTex("g(x)=0.5x", color=c["g"]).next_to(planes[1], UP, buff=0.1),
            VGroup(
                MathTex("h(x)=f(x) + g(x)", color=c["h"]),
                MathTex("h(x) = 0.2x^2+0.5x", color=c["h"]),
            ).arrange(DOWN, aligned_edge=LEFT).next_to(planes[2], UP, buff=0.1)
        ).set_z_index(3)
        lrec = get_background_rect(func_labels, buff=0)
        eq_operators = VGroup(
            MathTex("+").move_to(between_mobjects(*func_labels[:2])),
            MathTex("=").move_to(between_mobjects(func_labels[1], func_labels[2][1])),
            MathTex("+").move_to(between_mobjects(*planes[:2])),
            MathTex("=").move_to(between_mobjects(*planes[1:])),
        ).set_z_index(3)
        # self.add(planes, f, g, h, func_labels)
        self.add(lrec)
        self.play(
            LaggedStart(
                DrawBorderThenFill(planes),
                Create(VGroup(f, g, h)),
                Write(func_labels),
                lag_ratio=0.75
            )
        )
        self.play(
            Write(eq_operators)
        )
        self.slide_pause()
        # self.play(
        #     DrawBorderThenFill(plane, run_time=0.25),
        #     LaggedStart(
        #         LaggedStart(
        #             Create(f),
        #             Write(func_labels[0]),
        #             lag_ratio=0.25
        #         ),
        #         LaggedStart(
        #             Create(g),
        #             Write(func_labels[1]),
        #             lag_ratio=0.25
        #         ),
        #         lag_ratio=0.5
        #     )
        # )
        self.slide_pause()

        # diff_planes = planes.copy().to_edge(DOWN)
        diff_planes = VGroup(*[
            NumberPlane(
                x_range=[xmin, xmax, 1],
                y_range=[-3, 4, 1],
                x_length=self.camera.frame.get_width(),
                y_length=self.camera.frame.get_height(),
                background_line_style={
                    "stroke_color": TEAL,
                    "stroke_width": 1,
                    "stroke_opacity": 0.3
                }
            ).scale(0.25) for _ in range(3)
        ]).arrange(RIGHT, buff=1).to_edge(DOWN)
        arrows = VGroup(
            *[Arrow(
                plane.get_edge_center(DOWN), diff_plane.get_edge_center(UP)
            ) for plane, diff_plane in zip(planes, diff_planes)]
        )
        arrow_labels = VGroup(
            MathTex("f'(x)=0.4x", color=interpolate_color(WHITE, c["f"], 0.5)).scale(0.5).next_to(arrows[0], RIGHT),
            MathTex("g'(x)=0.5", color=interpolate_color(WHITE, c["g"], 0.5)).scale(0.5).next_to(arrows[1], RIGHT),
            MathTex("h'(x)=0.4x+0.5", color=interpolate_color(WHITE, c["h"], 0.5)).scale(0.5).next_to(arrows[2], RIGHT),
        )
        diff_ops = VGroup(
            MathTex("+").move_to(between_mobjects(*diff_planes[:2])),
            MathTex("=").move_to(between_mobjects(*diff_planes[1:])),
        )
        # self.add(diff_planes, arrows, arrow_labels, eq_operators, diff_ops)
        self.play(
            DrawBorderThenFill(diff_planes)
        )
        self.slide_pause()
        self.play(
            FadeIn(arrows, shift=DOWN),
            FadeIn(arrow_labels, shift=DOWN)
        )
        self.slide_pause()
        self.play(
            Write(diff_ops)
        )
        self.slide_pause()

        tracker = ValueTracker(xmin)
        df = always_redraw(lambda: diff_planes[0].plot(
            lambda x: 0.4*x,
            color=arrow_labels[0].get_color(),
            x_range=[xmin, tracker.get_value()]
        ))
        dg = always_redraw(lambda: diff_planes[1].plot(
            lambda x: 0.5,
            color=arrow_labels[1].get_color(),
            x_range=[xmin, tracker.get_value()]
        ))
        dh = always_redraw(lambda: diff_planes[2].plot(
            lambda x: 0.4*x + 0.5,
            color=arrow_labels[2].get_color(),
            x_range=[xmin, tracker.get_value()]
        ))
        tangents = always_redraw(lambda: VGroup(
            *[
                plane.get_secant_slope_group(
                    x=tracker.get_value(),
                    graph=graph,
                    dx=0.01,
                    secant_line_color=RED,
                    secant_line_length=2
                ) for plane, graph in zip(planes, [f, g, h])
            ]
        ))
        moving_points = always_redraw(lambda: VGroup(
            *[
                Dot(
                    plane.c2p(tracker.get_value(), graph.underlying_function(tracker.get_value())),
                    color=RED
                ) for plane, graph in zip([*planes, *diff_planes], [f, g, h, df, dg, dh])
            ]
        ))
        self.add(df, dg, dh)  # , tangents, moving_points)
        self.play(
            Create(tangents),
            Create(moving_points)
        )
        self.slide_pause()
        self.play(
            tracker.animate.set_value(xmax),
            run_time=10
        )
        self.play(
            FadeOut(tangents),
            FadeOut(moving_points)
        )
        self.slide_pause()

    def subtraktion(self):
        c = {"f": GREEN, "g": BLUE, "h": YELLOW}
        xmin, xmax = -8, 8
        plane = NumberPlane(
            x_range=[xmin, xmax, 1],
            y_range=[-3, 9, 1],
            x_length=self.camera.frame.get_width(),
            y_length=self.camera.frame.get_height(),
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.5
            }
        )
        planes = VGroup(
            *[plane.copy().scale(0.25) for _ in range(2)],
            NumberPlane(
                x_range=[xmin, xmax, 1],
                y_range=[-9, 3, 1],
                x_length=self.camera.frame.get_width(),
                y_length=self.camera.frame.get_height(),
                background_line_style={
                    "stroke_color": TEAL,
                    "stroke_width": 1,
                    "stroke_opacity": 0.5
                }
            ).scale(0.25)
        ).arrange(RIGHT, buff=1).shift(UP)

        f = planes[0].plot(
            lambda x: 0.25 * x**2,
            color=c["f"]
        )
        g = planes[1].plot(
            lambda x: 0.5 * x**2,
            color=c["g"]
        )
        h = planes[2].plot(
            lambda x: f.underlying_function(x) - g.underlying_function(x),
            color=c["h"],
            x_range=[-7, 7]
        )
        func_labels = VGroup(
            MathTex("f(x)=0.25x^2", color=c["f"]).next_to(planes[0], UP, buff=0.1),
            MathTex("g(x)=0.5x^2", color=c["g"]).next_to(planes[1], UP, buff=0.1),
            VGroup(
                MathTex("h(x)=f(x) - g(x)", color=c["h"]),
                MathTex("h(x) = - 0.25x^2", color=c["h"]),
            ).arrange(DOWN, aligned_edge=LEFT).next_to(planes[2], UP, buff=0.1)
        ).set_z_index(3)
        lrec = get_background_rect(func_labels, buff=0)
        eq_operators = VGroup(
            MathTex("-").move_to(between_mobjects(*func_labels[:2])),
            MathTex("=").move_to(between_mobjects(func_labels[1], func_labels[2][1])),
            MathTex("-").move_to(between_mobjects(*planes[:2])),
            MathTex("=").move_to(between_mobjects(*planes[1:])),
        ).set_z_index(3)
        # self.add(planes, f, g, h, func_labels, lrec, eq_operators)
        self.add(lrec)
        self.play(
            LaggedStart(
                DrawBorderThenFill(planes),
                Create(VGroup(f, g, h)),
                Write(func_labels),
                lag_ratio=0.75
            )
        )
        self.play(
            Write(eq_operators)
        )
        self.slide_pause()

        diff_planes = VGroup(*[
            NumberPlane(
                x_range=[xmin, xmax, 1],
                y_range=[-6, 8, 1],
                x_length=self.camera.frame.get_width(),
                y_length=self.camera.frame.get_height(),
                background_line_style={
                    "stroke_color": TEAL,
                    "stroke_width": 1,
                    "stroke_opacity": 0.5
                }
            ).scale(0.25) for _ in range(3)
        ]).arrange(RIGHT, buff=1).to_edge(DOWN)
        arrows = VGroup(
            *[Arrow(
                plane.get_edge_center(DOWN), diff_plane.get_edge_center(UP)
            ) for plane, diff_plane in zip(planes, diff_planes)]
        )
        arrow_labels = VGroup(
            MathTex("f'(x)=0.5x", color=interpolate_color(WHITE, c["f"], 0.5)).scale(0.5).next_to(arrows[0], RIGHT),
            MathTex("g'(x)=x", color=interpolate_color(WHITE, c["g"], 0.5)).scale(0.5).next_to(arrows[1], RIGHT),
            MathTex("h'(x)=-0.5x", color=interpolate_color(WHITE, c["h"], 0.5)).scale(0.5).next_to(arrows[2], RIGHT),
        )
        diff_ops = VGroup(
            MathTex("-").move_to(between_mobjects(*diff_planes[:2])),
            MathTex("=").move_to(between_mobjects(*diff_planes[1:])),
        )
        # self.add(diff_planes, arrows, arrow_labels, eq_operators, diff_ops)
        self.play(
            DrawBorderThenFill(diff_planes)
        )
        self.slide_pause()
        self.play(
            FadeIn(arrows, shift=DOWN),
            FadeIn(arrow_labels, shift=DOWN)
        )
        self.slide_pause()
        self.play(
            Write(diff_ops)
        )
        self.slide_pause()

        tracker = ValueTracker(xmin)
        df = always_redraw(lambda: diff_planes[0].plot(
            lambda x: 0.5*x,
            color=arrow_labels[0].get_color(),
            x_range=[xmin, tracker.get_value()]
        ))
        dg = always_redraw(lambda: diff_planes[1].plot(
            lambda x: x,
            color=arrow_labels[1].get_color(),
            x_range=[xmin, tracker.get_value()]
        ))
        dh = always_redraw(lambda: diff_planes[2].plot(
            lambda x: -0.5*x,
            color=arrow_labels[2].get_color(),
            x_range=[xmin, tracker.get_value()]
        ))
        tangents = always_redraw(lambda: VGroup(
            *[
                plane.get_secant_slope_group(
                    x=tracker.get_value(),
                    graph=graph,
                    dx=0.01,
                    secant_line_color=RED,
                    secant_line_length=2
                ) for plane, graph in zip(planes, [f, g, h])
            ]
        ))
        moving_points = always_redraw(lambda: VGroup(
            *[
                Dot(
                    plane.c2p(tracker.get_value(), graph.underlying_function(tracker.get_value())),
                    color=RED
                ) for plane, graph in zip([*planes, *diff_planes], [f, g, h, df, dg, dh])
            ]
        ))
        self.add(df, dg, dh)  # , tangents, moving_points)
        # self.add(df, dg, dh, tangents, moving_points)
        self.play(
            Create(tangents),
            Create(moving_points)
        )
        self.slide_pause()
        self.play(
            tracker.animate.set_value(xmax),
            run_time=10
        )
        self.play(
            FadeOut(tangents),
            FadeOut(moving_points)
        )
        self.slide_pause()

    def multiplikation(self):
        c = {"f": YELLOW, "g": PINK, "h": PURE_GREEN}
        xmin, xmax = -8, 8
        plane = NumberPlane(
            x_range=[xmin, xmax, 1],
            y_range=[-3, 9, 1],
            x_length=self.camera.frame.get_width(),
            y_length=self.camera.frame.get_height(),
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.5
            }
        )
        fg_planes = VGroup(*[
            plane.copy().scale(0.4) for _ in range(2)
        ]).arrange(DOWN).to_edge(LEFT)
        h_plane = plane.copy().scale(0.4).to_edge(RIGHT).shift(DOWN)
        prects = VGroup(*[
            get_background_rect(
                p, stroke_colour=c[col], stroke_width=0.5, buff=0.0
            ) for p, col in zip([*fg_planes, h_plane], ["f", "g", "h"])
        ])

        f = fg_planes[0].plot(
            lambda x: 0.5 * x + 3,
            color=c["f"]
        )
        g = fg_planes[1].plot(
            lambda x: -0.7 * x + 3,
            color=c["g"]
        )
        h = h_plane.plot(
            lambda x: f.underlying_function(x) * g.underlying_function(x),
            color=c["h"]
        )
        self.play(
            LaggedStart(
                DrawBorderThenFill(VGroup(*fg_planes, h_plane)),
                Create(f),
                Create(g),
                DrawBorderThenFill(prects),
                lag_ratio=0.33
            ),
            run_time=1
        )
        self.slide_pause()
        # self.add(fg_planes, f, g, h, h_plane, prects)
        # self.remove(h)

        n_lines = 20
        flines = VGroup(*[
            Line(
                start=fg_planes[0].c2p(i, 0),
                end=fg_planes[0].c2p(i, f.underlying_function(i)),
                stroke_color=color_gradient(
                    [WHITE, f.get_color()] if f.underlying_function(i) > 0 else [f.get_color(), WHITE],
                    2
                )
            ) for i in np.linspace(xmin, xmax, n_lines)
        ])
        glines = VGroup(*[
            Line(
                start=fg_planes[1].c2p(i, 0),
                end=fg_planes[1].c2p(i, g.underlying_function(i)),
                stroke_color=color_gradient(
                    [WHITE, g.get_color()] if g.underlying_function(i) > 0 else [g.get_color(), WHITE],
                    2
                )
            ) for i in np.linspace(xmin, xmax, n_lines)
        ])
        # self.add(flines, glines)
        self.play(
            LaggedStart(
                LaggedStart(
                    *[Create(fl) for fl in flines], lag_ratio=0.1
                ),
                LaggedStart(
                    *[Create(gl) for gl in glines], lag_ratio=0.1
                ),
                lag_ratio=0.5
            ),
            run_time=1
        )
        self.slide_pause()

        hlines = VGroup(*[
            Line(
                start=h_plane.c2p(i, 0),
                end=h_plane.c2p(i, h.underlying_function(i)),
                stroke_color=color_gradient(
                    [WHITE, h.get_color()] if h.underlying_function(i) > 0 else [h.get_color(), WHITE],
                    2
                )
            ) for i in np.linspace(xmin, xmax, n_lines)
        ])
        i = 0
        for fl, gl, hl in zip(flines, glines, hlines):
            eq = VGroup(
                fl.copy(), MathTex(r"\times"), gl.copy(), MathTex(r"="), hl.copy()
            # ).arrange(RIGHT, aligned_edge=DOWN).next_to(h_plane, UP)
            ).arrange(RIGHT).next_to(h_plane, UP)
            self.play(
                TransformMatchingShapes(
                    VGroup(fl.copy(), gl.copy()),
                    eq[:3]
                ),
                run_time=0.2**(i/len(hlines))
            )
            self.play(
                FadeIn(eq[3:]),
                run_time=0.2**(i/len(hlines))
            )
            self.play(
                TransformMatchingShapes(
                    eq[-1].copy(),
                    hl
                ),
                run_time=0.2**(i/len(hlines))
            )
            self.play(
                FadeOut(eq),
                run_time=0.2**(i/len(hlines))
            )
            i += 1
            # break
        self.slide_pause()

        self.play(
            Create(h)
        )


