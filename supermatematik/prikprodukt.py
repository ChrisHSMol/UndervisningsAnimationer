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


class PrikProdukt(Scene if not slides else Slide):
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


class PrikProduktThumbnail(Scene):
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


if __name__ == "__main__":
    cls = PrikProdukt
    class_name = cls.__name__
    transparent = cls.btransparent
    command = rf"manim {sys.argv[0]} {class_name} -p --resolution={_RESOLUTION[q]} --frame_rate={_FRAMERATE[q]}"
    # if transparent:
    #     command += " --transparent --format=webm"
    scene_marker(rf"RUNNNING:    {command}")
    subprocess.run(command)

    if slides:
        command = rf"manim {sys.argv[0]} {class_name}Thumbnail -pqh -o {class_name}Thumbnail.png"
        scene_marker(rf"RUNNNING:    {command}")
        subprocess.run(command)

        command = rf"manim-slides convert {class_name} {class_name}.html"
        scene_marker(rf"RUNNNING:    {command}")
        subprocess.run(command)
