from manim import *
import sys
sys.path.append("../")
from helpers import *
import subprocess
import random

slides = False
if slides:
    from manim_slides import Slide


q = "l"
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


class AnnuitetsOpsparing(MovingCameraScene, Slide if slides else Scene):
    btransparent = False

    def construct(self):
        self.annuitet()
        self.wait(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t=t, slides_bool=slides_bool)

    def annuitet(self):
        # startudtryk = VGroup(
        #     MathTex(r"A_n = "), MathTex(r"b"), MathTex(" + "), MathTex(r"b \cdot (1+r)"), MathTex(" + "),
        #     MathTex(r"b \cdot (1+r)^2"), MathTex(" + "), MathTex(r"\dotsb"), MathTex(" + "), MathTex(r"b \cdot (1+r)^{n-1}")
        # ).arrange(RIGHT)
        _cols = {
            "A": RED,
            "b": BLUE,
            "n": YELLOW
        }
        # startudtryk = MathTex(
        #     r"A_n", r"=b", r"+ b \cdot (1+r)", r"+ b \cdot (1+r)^2", r"+\dotsb+",
        #     r"b \cdot (1+r)^{n-1}"#, substrings_to_isolate=list(_cols.keys())
        # ).scale(0.75).shift(2*UP)#.set_color_by_tex_to_color_map(_cols)
        startudtryk = VGroup(*[
            MathTex(t) for t in r"A_n = b + b \cdot (1+r) + b \cdot (1+r)^2 + \dotsb + b \cdot (1+r)^{n-1}".split(" ")
        ]).arrange(RIGHT, buff=0.15).scale(0.75).shift(4*UP)
        # startforklaring = VGroup(
        #     VGroup(Tex("Opsparingsannuiteten").scale(0.75).next_to(startudtryk[0], 2*UP)),
        #     VGroup(Tex(r"Den seneste indbetaling.\\Ingen rente indtjent").scale(0.75).next_to(startudtryk[1], 2*UP)),
        #     VGroup(Tex(r"Den næstseneste indbetaling.\\Rente indtjent 1 gang").scale(0.75).next_to(startudtryk[2], 2*UP)),
        #     VGroup(Tex(r"Den tredjeseneste indbetaling.\\Rente indtjent 2 gange").scale(0.75).next_to(startudtryk[3], 2*UP)),
        #     VGroup(Tex(r"Og så videre...").scale(0.75).next_to(startudtryk[4], 2*UP)),
        #     VGroup(Tex(r"Den første indbetaling.\\Rente indtjent $n-1$ gange").scale(0.75).next_to(startudtryk[5], 2*UP)),
        # )
        # for i in range(len(startforklaring)):
        #     startforklaring[i].add(
        #         # Arrow(start=startforklaring[i].get_bottom(), end=startudtryk[i].get_top(), buff=0)
        #         Brace(startudtryk[i], direction=startforklaring[i].get_bottom() - startudtryk[i].get_top())
        #     )
        # # self.add(startudtryk)
        # for i in range(len(startudtryk)):
        #     self.add(startudtryk[i], startforklaring[i])
        #     # self.play(
        #     #     Write(startudtryk[i]),
        #     #     GrowFromEdge(
        #     #         startforklaring[i][1], edge=DOWN
        #     #     ) if not i else ReplacementTransform(startforklaring[i-1][1], startforklaring[i][1]),
        #     #     FadeIn(startforklaring[i][0], shift=RIGHT) if not i else AnimationGroup(
        #     #         FadeOut(startforklaring[i-1][0], shift=RIGHT),
        #     #         FadeIn(startforklaring[i][0], shift=RIGHT)
        #     #     ),
        #     #     run_time=0.5
        #     # )
        #     self.wait(0.5)
        #     self.remove(startforklaring[i])
        # self.play(
        #     FadeOut(startforklaring[-1][0], shift=RIGHT),
        #     ShrinkToCenter(startforklaring[-1][1]),
        #     run_time=0.5
        # )
        self.add(startudtryk)

        # manip1 = MathTex(
        #     r"A_n", r"\cdot(1+r)", r"=\big(b", r"+ b \cdot (1+r)", r"+ b \cdot (1+r)^2", r"+\dotsb+",
        #     r"b \cdot (1+r)^{n-1}\big)", r"\cdot(1+r)"
        # ).scale(0.75).next_to(startudtryk, DOWN)
        manip1 = VGroup(*[
            MathTex(t) for t in r"A_n \cdot (1+r) = \big( b + b \cdot (1+r) + b \cdot (1+r)^2 + \dotsb + b \cdot (1+r)^{n-1} \big) \cdot (1+r)".split(" ")
        ]).arrange(RIGHT, buff=0.15).scale(0.75).next_to(startudtryk, DOWN)
        self.add(manip1)

        # manip2 = MathTex(
        #     r"A_n", r"\cdot(1+r)", r"=b\cdot(1+r)", r"+ b \cdot (1+r)^2", r"+ b \cdot (1+r)^3", r"+\dotsb+",
        #     r"b \cdot (1+r)^{n}"
        # ).scale(0.75).next_to(manip1, DOWN)
        manip2 = VGroup(*[
            MathTex(t) for t in r"A_n \cdot (1+r) = b \cdot (1+r) + b \cdot (1+r)^2 + b \cdot (1+r)^3 + \dotsb + b \cdot (1+r)^{n}".split(" ")
        ]).arrange(RIGHT, buff=0.15).scale(0.75).next_to(manip1, DOWN)
        self.add(manip2)

        # manip3 = MathTex(
        #     r"A_n", r"\cdot(1+r)", r"=b\cdot(1+r)", r"+ b \cdot (1+r)^2", r"+\dotsb+", r"b \cdot (1+r)^{n-1}"
        #     r"+b \cdot (1+r)^{n}"
        # ).scale(0.75).next_to(manip2, DOWN)
        manip3 = VGroup(*[
            MathTex(t) for t in r"A_n \cdot (1+r) = b \cdot (1+r) + b \cdot (1+r)^2 + \dotsb + b \cdot (1+r)^{n-1} + b \cdot (1+r)^{n}".split(" ")
        ]).arrange(RIGHT, buff=0.15).scale(0.75).next_to(manip2, DOWN)
        self.add(manip3)

        manip4 = VGroup(*[
            MathTex(t) for t in r"A_n \cdot (1+r) - A_n = b \cdot (1+r) + b \cdot (1+r)^2 + \dotsb + b \cdot (1+r)^{n-1} + b \cdot (1+r)^{n} - A_n".split(" ")
        ]).arrange(RIGHT, buff=0.15).scale(0.75).next_to(manip3, DOWN)
        self.add(manip4)

        manip5 = VGroup(*[
            MathTex(t) for t in r"A_n \cdot \left( (1+r) - 1 \right) = b \cdot (1+r)^{n} - b".split(" ")
        ]).arrange(RIGHT, buff=0.15).scale(0.75).next_to(manip4, DOWN)
        self.add(manip5)

        manip6 = VGroup(*[
            MathTex(t) for t in r"A_n \cdot \left( r \right) = b \cdot \left( (1+r)^{n} - 1 \right)".split(" ")
        ]).arrange(RIGHT, buff=0.15).scale(0.75).next_to(manip5, DOWN)
        self.add(manip6)

        manip7 = VGroup(*[
            MathTex(t) for t in r"A_n = \frac{b\cdot\left((1+r)^{n}-1\right)}{r}".split(" ")
        ]).arrange(RIGHT, buff=0.15).scale(0.75).next_to(manip6, DOWN)
        self.add(manip7)

        manip8 = VGroup(*[
            MathTex(t) for t in r"A_n = b \cdot \frac{(1+r)^{n}-1}{r}".split(" ")
        ]).arrange(RIGHT, buff=0.15).scale(0.75).next_to(manip7, DOWN)
        self.add(manip8)


if __name__ == "__main__":
    cls = AnnuitetsOpsparing
    class_name = cls.__name__
    transparent = cls.btransparent
    command = rf"manim {sys.argv[0]} {class_name} -p --resolution={_RESOLUTION[q]} --frame_rate={_FRAMERATE[q]}"
    # if transparent:
    #     command += " --transparent --format=webm"
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

