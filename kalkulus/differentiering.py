from manim import *
import sys
sys.path.append("../")
from helpers import *

slides = True
if slides:
    from manim_slides import Slide


class IntroTilDiff(MovingCameraScene, Slide if slides else Scene):
    def construct(self):
        self.udledning_af_forskrift()
        self.slide_pause(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def parabel(self, x, a=1.0, b=0.0):
        return a * x**2 + b

    def udledning_af_forskrift(self):
        pwidth = 16
        pheight = 9 * 16 / pwidth
        pxshift = 2
        pyshift = 20
        plane = NumberPlane(
            x_range=[-pwidth/2 + pxshift, pwidth/2 + pxshift, 1],
            y_range=[-pheight*10/2 + pyshift, pheight*10/2 + pyshift, 10],
            x_length=pwidth,
            y_length=pheight,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.3
            }
        )
        graph = plane.plot(
            lambda x: self.parabel(x),
            x_range=[-1, 15]
        )
        self.play(
            LaggedStart(
                DrawBorderThenFill(plane),
                Create(graph),
                lag_ratio=0.75
            )
        )
        self.slide_pause()

        xvals = np.linspace(0, 6.01, 7)
        yvals = self.parabel(xvals)
        dotcols = [interpolate_color(YELLOW, RED, i/(len(xvals)-1)) for i in range(len(xvals))]
        dots = VGroup(
            *[
                Dot(
                    point=plane.c2p(x, y),
                    color=color
                ).set_z_index(4) for x, y, color in zip(xvals, yvals, dotcols)
            ]
        )
        self.play(
            Create(dots)
        )
        self.slide_pause()

        coords_title = VGroup(
            MathTex("x"), MathTex("y")
        ).arrange(RIGHT, buff=1).to_edge(UL).set_z_index(4)
        coords = VGroup(*[
            # MathTex(f"({x:.0f}, {y:.0f})", color=c) for x, y, c in zip(xvals, yvals, dotcols)
            VGroup(
                DecimalNumber(x, color=c, num_decimal_places=1),
                DecimalNumber(y, color=c, num_decimal_places=1)
            ).arrange(RIGHT, buff=0.7) for x, y, c in zip(xvals, yvals, dotcols)
        ]).arrange(UP, aligned_edge=LEFT).next_to(coords_title, DOWN, aligned_edge=LEFT).set_z_index(4)
        brect1 = get_background_rect(VGroup(coords_title, coords))
        self.play(
            Write(coords_title),
            *[
                ReplacementTransform(
                    d.copy(),
                    c
                ) for d, c in zip(dots, coords)
            ],
            FadeIn(brect1)
        )
        self.slide_pause()

        brace = Brace(coords, RIGHT).set_z_index(4).set_color(color_gradient([dotcols[-1], dotcols[0]], len(xvals)))
        forskrift = MathTex("f(x)=x^2").set_z_index(4).next_to(brace)
        brect2 = get_background_rect(VGroup(coords, brace, forskrift).set_z_index(4))
        self.play(
            LaggedStart(
                Create(brace),
                Write(forskrift),
                lag_ratio=0.8
            ),
            ReplacementTransform(brect1, brect2)
        )
        self.slide_pause()

        self.play(
            forskrift.animate.move_to(plane.c2p(5, self.parabel(5)*1.75)),
            *[FadeOut(m) for m in [coords, brace, brect1, brect2, coords_title]]
        )
        self.slide_pause()

        x_tracker = ValueTracker(0.0)
        tangent_line = always_redraw(
            lambda: plane.get_secant_slope_group(
                x=x_tracker.get_value(),
                graph=graph,
                dx=0.01,
                secant_line_color=BLUE,
                secant_line_length=4
            ).set_z_index(5)
        )
        x_dot = always_redraw(lambda:
            Dot(
                plane.c2p(x_tracker.get_value(), self.parabel(x_tracker.get_value())),
                color=BLUE
            ).set_z_index(5)
        )
        self.play(
            Create(tangent_line),
            Create(x_dot)
        )
        self.play(
            x_tracker.animate.set_value(6),
            run_time=5
        )
        self.play(x_tracker.animate.set_value(0))
        self.slide_pause()

        self.camera.frame.save_state()
        self.play(
            self.camera.frame.animate.set(
                width=4
            ).move_to(dots[0]),
            run_time=2
        )

        slopes = VGroup(*[
            MathTex(
                f"{2*plane.p2c(d.get_center())[0]:.1f}",
                color=d.get_color(),
                font_size=16
            ).set_z_index(5).next_to(d, DOWN, buff=0.1) for d in dots
        ])
        pictures = VGroup(*[
            get_background_rect(slope, fill_color=GRAY, buff=0.05) for slope in slopes
        ])
        rolling_slope = always_redraw(lambda:
            MathTex(
                f"Hældning={2*x_tracker.get_value():.1f}",
                color=BLUE,
                font_size=16
            ).set_z_inddex(slopes[0].get_z_index() + 2).next_to(x_dot, DOWN, buff=0.1).shift(LEFT * 0.49)
        )
        self.play(
            Write(rolling_slope)
        )
        self.slide_pause()

        self.play(
            FadeOut(pictures[0]),
            FadeIn(slopes[0], run_time=0.01)
        )
        self.slide_pause()

        for i in np.arange(len(xvals) - 1) + 1:
            self.play(
                self.camera.frame.animate.move_to(dots[i]),
                x_tracker.animate.set_value(i),
                run_time=6
            )
            self.play(
                FadeOut(pictures[i]),
                FadeIn(slopes[i], run_time=0.01)
            )

        self.play(
            Restore(self.camera.frame),
            FadeOut(rolling_slope)
        )

        coords_title = VGroup(
            MathTex("x"), Tex("Hældning")
        ).arrange(RIGHT, buff=1).to_edge(UL).set_z_index(4)
        coords = VGroup(*[
            VGroup(
                DecimalNumber(x, color=c, num_decimal_places=1),
                DecimalNumber(2*x, color=c, num_decimal_places=1)
            ).arrange(RIGHT, buff=0.7) for x, c in zip(xvals, dotcols)
        ]).arrange(UP, aligned_edge=LEFT).next_to(coords_title, DOWN, aligned_edge=LEFT).set_z_index(4)
        brect1 = get_background_rect(VGroup(coords_title, coords))
        self.play(
            Write(coords_title),
            *[
                ReplacementTransform(
                    d.copy(),
                    c
                ) for d, c in zip(slopes, coords)
            ],
            FadeIn(brect1)
        )
        self.slide_pause()

        brace = Brace(coords, RIGHT).set_z_index(4).set_color(color_gradient([dotcols[-1], dotcols[0]], len(xvals)))
        forskrift = MathTex("f'(x)=2x").set_z_index(4).next_to(brace)
        brect2 = get_background_rect(VGroup(coords, brace, forskrift).set_z_index(4))
        self.play(
            LaggedStart(
                Create(brace),
                Write(forskrift),
                lag_ratio=0.8
            ),
            ReplacementTransform(brect1, brect2)
        )
        self.slide_pause()


class TreTrinsRegel(MovingCameraScene, Slide if slides else Scene):
    def construct(self):
        self.tretrin()
        self.slide_pause(5)

    def distance(self, x1, dx, func):
        # return ((x2 - x1)**2 + (y2 - y1)**2)**0.5
        return (dx**2 + (func(x1 + dx) - func(x1))**2)**0.5

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def tretrin(self):
        pwidth = 16
        pheight = 9 * 16 / pwidth
        pxshift = 5
        pyshift = 15
        plane = NumberPlane(
            x_range=[-pwidth/2 + pxshift, pwidth/2 + pxshift, 1],
            y_range=[-pheight*10 + pyshift, pheight*10 + pyshift, 20],
            x_length=pwidth,
            y_length=pheight,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.3
            }
        )
        graph_stroke = ValueTracker(2)
        graph = always_redraw(lambda: plane.plot(
            lambda x: -10 * (x - 1) * (x - 4) * (x - 5) + 50,
            color=YELLOW,
            stroke_width=graph_stroke.get_value()
        ))
        self.play(
            LaggedStart(
                DrawBorderThenFill(plane),
                Create(graph, run_time=3),
                lag_ratio=0.75
            )
        )
        self.slide_pause()

        x_tracker = ValueTracker(3)
        dx_tracker = ValueTracker(0.0)
        lines_tracker = ValueTracker(1.0)
        xlines = always_redraw(lambda:
            VGroup(
                DashedLine(
                    start=plane.c2p(x_tracker.get_value(), 0),
                    end=plane.c2p(
                        x_tracker.get_value(),
                        graph.underlying_function(x_tracker.get_value()),
                    ),
                    stroke_width=graph_stroke.get_value(),
                    stroke_opacity=lines_tracker.get_value()
                ),
                DashedLine(
                    start=plane.c2p(x_tracker.get_value() + dx_tracker.get_value(), 0),
                    end=plane.c2p(
                        x_tracker.get_value() + dx_tracker.get_value(),
                        graph.underlying_function(x_tracker.get_value() + dx_tracker.get_value())
                    ),
                    stroke_width=4 if np.abs(dx_tracker.get_value()) > 1 else np.exp(0.5*dx_tracker.get_value()),
                    stroke_opacity=lines_tracker.get_value()
                )
            )
        )
        ylines = always_redraw(lambda:
            VGroup(
                DashedLine(
                    start=plane.c2p(0, graph.underlying_function(x_tracker.get_value())),
                    end=plane.c2p(
                        x_tracker.get_value(),
                        graph.underlying_function(x_tracker.get_value())
                    ),
                    stroke_width=graph_stroke.get_value(),
                    stroke_opacity=lines_tracker.get_value()
                ),
                DashedLine(
                    start=plane.c2p(0, graph.underlying_function(x_tracker.get_value() + dx_tracker.get_value())),
                    end=plane.c2p(
                        x_tracker.get_value() + dx_tracker.get_value(),
                        graph.underlying_function(x_tracker.get_value() + dx_tracker.get_value()),
                    ),
                    stroke_width=4 if np.abs(dx_tracker.get_value()) > 1 else np.exp(0.5*dx_tracker.get_value()),
                    stroke_opacity=lines_tracker.get_value()
                )
            )
        )
        dx_brace = always_redraw(lambda:
            BraceBetweenPoints(
                plane.c2p(x_tracker.get_value(), 0),
                plane.c2p(x_tracker.get_value() + dx_tracker.get_value(), 0),
                direction=DOWN
            )
        )
        dx_label = always_redraw(lambda:
            MathTex(r"h").next_to(dx_brace, DOWN)
        )
        labels = always_redraw(lambda:
            VGroup(
                MathTex("x_0", font_size=34).next_to(xlines[0], DOWN),
                MathTex(r"x_0 + h", font_size=min(17*dx_tracker.get_value() + 1, 34)).next_to(xlines[1], DOWN),
                MathTex("f(x_0)", font_size=34).next_to(ylines[0], LEFT),
                MathTex(r"f(x_0 + h)", font_size=min(17*dx_tracker.get_value() + 1, 34)).next_to(ylines[1], LEFT),
            )
        )

        dots = always_redraw(lambda: VGroup(
            Dot(
                plane.c2p(
                    x_tracker.get_value(), graph.underlying_function(x_tracker.get_value())
                ),
                color=RED
            ).set_z_index(3),
            Dot(
                plane.c2p(
                    x_tracker.get_value() + dx_tracker.get_value(),
                    graph.underlying_function(x_tracker.get_value() + dx_tracker.get_value())
                ),
                color=RED
            ).set_z_index(3)
        ))
        self.play(
            Create(xlines),
            Create(ylines),
            Create(dots),
            Write(labels, run_time=0.25),
        )
        self.slide_pause()
        self.play(
            dx_tracker.animate.set_value(2.0)
        )
        self.slide_pause()

        secant_line = always_redraw(lambda:
            plane.get_secant_slope_group(
                x=x_tracker.get_value(),
                graph=graph,
                dx=dx_tracker.get_value(),
                secant_line_color=RED if np.abs(dx_tracker.get_value()) > 1E-4 else GREEN,
                secant_line_length=5,
                include_dx_line=False,
                include_dy_line=False,
            ).set_style(stroke_width=graph_stroke.get_value())
        )
        self.play(
            Create(secant_line)
        ),
        self.play(
            dx_tracker.animate.set_value(0.0001),
            run_time=10
        )
        self.slide_pause()

        tretrinsregel_trin = VGroup(
            Text("Trin 1: Find funktionstilvæksten", t2c={"Trin 1": RED, "funktionstilvæksten": BLUE_A}).set_z_index(plane.get_z_index() + 2),
            Text("Trin 2: Find differenskvotienten", t2c={"Trin 2": RED, "differenskvotienten": BLUE_B}).set_z_index(plane.get_z_index() + 2),
            Text("Trin 3: Find differentialkvotienten", t2c={"Trin 3": RED, "differentialkvotienten": BLUE_C}).set_z_index(plane.get_z_index() + 2),
        ).scale(0.5).arrange(DOWN, aligned_edge=LEFT, buff=1.25).to_edge(UR)
        tretrinsregel_ligninger = VGroup(
            MathTex(
                r"\Delta y", "=", rf"f(x_0 + h)", "-", "f(x_0)"
            ).set_color_by_tex_to_color_map(
                {r"\Delta y": BLUE_A}
            ).set_z_index(plane.get_z_index() + 2).scale(0.5).next_to(tretrinsregel_trin[0], DOWN, aligned_edge=LEFT),
            MathTex(
                r"\frac{\Delta y}{h}", "=", r"\frac{f(x_0 + h) - f(x_0)}{h}"
            ).set_color_by_tex_to_color_map(
                {r"\Delta y": BLUE_B}
            ).set_z_index(plane.get_z_index() + 2).scale(0.5).next_to(tretrinsregel_trin[1], DOWN, aligned_edge=LEFT),
            MathTex(
                r"f'(x_0)", "=" r"\lim_{h \rightarrow 0}",
                r"\left(\frac{f(x_0 + h) - f(x_0)}{h}\right)"
            ).set_color_by_tex_to_color_map(
                {r"'": BLUE_C}
            ).set_z_index(plane.get_z_index() + 2).scale(0.5).next_to(tretrinsregel_trin[2], DOWN, aligned_edge=LEFT)
        )
        self.play(
            FadeOut(secant_line),
            Write(tretrinsregel_trin[0])
        )
        self.play(
            dx_tracker.animate.set_value(2.0)
        )
        self.slide_pause()

        self.play(
            TransformMatchingTex(
                labels[-2:].copy(),
                tretrinsregel_ligninger[0],
                transform_mismatches=True
            )
        )
        for label, ligning in zip(labels[-2:], [tretrinsregel_ligninger[0][4], tretrinsregel_ligninger[0][2]]):
            self.play(
                *[
                    Circumscribe(
                        m, fade_out=True, color=tretrinsregel_trin[0][-1].get_color()
                    ) for m in [label, ligning]
                ],
                run_time=2
            )
        self.slide_pause()

        secant_line = always_redraw(lambda:
            plane.get_secant_slope_group(
                x=x_tracker.get_value(),
                graph=graph,
                dx=dx_tracker.get_value(),
                secant_line_color=RED if np.abs(dx_tracker.get_value()) > 1E-4 else GREEN,
                secant_line_length=5,
                include_dx_line=False,
                include_dy_line=False
            ).set_z_index(2).set_style(stroke_width=graph_stroke.get_value())
        )
        self.play(
            LaggedStart(
                Write(tretrinsregel_trin[1]),
                Write(tretrinsregel_ligninger[1]),
                Create(secant_line),
                lag_ratio=0.5
            )
        )
        self.slide_pause()

        self.camera.frame.save_state()
        self.play(
            LaggedStart(
                Write(tretrinsregel_trin[2]),
                Write(tretrinsregel_ligninger[2]),
                lag_ratio=0.5
            )
        )
        self.slide_pause()
        self.remove(dots)
        dots = always_redraw(lambda: VGroup(
            Dot(
                plane.c2p(
                    x_tracker.get_value(), graph.underlying_function(x_tracker.get_value())
                ),
                stroke_width=0.01,
                stroke_color=WHITE,
                color=RED,
                radius=min(0.08, 0.001*np.exp(0.1*dx_tracker.get_value()))
            ).set_z_index(3),
            Dot(
                plane.c2p(
                    x_tracker.get_value() + dx_tracker.get_value(),
                    graph.underlying_function(x_tracker.get_value() + dx_tracker.get_value())
                ),
                color=RED,
                stroke_width=0.01,
                stroke_color=WHITE,
                radius=min(0.08, 0.001*np.exp(0.1*dx_tracker.get_value()))
            ).set_z_index(3)
        ))
        self.add(dots)
        self.play(
            self.camera.frame.animate.move_to(
                between_mobjects(dots[0], dots[1])
            ).set(width=2.5*dx_tracker.get_value()),
            run_time=4
        )
        self.slide_pause()
        self.play(
            dx_tracker.animate.set_value(1E-5),
            self.camera.frame.animate.move_to(
                plane.c2p(x_tracker.get_value(), graph.underlying_function(x_tracker.get_value()))
            ).set(width=0.01),
            graph_stroke.animate.set_value(0.1),
            lines_tracker.animate.set_value(0),
            run_time=10
        )
        self.slide_pause()

        brect = get_background_rect(
            VGroup(*tretrinsregel_trin, *tretrinsregel_ligninger).set_z_index(plane.get_z_index() + 2),
            stroke_colour=color_gradient([RED, BLUE_A, BLUE_B, BLUE_C], 4)
        )
        frects = VGroup(*[
            get_background_rect(
                VGroup(tretrinsregel_trin[i], tretrinsregel_ligninger[i])
            ).set_z_index(brect.get_z_index() + 2) for i in range(len(tretrinsregel_trin))
        ])
        self.add(brect, frects)
        self.play(
            self.camera.frame.animate.move_to(
                VGroup(tretrinsregel_trin[0], tretrinsregel_ligninger[0])
            ).set(width=1.1*tretrinsregel_trin.width),
            FadeOut(frects[0]),
            run_time=5
        )
        self.play(
            Indicate(tretrinsregel_ligninger[0])
        )
        self.slide_pause()

        self.play(
            FadeIn(frects[0]),
            self.camera.frame.animate.move_to(
                VGroup(tretrinsregel_trin[1], tretrinsregel_ligninger[1])
            ),
            FadeOut(frects[1]),
            run_time=2
        )
        self.play(
            Indicate(tretrinsregel_ligninger[1])
        )
        self.slide_pause()

        self.play(
            FadeIn(frects[1]),
            self.camera.frame.animate.move_to(
                VGroup(tretrinsregel_trin[2], tretrinsregel_ligninger[2])
            ),
            FadeOut(frects[2]),
            run_time=2
        )
        self.play(
            Indicate(tretrinsregel_ligninger[2])
        )
        self.slide_pause()

        self.play(
            Restore(self.camera.frame),
            FadeOut(frects[:2]),
            run_time=2
        )
        self.slide_pause()

        self.play(
            LaggedStart(
                *[Uncreate(m) for m in [plane, graph, xlines, ylines, secant_line]],
                Unwrite(labels),
                VGroup(tretrinsregel_trin, tretrinsregel_ligninger, brect).animate.scale(1.25).move_to(ORIGIN),
                lag_ratio=0.1
            ),
            run_time=2
        )
        self.slide_pause()
        self.play(
            LaggedStart(
                *[Unwrite(m) for m in [tretrinsregel_trin, tretrinsregel_ligninger]],
                Uncreate(brect),
                lag_ratio=0.2
            ),
            run_time=2
        )


class TreTrinThumbnail(TreTrinsRegel):
    def construct(self):
        title = VGroup(
            Tex("Tretrinsreglen", color=YELLOW), Tex(" for differentiering")
        ).arrange(RIGHT).scale(1.25).to_edge(UL)
        tretrinsregel_trin = VGroup(
            Text("Trin 1: Find funktionstilvæksten", t2c={"Trin 1": RED, "funktionstilvæksten": BLUE_A}),
            Text("Trin 2: Find differenskvotienten", t2c={"Trin 2": RED, "differenskvotienten": BLUE_B}),
            Text("Trin 3: Find differentialkvotienten", t2c={"Trin 3": RED, "differentialkvotienten": BLUE_C}),
        ).scale(0.5).arrange(DOWN, aligned_edge=LEFT, buff=1.25).to_edge(UR)
        tretrinsregel_ligninger = VGroup(
            MathTex(
                r"\Delta y", "=", rf"f(x_0 + h)", "-", "f(x_0)"
            ).set_color_by_tex_to_color_map(
                {r"\Delta y": BLUE_A}
            ).scale(0.5).next_to(tretrinsregel_trin[0], DOWN, aligned_edge=LEFT),
            MathTex(
                r"\frac{\Delta y}{h}", "=", r"\frac{f(x_0 + h) - f(x_0)}{h}"
            ).set_color_by_tex_to_color_map(
                {r"\Delta y": BLUE_B}
            ).scale(0.5).next_to(tretrinsregel_trin[1], DOWN, aligned_edge=LEFT),
            MathTex(
                r"f'(x_0)", "=" r"\lim_{h \rightarrow 0}",
                r"\left(\frac{f(x_0 + h) - f(x_0)}{h}\right)"
            ).set_color_by_tex_to_color_map(
                {r"'": BLUE_C}
            ).scale(0.5).next_to(tretrinsregel_trin[2], DOWN, aligned_edge=LEFT)
        )
        VGroup(tretrinsregel_trin, tretrinsregel_ligninger).scale(1.25).move_to(ORIGIN)
        brect = get_background_rect(
            VGroup(*tretrinsregel_trin, *tretrinsregel_ligninger),
            stroke_colour=color_gradient([RED, BLUE_A, BLUE_B, BLUE_C], 4)
        )
        self.add(title, tretrinsregel_trin, tretrinsregel_ligninger, brect)
