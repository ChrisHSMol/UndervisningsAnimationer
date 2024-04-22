from manim import *
import sys
sys.path.append("../")
from helpers import *
import subprocess

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


class RetningsVektorer(Scene if not slides else Slide):
    btransparent = True

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t=t, slides_bool=slides_bool)

    def construct(self):
        pa, pb, pc = [-2, 5], [3, -2], [2, 6]
        _c = {"A": YELLOW, "B": BLUE, "C": RED}
        opgave = VGroup(
            Tex("I et koordinatsystem er der givet punkterne:"),
            MathTex(
                f"A({pa[0]}, {pa[1]})", ", ", f"B({pb[0]}, {pb[1]})", ", ", f"C({pc[0]}, {pc[1]})"
            ).set_color_by_tex_to_color_map(_c),
            Tex("Bestem koordinatsættet til hver af vektorerne ", "$\\overrightarrow{AB}$", " og ", "$\\overrightarrow{AC}$", ".")
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(UP)
        opgave[2][1].set_color(color_gradient([_c["A"], _c["B"]], 2))
        opgave[2][3].set_color(color_gradient([_c["A"], _c["C"]], 2))
        # self.add(opgave)
        self.play(
            LaggedStart(
                *[FadeIn(o, shift=d) for o, d in zip(opgave, [DOWN, RIGHT, LEFT])],
                lag_ratio=0.25
            )
        )
        self.slide_pause()

        vekab = VGroup(
            MathTex(r"\overrightarrow{AB}", " = ", r"\begin{pmatrix} x_B - x_A \\ y_B - y_A \end{pmatrix}"),
            MathTex(r"\overrightarrow{AB}", " = ", r"\begin{pmatrix} 3 - (-2) \\ (-2) - 5 \end{pmatrix}"),
            MathTex(r"\overrightarrow{AB}", " = ", r"\begin{pmatrix} 5 \\ -7 \end{pmatrix}")
        ).arrange(DOWN, aligned_edge=LEFT).next_to(opgave, DOWN, aligned_edge=LEFT)
        vekab[0][0].set_color(color_gradient([_c["A"], _c["B"]], 2))
        vekab[0][2][1:3].set_color(_c["B"])
        vekab[0][2][6:8].set_color(_c["B"])
        vekab[0][2][4:6].set_color(_c["A"])
        vekab[0][2][9:11].set_color(_c["A"])
        vekab[1][0].set_color(color_gradient([_c["A"], _c["B"]], 2))
        vekab[1][2][1].set_color(_c["B"])
        vekab[1][2][7:11].set_color(_c["B"])
        vekab[1][2][3:7].set_color(_c["A"])
        vekab[1][2][12].set_color(_c["A"])
        vekab[2][0].set_color(color_gradient([_c["A"], _c["B"]], 2))
        vekab[2][2][1:4].set_color(color_gradient([_c["A"], _c["B"]], 2))
        srec = get_background_rect(vekab, stroke_colour=color_gradient([_c["A"], _c["B"]], 8))
        # self.add(vekab)
        self.play(
            FadeIn(vekab[0], shift=RIGHT),
            FadeIn(srec, shift=RIGHT)
        )
        self.slide_pause()
        for i, _v in enumerate(vekab[1:]):
            self.play(
                ReplacementTransform(vekab[i].copy(), _v)
            )
            self.slide_pause()

        self.play(
            FadeOut(vekab[:-1], shift=LEFT),
            FadeOut(srec, shift=LEFT),
            vekab[-1].animate.next_to(opgave, DOWN, aligned_edge=LEFT)
        )
        self.slide_pause()

        vekac = VGroup(
            MathTex(r"\overrightarrow{AC}", " = ", r"\begin{pmatrix} x_C - x_A \\ y_C - y_A \end{pmatrix}"),
            MathTex(r"\overrightarrow{AC}", " = ", r"\begin{pmatrix} 2 - (-2) \\ 6 - 5 \end{pmatrix}"),
            MathTex(r"\overrightarrow{AC}", " = ", r"\begin{pmatrix} 4 \\ 1 \end{pmatrix}")
        ).arrange(DOWN, aligned_edge=LEFT).next_to(opgave, DOWN, aligned_edge=RIGHT)
        vekac[0][0].set_color(color_gradient([_c["A"], _c["C"]], 2))
        vekac[0][2][1:3].set_color(_c["C"])
        vekac[0][2][6:8].set_color(_c["C"])
        vekac[0][2][4:6].set_color(_c["A"])
        vekac[0][2][9:11].set_color(_c["A"])
        vekac[1][0].set_color(color_gradient([_c["A"], _c["C"]], 2))
        vekac[1][2][1].set_color(_c["C"])
        vekac[1][2][7].set_color(_c["C"])
        vekac[1][2][3:7].set_color(_c["A"])
        vekac[1][2][9].set_color(_c["A"])
        vekac[2][0].set_color(color_gradient([_c["A"], _c["C"]], 2))
        vekac[2][2][1:3].set_color(color_gradient([_c["A"], _c["C"]], 2))
        srec = get_background_rect(vekac, stroke_colour=color_gradient([_c["A"], _c["C"]], 8))
        # self.add(vekac)
        self.play(
            FadeIn(vekac[0], shift=LEFT),
            FadeIn(srec, shift=LEFT)
        )
        self.slide_pause()
        for i, _v in enumerate(vekac[1:]):
            self.play(
                ReplacementTransform(vekac[i].copy(), _v)
            )
            self.slide_pause()

        self.play(
            FadeOut(vekac[:-1], shift=RIGHT),
            FadeOut(srec, shift=RIGHT),
            vekac[-1].animate.next_to(vekab[-1], DOWN, aligned_edge=LEFT)
        )
        self.slide_pause()

        plane = NumberPlane(
            x_range=[-5, 8, 1],
            y_range=[-3, 7, 1],
            x_length=13/2,
            y_length=10/2,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1.5,
                "stroke_opacity": 0.3
            }
        ).to_edge(DR, buff=0.25)
        srec = get_background_rect(plane, buff=0, stroke_colour=color_gradient([_c["A"], _c["B"], _c["C"]], 9))
        self.play(
            DrawBorderThenFill(plane),
            FadeIn(srec)
        )
        self.slide_pause()

        points = VGroup(*[
            Dot(fill_color=_col, fill_opacity=1).move_to(plane.c2p(*_point)) for _point, _col in zip(
                [pa, pb, pc], [_c["A"], _c["B"], _c["C"]]
            )
        ])
        # self.add(points)
        self.play(
            LaggedStart(
                *[DrawBorderThenFill(_p, run_time=0.5) for _p in points],
                lag_ratio=0.25
            )
        )
        self.slide_pause()

        plabs = VGroup(*[
            _lab.copy().scale(0.75).next_to(_point, _d) for _lab, _point, _d in zip(
                [opgave[1][0], opgave[1][2], opgave[1][4]], points, [LEFT, RIGHT, RIGHT]
            )
        ])
        # self.add(plabs)
        self.play(
            LaggedStart(
                *[ReplacementTransform(opgave[1][i].copy(), _l) for i, _l in zip([0, 2, 4], plabs)],
                lag_ratio=0.25
            )
        )
        self.slide_pause()

        vectors = VGroup(*[
            Arrow(start=points[0], end=_p, buff=0).set_color(color_gradient([_col, _c["A"]], 2)) for _p, _col in zip(
                points[1:], [_c["B"], _c["C"]]
            )
            # Arrow(start=points[0], end=_p) for _p in points[1:]
        ])
        vlabs = VGroup(*[
            _l.copy().scale(0.5).rotate(_a).move_to(_v).shift(_s) for _l, _a, _v, _s in zip(
                [vekab[-1], vekac[-1]], [np.arctan((pb[1]-pa[1])/(pb[0]-pa[0])), np.arctan((pc[1]-pa[1])/(pc[0]-pa[0]))],
                vectors, [0.5*LEFT, 0.5*UP]
            )
        ])
        # self.add(vectors)
        self.play(
            LaggedStart(
                # *[GrowFromPoint(_v, points[0]) for _v in vectors],
                *[GrowArrow(_v) for _v in vectors],
                lag_ratio=0.75
            ),
            LaggedStart(
                *[FadeIn(_vl) for _vl in vlabs],
                lag_ratio=0.75
            )
        )
        self.slide_pause()


class RetningsVektorerThumbnail(Scene):
    def construct(self):
        titel = Tex("Opgave om ", "vektorer mellem punkter", font_size=72).to_edge(UL)
        titel[1].set_color(YELLOW)
        pa, pb, pc = [-2, 5], [3, -2], [2, 6]
        _c = {"A": YELLOW, "B": BLUE, "C": RED}
        opgave = VGroup(
            Tex("I et koordinatsystem er der givet punkterne:"),
            MathTex(
                f"A({pa[0]}, {pa[1]})", ", ", f"B({pb[0]}, {pb[1]})", ", ", f"C({pc[0]}, {pc[1]})"
            ).set_color_by_tex_to_color_map(_c),
            Tex("Bestem koordinatsættet til hver af vektorerne ", "$\\overrightarrow{AB}$", " og ", "$\\overrightarrow{AC}$", ".")
        ).arrange(DOWN, aligned_edge=LEFT)
        opgave[2][1].set_color(color_gradient([_c["A"], _c["B"]], 2))
        opgave[2][3].set_color(color_gradient([_c["A"], _c["C"]], 2))
        self.add(titel, opgave)


if __name__ == "__main__":
    cls = RetningsVektorer
    class_name = cls.__name__
    transparent = cls.btransparent
    command = rf"manim {sys.argv[0]} {class_name} -p --resolution={_RESOLUTION[q]} --frame_rate={_FRAMERATE[q]}"
    # if transparent:
    #     command += " --transparent --format=webm"
    scene_marker(rf"RUNNNING:    {command}")
    subprocess.run(command)
