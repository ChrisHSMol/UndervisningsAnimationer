import math
import random

from manim import *
import sys

sys.path.append("../../")
sys.path.append("../../../")
import subprocess
from helpers import *
from custom_classes import *

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
_ONEFRAME = 1/_FRAMERATE[q]


class WritingEquilibriumFraction(MovingCameraScene, Slide if slides else Scene):
    def _bkg_col(self):
        return DARKER_GRAY

    def construct(self):
        self.camera.background_color = self._bkg_col()
        # title = Tex(r"Opskrivning af\\ligevægtsbrøker").scale(2)
        # self.add(title)
        # self.slide_pause()
        # self.play(
        #     FadeOut(title),
        #     run_time=0.25
        # )
        self.generel_opskrivning()
        self.example_ammonia()
        self.wait(5)

    def slide_pause(self, t=0.5, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def get_cmap(self):
        cmap = {"a": BLUE, "b": GREEN, "c": YELLOW, "d": RED}
        ks = ["a", "b", "c", "d"]
        for k in ks:
            cmap[f"${k}$"] = cmap[k]
            cmap[f"^{k}"] = cmap[k]
        return cmap

    def generel_opskrivning(self):
        _c = self.get_cmap()
        titel = Tex("Generel reaktionsbrøk").scale(2).to_edge(UP)
        titel_underline = Line(
            start=titel.get_corner(DL) + 0.25*DL + LEFT, end=titel.get_corner(DR) + 0.25*DR + RIGHT,
            stroke_opacity=[0, 1, 0], stroke_width=3
        )
        reaktionsskema = Tex(
            "$a$", "A", " + ", "$b$", "B", " + ", "...", r" $\rightleftharpoons$ ",
            "$c$", "C", " + ", "$d$", "D", " + ", "..."
        ).set_color_by_tex_to_color_map(_c).shift(UP)
        # self.add(reaktionsskema, titel, titel_underline)
        self.play(
            LaggedStart(
                Write(titel),
                Create(titel_underline),
                lag_ratio=0.5
            ),
            run_time=1
        )
        self.slide_pause()

        for r in [(0, 2), (2, 3), (3, 5), (5, 7), (7, 8), (8, 10), (10, 11), (11, 13), (13, 15)]:
            self.play(
                Write(reaktionsskema[r[0]:r[1]]),
                run_time=0.25
            )
            if r[-1]-r[0] > 1:
                self.slide_pause()
        # self.remove(reaktionsskema)
        # self.add(reaktionsskema)

        reaktionsbrøk = MathTex(
            "Y", "=", r"\frac{", r"[\text{C}]", "^c", r"\cdot", r"[\text{D}]", "^d", r"\cdot", "...", "}{",
            r"[\text{A}]", "^a", r"\cdot", r"[\text{B}]", "^b", r"\cdot", "...", "}"
        ).set_color_by_tex_to_color_map(_c).shift(DOWN)
        dkemaindeks = index_labels(reaktionsskema)
        brøkindeks = index_labels(reaktionsbrøk)
        # self.add(dkemaindeks, brøkindeks)
        # self.add(reaktionsbrøk)
        self.play(
            LaggedStart(
                *[Write(reaktionsbrøk[i]) for i in [0, 1, 10]],
                lag_ratio=0.25
            ),
            run_time=0.25
        )
        self.slide_pause()

        # for i in (
        #         (9, 3), (8, 4), (10, 5), (12, 6), (11, 7), (13, 8), (14, 9),
        #         (1, 11), (0, 12), (2, 13), (4, 14), (3, 15), (5, 16), (6, 17)
        # ):
        #     ifrom, ito = i
        #     self.play(
        #         ReplacementTransform(
        #             reaktionsskema[ifrom].copy(),
        #             reaktionsbrøk[ito],
        #         ),
        #         run_time=0.5
        #     )
        #     self.slide_pause()
        for i in (
            [(9, 3), (8, 4)], [(10, 5)], [(12, 6), (11, 7)], [(13, 8), (14, 9)],
            [(1, 11), (0, 12)], [(2, 13)], [(4, 14), (3, 15)], [(5, 16), (6, 17)]
        ):
            self.play(
                LaggedStart(
                    *[
                        ReplacementTransform(
                            reaktionsskema[j[0]].copy(),
                            reaktionsbrøk[j[1]]
                        ) for j in i
                    ],
                    lag_ratio=0.75
                ),
                run_time=1.5
            )
            if len(i) > 1:
                self.slide_pause()

        self.play(
            LaggedStart(
                *[FadeOut(m) for m in self.mobjects],
                lag_ratio=0.05
            )
        )

    def example_ammonia(self):
        _c = self.get_cmap()
        titel = Tex("Eksempel: Ammoniak").scale(2).to_edge(UP)
        titel_underline = Line(
            start=titel.get_corner(DL) + 0.25*DL + LEFT, end=titel.get_corner(DR) + 0.25*DR + RIGHT,
            stroke_opacity=[0, 1, 0], stroke_width=3
        )
        reaktionsskema = Tex(
            "3", "H$_2$", " + ", "1", "N$_2$", r" $\rightleftharpoons$ ", "2", "NH$_3$"
        ).shift(UP)
        reaktionsskema[0].set_color(_c["a"])
        reaktionsskema[3].set_color(self._bkg_col())
        reaktionsskema[6].set_color(_c["c"])
        self.play(
            LaggedStart(
                Write(titel),
                Create(titel_underline),
                lag_ratio=0.5
            ),
            run_time=1
        )
        self.slide_pause()

        self.play(
            Write(reaktionsskema)
        )

        reaktionsbrøk = MathTex(
            "Y", "=", r"\frac{", r"[\text{NH}_3]", "^2", "}{",
            r"[\text{H}_2]", "^3", r"\cdot", r"[\text{N}_2]", "^1", "}"
        ).shift(DOWN)
        reaktionsbrøk[4].set_color(_c["c"])
        reaktionsbrøk[7].set_color(_c["a"])
        reaktionsbrøk[10].set_color(self._bkg_col())
        # dkemaindeks = index_labels(reaktionsskema)
        # brøkindeks = index_labels(reaktionsbrøk)
        # self.add(dkemaindeks, brøkindeks)
        # self.add(reaktionsbrøk)
        self.play(
            LaggedStart(
                *[Write(reaktionsbrøk[i]) for i in [0, 1, 5]],
                lag_ratio=0.25
            ),
            run_time=0.25
        )
        self.slide_pause()

        for i in (
            [(7, 3), (6, 4)],
            [(1, 6), (0, 7)], [(2, 8)], [(4, 9)]#, (3, 10)]
        ):
            self.play(
                LaggedStart(
                    *[
                        ReplacementTransform(
                            reaktionsskema[j[0]].copy(),
                            reaktionsbrøk[j[1]]
                        ) for j in i
                    ],
                    lag_ratio=0.75
                ),
                run_time=1.5
            )
            if len(i) > 1:
                self.slide_pause()

        for _ in range(5):
            self.play(
                Indicate(reaktionsskema[3], color=_c["b"]),
                Indicate(reaktionsbrøk[10], color=_c["b"]),
            )
        self.slide_pause()


class DynamicFraction(WritingEquilibriumFraction):
    def construct(self):
        self.camera.background_color = self._bkg_col()
        title = Tex(r"På vej til ligevægt").scale(2)
        self.add(title)
        self.slide_pause()
        self.play(
            FadeOut(title),
            run_time=0.25
        )
        self.graphic_representation()
        self.wait(5)

    def get_cmap(self):
        return {"time": BLUE, "conc": RED, "H$_2$": YELLOW, "I$_2$": PURPLE, "HI": GREEN}

    def graphic_representation(self):
        cmap = self.get_cmap()
        x_start, x_slut, dx, eps = 0, 35*3600, 5*3600, 1e-6
        y_start, y_slut, dy = 0, 1, 0.2
        plane = NumberPlane(
            x_range=(x_start, x_slut+eps, dx),
            y_range=(y_start, y_slut+eps, dy),
            x_length=6,
            y_length=6,
            background_line_style={
                "stroke_color": LIGHTER_GRAY,
                "stroke_width": 1,
                "stroke_opacity": 0.3,
            },
            axis_config={
                "include_tip": True,
                "tip_shape": StealthTip,
                "tip_width": 0.2,
                "tip_height": 0.2
            },
        ).to_edge(LEFT, buff=1)
        axis_labels = VGroup(*[
            MathTex(
                lab, color=c, font_size=36
            ).move_to(plane.c2p(coord)).set_z_index(plane.get_z_index()+5)
            for lab, c, coord in zip(
                [r"t~[h]", r"c~[M]"], [cmap["time"], cmap["conc"]], [(x_slut*1.10, 0), (0, y_slut*1.05)]
            )
        ])
        tickmarks = {
            "x": VGroup(*[Line(
                start=plane.c2p(x, dy/10), end=plane.c2p(x, -dy/10), color=WHITE, stroke_width=1.5
            ) for x in np.arange(x_start, x_slut+eps, dx)]).set_z_index(4),
            "y": VGroup(*[Line(
                start=plane.c2p(dx/10, y), end=plane.c2p(-dx/10, y), color=WHITE, stroke_width=1.5
            ) for y in np.arange(y_start, y_slut+eps, dy)]).set_z_index(4),
        }
        ticks = {
            "x": VGroup(*[DecimalNumber(
                number=x/3600, num_decimal_places=0, include_sign=x < 0, color=cmap["time"], font_size=24 if x != 0 else 0.01
            ).set_z_index(4).next_to(
                tm, DOWN, buff=0.2
            ) for x, tm in zip(np.arange(x_start, x_slut+eps, dx), tickmarks["x"])]),
            "y": VGroup(*[DecimalNumber(
                number=y, num_decimal_places=1, include_sign=y < 0, color=cmap["conc"], font_size=24 if np.abs(y) > eps else 0.01
            ).set_z_index(4).next_to(
                tm, LEFT, buff=0.2
            ) for y, tm in zip(np.arange(y_start, y_slut+eps, dy), tickmarks["y"])]),
        }
        # self.add(plane, axis_labels, *tickmarks.values(), *ticks.values())
        self.play(
            LaggedStart(
                DrawBorderThenFill(plane),
                *[Create(t) for t in tickmarks.values()],
                *[Write(t) for t in ticks.values()],
                Write(axis_labels),
                lag_ratio=0.2
            )
        )
        self.slide_pause()

        reaction_scheme = Tex(
            "H$_2$", " (g)", " + ", "I$_2$", " (g)", r" $\rightleftharpoons$ ",
            "2 ", "HI", " (g)"
        ).set_color_by_tex_to_color_map(cmap).to_edge(RIGHT).shift(2*UP)
        reaction_fraction = MathTex(
            "Y", "=", r"\frac{", r"[\text{HI}]", "^2", "}{",
            r"[\text{H}_2]", r"\cdot", r"[\text{I}_2]", "}"
        ).next_to(reaction_scheme, DOWN, aligned_edge=LEFT)
        reaction_fraction[3].set_color(cmap["HI"])
        reaction_fraction[6].set_color(cmap["H$_2$"])
        reaction_fraction[8].set_color(cmap["I$_2$"])
        fraction_frame = VGroup(
            MathTex("Y = "),
            Line(start=2*LEFT, end=2*RIGHT)
        ).arrange(RIGHT).next_to(reaction_fraction, DOWN, buff=1, aligned_edge=LEFT)
        fraction_frame.add(VGroup(
            Tex("("), Tex(r")$^2$")
        ).arrange(RIGHT, buff=1.75).next_to(fraction_frame[1], UP))
        fraction_frame.add(MathTex(r"\cdot").next_to(fraction_frame[1], DOWN))
        # self.add(reaction_scheme, reaction_fraction, fraction_frame)
        self.play(
            Write(reaction_scheme),
        )
        self.slide_pause()

        self.play(
            Write(reaction_fraction),
        )
        self.slide_pause()

        k_reac = 2.5e-4 # M^-1 s^-1
        c_h2_start = 0.6 # M
        c_i2_start = 0.5 # M
        c_hi_start = 0 # M

        def extent(t):
            x_eq = 0.42450073898720975
            x2 = 0.7628008483143776
            C = 0.5565027096197693
            lam = 7.835627532210137e-5
            return (x_eq - C * x2 * math.exp(-lam * t)) / (1 - C * math.exp(-lam * t))

        def H2(t, c0):
            return c0 - extent(t)

        def I2(t, c0):
            return c0 - extent(t)

        def HI(t, c0):
            return c0 + 2 * extent(t)

        time_tracker = ValueTracker(0)
        c_h2_graph = always_redraw(lambda: plane.plot(
            lambda t: H2(t, c0=c_h2_start),
            color=cmap["H$_2$"],
            x_range=(0, time_tracker.get_value())
        ))
        c_i2_graph = always_redraw(lambda: plane.plot(
            lambda t: I2(t, c0=c_i2_start),
            color=cmap["I$_2$"],
            x_range=(0, time_tracker.get_value())
        ))
        c_hi_graph = always_redraw(lambda: plane.plot(
            lambda t: HI(t, c0=c_hi_start),
            color=cmap["HI"],
            x_range=(0, time_tracker.get_value())
        ))
        c_dots = always_redraw(lambda:
            VGroup(
                Dot(fill_color=col, stroke_width=0).move_to(
                    plane.c2p(time_tracker.get_value(), g.underlying_function(time_tracker.get_value()))
                ) for col, g in zip(
                    (cmap["H$_2$"], cmap["I$_2$"], cmap["HI"]), (c_h2_graph, c_i2_graph, c_hi_graph)
                )
            )
        )
        self.add(c_h2_graph, c_i2_graph, c_hi_graph)
        self.play(
            FadeIn(c_dots)
        )
        self.slide_pause()

        fraction_values = always_redraw(lambda:
            VGroup(
                DecimalNumber(
                    c_h2_graph.underlying_function(time_tracker.get_value()),
                    num_decimal_places=3,
                    unit=r"~\text{ M}",
                    color=cmap["H$_2$"],
                ).next_to(fraction_frame[3], LEFT),
                DecimalNumber(
                    c_i2_graph.underlying_function(time_tracker.get_value()),
                    num_decimal_places=3,
                    unit=r"~\text{ M}",
                    color=cmap["I$_2$"],
                ).next_to(fraction_frame[3], RIGHT),
                DecimalNumber(
                    c_hi_graph.underlying_function(time_tracker.get_value()),
                    num_decimal_places=3,
                    unit=r"~\text{ M}",
                    color=cmap["HI"],
                # ).next_to(fraction_frame[1], UP)
                ).move_to(between_mobjects(*fraction_frame[2]))
            )
        )
        # self.add(fraction_values)
        self.play(
            FadeIn(fraction_frame),
            Write(fraction_values)
        )
        self.slide_pause()

        fraction_result_frame = MathTex("Y = ").next_to(fraction_frame, DOWN, aligned_edge=LEFT, buff=1)
        fraction_result = always_redraw(lambda:
            DecimalNumber(
                HI(time_tracker.get_value(), c0=c_hi_start)**2 / (H2(time_tracker.get_value(), c0=c_h2_start) * I2(time_tracker.get_value(), c0=c_i2_start)),
                num_decimal_places=1,
            ).next_to(fraction_result_frame, RIGHT)
        )
        # self.add(fraction_result, fraction_result_frame)
        self.play(
            Write(fraction_result_frame),
            Write(fraction_result)
        )
        self.slide_pause()

        self.play(
            time_tracker.animate.set_value(x_slut),
            run_time=(x_slut - x_start)/3600,
            rate_func=rate_functions.linear
        )
        self.slide_pause()



if __name__ == "__main__":
    classes = [
        # WritingEquilibriumFraction,
        DynamicFraction,
    ]
    for cls in classes:
        class_name = cls.__name__
        command = rf"manim {sys.argv[0]} {class_name} -p --resolution={_RESOLUTION[q]} --frame_rate={_FRAMERATE[q]}"
        scene_marker(rf"RUNNNING:    {command}")
        subprocess.run(command)
        if slides and q == "h":
            command = rf"manim-slides convert {class_name} {class_name}.html --one-file --offline"
            scene_marker(rf"RUNNNING:    {command}")
            subprocess.run(command)
            if class_name + "Thumbnail" in dir():
                command = rf"manim {sys.argv[0]} {class_name}Thumbnail -pq{q} -o {class_name}Thumbnail.png"
                scene_marker(rf"RUNNNING:    {command}")
                subprocess.run(command)