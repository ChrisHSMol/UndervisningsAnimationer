from manim import *
import sys
sys.path.append("../")
from helpers import *
slides = True
if slides:
    from manim_slides import Slide


class StykFunk(MovingCameraScene if not slides else MovingCameraScene, Slide):
    def construct(self):
        play_title(self, "Stykkevist definerede funktioner")

        xmin, xmax, xstep = -2, 8.5, 0.5
        ymin, ymax, ystep = -2, 4.5, 0.5
        plane = NumberPlane(
            x_range=[xmin, xmax, xstep],
            y_range=[ymin, ymax, ystep],
            x_length=12,
            y_length=12 / 16 * 9,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 2,
                "stroke_opacity": 0.3
            },
            axis_config={"include_numbers": True}
        )
        self.play(
            DrawBorderThenFill(
                plane
            ),
            run_time=2
        )

        x1, x2 = 2.5, 5.0
        xs = [x1, x2]
        xrangs = [
            # [0.0, 2.50, 0.5],
            [0.0, x1, 0.5],
            [x1, x2, 0.5],
            [x2, xmax, 0.5]
        ]
        renter = [
            # 0.30,
            0.20,
            0.40,
            0.55
        ]
        # cs = [
        #     BLUE,
        #     PURPLE,
        #     GREEN
        # ]
        # cs = sunset_color_scheme(3)
        cs = [
            BLUE, *sunset_color_scheme(3)[1:]
        ]
        graphs = VGroup(
            # *[
            #     plane.plot(
            #         lambda x: renter[i] * x - (renter[i]-renter[i-1])*xrangs[i-1][1],
            #         x_range=xrangs[i], color=YELLOW,
            #         stroke_width=1) for i in np.arange(len(xrangs)-1)+1
            # ]
            plane.plot(lambda x: renter[0] * x, x_range=xrangs[0],
                       color=YELLOW, stroke_width=1.5
                       ),
            plane.plot(lambda x: renter[1] * x - (renter[1] - renter[0]) * xrangs[0][1], x_range=xrangs[1],
                       color=YELLOW, stroke_width=1.5
                       ),
            plane.plot(
                lambda x: renter[2] * x - (renter[2] - renter[1]) * xrangs[1][1] - (renter[1] - renter[0]) * xrangs[0][
                    1], x_range=xrangs[2],
                color=YELLOW, stroke_width=1.5
                )
        )

        self.play(
            DrawBorderThenFill(
                graphs
            ),
            run_time=2
        )
        self.slide_pause(2)
        for graph in graphs:
            self.play(
                ApplyWave(graph),
                run_time=1
            )
            self.wait(0.5)

        dots = VGroup(
            *[
                Dot(
                    plane.c2p(xs[i], graphs[i].underlying_function(xs[i])),
                    color=RED
                ) for i in range(len(xs))
            ]
        )
        self.play(
            DrawBorderThenFill(
                dots
            ),
            run_time=1
        )
        self.slide_pause(2)

        knaeks = VGroup(
            *[
                # plane.get_T_label(
                #     x_val=dots[i].get_x(),
                #     graph=dots[i].get_y(),
                #     label=Tex("x-value")
                # ) for i in range(len(dots))
                # plane.get_line_from_axis_to_point(0, dots[i]) for i in range(len(dots))
                Line(
                    start=plane.c2p(xs[i], graphs[i].underlying_function(xs[i])),
                    end=plane.c2p(xs[i], 0),
                    color=RED,
                    stroke_width=1.2,
                ) for i in range(len(dots))
            ]
        )
        knaeks_text = VGroup(
            *[
                MathTex(
                    str(xs[i]),
                    color=RED
                ).move_to(plane.c2p(xs[i] + 0.1875, 0.15)).scale(0.65) for i in range(len(xs))
            ]
        )
        self.play(
            Create(
                knaeks
            ),
            run_time=1
        )
        self.play(
            Write(
                knaeks_text
            )
        )
        self.play(
            FadeOut(
                dots,
                knaeks
            ),
            run_time=1
        )
        self.slide_pause(2)

        # =====================================================================
        # =====================================================================
        # =====================================================================

        self.camera.frame.save_state()
        self.play(
            self.camera.frame.animate.set(
                width=x1 * 1.75
            ).move_to(graphs[0]),
            run_time=2
        )
        self.play(
            graphs[0].animate.set_color(cs[0])
        )
        self.slide_pause(2)

        alines = VGroup(
            Line(
                start=plane.c2p(0, 0),
                end=plane.c2p(1, 0),
                color=cs[0],
                stroke_width=1.2,
            ),
            Line(
                start=plane.c2p(1, 0),
                end=plane.c2p(1, renter[0]),
                color=cs[0],
                stroke_width=1.2,
            )
        )
        anum = [MathTex("1").next_to(alines[0], UP).shift(0.3 * RIGHT + 0.35 * DOWN),
                MathTex(str(renter[0])).next_to(alines[1], RIGHT).shift(0.4 * LEFT)]
        for i in range(len(anum)):
            self.play(
                LaggedStart(
                    Create(alines[i]),
                    Write(anum[i].scale(0.25).set_color(cs[0])),
                    lag_ratio=2
                ),
                run_time=2
            )
            self.wait(1)
        a1 = MathTex("a", "=", f"{renter[0]}", color=cs[0]).next_to(graphs[0], 1.2 * UP).set_z_index(3)
        a1_rect = get_background_rect(a1, buff=0.1)
        self.play(
            Write(
                a1
            ),
            FadeIn(a1_rect),
            run_time=1
        )
        self.play(FadeOut(VGroup(alines, *anum)), run_time=0.5)
        self.slide_pause(2)
        b1dot = Dot(plane.c2p(0, graphs[0].underlying_function(0)), color=cs[0])
        self.play(
            LaggedStart(
                ShowPassingFlash(
                    Line(
                        start=plane.c2p(x1, graphs[0].underlying_function(x1)),
                        end=plane.c2p(-2, graphs[0].underlying_function(-2)),
                        stroke_width=1.2,
                    ).set_color(YELLOW),
                    time_width=2
                ),
                FadeIn(b1dot),
                lag_ratio=0.1
            ),
            run_time=3
        )
        # INDSÆT LAGGEDSTART MED SHOWPASSINGFLASH OG TEGNING AF B-PUNKT
        b1 = MathTex("b", "=", "0", color=cs[0]).next_to(a1, 0.8 * DOWN, aligned_edge=LEFT).set_z_index(3)
        b1_rect = get_background_rect(b1, buff=0.1)
        self.play(
            Write(
                b1
            ),
            FadeIn(b1_rect),
            run_time=0.5
        )
        self.slide_pause(2)
        eq1 = MathTex(
            "y_1", "=", f"{renter[0]}", "\cdot", "x", "+", "0",
            color=cs[0]
        ).next_to(graphs[0], UP).shift(0.5 * RIGHT).set_z_index(3)
        eq1_rect_temp = get_background_rect(eq1, buff=0.1)
        eq1_rect = get_background_rect(eq1[:-2], buff=0.1).set_z_index(2)
        self.play(
            # ReplacementTransform(
            TransformMatchingTex(
                VGroup(
                    a1, b1
                ),
                eq1,
                transform_mismatches=True
            ),
            ReplacementTransform(
                VGroup(a1_rect, b1_rect),
                eq1_rect_temp
            ),
            FadeOut(b1dot),
            run_time=1.5
        )
        self.slide_pause(2)
        self.play(
            FadeOut(
                eq1[-2:]
            ),
            # eq1[:-2].animate.shift(0.25 * RIGHT),
            ReplacementTransform(eq1_rect_temp, eq1_rect),
            run_time=1
        )
        self.slide_pause(2)

        # =====================================================================
        # =====================================================================
        # =====================================================================

        self.play(
            self.camera.frame.animate.move_to(graphs[1]),
            # FadeOut(eq1[:-2]),
            VGroup(eq1[:-2], eq1_rect).animate.shift(0.4 * LEFT),
            # eq1_rect.animate.shift(0.4 * LEFT),
            run_time=2
        )
        self.play(
            graphs[1].animate.set_color(cs[1])
        )
        self.slide_pause(2)

        alines = VGroup(
            Line(
                start=plane.c2p(x1, graphs[1].underlying_function(x1)),
                end=plane.c2p(x1 + 1, graphs[1].underlying_function(x1)),
                color=cs[1],
                stroke_width=1.2,
            ),
            Line(
                start=plane.c2p(x1 + 1, graphs[1].underlying_function(x1)),
                end=plane.c2p(x1 + 1, graphs[1].underlying_function(x1 + 1)),
                color=cs[1],
                stroke_width=1.2,
            )
        )
        anum = [
            MathTex("1").next_to(alines[0], UP).shift(0.3 * RIGHT + 0.35 * DOWN),
            MathTex(str(renter[1])).next_to(alines[1], RIGHT).shift(0.4 * LEFT)
        ]
        for i in range(len(anum)):
            self.play(
                LaggedStart(
                    Create(alines[i]),
                    Write(anum[i].scale(0.25).set_color(cs[1])),
                    lag_ratio=2
                ),
                run_time=2
            )
            self.wait(1)
        a2 = MathTex(
            "a", "=", f"{renter[1]}",
            color=cs[1]
        ).next_to(graphs[1], 1.1 * UP).shift(0.3 * LEFT).set_z_index(3)
        a2_rect = get_background_rect(a2, buff=0.1)
        self.play(
            Write(
                a2
            ),
            FadeIn(a2_rect),
            run_time=1
        )
        self.play(FadeOut(VGroup(alines, *anum)), run_time=0.5)
        self.slide_pause(2)

        self.play(
            self.camera.frame.animate.set(
                width=x1 * 1.75 * 2
            ).move_to(graphs[0]),
            run_time=2
        )
        b2dot = Dot(plane.c2p(0, graphs[1].underlying_function(0)), color=cs[1])
        self.play(
            LaggedStart(
                ShowPassingFlash(
                    Line(
                        start=plane.c2p(x2, graphs[1].underlying_function(x2)),
                        end=plane.c2p(-2, graphs[1].underlying_function(-2)),
                        stroke_width=1.2,
                    ).set_color(YELLOW),
                    time_width=2
                ),
                FadeIn(b2dot),
                lag_ratio=0.1
            ),
            run_time=3
        )
        b2 = MathTex(
            "b", "=", f"{graphs[1].underlying_function(0)}",
            color=cs[1]
        ).next_to(b2dot, LEFT).set_z_index(3)  # a2, 0.9*DOWN, aligned_edge=LEFT)
        b2_rect = get_background_rect(b2, buff=0.1)
        self.play(
            Write(
                b2
            ),
            FadeIn(b2_rect),
            run_time=0.5
        )
        self.play(
            # b2.animate.next_to(a2, 0.9 * DOWN, aligned_edge=LEFT),
            VGroup(b2, b2_rect).animate.next_to(a2_rect, 0.8 * DOWN, aligned_edge=LEFT),
            self.camera.frame.animate.set(
                width=x1 * 1.75
            ).move_to(graphs[1]),
            FadeOut(b2dot),
            run_time=2
        )
        self.slide_pause(2)

        if float(b2[2].tex_string) < 0:
            sign = ""
        else:
            sign = "+"
        eq2 = MathTex(
            "y_2", "=", f"{renter[1]}", "\cdot", "x", sign, b2[2].tex_string,
            color=cs[1]
        ).next_to(graphs[1], UP).shift(0.25 * LEFT + 0.2 * DOWN).set_z_index(3)
        eq2_rect = get_background_rect(eq2, buff=0.1)
        self.play(
            # ReplacementTransform(
            TransformMatchingTex(
                VGroup(
                    a2, b2
                ),
                eq2,
                transform_mismatches=True
            ),
            ReplacementTransform(
                VGroup(a2_rect, b2_rect),
                eq2_rect
            ),
            run_time=1.5
        )
        self.slide_pause(2)

        # =====================================================================
        # =====================================================================
        # =====================================================================

        self.play(
            self.camera.frame.animate.set(
                width=(xmax - x2) * 1.75
            ).move_to(graphs[2]),
            VGroup(eq2, eq2_rect).animate.shift(0.4 * LEFT),
            run_time=2
        )
        self.play(
            graphs[2].animate.set_color(cs[2])
        )
        self.slide_pause(2)

        alines = VGroup(
            Line(
                start=plane.c2p(x2, graphs[2].underlying_function(x2)),
                end=plane.c2p(x2 + 1, graphs[2].underlying_function(x2)),
                color=cs[2],
                stroke_width=1.2,
            ),
            Line(
                start=plane.c2p(x2 + 1, graphs[2].underlying_function(x2)),
                end=plane.c2p(x2 + 1, graphs[2].underlying_function(x2 + 1)),
                color=cs[2],
                stroke_width=1.2,
            )
        )
        anum = [MathTex("1").next_to(alines[0], UP).shift(0.3 * RIGHT + 0.35 * DOWN),
                MathTex(str(renter[2])).next_to(alines[1], RIGHT).shift(0.4 * LEFT)]
        for i in range(len(anum)):
            self.play(
                LaggedStart(
                    Create(alines[i]),
                    Write(anum[i].scale(0.25).set_color(cs[2])),
                    lag_ratio=2
                ),
                run_time=2
            )
            self.wait(1)
        a3 = MathTex(
            "a", "=", f"{renter[2]}",
            color=cs[2]
        ).next_to(graphs[2], 0.9 * UP).shift(0.3 * LEFT).set_z_index(3)
        a3_rect = get_background_rect(a3, buff=0.1)
        self.play(
            Write(
                a3
            ),
            FadeIn(a3_rect),
            run_time=1
        )
        self.play(FadeOut(VGroup(alines, *anum)), run_time=0.5)
        self.slide_pause(2)

        self.play(
            self.camera.frame.animate.set(
                width=xmax * 1.5
            ).move_to(graphs[1]).shift(DOWN),
            run_time=2
        )
        b3dot = Dot(plane.c2p(0, graphs[2].underlying_function(0)), color=cs[2])
        self.play(
            LaggedStart(
                ShowPassingFlash(
                    Line(
                        start=plane.c2p(xmax, graphs[2].underlying_function(xmax)),
                        end=plane.c2p(-2, graphs[2].underlying_function(-2)),
                        stroke_width=1.2,
                    ).set_color(YELLOW),
                    time_width=2
                ),
                FadeIn(b3dot),
                lag_ratio=0.1
            ),
            run_time=3
        )
        b3 = MathTex(
            "b", "=", f"{graphs[2].underlying_function(0)}",
            color=cs[2]
        ).next_to(b3dot, LEFT).set_z_index(3)  # a2, 0.9*DOWN, aligned_edge=LEFT)
        b3_rect = get_background_rect(b3, buff=0.1)
        self.play(
            Write(
                b3
            ),
            FadeIn(b3_rect),
            run_time=0.5
        )
        self.play(
            # b3.animate.next_to(a3, 0.9 * DOWN, aligned_edge=LEFT),
            VGroup(b3, b3_rect).animate.next_to(a3_rect, 0.8 * DOWN, aligned_edge=LEFT),
            self.camera.frame.animate.set(
                width=(xmax - x2) * 1.75
            ).move_to(graphs[2]),
            FadeOut(b3dot),
            eq2.animate.shift(0.4 * RIGHT),
            eq1[:-2].animate.shift(0.4 * RIGHT),
            run_time=2
        )
        self.slide_pause(2)

        if float(b3[2].tex_string) < 0:
            sign = ""
        else:
            sign = "+"
        eq3 = MathTex(
            "y_3", "=", f"{renter[2]}", "\cdot", "x", sign, b3[2].tex_string,
            color=cs[2]
        ).next_to(graphs[2], UP).shift(0.25 * LEFT + 0.2 * DOWN).set_z_index(3)
        eq3_rect = get_background_rect(eq3, buff=0.1)
        self.play(
            # ReplacementTransform(
            TransformMatchingTex(
                VGroup(
                    a3, b3
                ),
                eq3,
                transform_mismatches=True
            ),
            ReplacementTransform(
                VGroup(a3_rect, b3_rect),
                eq3_rect
            ),
            run_time=1.5
        )
        self.slide_pause(2)

        # =====================================================================
        # =====================================================================
        # =====================================================================

        self.play(
            Restore(
                self.camera.frame
            ),
            run_time=2
        )
        self.slide_pause(2)

        # for eq in (eq1[:-2], eq2, eq3):
        #     self.play(
        #         Indicate(eq),
        #         run_time=2
        #     )
        #     self.wait(0.5)

        # for i, eq in enumerate((eq1[:-2], eq2, eq3)):
        for i, eq, rect in zip(range(len(renter)), [eq1[:-2], eq2, eq3], [eq1_rect, eq2_rect, eq3_rect]):
            if i == 0:
                eq_base = eq
                self.play(
                    eq.animate.scale(0.75).next_to(
                        plane, UL
                    ).shift((i * 0.5 + 1) * DOWN + 1.0 * RIGHT),
                    FadeOut(rect, run_time=0.1),
                    run_time=1
                )
            else:
                self.play(
                    eq.animate.scale(0.75).next_to(
                        eq_base, DOWN, aligned_edge=LEFT
                    ),
                    FadeOut(rect, run_time=0.25),
                    run_time=1
                )
                eq_base = eq
            # self.play(FadeIn(rect.move_to(eq)), run_time=0.25)
            self.wait(1)
        self.slide_pause(2)

        eqpart1 = eq1[2:-2].copy()
        self.play(
            eqpart1.animate.shift(5 * RIGHT),
            run_time=1
        ),
        self.slide_pause(2)
        lines = VGroup(
            Line(
                start=plane.c2p(0, 0),
                end=plane.c2p(x1, 0),
                stroke_width=1.5,
                color=RED
            ),
            Line(
                start=plane.c2p(x1, 0),
                end=plane.c2p(x2, 0),
                stroke_width=1.5,
                color=RED
            ),
            Line(
                start=plane.c2p(x2, 0),
                end=plane.c2p(xmax, 0),
                stroke_width=1.5,
                color=RED
            )
        )
        self.play(
            Create(
                lines[0]
            ),
            run_time=2
        )
        self.slide_pause(1)
        xlim1 = MathTex(
            ",", "0", "\leq", "x", "<", f"{x1}"
        ).scale(0.75).next_to(eqpart1, RIGHT).shift(1.25 * RIGHT)
        xlim1[5][:].set_color(RED)
        self.play(
            Write(
                xlim1
            ),
            run_time=1
        )
        self.play(
            Uncreate(
                lines[0].set_points(lines[0].get_points()[::-1])
            ),
            run_time=1
        )
        self.slide_pause(2)

        eqpart2 = eq2[2:].copy()
        self.play(
            eqpart2.animate.shift(5 * RIGHT),
            run_time=1
        ),
        self.slide_pause(2)
        self.play(Create(lines[1]), run_time=2)
        self.slide_pause(1)
        xlim2 = MathTex(
            ",", f"{x1}", "\leq", "x", "<", f"{x2}"
        ).scale(0.75).next_to(xlim1, DOWN, aligned_edge=LEFT)
        xlim2[1][:].set_color(RED)
        xlim2[5][:].set_color(RED)
        self.play(
            Write(
                xlim2
            ),
            run_time=1
        )
        self.play(
            Uncreate(
                lines[1].set_points(lines[1].get_points()[::-1])
            ),
            run_time=1
        )
        self.slide_pause(2)

        eqpart3 = eq3[2:].copy()
        self.play(
            eqpart3.animate.shift(5 * RIGHT),
            run_time=1
        ),
        self.slide_pause(2)
        self.play(Create(lines[2]), run_time=2)
        self.slide_pause(1)
        xlim3 = MathTex(
            ",", f"{x2}", r"\leq", "x", "<", f"{xmax}"
        ).scale(0.75).next_to(xlim2, DOWN, aligned_edge=LEFT)
        xlim3[1][:].set_color(RED)
        self.play(
            Write(
                xlim3
            ),
            run_time=1
        )
        self.play(
            Uncreate(
                lines[2].set_points(lines[2].get_points()[::-1])
            ),
            run_time=1
        )
        self.slide_pause(2)

        brace = Brace(VGroup(eqpart1, eqpart2, eqpart3), LEFT)
        self.play(
            DrawBorderThenFill(
                brace
            ),
            run_time=1
        )
        self.slide_pause(1)
        fx = MathTex(
            "f(x)", "="
        ).scale(0.75).next_to(eqpart2, LEFT).shift(0.5 * LEFT)
        self.play(
            Write(
                fx
            ),
            run_time=0.5
        )
        self.slide_pause(2)

        full_eq = VGroup(fx, brace, eqpart1, eqpart2, eqpart3, xlim1, xlim2, xlim3).set_z_index(3)
        full_eq_rect = get_background_rect(full_eq, stroke_colour=YELLOW).set_opacity(0)
        self.remove(fx, brace, eqpart1, eqpart2, eqpart3, xlim1, xlim2, xlim3)
        self.add(full_eq)
        self.play(
            *[FadeOut(m) for m in self.mobjects if m not in [full_eq, full_eq_rect]],
            full_eq.animate.scale(1.5).move_to(ORIGIN),
            full_eq_rect.animate.scale(1.5).move_to(ORIGIN).set_opacity(1.0),
            run_time=2
        )
        self.slide_pause()

        fade_out_all(self, rt=1)
        play_title_reverse(self, "Stykkevist definerede funktioner")

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)


class StykFunkThumbnail(Scene):
    def construct(self):
        cs = [
            BLUE, *sunset_color_scheme(3)[1:]
        ]
        eq = VGroup(
            VGroup(
                MathTex(r"0.2 \cdot x", color=cs[0]),
                MathTex(r"0.4 \cdot x - 0.5", color=cs[1]),
                MathTex(r"0.55 \cdot x - 1.25", color=cs[2]),
            ).arrange(DOWN, aligned_edge=LEFT),
            VGroup(
                MathTex(r", 0 \leq x < ", "2.5"),
                MathTex(r", ", "2.5", r"\leq x < ", "5.0"),
                MathTex(r", ", "5.0", r"\leq x < ", "8.5"),
            ).arrange(DOWN, aligned_edge=LEFT)
        ).arrange(RIGHT)
        eq[1][0][-1].set_color(RED)
        eq[1][1][1].set_color(RED)
        eq[1][1][-1].set_color(RED)
        eq[1][2][1].set_color(RED)
        eq[1][2][-1].set_color(RED)
        brace = Brace(eq, LEFT).next_to(eq, LEFT)
        fx = MathTex("f(x)=").next_to(brace, LEFT)
        title = VGroup(
            Tex("Stykvist definerede", color=YELLOW), Tex(" funktioner")
        ).arrange(RIGHT).next_to(VGroup(fx, brace, eq), UP, aligned_edge=LEFT, buff=1)
        VGroup(eq, brace, fx, title).scale(1.5).to_edge(UL)
        self.add(eq, brace, fx, title)
