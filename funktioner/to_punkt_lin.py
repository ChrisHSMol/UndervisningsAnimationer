from manim import *
import sys
sys.path.append("../")
from helpers import *
slides = True
if slides:
    from manim_slides import Slide


class ToPunktLin(Slide if slides else Scene):
    def construct(self):
        def maybe_round(val, dec=2):
            if val == int(val):
                return int(val)
            else:
                return np.round(val, dec)

        x1, x2 = 4, 12
        y1, y2 = 3, 7
        p1_col = RED
        p2_col = BLUE
        b_col = GREEN
        a_col = PURPLE
        eq_color_map = {
            "x_1": p1_col,
            "y_1": p1_col,
            "x_2": p2_col,
            "y_2": p2_col,
            "a": a_col,
            "b": b_col
        }

        difx = maybe_round(x2 - x1)
        dify = maybe_round(y2 - y1)
        a_ex = maybe_round(dify / difx)
        b_ex = maybe_round(y1 - a_ex * x1)

        self.slide_pause(0.5)
        title = VGroup(
            Tex("Topunktsformlen for en"),
            Tex("Lineær", " funktion"),
        ).arrange(DOWN, aligned_edge=LEFT)
        title[1][0].set_color(YELLOW)
        play_title(self, title)

        plane = NumberPlane(
            x_range=[-2, 16.5, 1],
            y_range=[-2, 12.5, 1],
            x_length=7.5,
            y_length=5,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 2,
                "stroke_opacity": 0.3
            },
            # axis_config={"include_numbers": True}
        ).to_edge(UL)
        self.play(
            DrawBorderThenFill(
                plane
            ),
            run_time=2
        )

        axis_labels = plane.get_axis_labels(
            x_label="x",
            y_label="y"
        )
        self.play(
            Create(axis_labels),
            run_time=1
        )

        p1 = Dot().move_to(plane.c2p(x1, y1)).set_color(p1_col)
        p2 = Dot().move_to(plane.c2p(x2, y2)).set_color(p2_col)
        ps = VGroup(p1, p2)
        self.slide_pause(2)

        lab1 = MathTex(
            "(", "x_1", ", ", "y_1", ")"
        ).set_color_by_tex_to_color_map(
            eq_color_map
        ).next_to(p1, UP + 0.25 * LEFT)
        lab2 = MathTex(
            "(", "x_2", ", ", "y_2", ")"
        ).set_color_by_tex_to_color_map(
            eq_color_map
        ).next_to(p2, UP + 0.25 * LEFT)
        labels = VGroup(lab1, lab2)

        eq1 = MathTex(
            "y_1", " = ", "a", "\\cdot", "x_1", "+", "b"
        ).set_color_by_tex_to_color_map(
            eq_color_map
        ).scale(0.75).move_to(3 * UR)
        eq2 = MathTex(
            "y_2", " = ", "a", "\\cdot", "x_2", "+", "b"
        ).set_color_by_tex_to_color_map(
            eq_color_map
        ).scale(0.75).next_to(eq1, 0.75 * DOWN)

        self.play(
            Create(p1),
            Write(lab1),
            Write(eq1),
            run_time=2
        )
        self.play(eq1.animate.to_edge(UR))
        # self.wait(2)
        self.slide_pause(2)

        self.play(
            Create(p2),
            Write(lab2),
            Write(eq2),
            run_time=2
        )
        self.play(eq2.animate.to_edge(UR - 0.75 * DOWN))

        whole_graph = VGroup(plane, axis_labels, ps, labels)
        whole_graph.generate_target()
        whole_graph.target.scale(0.75)
        whole_graph.target.to_edge(UL)
        self.play(
            MoveToTarget(whole_graph)
        )
        # self.wait(2)
        self.slide_pause(2)

        # =====================================================================
        # =====================================================================
        # =====================================================================

        tp1old = MathTex(
            "y_2", "-", "y_1",
            " = ",
            "a", "\\cdot", "x_2", "+", "b", "-", r"\left(",
            "a", "\\cdot", "x_1", "+", "b", r"\right)"
        ).set_color_by_tex_to_color_map(
            eq_color_map
        ).scale(0.75).move_to(3 * RIGHT + 2 * UP)
        self.play(
            DrawBorderThenFill(tp1old)
        )
        # self.wait(2)
        self.slide_pause(2)

        tp1 = MathTex(
            "y_2", "-", "y_1",
            " = ",
            "a", "\\cdot", "x_2", "+", "b", "-", "a", "\\cdot", "x_1", "-", "b"
        ).set_color_by_tex_to_color_map(
            eq_color_map
        ).scale(0.75).next_to(tp1old, DOWN, aligned_edge=LEFT)
        self.play(
            TransformMatchingTex(
                tp1old.copy(), tp1,
                transform_mismatches=True
            )
        )

        self.play(
            *[
                Circumscribe(b, fade_out=True) for b in tp1.get_parts_by_tex("b")
            ],
            # Circumscribe(
            #     tp1.get_parts_by_tex("b"),
            #     fade_out=True
            # ),
            run_time=2
        )
        # self.wait()
        self.slide_pause(1)

        tp2 = MathTex(
            "y_2", "-", "y_1",
            " = ",
            "a", "\\cdot", "x_2", "-", "a", "\\cdot", "x_1"
        ).set_color_by_tex_to_color_map(
            eq_color_map
        ).scale(0.75).next_to(tp1, DOWN, aligned_edge=LEFT)
        self.play(
            # ReplacementTransform(
            TransformMatchingTex(
                tp1.copy(),
                tp2,
                transform_mismatches=True
            )
        )
        # self.wait(2)
        self.slide_pause(2)

        self.play(
            *[
                Circumscribe(a, fade_out=True) for a in tp1.get_parts_by_tex("a")
            ],
            # Circumscribe(
            #     tp2.get_parts_by_tex("a"),
            #     fade_out=True
            # ),
            run_time=2
        )
        # self.wait()
        self.slide_pause(1)

        tp3 = MathTex(
            "y_2", "-", "y_1",
            " = ",
            "a", r"\cdot\left(", "x_2", "-", "x_1", r"\right)"
        ).set_color_by_tex_to_color_map(
            eq_color_map
        ).scale(0.75).next_to(tp2, DOWN, aligned_edge=LEFT)
        self.play(
            # ReplacementTransform(
            TransformMatchingTex(
                tp2.copy(),
                tp3,
                transform_mismatches=True
            )
        )
        # self.wait(2)
        self.slide_pause(2)

        self.play(
            Circumscribe(
                VGroup(
                    tp3.get_parts_by_tex("x_2"),
                    tp3.get_parts_by_tex("x_1")
                ),
                fade_out=True
            ),
            run_time=2
        )
        # self.wait()
        self.slide_pause(1)

        tp4 = VGroup(
            MathTex(
                "{y_2", "-", "y_1}", r"\over",
                "{x_2", "-", "x_1}"
            ).set_color_by_tex_to_color_map(eq_color_map),
            MathTex("=", "a").set_color_by_tex_to_color_map(eq_color_map)
        ).arrange(RIGHT).scale(0.75).next_to(tp3, DOWN, aligned_edge=LEFT)
        self.play(
            # ReplacementTransform(
            TransformMatchingTex(
                tp3.copy(),
                tp4,
                transform_mismatches=True
            )
        )
        # self.wait(2)
        self.slide_pause(2)

        eq_a = VGroup(
            MathTex("a", "=").set_color_by_tex_to_color_map(eq_color_map),
            MathTex(
                "{y_2", "-", "y_1}", r"\over",
                "{x_2", "-", "x_1}"
            ).set_color_by_tex_to_color_map(eq_color_map)
        ).arrange(RIGHT).scale(0.75).next_to(tp3, DOWN, aligned_edge=LEFT)
        self.play(
            # *[
            #     p2p_anim(tp4, eq_a, tex.tex_string) for tex in eq_a
            # ]
            TransformMatchingTex(
                tp4, eq_a
            )
        )
        self.slide_pause(2)

        self.play(
            eq_a.animate.next_to(eq2, DOWN),
            FadeOut(
                VGroup(
                    tp1old,
                    tp1,
                    tp2,
                    tp3,
                )
            ),
            run_time=1
        )
        self.slide_pause(2)

        # =====================================================================
        # =====================================================================
        # =====================================================================

        tpb1 = eq1.copy().scale(1.33).move_to(2 * RIGHT + 1 * UP)
        self.play(
            ReplacementTransform(
                eq1.copy(),
                tpb1
            ),
            run_time=2
        )
        self.slide_pause(2)
        self.play(
            Circumscribe(
                VGroup(
                    tpb1.get_parts_by_tex("a"),
                    tpb1.get_parts_by_tex("x_1")
                ),
                fade_out=True
            ),
            run_time=2
        )
        self.slide_pause(2)

        tpb2 = MathTex(
            "y_1", "-", "a", r"\cdot", "x_1", " = ", "b"
        ).set_color_by_tex_to_color_map(
            eq_color_map
        ).next_to(tpb1, DOWN, aligned_edge=LEFT)
        self.play(
            p2p_anim_copy(tpb1, tpb2, "y_1"),
            p2p_anim_copy(tpb1, tpb2, "x_1"),
            p2p_anim_copy(tpb1, tpb2, "a"),
            p2p_anim_copy(tpb1, tpb2, "b"),
            p2p_anim_copy(tpb1, tpb2, "="),
            p2p_anim_copy(tpb1, tpb2, "+", "-"),
            run_time=2
        )
        self.slide_pause(2)

        eq_b = MathTex(
            "b", " = ", "y_1", "-", "a", r"\cdot", "x_1"
        ).set_color_by_tex_to_color_map(
            eq_color_map
        ).next_to(tpb1, DOWN, aligned_edge=LEFT)
        self.play(
            # *[
            #     p2p_anim(tpb2, eq_b, tex.tex_string) for tex in eq_b
            # ],
            TransformMatchingTex(
                tpb2, eq_b
            ),
            run_time=2
        )
        self.slide_pause(2)

        self.play(
            eq_b.animate.scale(0.75).next_to(eq_a, DOWN, aligned_edge=LEFT),
            Uncreate(
                tpb1,
            ),
            run_time=1
        )
        self.slide_pause(2)

        # =====================================================================
        # =====================================================================
        # =====================================================================

        lab1_ex = MathTex(
            "(", f"{x1}", ", ", f"{y1}", ")"
        ).next_to(p1, UP + 0.25 * LEFT).scale(0.9)
        lab2_ex = MathTex(
            "(", f"{x2}", ", ", f"{y2}", ")"
        ).next_to(p2, UP + 0.25 * LEFT).scale(0.9)
        lab1_ex[1].set_color(p1_col)
        lab1_ex[3].set_color(p1_col)
        lab2_ex[1].set_color(p2_col)
        lab2_ex[3].set_color(p2_col)
        self.play(
            ReplacementTransform(
                lab1,
                lab1_ex
            ),
            ReplacementTransform(
                lab2,
                lab2_ex
            ),
            run_time=2
        )
        self.slide_pause(2)

        eq_ex_a1 = eq_a.copy().scale(4 / 3).next_to(plane, DOWN, aligned_edge=LEFT)
        self.play(
            ReplacementTransform(
                eq_a.copy(),
                eq_ex_a1
            ),
            run_time=2
        )
        self.slide_pause(2)

        eq_ex_a2 = VGroup(
            MathTex("="),
            MathTex(
                "{", f"{y2}", "-", f"{y1}", "}", r"\over",
                "{", f"{x2}", "-", f"{x1}", "}"
            )
        ).arrange(RIGHT).next_to(eq_ex_a1, RIGHT)
        eq_ex_a2[1][1][:].set_color(p2_col)
        eq_ex_a2[1][3][:].set_color(p1_col)
        eq_ex_a2[1][7][:].set_color(p2_col)
        eq_ex_a2[1][9][:].set_color(p1_col)
        self.play(
            ReplacementTransform(
                eq_ex_a1.copy(),
                eq_ex_a2
            ),
            run_time=1
        )
        self.slide_pause(2)

        eq_ex_a3 = VGroup(
            MathTex("="),
            MathTex(
                "{", f"{dify}", "}", r"\over",
                "{", f"{difx}", "}"
            )
        ).arrange(RIGHT).next_to(eq_ex_a2, RIGHT)
        eq_ex_a3[1].set_color(a_col)
        self.play(
            ReplacementTransform(
                eq_ex_a2.copy(),
                eq_ex_a3
            ),
            run_time=1
        )
        self.slide_pause(2)

        eq_ex_a4 = MathTex(
            "=", f"{a_ex}"
        ).next_to(eq_ex_a3, RIGHT)
        eq_ex_a4[1].set_color(a_col)
        self.play(
            ReplacementTransform(
                eq_ex_a3.copy(),
                eq_ex_a4
            ),
            run_time=1
        )
        self.slide_pause(2)

        eq_ex_b1 = eq_b.copy().scale(4 / 3).next_to(plane, DOWN, aligned_edge=LEFT).shift(1.25 * DOWN)
        self.play(
            ReplacementTransform(
                eq_b.copy(),
                eq_ex_b1
            ),
            run_time=2
        )
        self.slide_pause(2)

        eq_ex_b2 = MathTex(
            "=", f"{y1}", "-", f"{a_ex}", r"\cdot", f"{x1}", ""
        ).next_to(eq_ex_b1, RIGHT)
        eq_ex_b2[1].set_color(p1_col)
        eq_ex_b2[3].set_color(a_col)
        eq_ex_b2[5].set_color(p1_col)
        self.play(
            ReplacementTransform(
                eq_ex_b1.copy(),
                eq_ex_b2
            ),
            run_time=1
        )
        self.slide_pause(2)

        eq_ex_b3 = MathTex(
            "=", f"{b_ex}"
        ).next_to(eq_ex_b2, RIGHT)
        eq_ex_b3[1].set_color(b_col)
        self.play(
            ReplacementTransform(
                eq_ex_b2.copy(),
                eq_ex_b3
            ),
            run_time=1
        )
        self.slide_pause(2)

        a_final = MathTex(
            f"a = {a_ex}"
        ).set_color(a_col).next_to(plane, DOWN, aligned_edge=LEFT)
        b_final = MathTex(
            f"b = {b_ex}"
        ).set_color(b_col).next_to(plane, DOWN, aligned_edge=LEFT).shift(0.50 * DOWN)
        self.play(
            ReplacementTransform(
                VGroup(
                    eq_ex_a1,
                    eq_ex_a2,
                    eq_ex_a3,
                    eq_ex_a4
                ),
                a_final
            ),
            ReplacementTransform(
                VGroup(
                    eq_ex_b1,
                    eq_ex_b2,
                    eq_ex_b3
                ),
                b_final
            ),
            run_time=1
        )
        self.slide_pause(2)

        graph = plane.plot(
            lambda x: b_ex + a_ex * x,
            x_range=[-2, 16.5, 1],
            color=YELLOW,
            stroke_width=1
        )
        eq = MathTex(
            rf"y = {a_ex} \cdot x + {b_ex}"
        ).next_to(graph, RIGHT).set_color(YELLOW)
        self.play(
            Create(
                graph
            ),
            run_time=2
        )
        self.slide_pause(2)
        self.play(
            Write(
                eq
            ),
            run_time=1
        )
        self.slide_pause(2)

        fade_out_all(self)
        play_title_reverse(self, title)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)


class ToPunktLinThumbnail(Scene):
    def construct(self):
        plane = NumberPlane(
            x_range=[-2, 16.5, 1],
            y_range=[-2, 12.5, 1],
            x_length=4.5,
            y_length=3.5,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 2,
                "stroke_opacity": 0.2
            },
        ).to_edge(UL)
        x1, x2 = 4, 12
        y1, y2 = 3, 7
        graph = plane.plot(
            lambda x: (y1-(y2-y1)/(x2-x1)*x1) + (y2-y1)/(x2-x1) * x,
            x_range=[-2, 16.5, 1],
            color=YELLOW,
            stroke_width=3
        )

        title = VGroup(
            Tex("To-Punkt-Formel for"), Tex("Lineære Funktioner", color=YELLOW)
        ).scale(0.8).arrange(RIGHT).next_to(plane, UP, aligned_edge=LEFT)
        p1_col = RED
        p2_col = BLUE
        eq_color_map = {
            "x_1": p1_col,
            "y_1": p1_col,
            "x_2": p2_col,
            "y_2": p2_col,
        }
        p1 = Dot().move_to(plane.c2p(x1, y1)).set_color(p1_col)
        p2 = Dot().move_to(plane.c2p(x2, y2)).set_color(p2_col)
        eq_a = VGroup(
            MathTex("a", "="),
            MathTex(
                "{y_2", "-", "y_1}", r"\over",
                "{x_2", "-", "x_1}"
            ).set_color_by_tex_to_color_map(eq_color_map)
        ).arrange(RIGHT).next_to(plane, RIGHT, aligned_edge=UP).shift(0.5*DOWN)
        eq_b = MathTex(
            "b", " = ", "y_1", "-", "a", r"\cdot", "x_1"
        ).set_color_by_tex_to_color_map(eq_color_map).next_to(eq_a, DOWN, aligned_edge=LEFT)
        # VGroup(title, eq_b, eq_a).next_to(plane, RIGHT)
        self.add(title, plane, eq_b, eq_a, graph, p1, p2)
        VGroup(title, plane, eq_b, eq_a, graph, p1, p2).scale(1.75).move_to(ORIGIN)
