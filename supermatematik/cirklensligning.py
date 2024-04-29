from manim import *
import sys
sys.path.append("../")
from helpers import *
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


class CirklensLigning(Scene if not slides else Slide):
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


class CirklensLigningThumbnail(Scene):
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


if __name__ == "__main__":
    cls = CirklensLigning
    class_name = cls.__name__
    transparent = cls.btransparent
    command = rf"manim {sys.argv[0]} {class_name} -p --resolution={_RESOLUTION[q]} --frame_rate={_FRAMERATE[q]}"
    # if transparent:
    #     command += " --transparent --format=webm"
    scene_marker(rf"RUNNNING:    {command}")
    subprocess.run(command)
    if slides:
        class_name += "Thumbnail"
        command = rf"manim {sys.argv[0]} {class_name} -pq{q} -o {class_name}.png"

