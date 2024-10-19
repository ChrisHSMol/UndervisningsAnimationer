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


class SumOgDifferensAfFunktioner(MovingCameraScene, Slide if slides else Scene):
    def construct(self):
        self.sum_af_funktioner()
        self.wait(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t=t, slides_bool=slides_bool)

    def get_cmap(self):
        return {"f": BLUE, "g": YELLOW, "f+g": GREEN, "f-g": RED_B, "g-f": RED_D}

    def sum_af_funktioner(self):
        cmap = self.get_cmap()
        xmin, xmax, xstep = -8, 8, 1
        ymin, ymax, ystep = -8, 8, 1
        width = 14
        plane = NumberPlane(
            x_range=[xmin, xmax, xstep],
            y_range=[ymin, ymax, ystep],
            x_length=width,
            y_length=9/16 * width,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 2,
                "stroke_opacity": 0.3
            },
            axis_config={"include_numbers": True, "include_ticks": True},
            x_axis_config={"label_direction": DOWN},
            y_axis_config={"label_direction": LEFT}
        )
        self.play(
            DrawBorderThenFill(plane)
        )
        self.slide_pause()

        f = plane.plot(
            lambda x: -0.5 * x + 2,
            stroke_color=cmap["f"]
        )
        f_label = MathTex(
            "{{f}}(x) = -0.5 \\cdot x + 2"
        ).set_color_by_tex_to_color_map(cmap).to_edge(DR).set_z_index(4)
        f_box = get_background_rect(f_label)
        g = plane.plot(
            lambda x: x - 1,
            stroke_color=cmap["g"]
        )
        g_label = MathTex(
            "{{g}}(x) = x - 1"
        ).set_color_by_tex_to_color_map(cmap).next_to(f_label, UP, aligned_edge=LEFT).set_z_index(4)
        g_box = get_background_rect(g_label)
        self.play(
            LaggedStart(
                *[LaggedStart(
                    Create(graph),
                    Write(label),
                    FadeIn(box),
                    lag_ratio=0.25
                ) for graph, label, box in zip([f, g], [f_label, g_label], [f_box, g_box])],
                # Create(f),
                # Create(g),
                lag_ratio=0.75
            )
        )
        self.slide_pause()

        x_ticks = plane[2].get_tick_range()
        f_lines = VGroup(*[
            Line(
                start=plane.c2p(x_tick, 0), end=plane.c2p(x_tick, f.underlying_function(x_tick)), stroke_color=cmap["f"]
            ) for x_tick in x_ticks
        ])
        g_lines = VGroup(*[
            Line(
                start=plane.c2p(x_tick, 0), end=plane.c2p(x_tick, g.underlying_function(x_tick)), stroke_color=cmap["g"]
            ) for x_tick in x_ticks
        ])
        fpg_lines = VGroup(*[
            Line(
                start=plane.c2p(x_tick, 0),
                end=plane.c2p(x_tick, f.underlying_function(x_tick) + g.underlying_function(x_tick)),
                stroke_color=cmap["f+g"]
            ) for x_tick in x_ticks
        ])
        fpg_dots = VGroup(*[
            Dot(
                fpg_line.get_end(),
                fill_color=cmap["f+g"]
            ) for fpg_line in fpg_lines
        ])
        f_line_labels = VGroup(*[
            DecimalNumber(
                number=f.underlying_function(x_tick),
                num_decimal_places=0 if f.underlying_function(x_tick).is_integer() else 1,
                include_sign=True,
                color=cmap["f"]
            ).scale(0.75).next_to(
                f_line, np.sign(x_tick) * LEFT, buff=0.1
            ) for f_line, x_tick in zip(f_lines, x_ticks)
        ])
        g_line_labels = VGroup(*[
            DecimalNumber(
                number=g.underlying_function(x_tick),
                num_decimal_places=0 if g.underlying_function(x_tick).is_integer() else 1,
                include_sign=True,
                color=cmap["g"]
            ).scale(0.75).next_to(
                g_line, np.sign(x_tick) * LEFT, buff=0.1
            ) for g_line, x_tick in zip(g_lines, x_ticks)
        ])
        fpg_line_labels = VGroup(*[
            DecimalNumber(
                number=f.underlying_function(x_tick) + g.underlying_function(x_tick),
                num_decimal_places=0 if (
                            f.underlying_function(x_tick) + g.underlying_function(x_tick)).is_integer() else 1,
                include_sign=True,
                color=cmap["f+g"]
            ).scale(0.75).next_to(
                fpg_line, np.sign(x_tick) * LEFT, buff=0.1
            ) for fpg_line, x_tick in zip(fpg_lines, x_ticks)
        ])

        i_separator = 4
        for i, x_tick in enumerate(x_ticks[:i_separator]):
            rt_modifier = np.exp(-i * 0.1)
            self.play(
                LaggedStart(
                    *[LaggedStart(
                        Create(graph),
                        Write(label),
                        lag_ratio=0.25
                    ) for graph, label in zip([f_lines[i], g_lines[i]], [f_line_labels[i], g_line_labels[i]])],
                    lag_ratio=0.5
                ),
                run_time=1 * rt_modifier
            )
            self.slide_pause(rt_modifier)

            self.play(
                ReplacementTransform(
                    VGroup(f_lines[i], g_lines[i]),
                    fpg_lines[i]
                ),
                ReplacementTransform(
                    VGroup(f_line_labels[i], g_line_labels[i]),
                    fpg_line_labels[i]
                ),
                run_time=1 * rt_modifier
            )
            self.slide_pause(rt_modifier)

            self.play(
                ReplacementTransform(
                    fpg_lines[i], fpg_dots[i]
                ),
                FadeOut(fpg_line_labels[i], run_time=0.5),
                run_time=1 * rt_modifier
            )
            self.slide_pause(rt_modifier)

        self.play(
            LaggedStart(
                *[LaggedStart(
                    Create(fgraph),
                    Write(flabel),
                    Create(ggraph),
                    Write(glabel),
                    lag_ratio=0.25
                ) for fgraph, flabel, ggraph, glabel in zip(
                    f_lines[i_separator:], f_line_labels[i_separator:],
                    g_lines[i_separator:], g_line_labels[i_separator:]
                )],
                lag_ratio=0.1
            ),
            run_time=rt_modifier
        )
        self.slide_pause(rt_modifier)

        self.play(
            *[LaggedStart(
                ReplacementTransform(
                    VGroup(f_line, g_line),
                    fpg_line
                ),
                ReplacementTransform(
                    VGroup(f_line_label, g_line_label),
                    fpg_line_label
                ),
                lag_ratio=0.25
            ) for f_line, g_line, fpg_line, f_line_label, g_line_label, fpg_line_label in zip(
                f_lines[i_separator:], g_lines[i_separator:], fpg_lines[i_separator:],
                f_line_labels[i_separator:], g_line_labels[i_separator:], fpg_line_labels[i_separator:]
            )],
            run_time=1
        )
        self.slide_pause(rt_modifier)

        self.play(
            *[LaggedStart(
                ReplacementTransform(
                    fpg_line, fpg_dot
                ),
                FadeOut(fpg_line_label, run_time=0.5),
                lag_ratio=0.25
            ) for fpg_line, fpg_dot, fpg_line_label in zip(
                fpg_lines[i_separator:], fpg_dots[i_separator:], fpg_line_labels[i_separator:]
            )],
            run_time=1
        )
        self.slide_pause(rt_modifier)

        fpg = plane.plot(
            lambda x: f.underlying_function(x) + g.underlying_function(x),
            stroke_color=cmap["f+g"]
        )
        fpg_label = MathTex(
            "{{f}}(x) + {{g}}(x) = ({{-0.5 \\cdot x + 2}}) + ({{x - 1}})"
        ).set_color_by_tex_to_color_map(cmap).to_edge(DL).set_z_index(4)
        fpg_label[4].set_color(cmap["f"])
        fpg_label[6].set_color(cmap["g"])
        fpg_box = get_background_rect(fpg_label)
        self.play(
            Create(fpg),
            Write(fpg_label),
            FadeIn(fpg_box),
            f.animate.set_style(stroke_opacity=0.25),
            g.animate.set_style(stroke_opacity=0.25)
        )
        self.slide_pause()

        fpg_label_full = MathTex(
            "{{(f+g)}}(x) = 0.5 \\cdot x + 1"
        ).set_color_by_tex_to_color_map(cmap).to_edge(DL).set_z_index(4)
        fpg_full_box = get_background_rect(fpg_label_full)
        self.play(
            TransformMatchingShapes(fpg_label, fpg_label_full, transform_mismatches=False),
            ReplacementTransform(fpg_box, fpg_full_box)
        )
        self.slide_pause()


class ProduktOgForholdAfFunktioner(SumOgDifferensAfFunktioner):
    def construct(self):
        self.produkt_af_funktioner()
        self.roots_of_products()
        self.wait(5)

    def get_cmap(self):
        return {"f": BLUE, "g": YELLOW, "f*g": GREEN}

    def produkt_af_funktioner(self):
        cmap = self.get_cmap()
        xmin, xmax, xstep = -8, 8, 1
        ymin, ymax, ystep = -8, 8, 1
        width = 14
        plane = NumberPlane(
            x_range=[xmin, xmax, xstep],
            y_range=[ymin, ymax, ystep],
            x_length=width,
            y_length=9/16 * width,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 2,
                "stroke_opacity": 0.3
            },
            axis_config={"include_numbers": True, "include_ticks": True},
            x_axis_config={"label_direction": DOWN},
            y_axis_config={"label_direction": LEFT}
        )
        self.play(
            DrawBorderThenFill(plane)
        )
        self.slide_pause()

        f = plane.plot(
            lambda x: -0.5 * x + 2,
            stroke_color=cmap["f"]
        )
        f_label = MathTex(
            "{{f}}(x) = -0.5 \\cdot x + 2"
        ).set_color_by_tex_to_color_map(cmap).to_edge(UL).set_z_index(4)
        f_box = get_background_rect(f_label)
        g = plane.plot(
            lambda x: x - 1,
            stroke_color=cmap["g"]
        )
        g_label = MathTex(
            "{{g}}(x) = x - 1"
        ).set_color_by_tex_to_color_map(cmap).next_to(f_label, DOWN, aligned_edge=LEFT).set_z_index(4)
        g_box = get_background_rect(g_label)
        self.play(
            LaggedStart(
                *[LaggedStart(
                    Create(graph),
                    Write(label),
                    FadeIn(box),
                    lag_ratio=0.25
                ) for graph, label, box in zip([f, g], [f_label, g_label], [f_box, g_box])],
                # Create(f),
                # Create(g),
                lag_ratio=0.75
            )
        )
        self.slide_pause()

        # x_ticks = plane[2].get_tick_range()
        x_ticks = np.arange(-2, 7, 1)
        f_lines = VGroup(*[
            Line(
                start=plane.c2p(x_tick, 0), end=plane.c2p(x_tick, f.underlying_function(x_tick)), stroke_color=cmap["f"]
            ) for x_tick in x_ticks
        ])
        g_lines = VGroup(*[
            Line(
                start=plane.c2p(x_tick, 0), end=plane.c2p(x_tick, g.underlying_function(x_tick)), stroke_color=cmap["g"]
            ) for x_tick in x_ticks
        ])
        f_line_labels = VGroup(*[
            DecimalNumber(
                number=f.underlying_function(x_tick),
                num_decimal_places=0 if f.underlying_function(x_tick).is_integer() else 1,
                include_sign=True,
                color=cmap["f"]
            ).scale(0.5).next_to(
                f_line, np.sign(x_tick) * LEFT, buff=0.1
            ) for f_line, x_tick in zip(f_lines, x_ticks)
        ])
        g_line_labels = VGroup(*[
            DecimalNumber(
                number=g.underlying_function(x_tick),
                num_decimal_places=0 if g.underlying_function(x_tick).is_integer() else 1,
                include_sign=True,
                color=cmap["g"]
            ).scale(0.5).next_to(
                g_line, np.sign(x_tick) * LEFT, buff=0.1
            ) for g_line, x_tick in zip(g_lines, x_ticks)
        ])
        self.play(
            LaggedStart(
                LaggedStart(*[Create(fline) for fline in f_lines], lag_ratio=0.1),
                LaggedStart(*[Create(gline) for gline in g_lines], lag_ratio=0.1),
                LaggedStart(*[Write(flabel) for flabel in f_line_labels], lag_ratio=0.1),
                LaggedStart(*[Write(glabel) for glabel in g_line_labels], lag_ratio=0.1),
                lag_ratio=0.25
            )
        )

        produkt_udr = VGroup(
            *[
                MathTex("(", flabel.get_value(), r") \cdot (", glabel.get_value(), ")").scale(0.4).next_to(
                    fline if f.underlying_function(x_tick) < g.underlying_function(x_tick) else gline, DOWN
                ) for flabel, glabel, fline, gline, x_tick in zip(
                    f_line_labels, g_line_labels, f_lines, g_lines, x_ticks
                )
            ]
        )
        for udr in produkt_udr:
            udr[1].set_color(f_line_labels[0].get_color())
            udr[3].set_color(g_line_labels[0].get_color())
        self.play(
            *[LaggedStart(
                ReplacementTransform(
                    VGroup(flabel, glabel), udr
                ),
                lag_ratio=0.25
            ) for flabel, glabel, udr in zip(f_line_labels, g_line_labels, produkt_udr)]
        )
        self.slide_pause()

        produkt = VGroup(*[
            DecimalNumber(
                number=f.underlying_function(x_tick) * g.underlying_function(x_tick),
                num_decimal_places=2,
                include_sign=True,
                color=cmap["f*g"]
            ).scale(0.5).move_to(udr) for x_tick, udr in zip(x_ticks, produkt_udr)
        ])
        self.play(
            *[LaggedStart(
                ReplacementTransform(
                    udr, res
                ),
                lag_ratio=0.25
            ) for udr, res in zip(produkt_udr, produkt)],
            FadeOut(f_lines),
            FadeOut(g_lines)
        )
        self.slide_pause()

        fgg_points = VGroup(*[
            Dot(
                plane.c2p(x_tick, res.get_value()),
                fill_color=cmap["f*g"]
            ) for x_tick, res in zip(x_ticks, produkt)
        ])
        self.play(
            *[LaggedStart(
                ReplacementTransform(
                    res, point
                ),
                lag_ratio=0.25
            ) for res, point in zip(produkt, fgg_points)],
            f.animate.set_style(stroke_opacity=0.25),
            g.animate.set_style(stroke_opacity=0.25)
        )
        self.slide_pause()

        fgg = plane.plot(
            lambda x: f.underlying_function(x) * g.underlying_function(x),
            stroke_color=cmap["f*g"]
        )
        self.play(
            Create(fgg)
        )
        self.slide_pause()

        fgg_label0 = MathTex(
            "{{f}}(x) \\cdot {{g}}(x) = ({{-0.5 \\cdot x + 2}}) \\cdot ({{x - 1}})"
        ).set_color_by_tex_to_color_map(cmap).scale(0.8).next_to(g_label, DOWN, aligned_edge=LEFT).set_z_index(4)
        fgg_label0[4].set_color(cmap["f"])
        fgg_label0[6].set_color(cmap["g"])
        fgg_box0 = get_background_rect(fgg_label0)
        self.play(
            Write(fgg_label0),
            FadeIn(fgg_box0)
        )
        self.slide_pause()

        fgg_label1 = MathTex(
            "{{f}}(x) \\cdot {{g}}(x) = (",
            r"-0.5 \cdot x", r")\cdot(", "x", ") + (",
            r"-0.5 \cdot x", r")\cdot(", "-1", ") + (",
            "+2", r") \cdot (", "x", ") + (",
            "+2", r") \cdot (", "-1", ")",
        ).set_color_by_tex_to_color_map(cmap).scale(0.8).next_to(fgg_label0, DOWN, aligned_edge=LEFT).set_z_index(4)
        for i in [4, 8, 12, 16]:
            fgg_label1[i].set_color(cmap["f"])
        for i in [6, 10, 14, 18]:
            fgg_label1[i].set_color(cmap["g"])
        fgg_box1 = get_background_rect(fgg_label1)
        self.play(
            # ReplacementTransform(fgg_label0.copy(), fgg_label1),
            TransformMatchingTex(fgg_label0.copy(), fgg_label1),
            FadeIn(fgg_box1)
        )
        self.slide_pause()

        fgg_label2 = MathTex(
            "{{f}}(x) \\cdot {{g}}(x) = ",
            r"-0.5 \cdot x^2", " + ",
            r"0.5 \cdot x", " + ",
            r"2 \cdot x", " - ",
            "2",
        ).set_color_by_tex_to_color_map(cmap).scale(0.8).next_to(fgg_label1, DOWN, aligned_edge=LEFT).set_z_index(4)
        for i in [4, 6, 8, 10]:
            fgg_label2[i].set_color(cmap["f*g"])
        fgg_box2 = get_background_rect(fgg_label2)
        self.play(
            # ReplacementTransform(fgg_label1.copy(), fgg_label2),
            TransformMatchingTex(fgg_label1.copy(), fgg_label2),
            FadeIn(fgg_box2)
        )
        self.slide_pause()

        fgg_label = MathTex(
            "({{f \\cdot g}})(x) = ",
            r"-0.5 \cdot x^2", " + ",
            r"2.5 \cdot x", " + ",
            "2",
        ).next_to(fgg_label2, DOWN, aligned_edge=LEFT).set_z_index(4)
        fgg_label[1].set_color(cmap["f*g"])
        fgg_label[3:].set_color(cmap["f*g"])
        fgg_box = get_background_rect(fgg_label)
        self.play(
            # ReplacementTransform(fgg_label2.copy(), fgg_label),
            TransformMatchingTex(fgg_label2.copy(), fgg_label),
            FadeIn(fgg_box)
        )
        self.slide_pause()

        self.play(
            *[FadeOut(m) for m in [fgg_label0, fgg_label1, fgg_label2, fgg_box0, fgg_box1, fgg_box2]],
            VGroup(fgg_label, fgg_box).animate.next_to(g_box, DOWN, aligned_edge=LEFT, buff=0),
            FadeOut(fgg_points)
        )
        self.slide_pause()

        self.play(
            *[FadeOut(m) for m in self.mobjects if m not in (f, g, fgg, plane)],
            f.animate.set_style(stroke_opacity=1),
            g.animate.set_style(stroke_opacity=1)
        )
        self.remove(f, g, fgg, plane, f_label, g_label, fgg_label)

    def roots_of_products(self):
        cmap = self.get_cmap()
        xmin, xmax, xstep = -8, 8, 1
        ymin, ymax, ystep = -8, 8, 1
        width = 14
        plane = NumberPlane(
            x_range=[xmin, xmax, xstep],
            y_range=[ymin, ymax, ystep],
            x_length=width,
            y_length=9/16 * width,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 2,
                "stroke_opacity": 0.3
            },
            axis_config={"include_numbers": True, "include_ticks": True},
            x_axis_config={"label_direction": DOWN},
            y_axis_config={"label_direction": LEFT}
        )
        fa, fb = ValueTracker(-0.5), ValueTracker(2)
        ga, gb = ValueTracker(1), ValueTracker(-1)
        f = always_redraw(lambda: plane.plot(
            lambda x: fa.get_value() * x + fb.get_value(),
            stroke_color=cmap["f"]
        ))
        g = always_redraw(lambda: plane.plot(
            lambda x: ga.get_value() * x + gb.get_value(),
            stroke_color=cmap["g"]
        ))
        fgg = always_redraw(lambda: plane.plot(
            lambda x: f.underlying_function(x) * g.underlying_function(x),
            stroke_color=cmap["f*g"]
        ))
        self.add(f, g, fgg, plane)

        f_label = always_redraw(lambda:
            VGroup(
                MathTex("{{f}}(x) = ").set_color_by_tex_to_color_map(cmap),
                DecimalNumber(
                    fa.get_value(), num_decimal_places=2, color=cmap["f"], include_sign=True if fa.get_value() < 0 else False
                ),
                MathTex(r" \cdot x "),
                DecimalNumber(
                    fb.get_value(), num_decimal_places=2, color=cmap["f"], include_sign=True
                )
            ).arrange(RIGHT, aligned_edge=DOWN).to_edge(UL, buff=0.1).set_z_index(5)
        )
        g_label = always_redraw(lambda:
            VGroup(
                MathTex("{{g}}(x) = ").set_color_by_tex_to_color_map(cmap),
                DecimalNumber(
                    ga.get_value(), num_decimal_places=2, color=cmap["g"], include_sign=True if ga.get_value() < 0 else False
                ),
                MathTex(r" \cdot x "),
                DecimalNumber(
                    gb.get_value(), num_decimal_places=2, color=cmap["g"], include_sign=True
                )
            ).arrange(RIGHT, aligned_edge=DOWN).next_to(f_label, DOWN, aligned_edge=LEFT, buff=0.1).set_z_index(5)
        )
        fgg_label = always_redraw(lambda:
            VGroup(
                MathTex("({{f \\cdot g}})(x) = ").set_color_by_tex_to_color_map({"f \\cdot g": cmap["f*g"]}),
                DecimalNumber(
                    fa.get_value() * ga.get_value(), num_decimal_places=2, color=cmap["f*g"],
                    include_sign=True if fa.get_value() * ga.get_value() < 0 else False
                ),
                MathTex(r" \cdot x^2 "),
                DecimalNumber(
                    fa.get_value() * gb.get_value() + fb.get_value() * ga.get_value(),
                    num_decimal_places=2, color=cmap["f*g"], include_sign=True
                ),
                MathTex(r" \cdot x "),
                DecimalNumber(
                    fb.get_value() * gb.get_value(), num_decimal_places=2, color=cmap["f*g"], include_sign=True
                )
            ).arrange(RIGHT, aligned_edge=DOWN).next_to(g_label, DOWN, aligned_edge=LEFT, buff=0.1).set_z_index(5)
        )
        srec = get_background_rect(VGroup(f_label, g_label, fgg_label).set_z_index(5))
        self.play(
            *[FadeIn(m, run_time=0.1) for m in (f_label, g_label, fgg_label, srec)]
        )
        self.play(
            fa.animate.set_value(0.5),
            run_time=5
        )
        self.slide_pause()

        self.play(
            ga.animate.set_value(0.5),
            run_time=5
        )
        self.slide_pause()

        self.play(
            gb.animate.set_value(-3),
            fb.animate.set_value(1),
            run_time=5
        )
        self.slide_pause()

        self.play(
            fa.animate.set_value((np.random.rand() - 0.5) * 4),
            fb.animate.set_value((np.random.rand() - 0.5) * 4),
            ga.animate.set_value((np.random.rand() - 0.5) * 6),
            gb.animate.set_value((np.random.rand() - 0.5) * 6),
            run_time=10
        )



if __name__ == "__main__":
    classes = [
        # SumOgDifferensAfFunktioner,
        ProduktOgForholdAfFunktioner
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

