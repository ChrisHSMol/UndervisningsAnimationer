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


class Toppunkter(Slide if slides else Scene):
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
        funktion = MathTex("f(x) = ", " ", "x^2", " + ", "6", "x", " + ", "9").next_to(opgave, DOWN, aligned_edge=LEFT)
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
        # print([[f, g] for f, g in zip(funktion, generel_form)])
        self.play(
            # TransformMatchingTex(funktion.copy(), generel_form, transform_mismatches=True)
            Transform(funktion.copy(), generel_form, transform_mismatches=True)
            # *[p2p_anim_copy(f, g) for f, g in zip(funktion, generel_form)]
            # *[
            #     p2p_anim_copy(funktion, generel_form, g.get_tex_string()) for g in generel_form
            # ]
            # *[
            #     TransformMatchingTex(
            #         f, g, transform_mismatches=True
            #     ) for f, g in zip(funktion.copy(), generel_form)
            # ]
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
            MathTex(f"d", " = ", "6", r"^2 - 4\cdot", "1", r"\cdot", "9"),
            MathTex(f"d", " = ", "36", " - ", "36", " ", " "),
            MathTex("d", " = ", "0")
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT)
        srec = get_background_rect(trin1, stroke_colour=_c["d"])
        for i in [1, 2, 3]:
            trin1[i][0].set_color(_c["d"])
            trin1[i][2].set_color(_c["b"])
            trin1[i][4].set_color(_c["a"])
            trin1[i][6].set_color(_c["c"])
        trin1[4][0].set_color(_c["d"])
        # self.add(trin1[:2])
        # self.wait(1)
        # self.add(trin1[2])
        # self.wait(1)
        # self.add(trin1[3])
        # self.wait(1)
        # self.add(trin1[4])
        # self.wait(1)
        self.play(
            # Write(trin1[:2])
            FadeIn(trin1[:2], shift=LEFT),
            FadeIn(srec, shift=LEFT)
        )
        # self.wait(1)
        self.slide_pause()
        for i in [2, 3, 4]:
            self.play(
                # FadeIn(trin1[i], shift=DOWN)
                ReplacementTransform(trin1[i-1].copy(), trin1[i])
            )
            # self.wait(1)
            self.slide_pause()

        # self.remove(trin1[:3])
        # trin1[-1].next_to(koef_vals, DOWN, aligned_edge=LEFT)
        # self.remove(trin1[:3])
        self.play(
            FadeOut(trin1[:-1], shift=UP),
            FadeOut(srec, shift=UP),
            trin1[-1].animate.next_to(koef_vals, DOWN, aligned_edge=LEFT)
        )
        # self.wait(1)
        self.slide_pause()

        _xycol = {"x": GREEN, "y": PURE_GREEN}
        trin2 = VGroup(
            Tex("Trin 2: Beregn ", "$x$", "-koordinatet").set_color_by_tex_to_color_map(_xycol),
            VGroup(
                MathTex("x", "_T = ").set_color_by_tex_to_color_map(_xycol),
                self._fraction(
                    MathTex("-", "b").set_color_by_tex("b", _c["b"]),
                    MathTex(r"2\cdot", "a").set_color_by_tex("a", _c["a"])
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
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT)
        srec = get_background_rect(trin2, stroke_colour=_xycol["x"])
        # self.add(trin2[:2])
        # self.wait(1)
        # self.add(trin2[2])
        # self.wait(1)
        # self.add(trin2[3])
        # self.wait(1)
        # self.add(trin2[4])
        # self.wait(1)
        self.play(
            # Write(trin2[:2])
            FadeIn(trin2[:2], shift=LEFT),
            FadeIn(srec, shift=LEFT)
        )
        # self.wait(1)
        self.slide_pause()
        for i in [2, 3, 4]:
            self.play(
                # FadeIn(trin2[i], shift=DOWN)
                ReplacementTransform(trin2[i-1].copy(), trin2[i])
            )
            # self.wait(1)
            self.slide_pause()

        # self.remove(trin2[:3])
        # trin2[-1].next_to(trin1[-1], DOWN, aligned_edge=LEFT)
        # self.remove(trin2[:3])
        # self.wait(1)
        self.play(
            FadeOut(trin2[:-1], shift=UP),
            FadeOut(srec, shift=UP),
            trin2[-1].animate.next_to(trin1[-1], DOWN, aligned_edge=LEFT)
        )
        # self.wait(1)
        self.slide_pause()

        trin3 = VGroup(
            Tex("Trin 3: Beregn ", "$y$", "-koordinatet").set_color_by_tex_to_color_map(_xycol),
            VGroup(
                MathTex("y", "_T = ").set_color_by_tex_to_color_map(_xycol),
                self._fraction(
                    MathTex("-", "d").set_color_by_tex_to_color_map(_c),
                    MathTex(r"4\cdot", "a").set_color_by_tex("a", _c["a"])
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
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT)
        srec = get_background_rect(trin3, stroke_colour=_xycol["y"])
        # self.add(trin3[:2])
        # self.wait(1)
        # self.add(trin3[2])
        # self.wait(1)
        # self.add(trin3[3])
        # self.wait(1)
        # self.add(trin3[4])
        # self.wait(1)
        self.play(
            # Write(trin3[:2])
            FadeIn(trin3[:2], shift=LEFT),
            FadeIn(srec, shift=LEFT)
        )
        # self.wait(1)
        self.slide_pause()
        for i in [2, 3, 4]:
            self.play(
                # FadeIn(trin3[i], shift=DOWN)
                ReplacementTransform(trin3[i-1].copy(), trin3[i])
            )
            # self.wait(1)
            self.slide_pause()

        # self.remove(trin3[:3])
        # trin3[-1].next_to(trin2[-1], DOWN, aligned_edge=LEFT)
        # self.remove(trin3[:3])
        # self.wait(1)
        self.play(
            FadeOut(trin3[:-1], shift=UP),
            FadeOut(srec, shift=UP),
            trin3[-1].animate.next_to(trin2[-1], DOWN, aligned_edge=LEFT)
        )
        # self.wait(1)
        self.slide_pause()

        trin4 = VGroup(
            Tex("Trin 4: Saml ", "$x$", "- og ", "$y$", "-koordinaterne").set_color_by_tex_to_color_map(_xycol),
            MathTex(r"\left( ", "x", r"_T", ", ", "y", r"_T", r"\right) = ", r"\left( ", f"{-b/(2*a):.0f}", ", ", f"{-d/(4*a):.0f}", r"\right)")
        ).arrange(DOWN, aligned_edge=LEFT).shift(RIGHT).to_edge(RIGHT)
        trin4[1][1].set_color(_xycol["x"])
        trin4[1][8].set_color(_xycol["x"])
        trin4[1][4].set_color(_xycol["y"])
        trin4[1][10].set_color(_xycol["y"])
        srec = get_background_rect(trin4, stroke_colour=color_gradient(_xycol.values(), 2))
        # self.add(trin4)
        # self.wait(1)
        self.play(
            # Write(trin4)
            FadeIn(trin4, shift=LEFT),
            FadeIn(srec, shift=LEFT)
        )
        # self.wait(1)
        self.slide_pause()


class ToppunkterThumbnail(Scene):
    def construct(self):
        titel = Tex("Opgave om ", "parablens toppunkt", font_size=72).to_edge(UL)
        titel[1].set_color(YELLOW)
        opgave = Tex("Find koordinatsættet til toppunktet for parablen:", color=BLUE_B)
        funktion = MathTex("f(x) = ", " ", "x^2", " + ", "6", "x", " + ", "9").next_to(opgave, DOWN, aligned_edge=LEFT)
        self.add(titel, opgave, funktion)


if __name__ == "__main__":
    cls = Toppunkter
    class_name = cls.__name__
    transparent = cls.btransparent
    command = rf"manim {sys.argv[0]} {class_name} -p --resolution={_RESOLUTION[q]} --frame_rate={_FRAMERATE[q]}"
    # if transparent:
        # command += " --transparent --format=webm"
    scene_marker(rf"RUNNNING:    {command}")
    subprocess.run(command)
