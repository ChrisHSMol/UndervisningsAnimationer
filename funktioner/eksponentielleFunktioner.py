# from tarfile import data_filter

from manim import *
import sys
sys.path.append("../")
import numpy as np
import subprocess
from helpers import *

slides = True
if slides:
    from manim_slides import Slide

q = "h"
_RESOLUTION = {
    "ul": "426,240",
    "l": "854,480",
    "h": "1920,1080"
}
_FRAMERATE = {
    "ul": 5,
    "l": 15,
    "h": 60
}


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


class ToPunktExpThumbnail(Scene):
    def construct(self):
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
        }
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
        ).to_edge(DL).scale(1.25)
        points = VGroup(
            Dot(radius=0.15).move_to(plane.c2p(x1, y1)).set_color(p1_col),
            Dot(radius=0.15).move_to(plane.c2p(x2, y2)).set_color(p2_col)
        ).set_z_index(3)

        eqs = VGroup(
            MathTex(
                "a", "=", "\\sqrt", "[", "x_2", "-", "x_1", "]{", "y_2", "\\over", "y_1", "}"
            ).set_color_by_tex_to_color_map(eq_color_map),
            MathTex(
                "b", "=", "{", "y_1", "\\over", "a", "^{x_1}", "}"
            ).set_color_by_tex_to_color_map(eq_color_map)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT)
        eqs[0][2].set_color(p2_col)
        eqs[0][4].set_color(p1_col)
        eqs[0][6:8].set_color(p2_col)
        eqs[0][8:11].set_color(p1_col)
        lines = VGroup(
            Line(start=LEFT, end=1.5*RIGHT).scale(0.25).next_to(eqs[0], UR, buff=0).shift(0.6*LEFT)
        )
        lines.add(lines[0].copy().scale(0.75).shift(0.575*DOWN))
        VGroup(eqs, lines).scale(1.5).next_to(plane, RIGHT, aligned_edge=UP)
        diff = x2 - x1
        frac = y2 / y1
        a_ex = frac ** (1 / diff)
        b_ex = y1 / (a_ex ** x1)
        graph = plane.plot(
            lambda x: b_ex * a_ex ** x,
            x_range=[-2, 16.5, 1],
            color=YELLOW,
            stroke_width=2
        )
        title = Tex("To-Punkt-Formel for ", "Eksponentielle Funktioner").scale(1.25).to_edge(UL, buff=0.1)
        title[1].set_color(YELLOW)
        self.add(plane, points, eqs, lines, graph, title)


class TerningHenfald(MovingCameraScene, Slide if slides else Scene):
    def construct(self):
        self.terninger_henfald()
        self.slide_pause(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t=t, slides_bool=slides_bool)

    def get_random_die(self, **kwargs):
        value = np.random.randint(1, 7)
        return DieFace(value=value, fill_color=BLUE_C if value != 6 else RED_C, **kwargs)

    def get_distributed_numbers(self, size, distribution):
        if not isinstance(distribution, (list, tuple, np.ndarray)):
            raise Exception(f"prop_limits must be of type list")
        results = []
        for num in np.random.uniform(size=size):
            for i, lim in enumerate(distribution):
                if num < lim:
                    results.append(i + 1)
                    break
        return results

    def get_distributed_die(self, value, **kwargs):
        return DieFace(value=value, fill_color=BLUE_C if value != 6 else RED_C, **kwargs)

    def terninger_henfald(self):
        n_dice = 1000
        n_throws = 25
        n_cols = 15
        distribution = [(n + 1) / 6 for n in range(6)]
        # distribution = [0.1, 0.2, 0.3, 0.4, 0.5, 1.0]

        xmin, xmax, xstep = 0, n_throws * 1.2, (n_throws * 1.2) // 15
        ymin, ymax, ystep = 0, n_dice * 1.25, (n_dice * 1.25) // 10
        plane = Axes(
            x_range=(xmin, xmax+xstep, xstep),
            y_range=(ymin, ymax+ystep, ystep),
            x_length=9,
            y_length=6,
            axis_config={
                'tip_shape': StealthTip
            },
            # y_axis_config={
            #     "numbers_to_include": np.arange(ymin, ymax+ystep, ystep),
            # },
            # x_axis_config={
            #     "numbers_to_include": np.arange(xmin, xmax+xstep, xstep),
            # },
        ).to_edge(DR)
        plane[0].add_labels({v: Integer(v) for v in plane[0].get_tick_range()})
        plane[1].add_labels({v: Integer(v) for v in plane[1].get_tick_range()})
        data_points = VGroup(
            Dot(plane.c2p(0, n_dice), radius=0.1, stroke_width=0, fill_color=RED_C, fill_opacity=1)
        )
        counter = VGroup(
            Tex("Antal terninger i spil: "),
            Integer(n_dice)
        ).arrange(DOWN, aligned_edge=RIGHT).to_edge(UR)
        self.add(plane, data_points, counter)
        self.slide_pause(1)
        for i in range(n_throws):
            results = self.get_distributed_numbers(counter[1].get_value(), distribution)
            terninger = VGroup(
                *[
                    # self.get_random_die(stroke_width=0.1) for _ in range(counter[1].get_value())
                    self.get_distributed_die(val, stroke_width=0.1) for val in results
                ]
            ).arrange_in_grid(
                int(np.ceil(n_dice/n_cols)), n_cols
            # ).scale_to_fit_height(
            #     self.camera.frame.get_height() / 1.5
            # ).scale_to_fit_width(
            #     self.camera.frame.get_width() / 3
            ).scale(min(
                self.camera.frame.get_height() / (1.5*int(np.ceil(counter[1].get_value()/n_cols))),
                self.camera.frame.get_width() / (6*n_cols)
            )).to_edge(DL)
            self.remove(counter)
            counter = VGroup(
                Tex("Antal terninger i spil: "),
                Integer(len([d for d in terninger if d.value != 6]))
            ).arrange(DOWN, aligned_edge=RIGHT).to_edge(UR)
            data_points.add(
                data_points[0].copy().move_to(plane.c2p(i + 1, counter[1].get_value()))
            )
            self.add(terninger, counter, data_points[-1])
            self.slide_pause(1)
            self.remove(terninger, counter)
            if counter[1].get_value() <= 1:
                break

        fit = np.exp(
            np.polyfit(
                [plane.p2c(p.get_center())[0] for p in data_points],
                [np.log(plane.p2c(p.get_center())[1]) for p in data_points],
                1
            )
        )
        graph = plane.plot(
            lambda x: fit[1] * fit[0]**x,
            x_range=[xmin-5, xmax],
            stroke_color=data_points[0].get_color()
        ).set_z_index(2)
        params = VGroup(
            Tex(f"a = {fit[0]:.4f}"),
            Tex(f"b = {fit[1]:.4f}"),
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(DL)
        # self.add(graph, params)
        self.play(
            Create(graph),
            Write(params)
        )


if __name__ == "__main__":
    classes = [
        # ToPunktExp,
        TerningHenfald
    ]
    for cls in classes:
        class_name = cls.__name__
        command = rf"manim {sys.argv[0]} {class_name} -p --resolution={_RESOLUTION[q]} --frame_rate={_FRAMERATE[q]}"
        scene_marker(rf"RUNNNING:    {command}")
        subprocess.run(command)
        if slides and q == "h":
            command = rf"manim-slides convert {class_name} {class_name}.html"
            scene_marker(rf"RUNNNING:    {command}")
            subprocess.run(command)
            if class_name+"Thumbnail" in dir():
                command = rf"manim {sys.argv[0]} {class_name}Thumbnail -pq{q} -o {class_name}Thumbnail.png"
                scene_marker(rf"RUNNNING:    {command}")
                subprocess.run(command)
