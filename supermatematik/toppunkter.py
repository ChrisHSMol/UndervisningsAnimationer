from manim import *
import sys
sys.path.append("../")
from helpers import *
import subprocess

slides = False
# if slides:
#     from manim_slides import Slide

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


class Toppunkter(Scene):
    btransparent = True

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t=t, slides_bool=slides_bool)

    def _fraction(self, numerator=None, denominator=None):
        output = VGroup(numerator, denominator).arrange(DOWN)
        output.add(
            Line(start=output.get_edge_center(LEFT), end=output.get_edge_center(RIGHT))
        )
        return output

    def construct(self):
        myTemplate = TexTemplate()
        myTemplate.add_to_preamble(r"\usepackage{xcolor}")

        a, b, c = 1, 6, 9
        d = b**2 - 4*a*c
        opgave = Tex("Find koordinatsættet til toppunktet for parablen:").to_edge(UP)
        funktion = MathTex(f"f(x) = x^2 + 6x + 9").next_to(opgave, DOWN, aligned_edge=LEFT)
        self.add(opgave, funktion)
        self.wait(1)

        _c = {"a": RED_C, "b": BLUE_C, "c": YELLOW_C, "d": PINK}
        generel_form = MathTex(
            "f(x) = ax^2 + bx + c", substrings_to_isolate=["a", "b", "c"]
        ).set_color_by_tex_to_color_map(_c).next_to(funktion, DOWN, aligned_edge=LEFT)
        koef_vals = VGroup(*[
            MathTex(f"{kn} = {kv}", substrings_to_isolate=kn).set_color_by_tex_to_color_map(_c) for kn, kv in zip(["a", "b", "c"], [a, b, c])
        ]).arrange(DOWN, aligned_edge=LEFT).next_to(generel_form, DOWN, aligned_edge=LEFT)
        self.add(generel_form, koef_vals)

        trin1 = VGroup(
            Tex("Trin 1: Beregn ", "$d$").set_color_by_tex_to_color_map(_c),
            MathTex(f"d", " = ", "b", r"^2 - 4\cdot", "a", r"\cdot", "c"),
            MathTex(f"d", " = ", "6", r"^2 - 4\cdot", "1", r"\cdot", "9"),
            MathTex(f"d", " = ", "36", " - ", "36", " ", " "),
            MathTex("d", " = ", "0")
        ).arrange(DOWN, aligned_edge=LEFT).shift(RIGHT)
        for i in [1, 2, 3]:
            trin1[i][0].set_color(_c["d"])
            trin1[i][2].set_color(_c["b"])
            trin1[i][4].set_color(_c["a"])
            trin1[i][6].set_color(_c["c"])
        trin1[4][0].set_color(_c["d"])
        self.add(trin1[:2])
        self.wait(1)
        self.add(trin1[2])
        self.wait(1)
        self.add(trin1[3])
        self.wait(1)
        self.add(trin1[4])
        self.wait(1)

        self.remove(trin1[:3])
        trin1[-1].next_to(koef_vals, DOWN, aligned_edge=LEFT)
        self.remove(trin1[:3])
        self.wait(1)

        _xycol = {"x": GREEN_A, "y": GREEN_D}
        trin2 = VGroup(
            Tex("Trin 2: Beregn ", "x", "-koordinatet").set_color_by_tex_to_color_map(_xycol),
            VGroup(
                MathTex("x", "_T = ").set_color_by_tex_to_color_map(_xycol),
                self._fraction(
                    MathTex("-", "b").set_color_by_tex_to_color_map(_c),
                    MathTex(r"2\cdot", "a").set_color_by_tex_to_color_map(_c)
                )
            ).arrange(RIGHT),
            VGroup(
                MathTex("x", "_T = ").set_color_by_tex_to_color_map(_xycol),
                self._fraction(
                    MathTex("-", str(b)).set_color_by_tex(str(b), _c["b"]),
                    MathTex(r"2\cdot", str(a)).set_color_by_tex(str(a), _c["a"])
                )
            ).arrange(RIGHT),
            VGroup(
                MathTex("x", "_T = ").set_color_by_tex_to_color_map(_xycol),
                self._fraction(
                    MathTex("-", str(b)).set_color_by_tex(str(b), _c["b"]),
                    MathTex(str(2*a))
                )
            ).arrange(RIGHT),
            MathTex("x", f"_T = {-b/(2*a):.0f}").set_color_by_tex_to_color_map(_xycol)
        ).arrange(DOWN, aligned_edge=LEFT).shift(RIGHT)
        self.add(trin2[:2])
        self.wait(1)
        self.add(trin2[2])
        self.wait(1)
        self.add(trin2[3])
        self.wait(1)
        self.add(trin2[4])
        self.wait(1)

        self.remove(trin2[:3])
        trin2[-1].next_to(trin1[-1], DOWN, aligned_edge=LEFT)
        self.remove(trin2[:3])
        self.wait(1)

        trin3 = VGroup(
            Tex("Trin 3: Beregn ", "y", "-koordinatet").set_color_by_tex_to_color_map(_xycol),
            VGroup(
                MathTex("y", "_T = ").set_color_by_tex_to_color_map(_xycol),
                self._fraction(
                    MathTex("-", "d").set_color_by_tex_to_color_map(_c),
                    MathTex(r"4\cdot", "a").set_color_by_tex_to_color_map(_c)
                )
            ).arrange(RIGHT),
            VGroup(
                MathTex("y", "_T = ").set_color_by_tex_to_color_map(_xycol),
                self._fraction(
                    MathTex("-", str(d)).set_color_by_tex(str(d), _c["d"]),
                    MathTex(r"4\cdot", str(a)).set_color_by_tex(str(a), _c["a"])
                )
            ).arrange(RIGHT),
            VGroup(
                MathTex("y", "_T = ").set_color_by_tex_to_color_map(_xycol),
                self._fraction(
                    MathTex("-", str(d)).set_color_by_tex(str(d), _c["d"]),
                    MathTex(str(4*a))
                )
            ).arrange(RIGHT),
            MathTex("y", f"_T = {-d/(4*a):.0f}").set_color_by_tex_to_color_map(_xycol)
        ).arrange(DOWN, aligned_edge=LEFT).shift(RIGHT)
        self.add(trin3[:2])
        self.wait(1)
        self.add(trin3[2])
        self.wait(1)
        self.add(trin3[3])
        self.wait(1)
        self.add(trin3[4])
        self.wait(1)

        self.remove(trin3[:3])
        trin3[-1].next_to(trin2[-1], DOWN, aligned_edge=LEFT)
        self.remove(trin3[:3])
        self.wait(1)

        trin4 = VGroup(
            Tex("Trin 4: Saml ", "x", "- og ", "y", "-koordinaterne").set_color_by_tex_to_color_map(_xycol),
            MathTex(r"\left( ", "x", r"_T", ", ", "y", r"_T", r"\right) = ", r"\left( ", f"{-b/(2*a):.0f}", ", ", f"{-d/(4*a):.0f}", r"\right)")
        ).arrange(DOWN, aligned_edge=LEFT).shift(RIGHT).to_edge(RIGHT)
        trin4[1][1].set_color(_xycol["x"])
        trin4[1][8].set_color(_xycol["x"])
        trin4[1][4].set_color(_xycol["y"])
        trin4[1][10].set_color(_xycol["y"])
        self.add(trin4)
        self.wait(1)

        # _c = {"a": RED_C, "b": BLUE_C, "c": YELLOW_C, "d": PINK}
        # regneregel = VGroup(
        #     Tex("En parabel med forskriften"),
        #     MathTex("f(x) = ", "a", "x^2 + ", "b", "x + ", "c").set_color_by_tex_to_color_map(_c),
        #     Tex("har toppunkt $T$ med koordinaterne"),
        #     # MathTex(r"T\left(\frac{-b}{2", "a", r"}, \frac{-d}{4a}\right)").set_color_by_tex_to_color_map(_c)
        #     VGroup(
        #         MathTex(r"T\left("),
        #         self._fraction(
        #             MathTex("-", "b").set_color_by_tex_to_color_map(_c),
        #             MathTex("2", "a").set_color_by_tex_to_color_map(_c)
        #         ),
        #         MathTex(","),
        #         self._fraction(
        #             MathTex("-", "d").set_color_by_tex_to_color_map(_c),
        #             MathTex("4", "a").set_color_by_tex_to_color_map(_c)
        #         ),
        #         MathTex(r"\right)")
        #     ).arrange(RIGHT),
        #     MathTex(r"\text{hvor }d = b^2 - 4ac", substrings_to_isolate=list(_c.keys())).set_color_by_tex_to_color_map(_c)
        # ).arrange(DOWN, aligned_edge=LEFT).to_edge(UL, buff=0.1)
        # self.add(regneregel)
        # self.remove(opgave)
        # funktion.shift(DOWN)
        # self.wait(1)
        #
        # trin = VGroup(
        #     Tex("Trin 1: Find ", "$a$", ", ", "$b$", " og ", "$c$").set_color_by_tex_to_color_map(_c),
        #     Tex("Trin 2: Beregn ", "$d$").set_color_by_tex_to_color_map(_c),
        #     Tex("Trin 3: Beregn koordinaterne")
        # )
        # mellemtrin = VGroup(
        #     MathTex("f(x) = ", "1", r"x^2 + ", "6", "x + ", "9"),
        #     MathTex("d", " = ", "6", r"^2 - 4\cdot", "1", r"\cdot", "9", "=", str(6**2 - 4*1*9)),
        #     # MathTex(r"""T\left(
        #     # \frac{-{\color{blue}6}}{2\cdot{\color{red}1}} ,
        #     # \frac{-{\color{pink}{0}}{4\cdot{\color{red}1}}
        #     #  \right)"""),
        #     MathTex(r"""T\left(
        #     \frac{-6}{2\cdot 1} ,
        #     \frac{-0}{4\cdot 1}
        #      \right)""")
        # ).shift(DOWN)
        # mellemtrin[0][1].set_color(_c["a"])
        # mellemtrin[0][3].set_color(_c["b"])
        # mellemtrin[0][5].set_color(_c["c"])
        # mellemtrin[1][0].set_color(_c["d"])
        # mellemtrin[1][2].set_color(_c["b"])
        # mellemtrin[1][4].set_color(_c["a"])
        # mellemtrin[1][6].set_color(_c["c"])
        # mellemtrin[1][-1].set_color(_c["d"])
        #
        # self.add(trin[0], mellemtrin[0])
        # self.wait(1)
        #
        # self.remove(trin[0], mellemtrin[0])
        # self.add(trin[1], mellemtrin[1])
        # self.wait(1)
        #
        # self.remove(trin[1], mellemtrin[1])
        # self.add(trin[2], mellemtrin[2])
        # self.wait(1)


class ToppunkterThumbnail(Scene):
    def construct(self):
        pass


if __name__ == "__main__":
    cls = Toppunkter
    class_name = cls.__name__
    transparent = cls.btransparent
    command = rf"manim {sys.argv[0]} {class_name} -p --resolution={_RESOLUTION[q]} --frame_rate={_FRAMERATE[q]}"
    # if transparent:
        # command += " --transparent --format=webm"
    scene_marker(rf"RUNNNING:    {command}")
    subprocess.run(command)
