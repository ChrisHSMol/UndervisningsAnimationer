from manim import *
import sys
sys.path.append("../")
from helpers import *
import numpy as np
import subprocess
import random

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


class CirklensLigning(MovingCameraScene, Slide if slides else Scene):
    btransparent = True

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t=t, slides_bool=slides_bool)

    def construct(self):
        x0, y0, r = 4, -7, 8
        _c = {r"x_0": GREEN, r"y_0": BLUE, "r": RED}
        opgave = VGroup(
            Tex("En cirkel har centrum $C$ og radius $r$ som følger:"),
            MathTex("C(", f"{x0}", ", ", f"{y0}", ")", r",\quad ", "r=", f"{r}"),
            Tex("Bestem en ligning for cirklen.")
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(UP)
        opgave[1][1].set_color(_c[r"x_0"])
        opgave[1][3].set_color(_c[r"y_0"])
        opgave[1][7].set_color(_c["r"])
        opg_linje = Line(start=8*LEFT, end=8*RIGHT).next_to(opgave, DOWN)
        opg_linje.set_stroke(GREY_B, width=random.random() ** 2, opacity=random.random() ** 0.25)
        # self.add(opgave)
        self.play(
            LaggedStart(
                *[FadeIn(o, shift=d) for o, d in zip(opgave, [DOWN, RIGHT, LEFT])],
                Create(opg_linje, run_time=0.5),
                lag_ratio=0.25
            )
        )
        self.slide_pause()

        cirk_lign = VGroup(
            MathTex(r"(x-", "x_0", ")^2 + (y- ", "y_0", ")^2 = ", "r", "^2"),
            MathTex("(x-", f"({x0})", ")^2 + (y-", f"({y0})", ")^2 = ", f"{r}", "^2"),
            MathTex("(x-", f"{x0}", ")^2 + (y", f"+{np.abs(y0)}", ")^2 = ", f"{r}", "^2")
        ).arrange(DOWN, aligned_edge=LEFT).next_to(opgave, DOWN, aligned_edge=LEFT, buff=1)
        cirk_lign[0][1].set_color(_c[r"x_0"])
        cirk_lign[0][3].set_color(_c[r"y_0"])
        cirk_lign[0][-2].set_color(_c[r"r"])
        cirk_lign[1][1].set_color(_c[r"x_0"])
        cirk_lign[1][3].set_color(_c[r"y_0"])
        cirk_lign[1][-2].set_color(_c[r"r"])
        cirk_lign[2][1].set_color(_c[r"x_0"])
        cirk_lign[2][3].set_color(_c[r"y_0"])
        cirk_lign[2][-2].set_color(_c[r"r"])
        # self.add(cirk_lign)
        self.play(
            FadeIn(cirk_lign[0], shift=RIGHT)
        )
        self.slide_pause()
        for i, lign in enumerate(cirk_lign[1:]):
            self.play(
                ReplacementTransform(cirk_lign[i].copy(), lign)
            )
            self.slide_pause()

        self.play(
            FadeOut(cirk_lign[:-1], shift=LEFT),
            cirk_lign[-1].animate.next_to(opgave, DOWN, aligned_edge=LEFT, buff=1)
        )
        self.slide_pause()


class CirklensLigningThumbnail(CirklensLigning):
    def construct(self):
        titel = Tex("Opgave om ", "cirklens ligning", font_size=72).to_edge(UL)
        titel[1].set_color(YELLOW)
        x0, y0, r = 4, -7, 8
        _c = {r"x_0": GREEN, r"y_0": BLUE, "r": RED}
        opgave = VGroup(
            Tex("En cirkel har centrum $C$ og radius $r$ som følger:"),
            MathTex(
                "C(", f"{x0}", ", ", f"{y0}", ")", r",\quad ", "r=", f"{r}"
            ),
            Tex("Bestem en ligning for cirklen.")
        ).arrange(DOWN, aligned_edge=LEFT)
        opgave[1][1].set_color(_c[r"x_0"])
        opgave[1][3].set_color(_c[r"y_0"])
        opgave[1][7].set_color(_c["r"])
        self.add(titel, opgave)


class DifferentialRegning(CirklensLigning):
    btransparent = True

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t=t, slides_bool=slides_bool)

    def thumbnail(self):
        command = rf"manim {sys.argv[0]} DifferentialRegningThumbnail -p --resolution={_RESOLUTION[q]} --format=png"
        scene_marker(rf"RUNNNING:    {command}")
        subprocess.run(command)

    def construct(self):
        # self.thumbnail()
        myTemplate = TexTemplate()
        myTemplate.add_to_preamble(r"\usepackage{amsmath}")

        potens = VGroup(
            Tex("Potensreglen: "),
            MathTex("f(x) = x", "^n"),
            MathTex("\\rightarrow"),
            MathTex("f\'(x) = ", "n", "x", "^{n-1}")
        ).arrange(RIGHT, buff=1)
        potens[0][0][:6].set_color(RED)
        potens[1][-1].set_color(RED)
        potens[3][1].set_color(RED)
        potens[3][-1].set_color(RED)
        eksponent = VGroup(
            Tex("Eksponentreglen: "),
            MathTex("f(x) = ", "\\mathrm{e}", "^x"),
            MathTex("\\rightarrow"),
            MathTex("f\'(x) = ", "\\mathrm{e}", "^x")
        ).arrange(RIGHT, buff=1)
        eksponent[0][0][:9].set_color(RED)
        eksponent[1][1].set_color(RED)
        eksponent[3][1].set_color(RED)
        logaritme = VGroup(
            Tex("Logaritmereglen: "),
            MathTex("f(x) = ", "\\ln", "(x)"),
            MathTex("\\rightarrow"),
            MathTex("f\'(x) = ", "\\frac{1}{x}")
        ).arrange(RIGHT, buff=1)
        logaritme[0][0][:9].set_color(RED)
        logaritme[1][1].set_color(RED)
        logaritme[3][1][:-1].set_color(RED)
        naevner = VGroup(
            Tex("Nævnerreglen: "),
            MathTex("f(x) = ", "\\frac{1}{x^n}"),
            MathTex("\\rightarrow"),
            MathTex("f\'(x) = ", "\\frac{-n}{x^{n+1}}")
        ).arrange(RIGHT, buff=1)
        naevner[0][0][:6].set_color(RED)
        naevner[1][1][-1].set_color(RED)
        naevner[3][1][:2].set_color(RED)
        naevner[3][1][-3:].set_color(RED)

        ligning = VGroup(*[
            MathTex(t) for t in "f(x)= x^3 + x^2 + \\frac{1}{x} - \\mathrm{e}^x - \\ln(x)".split(" ")
        ]).arrange(RIGHT).to_edge(UP)
        solution = VGroup(*[
            MathTex(t) for t in "f\'(x)= 3x^2 + 2x + \\frac{-1}{x^2} - \\mathrm{e}^x - \\frac{1}{x}".split(" ")
        ]).arrange(RIGHT, buff=0.75).next_to(ligning, DOWN, buff=3)
        opgave = VGroup(
            Tex("En funktion $f$ er givet ved:", color=BLUE_B),
            ligning.copy(),
            Tex("Bestem $f\'$.", color=BLUE_B)
        ).arrange(DOWN, aligned_edge=LEFT)
        # self.add(opgave)
        # self.wait(2)
        self.play(
            Write(opgave)
        )
        self.slide_pause()

        # self.remove(opgave)
        self.play(
            FadeOut(opgave[0], shift=RIGHT),
            FadeOut(opgave[-1], shift=LEFT),
            # opgave[1].animate.become(ligning)
            opgave[1].animate.move_to(ligning)
        )
        self.remove(opgave[1])
        self.add(ligning)
        self.slide_pause()
        # ligning.arrange(RIGHT, buff=0.75).to_edge(UP)
        # self.add(ligning)
        # self.wait(2)
        self.play(
            ligning.animate.arrange(RIGHT, buff=0.75).to_edge(UP),
            Write(solution[0])
        )
        self.slide_pause()

        mellemregninger = VGroup(
            VGroup(
                MathTex("x", "^3"),
                MathTex("3", "x", "^{3-1}"),
                MathTex("3", "x", "^2")
            ).move_to(0.5 * (ligning[1].get_center() + solution[1].get_center())),
            VGroup(
                MathTex("", "x", "^2"),
                MathTex("2", "x", "^{2-1}"),
                MathTex("2", "x", "^1"),
                MathTex("2", "x", "")
            ).move_to(0.5 * (ligning[3].get_center() + solution[3].get_center())),
            VGroup(
                # MathTex("\\frac{1}{x}"),
                # MathTex("\\frac{1}{x^1}"),
                # MathTex("\\frac{-1}{x^{1+1}}"),
                # MathTex("\\frac{-1}{x^2}")
                MathTex("1", "\\over", "x"),
                MathTex("1", "\\over", "x^1"),
                MathTex("-1", "\\over", "x^{1+1}"),
                MathTex("-1", "\\over", "x^2")
            ).move_to(0.5 * (ligning[5].get_center() + solution[5].get_center())),
            VGroup(
                MathTex("\\mathrm{e}^x")
            ).move_to(0.5 * (ligning[7].get_center() + solution[7].get_center())),
            VGroup(
                MathTex("\\ln(x)"),
                MathTex("\\frac{1}{x}")
            ).move_to(0.5 * (ligning[9].get_center() + solution[9].get_center())),
        )
        # self.add(solution)

        for j, regneregel in enumerate([potens, potens, naevner, eksponent, logaritme]):
            udr = mellemregninger[j][0]
            # self.add(regneregel.to_edge(DL), udr)
            # self.wait(1)
            self.play(
                # Write(regneregel.to_edge(DL)),
                FadeIn(regneregel.to_edge(DL), shift=RIGHT),
                TransformFromCopy(ligning[2*j + 1], udr)
            )
            self.slide_pause()
            for i, udr in enumerate(mellemregninger[j][1:]):
                # self.remove(mellemregninger[j][i])
                # self.add(udr)
                # self.wait(1)
                self.play(
                    TransformMatchingTex(mellemregninger[j][i], udr, transform_mismatches=True)
                )
                self.slide_pause()
            self.play(
                udr.animate.move_to(solution[2*j + 1]),
                # Transform(udr, solution[2*j + 1]),
                FadeOut(regneregel, shift=RIGHT)
            )
            self.remove(udr)
            self.add(solution[2*j + 1])
            # self.remove(udr, mellemregninger[j][0], regneregel)
        # self.wait(2)
        self.slide_pause()

        self.play(
            # *[ligning[i].animate.move_to(solution[i]) for i in [2, 4, 6, 8]]
            *[FadeOut(ligning[i].copy(), shift=solution[i].get_center() - ligning[i].get_center()) for i in [2, 4, 6, 8]],
            *[FadeIn(solution[i], shift=solution[i].get_center() - ligning[i].get_center()) for i in [2, 4, 6, 8]]
        )
        self.slide_pause()
        final_result = VGroup(*[
            MathTex(t) for t in "f\'(x)= 3x^2 + 2x - \\frac{1}{x^2} - \\mathrm{e}^x - \\frac{1}{x}".split(" ")
        ]).arrange(RIGHT, buff=0.75).move_to(solution)
        self.play(
            # TransformMatchingTex(solution, final_result, transform_mismatches=True)
            *[TransformMatchingTex(m, n, transform_mismatches=True) for m, n in zip(solution, final_result)]
        )
        # self.wait(2)
        self.slide_pause()

        self.play(
            final_result.animate.arrange(RIGHT).next_to(opgave, DOWN),
            FadeOut(ligning, shift=UP),
            FadeIn(opgave.arrange(DOWN, aligned_edge=LEFT))
        )
        self.wait(2)


class DifferentialRegningThumbnail(DifferentialRegning):
    def construct(self):
        titel = Tex("Opgave om ", "differentiering af funktioner", font_size=72).to_edge(UL)
        titel[1].set_color(YELLOW)
        opgave = VGroup(
            Tex("En funktion $f$ er givet ved:", color=BLUE_B),
            MathTex("f(x)= x^3 + x^2 + \\frac{1}{x} - \\mathrm{e}^x - \\ln(x)"),
            Tex("Bestem $f\'$.", color=BLUE_B)
        ).arrange(DOWN, aligned_edge=LEFT)
        self.add(opgave, titel)


class LigningsLoesning(DifferentialRegning):
    btransparent = True

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t=t, slides_bool=slides_bool)

    def construct(self):
        # self.camera.background_color = WHITE
        ligninger = VGroup(
            MathTex("x", "-", "1", "=", "4x", "-", "7"),
            MathTex("x", "-", "1", "-", "4x", "=", "4x", "-", "7", "-", "4x"),
            MathTex("-3x", "-", "1", "=", "-", "7"),
            MathTex("-3x", "-", "1", "+", "1", "=", "-", "7", "+", "1"),
            MathTex("-3x", "=", "-6"),
            MathTex("{-3x", "\\over", "-3}", "=", "{-6", "\\over", "-3}"),
            MathTex("x", "=", "2")
        )
        ligninger[1][3:5].set_color(RED)
        ligninger[1][-2:].set_color(RED)
        ligninger[3][3:5].set_color(RED)
        ligninger[3][-2:].set_color(RED)
        ligninger[5][1:3].set_color(RED)
        ligninger[5][-2:].set_color(RED)

        forklaringer = VGroup(
            VGroup(
                Tex("Mål:  At samle alle ", "x", " på den ene side"),
                Tex("     og alle ", "ikke-x", " på den anden side")
            ).arrange(DOWN, aligned_edge=RIGHT),
            Tex("Ryk ", "$4x$", " over på venstre side"),
            Tex("Reducér"),
            Tex("Ryk ", "$-1$", " over på højre side"),
            Tex("Reducér"),
            Tex("Dividér med ", "$-3$", " på begge sider"),
            Tex("Reducér"),
        ).next_to(ligninger, UP)
        forklaringer[0][0][1].set_color(RED)
        forklaringer[0][1][1].set_color(RED)
        for i in [1, 3, 5]:
            forklaringer[i][1].set_color(RED)

        self.play(
            # Write(ligninger[0]),
            # Write(forklaringer[0][0], run_time=0.5)
            FadeIn(ligninger[0]),
            FadeIn(forklaringer[0][0])
        )
        self.play(
            ligninger[0][0].animate.set_color(RED),
            ligninger[0][4].animate.set_color(RED)
        )
        self.slide_pause()
        self.play(
            ligninger[0][0].animate.set_color(WHITE),
            ligninger[0][4].animate.set_color(WHITE),
            forklaringer[0][0][1].animate.set_color(WHITE),
            # Write(forklaringer[0][1], run_time=0.5),
            FadeIn(forklaringer[0][1]),
            ligninger[0][2].animate.set_color(RED),
            ligninger[0][6].animate.set_color(RED)
        )
        self.slide_pause()
        self.play(
            ligninger[0][2].animate.set_color(WHITE),
            ligninger[0][6].animate.set_color(WHITE)
        )

        i = 0
        self.play(
            # TransformMatchingTex(ligninger[i], ligninger[i+1], transform_mismatches=True),
            # TransformMatchingTex(forklaringer[i], forklaringer[1+i], transform_mismatches=True),
            FadeOut(forklaringer[i], shift=0.5 * UP),
            FadeIn(forklaringer[i+1], shift=0.5 * UP),
            FadeIn(ligninger[i+1].shift(DOWN * 0.5), shift=UP * 0.5)
        )
        self.slide_pause()

        self.play(
            ligninger[i+1].animate.shift(0.5 * UP),
            FadeOut(ligninger[i], shift=0.5 * UP)
        )
        self.slide_pause()

        i += 1
        self.play(
            FadeOut(forklaringer[i], shift=0.5 * UP),
            FadeIn(forklaringer[i+1], shift=0.5 * UP),
            FadeIn(ligninger[i+1].shift(DOWN * 0.5), shift=UP * 0.5)
        )
        self.slide_pause()

        self.play(
            ligninger[i+1].animate.shift(0.5 * UP),
            FadeOut(ligninger[i], shift=0.5 * UP)
        )
        self.slide_pause()

        i += 1
        self.play(
            FadeOut(forklaringer[i], shift=0.5 * UP),
            FadeIn(forklaringer[i+1], shift=0.5 * UP),
            FadeIn(ligninger[i+1].shift(DOWN * 0.5), shift=UP * 0.5)
        )
        self.slide_pause()

        self.play(
            ligninger[i+1].animate.shift(0.5 * UP),
            FadeOut(ligninger[i], shift=0.5 * UP)
        )
        self.slide_pause()

        i += 1
        self.play(
            FadeOut(forklaringer[i], shift=0.5 * UP),
            FadeIn(forklaringer[i+1], shift=0.5 * UP),
            FadeIn(ligninger[i+1].shift(DOWN * 0.5), shift=UP * 0.5)
        )
        self.slide_pause()

        self.play(
            ligninger[i+1].animate.shift(0.5 * UP),
            FadeOut(ligninger[i], shift=0.5 * UP)
        )
        self.slide_pause()

        i += 1
        self.play(
            FadeOut(forklaringer[i], shift=0.5 * UP),
            FadeIn(forklaringer[i+1], shift=0.5 * UP),
            FadeIn(ligninger[i+1].shift(DOWN * 1.0), shift=UP * 0.5)
        )
        self.slide_pause()

        self.play(
            ligninger[i+1].animate.shift(1.0 * UP),
            FadeOut(ligninger[i], shift=0.5 * UP)
        )
        self.slide_pause()

        i += 1
        self.play(
            FadeOut(forklaringer[i], shift=0.5 * UP),
            FadeIn(forklaringer[i+1], shift=0.5 * UP),
            FadeIn(ligninger[i+1].shift(DOWN * 1.0), shift=UP * 0.5)
        )
        self.slide_pause()

        self.play(
            ligninger[i+1].animate.shift(1.0 * UP),
            FadeOut(ligninger[i], shift=0.5 * UP)
        )
        self.slide_pause()

        self.play(
            LaggedStart(
                *[FadeOut(m) for m in self.mobjects],
                lag_ratio=0.25
            )
        )


class LigningsLoesningThumbnail(LigningsLoesning):
    def construct(self):
        titel = Tex("Opgave om ", "løsning af ligninger", font_size=80).to_edge(UL)
        titel[1].set_color(YELLOW)
        opgave = VGroup(
            Tex("Løs ligningen:", color=BLUE_B),
            MathTex("x", "-", "1", "=", "4x", "-", "7")
        ).arrange(DOWN, aligned_edge=LEFT)
        self.add(opgave, titel)


class NulPunkter(LigningsLoesning):
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


class NulpunkterThumbnail(NulPunkter):
    def construct(self):
        titel = Tex("Opgave om ", "parablens nulpunkter", font_size=72).to_edge(UL)
        titel[1].set_color(YELLOW)
        opgave = Tex("Bestem nulpunkterne for parablen:", color=BLUE_B)
        funktion = MathTex("f(x) = ", "-2", "x^2", " ", "-2", "x", " + ", "4").next_to(opgave, DOWN, aligned_edge=LEFT)
        self.add(titel, opgave, funktion)


class PrikProdukt(NulPunkter):
    btransparent = True

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t=t, slides_bool=slides_bool)

    def construct(self):
        va, vb = [-2, 5], [3, -2]
        _c = {r"\vec{a}": RED, r"\vec{b}": YELLOW}
        opgave = VGroup(
            Tex("I et koordinatsystem er der givet vektorerne:"),
            MathTex(
                r"\vec{a}", fr" = \begin{{pmatrix}} {va[0]} \\ {va[1]} \end{{pmatrix}}\quad",
                r"\vec{b}", fr" = \begin{{pmatrix}} {vb[0]} \\ {vb[1]} \end{{pmatrix}}"
            ).set_color_by_tex_to_color_map(_c),
            Tex(r"Bestem prikproduktet ", r"$\vec{a}$", r"$\bullet$", r"$\vec{b}$", ".").set_color_by_tex_to_color_map(_c)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(UL)
        opgave[1][1][2:5].set_color(_c[r"\vec{a}"])
        opgave[1][3][2:5].set_color(_c[r"\vec{b}"])
        # self.add(opgave)
        self.play(
            LaggedStart(
                *[FadeIn(o, shift=d) for o, d in zip(opgave, [DOWN, RIGHT, LEFT])],
                lag_ratio=0.25
            )
        )
        self.slide_pause()

        regneregel = VGroup(
            Tex("Regneregel: "),
            MathTex(
                r"\vec{a}", r"\bullet", r"\vec{b}", " &= ", r"\begin{pmatrix} a_x \\ a_y \end{pmatrix}", r"\bullet",
                r"\begin{pmatrix} b_x \\ b_y \end{pmatrix}", r" = ", "a_x", r"\cdot", "b_x", " + ", "a_y", r"\cdot", "b_y"
            ).set_color_by_tex_to_color_map(_c)
        ).scale(0.75).arrange(DOWN, aligned_edge=LEFT).to_edge(DR)
        regneregel[1][4][1:5].set_color(_c[r"\vec{a}"])
        regneregel[1][6][1:5].set_color(_c[r"\vec{b}"])
        regneregel[1][8].set_color(_c[r"\vec{a}"])
        regneregel[1][12].set_color(_c[r"\vec{a}"])
        regneregel[1][10].set_color(_c[r"\vec{b}"])
        regneregel[1][14].set_color(_c[r"\vec{b}"])
        srec1 = get_background_rect(regneregel, stroke_colour=color_gradient(list(_c.values()), 3))
        # self.add(regneregel, srec1)
        self.play(
            FadeIn(regneregel, shift=LEFT),
            FadeIn(srec1, shift=LEFT)
        )
        self.slide_pause()

        mellemregninger = VGroup(
            MathTex(
                r"\vec{a}", r"\bullet", r"\vec{b}", " = ", "a_x", r"\cdot", "b_x", " + ", "a_y", r"\cdot", "b_y"
            ).set_color_by_tex_to_color_map(_c),
            MathTex(
                r"\vec{a}", r"\bullet", r"\vec{b}", " = ", f"({va[0]})", r"\cdot", f"{vb[0]}", "+", f"{va[1]}", r"\cdot", f"({vb[1]})"
            ).set_color_by_tex_to_color_map(_c),
            MathTex(
                r"\vec{a}", r"\bullet", r"\vec{b}", " = ", f"({va[0]*vb[0]})", " ", " ", "+", f"({va[1]*vb[1]})", " ", " "
            ).set_color_by_tex_to_color_map(_c),
            MathTex(
                r"\vec{a}", r"\bullet", r"\vec{b}", " = ", f"{va[0]*vb[0]}", " ", " ", " ", f"{va[1]*vb[1]}", " ", " "
            ).set_color_by_tex_to_color_map(_c),
            MathTex(
                r"\vec{a}", r"\bullet", r"\vec{b}", " = ", f"{va[0]*vb[0] + va[1]*vb[1]}", " ", " ", " ", " ", " ", " "
            ).set_color_by_tex_to_color_map(_c)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(opgave, DOWN, aligned_edge=LEFT)
        mellemregninger[0][4].set_color(_c[r"\vec{a}"])
        mellemregninger[0][8].set_color(_c[r"\vec{a}"])
        mellemregninger[0][6].set_color(_c[r"\vec{b}"])
        mellemregninger[0][10].set_color(_c[r"\vec{b}"])
        mellemregninger[1][4].set_color(_c[r"\vec{a}"])
        mellemregninger[1][8].set_color(_c[r"\vec{a}"])
        mellemregninger[1][6].set_color(_c[r"\vec{b}"])
        mellemregninger[1][10].set_color(_c[r"\vec{b}"])
        mellemregninger[2][4].set_color(interpolate_color(_c[r"\vec{a}"], _c[r"\vec{b}"], 0.5))
        mellemregninger[2][8].set_color(interpolate_color(_c[r"\vec{a}"], _c[r"\vec{b}"], 0.5))
        mellemregninger[3][4].set_color(interpolate_color(_c[r"\vec{a}"], _c[r"\vec{b}"], 0.5))
        mellemregninger[3][8].set_color(interpolate_color(_c[r"\vec{a}"], _c[r"\vec{b}"], 0.5))
        mellemregninger[4][4].set_color(interpolate_color(_c[r"\vec{a}"], _c[r"\vec{b}"], 0.5))
        # self.add(mellemregninger)
        self.play(
            FadeIn(mellemregninger[0], shift=RIGHT)
        )
        self.slide_pause()
        for i, lign in enumerate(mellemregninger[1:]):
            self.play(
                ReplacementTransform(mellemregninger[i].copy(), lign)
            )
            self.slide_pause()

        self.play(
            FadeOut(mellemregninger[:-1], shift=LEFT),
            mellemregninger[-1].animate.next_to(opgave, DOWN, aligned_edge=LEFT)
        )
        self.slide_pause()


class PrikProduktThumbnail(PrikProdukt):
    def construct(self):
        titel = Tex("Opgave om ", "prikproduktet af to vektorer", font_size=72).to_edge(UL)
        titel[1].set_color(YELLOW)
        va, vb = [-2, 5], [3, -2]
        _c = {r"\vec{a}": RED, r"\vec{b}": YELLOW}
        opgave = VGroup(
            Tex("I et koordinatsystem er der givet vektorerne:"),
            MathTex(
                r"\vec{a}", fr" = \begin{{pmatrix}} {va[0]} \\ {va[1]} \end{{pmatrix}}\quad",
                r"\vec{b}", fr" = \begin{{pmatrix}} {vb[0]} \\ {vb[1]} \end{{pmatrix}}"
            ).set_color_by_tex_to_color_map(_c),
            Tex(r"Bestem prikproduktet ", r"$\vec{a}$", r"$\bullet$", r"$\vec{b}$", ".").set_color_by_tex_to_color_map(_c)
        ).arrange(DOWN, aligned_edge=LEFT)
        opgave[1][1][2:5].set_color(_c[r"\vec{a}"])
        opgave[1][3][2:5].set_color(_c[r"\vec{b}"])
        self.add(titel, opgave)


class RetningsVektorer(PrikProdukt):
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


class RetningsVektorerThumbnail(RetningsVektorer):
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


class TopPunkter(RetningsVektorer):
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


class ToppunkterThumbnail(TopPunkter):
    def construct(self):
        titel = Tex("Opgave om ", "parablens toppunkt", font_size=72).to_edge(UL)
        titel[1].set_color(YELLOW)
        opgave = Tex("Find koordinatsættet til toppunktet for parablen:", color=BLUE_B)
        funktion = MathTex("f(x) = ", " ", "x^2", " + ", "6", "x", " + ", "9").next_to(opgave, DOWN, aligned_edge=LEFT)
        self.add(titel, opgave, funktion)


if __name__ == "__main__":
    classes = [
        CirklensLigning,
        DifferentialRegning,
        LigningsLoesning,
        NulPunkter,
        PrikProdukt,
        RetningsVektorer,
        TopPunkter
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
            if class_name+"Thumbnail" in dir():
                command = rf"manim {sys.argv[0]} {class_name}Thumbnail -pq{q} -o {class_name}Thumbnail.png"
                scene_marker(rf"RUNNNING:    {command}")
                subprocess.run(command)
