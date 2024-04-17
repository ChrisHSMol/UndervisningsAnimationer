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


class Nulpunkter(Scene if not slides else Slide):
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
        a, b, c = -2, -2, 4
        d = b**2 - 4*a*c
        opgave = Tex("Bestem nulpunkterne for parablen:").to_edge(UL)
        funktion = MathTex("f(x) = ", "-2", "x^2", " ", "-2", "x", " + ", "4").next_to(opgave, DOWN, aligned_edge=LEFT)
        # self.add(opgave, funktion)
        self.play(
            FadeIn(opgave, shift=DOWN),
            FadeIn(funktion, shift=RIGHT)
        )
        # self.wait(1)
        self.slide_pause()

        _c = {"a": RED_C, "b": BLUE_C, "c": YELLOW_C, "d": PINK}
        generel_form = MathTex(
            "f(x) = ", "a", "x^2", " + ", "b", "x", " + ", "c"
        ).set_color_by_tex_to_color_map(_c).next_to(funktion, DOWN, aligned_edge=LEFT)
        koef_vals = VGroup(*[
            MathTex(f"{kn} = {kv}", substrings_to_isolate=kn).set_color_by_tex_to_color_map(_c) for kn, kv in zip(["a", "b", "c"], [a, b, c])
        ]).arrange(DOWN, aligned_edge=LEFT).next_to(generel_form, DOWN, aligned_edge=LEFT)
        # self.add(generel_form, koef_vals)
        # self.play(Succession(
        #     Write(generel_form),
        #     Write(koef_vals)
        # ))
        self.play(
            Transform(funktion.copy(), generel_form, transform_mismatches=True)
        )
        # self.wait(1)
        self.slide_pause()

        for i, _k in zip([1, 4, 7], koef_vals):
            self.play(
                ReplacementTransform(VGroup(generel_form[i].copy(), funktion[i].copy()), _k, path_arc=-PI/2)
            )
        # self.wait(1)
        self.slide_pause()

        trin1 = VGroup(
            Tex("Trin 1: Beregn ", "$d$").set_color_by_tex_to_color_map(_c),
            MathTex(f"d", " = ", "b", r"^2 - 4\cdot", "a", r"\cdot", "c"),
            MathTex(f"d", " = ", "(-2)", r"^2 - 4\cdot", "(-2)", r"\cdot", "4"),
            MathTex(f"d", " = ", "4", " + ", "32", " ", " "),
            MathTex("d", " = ", "36")
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT).set_z_index(3)
        srec = get_background_rect(trin1, fill_opacity=0.95, stroke_colour=_c["d"])
        for i in [1, 2, 3]:
            trin1[i][0].set_color(_c["d"])
            trin1[i][2].set_color(_c["b"])
            trin1[i][4].set_color(_c["a"])
            trin1[i][6].set_color(_c["c"])
        trin1[4][0].set_color(_c["d"])
        # self.add(trin1[:2], srec)
        # self.wait(1)
        # self.add(trin1[2])
        # self.wait(1)
        # self.add(trin1[3])
        # self.wait(1)
        # self.add(trin1[4])
        # self.wait(1)
        self.play(
            FadeIn(trin1[:2], shift=LEFT),
            FadeIn(srec, shift=LEFT)
        )
        self.slide_pause()
        for i in [2, 3, 4]:
            self.play(
                ReplacementTransform(trin1[i-1].copy(), trin1[i])
            )
            self.slide_pause()

        # self.remove(trin1[:3], srec)
        # trin1[-1].next_to(koef_vals, DOWN, aligned_edge=LEFT)
        # self.remove(trin1[:3])
        self.play(
            FadeOut(trin1[:-1], shift=UP),
            FadeOut(srec, shift=UP),
            trin1[-1].animate.next_to(koef_vals, DOWN, aligned_edge=LEFT)
        )
        self.slide_pause()

        _xycol = {"x_1": GREEN, "x_2": PURE_GREEN}
        trin2 = VGroup(
            VGroup(
                Tex("Trin 2: Hvis ", "$d$", "$>0$, er der 2 svar!").set_color_by_tex("$d$", _c["d"]),
                Tex("Beregn ", "$x$", "-koordinaterne").set_color_by_tex("x", color_gradient(_xycol.values(), 8)),
            ).arrange(DOWN, aligned_edge=RIGHT),
            VGroup(
                MathTex("x_1", " = ").set_color_by_tex_to_color_map(_xycol),
                self._fraction(
                    MathTex("- {{b}} + \\sqrt{d}").set_color_by_tex("b", _c["b"]),
                    MathTex(r"2\cdot", "a").set_color_by_tex("a", _c["a"])
                )
            ).arrange(RIGHT),
            VGroup(
                MathTex("x_1", " = ").set_color_by_tex_to_color_map(_xycol),
                self._fraction(
                    MathTex("-", f"({b:.0f})", rf"+\sqrt{{{d:.0f}}}"), #  .set_color_by_tex(["b", str(d)], [_c["b"], _c["d"]]),
                    MathTex(r"2\cdot", f"({a:.0f})").set_color_by_tex(f"({a:.0f})", _c["a"])
                )
            ).arrange(RIGHT),
            VGroup(
                MathTex("x_1", " = ").set_color_by_tex_to_color_map(_xycol),
                self._fraction(
                    MathTex(str(-b), "+", str(int(np.sqrt(d)))).set_color_by_tex_to_color_map(
                        {str(-b): _c["b"], str(int(np.sqrt(d))): _c["d"]}
                    ),
                    MathTex(str(2*a), color=_c["a"])
                )
            ).arrange(RIGHT),
            VGroup(
                MathTex("x_1", " = ").set_color_by_tex_to_color_map(_xycol),
                self._fraction(
                    MathTex(str(int(-b + np.sqrt(d)))),
                    MathTex(str(2*a))
                )
            ).arrange(RIGHT),
            MathTex("x_1", f" = {(-b + np.sqrt(d))/(2*a):.0f}").set_color_by_tex_to_color_map(_xycol)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT).set_z_index(3)
        trin2[1][1][0][-1][-1].set_color(_c["d"])
        trin2[2][1][0][1].set_color(_c["b"])
        trin2[2][1][0][-1][-2:].set_color(_c["d"])
        srec = get_background_rect(trin2, fill_opacity=0.95, stroke_colour=_xycol["x_1"])
        # self.add(trin2[:2], srec)
        # self.wait(1)
        # self.add(trin2[2])
        # self.wait(1)
        # self.add(trin2[3])
        # self.wait(1)
        # self.add(trin2[4])
        # self.wait(1)
        # self.add(trin2[5])
        # self.wait(1)
        self.play(
            FadeIn(trin2[:2], shift=LEFT),
            FadeIn(srec, shift=LEFT)
        )
        self.slide_pause()
        for i in [2, 3, 4, 5]:
            self.play(
                ReplacementTransform(trin2[i-1].copy(), trin2[i])
            )
            self.slide_pause()

        # self.remove(trin2[:3], srec)
        # trin2[-1].next_to(trin1[-1], DOWN, aligned_edge=LEFT)
        # self.remove(trin2[:3])
        # self.wait(1)
        self.play(
            FadeOut(trin2[:-1], shift=UP),
            FadeOut(srec, shift=UP),
            trin2[-1].animate.next_to(trin1[-1], DOWN, aligned_edge=LEFT)
        )
        self.slide_pause()

        trin2halv = VGroup(
            VGroup(
                Tex("Trin 2,5: Hvis ", "$d$", "$>0$, er der 2 svar!").set_color_by_tex("$d$", _c["d"]),
                Tex("Beregn ", "$x$", "-koordinaterne").set_color_by_tex("x", color_gradient(_xycol.values(), 8)),
            ).arrange(DOWN, aligned_edge=RIGHT),
            VGroup(
                MathTex("x_2", " = ").set_color_by_tex_to_color_map(_xycol),
                self._fraction(
                    MathTex("- {{b}} - \\sqrt{d}").set_color_by_tex("b", _c["b"]),
                    MathTex(r"2\cdot", "a").set_color_by_tex("a", _c["a"])
                )
            ).arrange(RIGHT),
            VGroup(
                MathTex("x_2", " = ").set_color_by_tex_to_color_map(_xycol),
                self._fraction(
                    MathTex("-", f"({b:.0f})", rf"-\sqrt{{{d:.0f}}}"), #  .set_color_by_tex(["b", str(d)], [_c["b"], _c["d"]]),
                    MathTex(r"2\cdot", f"({a:.0f})").set_color_by_tex(f"({a:.0f})", _c["a"])
                )
            ).arrange(RIGHT),
            VGroup(
                MathTex("x_2", " = ").set_color_by_tex_to_color_map(_xycol),
                self._fraction(
                    MathTex(str(-b), "-", str(int(np.sqrt(d)))).set_color_by_tex_to_color_map(
                        {str(-b): _c["b"], str(int(np.sqrt(d))): _c["d"]}
                    ),
                    MathTex(str(2*a), color=_c["a"])
                )
            ).arrange(RIGHT),
            VGroup(
                MathTex("x_2", " = ").set_color_by_tex_to_color_map(_xycol),
                self._fraction(
                    MathTex(str(int(-b - np.sqrt(d)))),
                    MathTex(str(2*a))
                )
            ).arrange(RIGHT),
            MathTex("x_2", f" = {(-b - np.sqrt(d))/(2*a):.0f}").set_color_by_tex_to_color_map(_xycol)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT).set_z_index(3)
        trin2halv[1][1][0][-1][-1].set_color(_c["d"])
        trin2halv[2][1][0][1].set_color(_c["b"])
        trin2halv[2][1][0][-1][-2:].set_color(_c["d"])
        srec = get_background_rect(trin2halv, fill_opacity=0.95, stroke_colour=_xycol["x_2"])
        # self.add(trin2halv[:2], srec)
        # self.wait(1)
        # self.add(trin2halv[2])
        # self.wait(1)
        # self.add(trin2halv[3])
        # self.wait(1)
        # self.add(trin2halv[4])
        # self.wait(1)
        # self.add(trin2halv[5])
        # self.wait(1)
        self.play(
            FadeIn(trin2halv[:2], shift=LEFT),
            FadeIn(srec, shift=LEFT)
        )
        self.slide_pause()
        for i in [2, 3, 4, 5]:
            self.play(
                ReplacementTransform(trin2halv[i-1].copy(), trin2halv[i])
            )
            self.slide_pause()

        # self.remove(trin3[:3])
        # trin3[-1].next_to(trin2[-1], DOWN, aligned_edge=LEFT)
        # self.remove(trin3[:3])
        # self.wait(1)
        self.play(
            FadeOut(trin2halv[:-1], shift=UP),
            FadeOut(srec, shift=UP),
            trin2halv[-1].animate.next_to(trin2[-1], DOWN, aligned_edge=LEFT)
        )
        self.slide_pause()

        trin4 = VGroup(
            Tex("Trin 3: Saml ", "$x$", "-værdierne").set_color_by_tex("x", color_gradient(_xycol.values(), 8)),
            MathTex("x_1", " = ", str(int((-b + np.sqrt(d))/(2*a))), r"\quad", "x_2", " = ", str(int((-b - np.sqrt(d))/(2*a))))
        ).arrange(DOWN, aligned_edge=LEFT).shift(RIGHT).to_edge(RIGHT).set_z_index(3)
        trin4[1][0].set_color(_xycol["x_1"])
        trin4[1][4].set_color(_xycol["x_2"])
        srec = get_background_rect(trin4, fill_opacity=0.95, stroke_colour=color_gradient(_xycol.values(), 8))
        self.play(
            FadeIn(trin4, shift=LEFT),
            FadeIn(srec, shift=LEFT)
        )
        self.slide_pause()


class NulpunkterThumbnail(Scene):
    def construct(self):
        titel = Tex("Opgave om ", "parablens nulpunkter", font_size=72).to_edge(UL)
        titel[1].set_color(YELLOW)
        opgave = Tex("Bestem nulpunkterne for parablen:", color=BLUE_B)
        funktion = MathTex("f(x) = ", "-2", "x^2", " ", "-2", "x", " + ", "4").next_to(opgave, DOWN, aligned_edge=LEFT)
        self.add(titel, opgave, funktion)


if __name__ == "__main__":
    cls = Nulpunkter
    class_name = cls.__name__
    transparent = cls.btransparent
    command = rf"manim {sys.argv[0]} {class_name} -p --resolution={_RESOLUTION[q]} --frame_rate={_FRAMERATE[q]}"
    # if transparent:
    #     command += " --transparent --format=webm"
    scene_marker(rf"RUNNNING:    {command}")
    subprocess.run(command)
