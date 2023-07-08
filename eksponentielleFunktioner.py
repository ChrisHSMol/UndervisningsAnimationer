from manim import *
import sys
sys.path.append("../")
from helpers import *
slides = True
if slides:
    from manim_slides import Slide


class ToPunktExp(Slide if slides else Scene):
    def construct(self):
        def p2p_anim(mob1, mob2, tex1, tex2=None, index=0):
            if tex2 is None:
                tex2 = tex1
            return ReplacementTransform(
                mob1.get_parts_by_tex(tex1)[index],
                mob2.get_parts_by_tex(tex2)[index],
            )

        def p2p_anim_copy(mob1, mob2, tex1, tex2=None, index=0):
            if tex2 is None:
                tex2 = tex1
            return TransformFromCopy(
                mob1.get_parts_by_tex(tex1)[index],
                mob2.get_parts_by_tex(tex2)[index],
            )

        def maybe_round(val, dec=2):
            if val == int(val):
                return int(val)
            else:
                return np.round(val, dec)

        def overlap(lst1, lst2):
            lst3 = [value for value in lst1 if value in lst2]
            return lst3

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

        diff = maybe_round(x2 - x1)
        frac = maybe_round(y2 / y1)
        a_ex = maybe_round(frac ** (1 / diff))
        b_ex = maybe_round(y1 / (a_ex ** x1))

        self.slide_pause(0.5)
        title = VGroup(
            Tex("Topunktsformlen for en"),
            Tex("Eksponentiel funktion")
        ).arrange(DOWN, aligned_edge=LEFT)
        title[1][:12].set_color(YELLOW)
        title_ul = Underline(title)
        title_ul_box = Rectangle(
            width=title.width,
            height=title.height * 1.6
        ).next_to(
            title_ul, DOWN, buff=0
        ).set_style(fill_opacity=1, stroke_width=0, fill_color=BLACK)
        ul_group = VGroup(title_ul, title_ul_box)
        self.play(Write(title), run_time=0.5)
        self.wait(2)
        self.play(GrowFromCenter(title_ul))
        self.add(ul_group)
        self.play(ul_group.animate.shift(UP * title_ul_box.height))
        self.play(ShrinkToCenter(title_ul))
        self.remove(ul_group, title)
        self.wait(2)
        # self.play(Unwrite(title), run_time=0.5)

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
        # self.wait(2)
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
            "y_1", " = ", "b", "\\cdot", "a", "^{x_1}"
        ).set_color_by_tex_to_color_map(
            eq_color_map
        ).scale(0.75).move_to(3 * UR)
        eq2 = MathTex(
            "y_2", " = ", "b", "\\cdot", "a", "^{x_2}"
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

        tp1 = MathTex(
            "{y_2", "\\over", "y_1}",
            " = ",
            "{b", "\\cdot", "a", "^{x_2}", "\\over", "b", "\\cdot", "a", "^{x_1}}"
        ).set_color_by_tex_to_color_map(
            eq_color_map
        ).scale(0.75).move_to(3 * RIGHT + 2 * UP)
        self.play(
            DrawBorderThenFill(tp1)
        )
        # self.wait(2)
        self.slide_pause(2)

        self.play(
            Circumscribe(
                tp1.get_parts_by_tex("b"),
                fade_out=True
            ),
            run_time=2
        )
        # self.wait()
        self.slide_pause(1)

        tp2 = MathTex(
            "{y_2", "\\over", "y_1}",
            " = ",
            "{a", "^{x_2}", "\\over", "a", "^{x_1}}"
        ).set_color_by_tex_to_color_map(
            eq_color_map
        ).scale(0.75).move_to(3 * RIGHT + 1.00 * UP)
        self.play(
            ReplacementTransform(
                tp1.copy(),
                tp2
            )
        )
        # self.wait(2)
        self.slide_pause(2)

        self.play(
            Circumscribe(
                tp2.get_parts_by_tex("a"),
                fade_out=True
            ),
            run_time=2
        )
        # self.wait()
        self.slide_pause(1)

        tp3 = MathTex(
            "{y_2", "\\over", "y_1}",
            " = ",
            "a", "^{x_2", " - ", "x_1}"
        ).set_color_by_tex_to_color_map(
            eq_color_map
        ).scale(0.75).move_to(3 * RIGHT + 0.00 * UP)
        self.play(
            ReplacementTransform(
                tp2.copy(),
                tp3
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

        # tp4 = MathTex(
        #     "\\sqrt", "[x_2", " - ", "x_1]",
        #     "{y_2", "\\over", "y_1}",
        #     " = ",
        #     "a"
        # ).set_color_by_tex_to_color_map(
        #     eq_color_map
        # ).scale(0.75).move_to(3*RIGHT - 1.00*UP)
        # tp4 = MathTex(
        #     "\\sqrt[x_2 - x_1]{y_2 \\over y_1} = a"
        # ).scale(0.75).move_to(3*RIGHT - 1.00*UP)
        # tp4[0][0:2].set_color(p2_col)
        # tp4[0][3:5].set_color(p1_col)
        # tp4[0][7:9].set_color(p2_col)
        # tp4[0][10:12].set_color(p1_col)
        # tp4[0][-1].set_color(a_col)
        tp4 = MathTex(
            "\\sqrt", "[", "x_2", "-", "x_1", "]{",
            "y_2", "\\over", "y_1", "}",
            "=", "a"
        ).scale(0.75).move_to(3 * RIGHT - 1.00 * UP)
        tp4[0][:].set_color(p2_col)
        tp4[2][:].set_color(p1_col)
        tp4[4][1:].set_color(p2_col)
        tp4[5][:1].set_color(p2_col)
        tp4[6][1:].set_color(p1_col)
        tp4[7][:1].set_color(p1_col)
        tp4[8][1:].set_color(a_col)
        self.play(
            ReplacementTransform(
                tp3.copy(),
                tp4
            )
        )
        # self.wait(2)
        self.slide_pause(2)

        # eq_a = MathTex(
        #     "a = \\sqrt[x_2 - x_1]{y_2 \\over y_1}"
        # ).scale(0.75).move_to(3*RIGHT - 1.00*UP)
        # eq_a[0][2:4].set_color(p2_col)
        # eq_a[0][5:7].set_color(p1_col)
        # eq_a[0][9:11].set_color(p2_col)
        # eq_a[0][12:14].set_color(p1_col)
        # eq_a[0][0].set_color(a_col)
        eq_a = MathTex(
            "a", "=",
            "\\sqrt", "[", "x_2", "-", "x_1", "]{",
            "y_2", "\\over", "y_1", "}"
        ).scale(0.75).move_to(3 * RIGHT - 1.00 * UP)
        eq_a[0][:].set_color(a_col)
        eq_a[2][:].set_color(p2_col)
        eq_a[4][:].set_color(p1_col)
        eq_a[6][1:].set_color(p2_col)
        eq_a[7][:1].set_color(p2_col)
        eq_a[8][1:].set_color(p1_col)
        eq_a[9][:1].set_color(p1_col)
        self.play(
            *[
                p2p_anim(tp4, eq_a, tex.tex_string) for tex in eq_a
            ]
        )
        # self.wait(2)
        self.slide_pause(2)

        self.play(
            Circumscribe(
                eq_a,
                fade_out=True
            ),
            run_time=2
        )
        # self.wait(2)
        self.slide_pause(2)

        self.play(
            eq_a.animate.next_to(eq2, DOWN),
            Uncreate(
                VGroup(
                    tp1,
                    tp2,
                    tp3,
                )
            ),
            run_time=1
        )
        # self.wait(2)
        self.slide_pause(2)

        # =====================================================================
        # =====================================================================
        # =====================================================================

        tpb1 = eq1.copy().scale(1.33).move_to(2 * RIGHT + 2 * UP)
        self.play(
            ReplacementTransform(
                eq1.copy(),
                tpb1
            ),
            run_time=2
        )
        # self.wait(2)
        self.slide_pause(2)
        self.play(
            Circumscribe(
                VGroup(
                    tpb1.get_parts_by_tex("a"),
                    tpb1.get_parts_by_tex("{x_1}")
                ),
                fade_out=True
            ),
            run_time=2
        )
        # self.wait(2)
        self.slide_pause(2)

        tpb2 = MathTex(
            "{", "y_1", "\\over", "a", "^{x_1}", "}", " = ", "b"
        ).set_color_by_tex_to_color_map(
            eq_color_map
        ).move_to(2 * RIGHT + 1 * UP)
        self.play(
            p2p_anim_copy(tpb1, tpb2, "y_1"),
            p2p_anim_copy(tpb1, tpb2, "x_1"),
            p2p_anim_copy(tpb1, tpb2, "a"),
            p2p_anim_copy(tpb1, tpb2, "b"),
            p2p_anim_copy(tpb1, tpb2, "="),
            p2p_anim_copy(tpb1, tpb2, "\\cdot", "\\over"),
            run_time=2
        )
        # self.wait(2)
        self.slide_pause(2)

        eq_b = MathTex(
            "b", " = ", "{", "y_1", "\\over", "a", "^{x_1}", "}"
        ).set_color_by_tex_to_color_map(
            eq_color_map
        ).move_to(2 * RIGHT + 1 * UP)
        self.play(
            *[
                p2p_anim(tpb2, eq_b, tex.tex_string) for tex in eq_b
            ],
            run_time=2
        )
        # self.wait(2)
        self.slide_pause(2)
        self.play(
            Circumscribe(
                eq_b,
                fade_out=True
            ),
            run_time=2
        )
        # self.wait(2)
        self.slide_pause(2)

        self.play(
            eq_b.animate.scale(0.75).next_to(eq_a, DOWN, aligned_edge=LEFT),
            Uncreate(
                tpb1
            ),
            run_time=1
        )
        # self.wait(2)
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
        # self.wait(2)
        self.slide_pause(2)

        eq_ex_a1 = eq_a.copy().scale(4 / 3).next_to(plane, DOWN, aligned_edge=LEFT)  # .shift(1.75 * LEFT)
        # eq_ex_a1 = eq_a.copy().scale(4/3).move_to(DL).shift(2.00 * UP)
        self.play(
            ReplacementTransform(
                eq_a.copy(),
                eq_ex_a1
            ),
            run_time=2
        )
        # self.wait(2)
        self.slide_pause(2)

        eq_ex_a2 = MathTex(
            "=",
            "\\sqrt", "[", f"{x2}", "-", f"{x1}", "]{",
            f"{y2}", "\\over", f"{y1}", "}"
        ).next_to(eq_ex_a1, RIGHT)
        eq_ex_a2[1][:].set_color(p2_col)
        eq_ex_a2[3][:1].set_color(p1_col)
        eq_ex_a2[5][:].set_color(p2_col)
        eq_ex_a2[7][:].set_color(p1_col)
        self.play(
            ReplacementTransform(
                eq_ex_a1.copy(),
                eq_ex_a2
            ),
            run_time=1
        )
        # self.wait(2)
        self.slide_pause(2)

        eq_ex_a3 = MathTex(
            "=",
            "\\sqrt", "[", f"{diff}", "]{",
            f"{frac}", "}"
        ).next_to(eq_ex_a2, RIGHT)
        eq_ex_a3[1][:1].set_color(a_col)
        eq_ex_a3[3][:].set_color(a_col)
        eq_ex_a3[-2][:].set_color(a_col)
        self.play(
            ReplacementTransform(
                eq_ex_a2.copy(),
                eq_ex_a3
            ),
            run_time=1
        )
        # self.wait(2)
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
        # self.wait(2)
        self.slide_pause(2)

        eq_ex_b1 = eq_b.copy().scale(4 / 3).next_to(plane, DOWN, aligned_edge=LEFT).shift(1.25 * DOWN)
        # eq_ex_b1 = eq_b.copy().scale(4/3).move_to(DL).shift(1.00 * UP)
        self.play(
            ReplacementTransform(
                eq_b.copy(),
                eq_ex_b1
            ),
            run_time=2
        )
        # self.wait(2)
        self.slide_pause(2)

        eq_ex_b2 = MathTex(
            "={", f"{y1}", "\\over", f"{a_ex}", f"^{x1}", "}"
        ).next_to(eq_ex_b1, RIGHT)
        eq_ex_b2[1].set_color(p1_col)
        eq_ex_b2[3].set_color(a_col)
        eq_ex_b2[4].set_color(p1_col)
        self.play(
            ReplacementTransform(
                eq_ex_b1.copy(),
                eq_ex_b2
            ),
            run_time=1
        )
        # self.wait(2)
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
        # self.wait(2)
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
        # self.wait(2)
        self.slide_pause(2)

        graph = plane.plot(
            lambda x: b_ex * a_ex ** x,
            x_range=[-2, 16.5, 1],
            color=YELLOW,
            stroke_width=1
        )
        eq = MathTex(
            f"y = {b_ex} \\cdot {a_ex}^x"
        ).next_to(graph, RIGHT).set_color(YELLOW)
        self.play(
            Create(
                graph
            ),
            run_time=2
        )
        # self.wait(2)
        self.slide_pause(2)
        self.play(
            Write(
                eq
            ),
            run_time=1
        )
        # self.wait(2)
        self.slide_pause(2)

        fade_out_all(self)
        play_title_reverse(self, title)

    def slide_pause(self, t=1.0, slides_bool=slides):
        if slides_bool:
            indicator = Dot(fill_opacity=0.25, fill_color=GREEN).scale(0.5).to_edge(DR, buff=0.1)
            self.play(FadeIn(indicator), run_time=0.25)
            xs_pause(self)
            self.pause()
            self.play(FadeOut(indicator), run_time=0.25)
        else:
            self.wait(t)




