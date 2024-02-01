from manim import *
import sys
sys.path.append("../")
from helpers import *
import subprocess


class Blypose(Scene):
    def construct(self):
        e_pot = MathTex(r"E_{pot}", r"=", r"m", r"\cdot", r"g", r"\cdot", r"h", color=YELLOW_A)
        e_term = MathTex(r"E_{term}", r"=", r"m", r"\cdot", r"c_{Pb}", r"\cdot", r"\Delta", r"T", color=RED_A).next_to(e_pot, DOWN)
        self.add(e_pot, e_term)
        self.wait()

        int_eq = VGroup(
            MathTex(r"m", r"\cdot", r"c_{Pb}", r"\cdot", r"\Delta", r"T", color=RED_A),
            MathTex(r"="),
            MathTex(r"m", r"\cdot", r"g", r"\cdot", r"h", color=YELLOW_A)
        ).arrange(RIGHT)
        self.play(
            TransformMatchingTex(
                e_pot,
                int_eq[-1],
            ),
            TransformMatchingTex(
                e_term,
                int_eq[0],
            ),
            FadeIn(int_eq[1])
        )
        self.wait()

        eq1 = VGroup(
            MathTex(r"c_{Pb}", r"\cdot", r"\Delta", r"T", color=RED_A),
            MathTex(r"="),
            MathTex(r"g", r"\cdot", r"h", color=YELLOW_A)
        ).arrange(RIGHT)

        crossouts = VGroup(
            Line(start=int_eq[0][0].get_corner(DL), end=int_eq[0][0].get_corner(UR), color=RED).scale(2),
            Line(start=int_eq[-1][0].get_corner(DL), end=int_eq[-1][0].get_corner(UR), color=RED).scale(2),
        )
        self.play(
            *[Create(c) for c in crossouts]
        )
        self.play(
            FadeOut(crossouts),
            TransformMatchingTex(int_eq, eq1, transform_mismatches=True)
        )
        self.wait()

        eq2 = VGroup(
            MathTex(r"\Delta", r"T", color=RED_A),
            MathTex(r"="),
            MathTex(r"{g", r"\cdot", r"h", r"\over", r"c_{Pb}}", color=YELLOW_A)
        ).arrange(RIGHT)
        self.play(
            TransformMatchingTex(eq1, eq2, transform_mismatches=True)
        )
        self.wait()

        eq3 = VGroup(
            MathTex(r"\Delta", r"T", color=RED_A),
            MathTex(r"="),
            MathTex(r"{g", r"\over", r"c_{Pb}}", r"\cdot", r"h", color=YELLOW_A)
        ).arrange(RIGHT)
        self.play(
            TransformMatchingTex(eq2, eq3, transform_mismatches=False)
        )
        self.wait()


if __name__ == "__main__":
    class_name = Blypose.__name__
    command = rf"manim {sys.argv[0]} {class_name} -pqh"
    scene_marker(rf"RUNNNING:    {command}")
    subprocess.run(command)
