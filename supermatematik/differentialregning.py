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


# class DifferentialRegning(Scene):
class DifferentialRegning(Slide):
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


class DifferentialRegningThumbnail(Scene):
    def construct(self):
        titel = Tex("Opgave om ", "differentiering af funktioner", font_size=72).to_edge(UL)
        titel[1].set_color(YELLOW)
        opgave = VGroup(
            Tex("En funktion $f$ er givet ved:", color=BLUE_B),
            MathTex("f(x)= x^3 + x^2 + \\frac{1}{x} - \\mathrm{e}^x - \\ln(x)"),
            Tex("Bestem $f\'$.", color=BLUE_B)
        ).arrange(DOWN, aligned_edge=LEFT)
        self.add(opgave, titel)


if __name__ == "__main__":
    cls = DifferentialRegning
    class_name = cls.__name__
    transparent = cls.btransparent
    command = rf"manim {sys.argv[0]} {class_name} -p --resolution={_RESOLUTION[q]} --frame_rate={_FRAMERATE[q]}"
    # if transparent:
        # command += " --transparent --format=webm"
    scene_marker(rf"RUNNNING:    {command}")
    subprocess.run(command)
