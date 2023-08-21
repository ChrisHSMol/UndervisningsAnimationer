import sys
sys.path.append("../")
from manim import *
from helpers import *

slides = True
if slides:
    from manim_slides import Slide


class TrigFunktioner(MovingCameraScene, Slide if slides else None):
    def construct(self):
        self.slide_pause()
        basis = self.enhedscirkel(banimation=True)
        self.trig_funktioner(basis)
        self.sin_og_cos_identiteter(basis)
        self.wait(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def enhedscirkel(self, banimation=True):
        scene_marker("Enhedscirkel")
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

        if banimation:
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
        edge_point = always_redraw(lambda: VGroup(
            Dot(radius=0.02, point=unit_circle.point_at_angle(theta.get_value()), color=GREEN).set_z_index(5),
            MathTex("P", font_size=8, color=GREEN).move_to(Circle(1.1).point_at_angle(theta.get_value())).set_z_index(5)
        ))
        lines_opa = ValueTracker(1)
        hline = always_redraw(lambda: Line(
            start=plane.c2p(0, edge_point[0].get_y()), end=edge_point[0].get_center(), color=BLUE, stroke_width=1,
            stroke_opacity=lines_opa.get_value()
        ).set_z_index(radius_line.get_z_index() - 1))
        vline = always_redraw(lambda: Line(
            start=plane.c2p(edge_point[0].get_x(), 0), end=edge_point[0].get_center(), color=YELLOW, stroke_width=1,
            stroke_opacity=lines_opa.get_value()
        ).set_z_index(radius_line.get_z_index() - 1))

        if banimation:
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

        axis_labels = VGroup(*[
            MathTex(lab, color=c, font_size=8)
                             .next_to(axis, cor, buff=0.05)
                             .shift(0.15*d)
                             .set_z_index(unit_circle.get_z_index())
            for lab, axis, cor, d, c in zip(["x", "y"], plane[2:4], [DR, UL], [LEFT, DOWN], [YELLOW, BLUE])
        ])
        if banimation:
            self.play(
                plane[2].animate.set_color(YELLOW).set(stroke_width=0.75),
                plane[3].animate.set_color(BLUE).set(stroke_width=0.75),
                Write(axis_labels),
                DrawBorderThenFill(edge_point)
            )
            self.add(hline, vline)
            self.slide_pause()

            self.play(
                theta.animate.set_value(2*TAU),
                run_time=TAU
            )
            theta.set_value(0)
            self.slide_pause()

        coords_cardinal = always_redraw(lambda:
            VGroup(
                DecimalNumber(
                    number=edge_point[0].get_x(),
                    num_decimal_places=2,
                    color=vline.get_color(),
                    include_sign=True,  # edge_point.get_x() < 0,
                    font_size=10,
                    fill_opacity=lines_opa.get_value(),
                ).set_z_index(vline.get_z_index()).next_to(
                    vline.get_start(), UP if edge_point[0].get_y() < 0 else DOWN, buff=0.05
                ),
                DecimalNumber(
                    number=edge_point[0].get_y(),
                    num_decimal_places=2,
                    color=hline.get_color(),
                    include_sign=True,  # edge_point.get_y() < 0,
                    font_size=10,
                    fill_opacity=lines_opa.get_value()
                ).set_z_index(hline.get_z_index()).next_to(
                    hline.get_start(), RIGHT if edge_point[0].get_x() <= 0 else LEFT, buff=0.05
                )
            )
        )
        if banimation:
            self.play(
                Write(coords_cardinal)
            )
            self.play(
                theta.animate.set_value(9/8*TAU),
                run_time=2*TAU
            )
            self.slide_pause()

        point_coords = always_redraw(lambda:
            # MathTex(
            #     rf"({coords_cardinal[0].get_value():.2f}; {coords_cardinal[1].get_value():.2f})", font_size=8
            # ).set_z_index(unit_circle.get_z_index()).move_to(Circle(1.1).point_at_angle(theta.get_value()))
            VGroup(
                MathTex("P", font_size=10, color=GREEN),
                MathTex("(", font_size=10),
                MathTex(f"{edge_point[0].get_x():.2f}", color=vline.get_color(), font_size=10),
                MathTex(";", font_size=10),
                MathTex(f"{edge_point[0].get_y():.2f}", color=hline.get_color(), font_size=10),
                MathTex(")", font_size=10),
            ).arrange(RIGHT, buff=0.025).set_z_index(vline.get_z_index()).move_to(
                # Circle(1.3).point_at_angle(theta.get_value())
                plane.c2p(1.0, 1.1)
            )
        )
        if banimation:
            self.play(
                # TransformMatchingShapes(
                #     coords_cardinal.copy(), point_coords
                # ),
                # TransformMatchingShapes(
                #     VGroup(*coords_cardinal.copy(), edge_point[1]), point_coords
                # ),
                FadeIn(point_coords),
                lines_opa.animate.set_value(0.25),
                run_time=2
            )
            self.slide_pause()

            self.play(
                theta.animate.set_value(PI/4),
                run_time=10
            )
            self.slide_pause()

        vek_bue = always_redraw(lambda:
            Arc(
                radius=0.15,
                start_angle=0,
                angle=theta.get_value(),
                color=RED,
                stroke_width=1
            ).set_z_index(radius_line.get_z_index())
        )
        vinkel = always_redraw(lambda:
            MathTex(
                rf"{theta.get_value() * 180/PI:.1f}^\circ",
                color=vek_bue.get_color(), font_size=10
            # ).next_to(vek_bue, RIGHT)
            ).move_to(Circle(0.35).point_at_angle(theta.get_value() - PI/8)).set_z_index(radius_line.get_z_index())
        )
        if banimation:
            self.play(
                *[FadeOut(m) for m in [hline, vline, coords_cardinal]],
                LaggedStart(
                    Create(vek_bue),
                    Write(vinkel),
                    lag_ratio=0.5
                ),
                run_time=2
            )
            for angle in [PI/2, PI, PI/5]:
                self.play(
                    theta.animate.set_value(angle),
                    run_time=2
                )
                self.wait(0.5)
            self.slide_pause()

            self.play(
                *[FadeOut(m) for m in self.mobjects if m not in [unit_circle, plane, plane_rec]],
                FadeOut(radius_line)
            )
        else:
            plane[2].set_color(YELLOW).set(stroke_width=0.75)
            plane[3].set_color(BLUE).set(stroke_width=0.75)
            self.camera.frame.set(height=1.1 * plane.height).move_to(plane.c2p(1, 0))
            self.add(unit_circle, plane, plane_rec)
        return VGroup(unit_circle, plane, plane_rec)

    def trig_funktioner(self, basis):
        scene_marker("Trigonometriske grafer")
        unit_circle, plane_circle, plane_rec = basis
        # unit_circle = Circle(radius=1, color=WHITE).to_edge(UL).set_z_index(2)
        # circle_plane = NumberPlane(
        #     x_range=[-1.1, 1.1, 0.2],
        #     y_range=[-1.1, 1.1, 0.2],
        #     x_length=2.2*unit_circle.radius,
        #     y_length=2.2*unit_circle.radius,
        #     background_line_style={
        #         "stroke_color": TEAL,
        #         "stroke_width": 1,
        #         "stroke_opacity": 0.1
        #     }
        # ).set_z_index(1).move_to(unit_circle)

        sin_plane = NumberPlane(
            x_range=[0, 6*PI, 1],
            y_range=[-1.5, 1.5, 0.25],
            x_length=1.5*PI,
            y_length=3*unit_circle.radius,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.4
            }
        ).set_z_index(1).next_to(plane_circle, RIGHT)
        cos_plane = NumberPlane(
            x_range=[0, 6*PI, 1],
            y_range=[-1.5, 1.5, 0.25],
            x_length=1.5*PI,
            y_length=3*unit_circle.radius,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.4
            }
        ).rotate(-PI/2).set_z_index(1).next_to(plane_circle, DOWN)

        sin_plane_rec = get_background_rect(
            sin_plane, buff=0, stroke_colour=plane_circle[3].get_color(), fill_opacity=0
        )
        cos_plane_rec = get_background_rect(
            cos_plane, buff=0, stroke_colour=plane_circle[2].get_color(), fill_opacity=0
        )
        cir_plane_rect = get_background_rect(
            plane_circle, buff=0, stroke_colour=color_gradient([sin_plane[3].get_color(), cos_plane[3].get_color()], 8)
        ).set_z_index(1)
        self.play(
            self.camera.frame.animate.set(height=3*PI).shift(1*PI * DR + 2 * RIGHT),
            plane_circle[2].animate.set(stroke_width=2),
            plane_circle[3].animate.set(stroke_width=2),
            unit_circle.animate.set(stroke_width=2),
            LaggedStart(
                DrawBorderThenFill(cos_plane),
                Create(cos_plane_rec, run_time=0.25),
                lag_ratio=0.5
            ),
            LaggedStart(
                DrawBorderThenFill(sin_plane),
                Create(sin_plane_rec, run_time=0.25),
                lag_ratio=0.5
            ),
            run_time=2
        )

        time_tracker = ValueTracker(0)
        moving_dot = always_redraw(lambda:
            Dot(
                unit_circle.point_at_angle(time_tracker.get_value()),
                color=GREEN
            ).set_z_index(5)
        )
        lines = always_redraw(lambda:
            VGroup(
                Line(
                    start=moving_dot.get_center(),
                    end=sin_plane.c2p(0, np.sin(time_tracker.get_value())),
                    color=BLUE
                ).set_z_index(4),
                Line(
                    start=moving_dot.get_center(),
                    end=cos_plane.c2p(0, np.cos(time_tracker.get_value())),
                    color=YELLOW
                ).set_z_index(4)
            )
        )
        sin_plot = always_redraw(lambda:
            sin_plane.plot(
                lambda x: np.sin(time_tracker.get_value() - x),
                color=BLUE,
                x_range=[0, min(6*PI, time_tracker.get_value())],
                z_index=sin_plane.get_z_index() + 1
            ).set_z_index(sin_plane.get_z_index() + 1)
        )
        cos_plot = always_redraw(lambda:
            cos_plane.plot(
                lambda x: np.cos(time_tracker.get_value() - x),
                color=YELLOW,
                x_range=[0, min(6*PI, time_tracker.get_value())],
                z_index=cos_plane.get_z_index() + 1
            ).set_z_index(cos_plane.get_z_index() + 1)
        )
        self.add(sin_plot, cos_plot)
        self.play(
            LaggedStart(
                Create(lines[0]),
                Create(lines[1]),
                DrawBorderThenFill(moving_dot),
                lag_ratio=0.5
            ),
            run_time=2
        )
        self.add(lines)
        target_time = 10*PI
        self.play(
            time_tracker.animate.set_value(target_time),
            run_time=target_time,
            rate_func=rate_functions.linear
        )
        self.slide_pause()

        sin_plane_copy = always_redraw(lambda: sin_plane.copy().scale(1.5).next_to(cos_plane, RIGHT))
        cos_plane_copy = always_redraw(lambda: cos_plane.copy().rotate(PI/2).scale(1.5).next_to(cos_plane, RIGHT))
        sin_plot_copy = always_redraw(lambda: sin_plot.copy().scale(1.5).next_to(cos_plane, RIGHT))
        cos_plot_copy = always_redraw(lambda: cos_plot.copy().rotate(PI/2).scale(1.5).next_to(cos_plane, RIGHT))
        sin_cos_plane_copy_rect = get_background_rect(
            sin_plane_copy, buff=0, fill_opacity=0,
            stroke_colour=color_gradient([sin_plot.get_color(), cos_plot.get_color()], 100)
        )
        cmap = {
            r"\sin": sin_plot.get_color(),
            r"\cos": cos_plot.get_color(),
        }
        fkt_labels = VGroup(
            MathTex("f(x)=", r"\sin", "(x)").set_color_by_tex_to_color_map(cmap),
            MathTex("g(x)=", r"\cos", "(x)").set_color_by_tex_to_color_map(cmap),
        ).arrange(DOWN, aligned_edge=LEFT).next_to(sin_cos_plane_copy_rect, RIGHT, aligned_edge=UP)
        self.play(
            LaggedStart(
                AnimationGroup(
                    ReplacementTransform(sin_plane.copy(), sin_plane_copy),
                    ReplacementTransform(sin_plot.copy(), sin_plot_copy),
                ),
                AnimationGroup(
                    ReplacementTransform(cos_plane.copy(), cos_plane_copy),
                    ReplacementTransform(cos_plot.copy(), cos_plot_copy),
                ),
                Create(sin_cos_plane_copy_rect, run_time=0.25),
                Write(fkt_labels),
                lag_ratio=0.9
            ),
            run_time=4
        )
        self.play(
            time_tracker.animate.set_value(14*PI),
            run_time=4*PI
        )
        self.slide_pause()

        self.play(
            *[FadeOut(m) for m in self.mobjects if m not in [unit_circle, plane_circle, plane_rec]],
            FadeOut(sin_plot),
            FadeOut(cos_plot),
            FadeOut(sin_plot_copy),
            FadeOut(cos_plot_copy),
            self.camera.frame.animate.set(height=1.1 * plane_circle.height).move_to(plane_circle.c2p(1, 0)),
            unit_circle.animate.set(stroke_width=0.75),
            run_time=2
        )

    def sin_og_cos_identiteter(self, basis):
        scene_marker("Enhedscirkel og sin(x), cos(x)")
        unit_circle, plane, plane_rec = basis

        theta = ValueTracker(PI/5)  # Rad

        radius_line = always_redraw(lambda: Line(
            start=plane.c2p(0, 0), end=unit_circle.point_at_angle(theta.get_value()), color=WHITE, stroke_width=1.5
        ).set_z_index(5))
        edge_point = always_redraw(lambda: VGroup(
            Dot(radius=0.02, point=unit_circle.point_at_angle(theta.get_value()), color=GREEN).set_z_index(5),
            MathTex("P", font_size=8, color=GREEN).move_to(Circle(1.1).point_at_angle(theta.get_value())).set_z_index(5)
        ))

        point_coords = always_redraw(lambda:
            VGroup(
                MathTex("P", font_size=10, color=GREEN),
                MathTex("(", font_size=10),
                MathTex(f"{edge_point[0].get_x():.2f}", color=plane[2].get_color(), font_size=10),
                MathTex(";", font_size=10),
                MathTex(f"{edge_point[0].get_y():.2f}", color=plane[3].get_color(), font_size=10),
                MathTex(")", font_size=10),
            ).arrange(RIGHT, buff=0.025).set_z_index(edge_point[0].get_z_index()).move_to(plane.c2p(1.0, 1.1))
        )

        vek_bue = always_redraw(lambda:
            Arc(
                radius=0.15,
                start_angle=0,
                angle=theta.get_value(),
                color=RED,
                stroke_width=1
            ).set_z_index(radius_line.get_z_index())
        )
        vinkel = always_redraw(lambda:
            MathTex(
                rf"{theta.get_value() * 180/PI:.1f}^\circ",
                color=vek_bue.get_color(), font_size=10
            ).move_to(Circle(0.35).point_at_angle(theta.get_value() - PI/8)).set_z_index(radius_line.get_z_index())
        )

        self.play(
            LaggedStart(
                Create(radius_line),
                Create(vek_bue),
                Write(vinkel),
                DrawBorderThenFill(edge_point),
                Write(point_coords),
                lag_ratio=0.2
            ),
            run_time=2
        )
        self.slide_pause()

        vinkler = [0, PI/6, PI/4, PI/2, 3*PI/4, PI, 3*PI/2, 15*PI/8]
        tabel_struktur = VGroup(*[
            VGroup(*[
                Rectangle(
                    height=0.25, stroke_color=WHITE, stroke_width=0.75, fill_opacity=0.15,
                    width=0.625, fill_color=c if i else BLACK
                ) for c in [vek_bue.get_color(), plane[2].get_color(), plane[3].get_color()]
            ]).arrange(RIGHT, buff=0) for i in range(len(vinkler) + 1)
        ]).arrange(DOWN, buff=0).next_to(plane_rec, RIGHT)
        tabel_overskrifter = VGroup(
            Tex(r"Vinkel, $\theta$", color=vek_bue.get_color(), font_size=12).move_to(tabel_struktur[0][0]),
            MathTex(r"\cos(\theta)", color=plane[2].get_color(), font_size=12).move_to(tabel_struktur[0][1]),
            MathTex(r"\sin(\theta)", color=plane[3].get_color(), font_size=12).move_to(tabel_struktur[0][2]),
        )
        # tabel_tekst = VGroup(
        #     VGroup(*[
        #         DecimalNumber(
        #             v * 180/PI, num_decimal_places=0, font_size=12
        #         ).move_to(tabel_struktur[i + 1][0]) for i, v in enumerate(vinkler)
        #     ]),
        #     VGroup(*[
        #         DecimalNumber(
        #             np.cos(v), num_decimal_places=2, font_size=12
        #         ).move_to(tabel_struktur[i + 1][1]) for i, v in enumerate(vinkler)
        #     ]),
        #     VGroup(*[
        #         DecimalNumber(
        #             np.sin(v), num_decimal_places=2, font_size=12
        #         ).move_to(tabel_struktur[i + 1][2]) for i, v in enumerate(vinkler)
        #     ])
        # )
        tabel_tekst = VGroup(
            VGroup(*[
                MathTex(
                    rf"{v*180/PI:.1f}^\circ", font_size=12
                ).next_to(tabel_struktur[i + 1][0], LEFT, buff=0.1).shift(tabel_struktur[i + 1][0].width * RIGHT)
                for i, v in enumerate(vinkler)
            ]),
            VGroup(*[
                DecimalNumber(
                    np.cos(v), num_decimal_places=2, font_size=12
                ).next_to(tabel_struktur[i + 1][1], LEFT, buff=0.1).shift(tabel_struktur[i + 1][1].width * RIGHT)
                for i, v in enumerate(vinkler)
            ]),
            VGroup(*[
                DecimalNumber(
                    np.sin(v), num_decimal_places=2, font_size=12
                ).next_to(tabel_struktur[i + 1][2], LEFT, buff=0.1).shift(tabel_struktur[i + 1][2].width * RIGHT)
                for i, v in enumerate(vinkler)
            ])
        )
        # self.add(tabel_overskrifter, tabel_struktur)
        self.play(
            LaggedStart(
                Write(tabel_overskrifter, lag_ratio=0.25),
                DrawBorderThenFill(tabel_struktur, lag_ratio=0.3),
                lag_ratio=0.75
            ),
            run_time=4
        )
        self.slide_pause()

        for j, v in enumerate(vinkler):
            self.play(
                theta.animate.set_value(v),
                run_time=np.abs(v - theta.get_value()),
                # run_time=0.25,
                # rate_func=rate_functions.linear
            )
            self.wait()
            self.play(
                LaggedStart(
                    ReplacementTransform(
                        vinkel.copy(), tabel_tekst[0][j]
                    ),
                    ReplacementTransform(
                        point_coords[2].copy(), tabel_tekst[1][j]
                    ),
                    ReplacementTransform(
                        point_coords[4].copy(), tabel_tekst[2][j]
                    ),
                    lag_ratio=0.9
                ),
                run_time=3
            )
            self.wait()
        self.slide_pause()

        self.play(
            theta.animate.set_value(0),
            Uncreate(tabel_struktur, lag_ratio=0.25),
            Unwrite(tabel_overskrifter, lag_ratio=0.3, reverse=False),
            Unwrite(tabel_tekst, lag_ratio=0.25, reverse=False),
            run_time=3
        )
        self.play(
            Unwrite(vinkel),
            *[Uncreate(m, lag_ratio=0.1) for m in [unit_circle, plane_rec, plane, edge_point, vek_bue, radius_line]],
            Unwrite(point_coords, reverse=False),
            run_time=2
        )
        self.remove(point_coords)
