from manim import *
import sys
sys.path.append("../")
from helpers import *
import subprocess

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


class GitterLigning(Scene):
    btransparent = True

    def construct(self):
        self.camera.background_color = WHITE
        laserbox = Rectangle(
            width=0.5, height=2, stroke_color=BLACK, fill_color=BLACK, fill_opacity=1
        ).to_edge(DOWN)
        gitter = Line(
            start=laserbox.get_corner(UL), end=laserbox.get_corner(UR), stroke_color=BLACK
        ).next_to(laserbox, UP, buff=1)
        wall = VGroup(
            Line(start=2*LEFT, end=2*RIGHT, stroke_color=BLACK),
            Square(side_length=3, stroke_color=self.camera.background_color, fill_color=self.camera.background_color,
                   fill_opacity=1).set_z_index(5)
        ).arrange(UP, buff=0.04).next_to(gitter, UP, buff=1)
        laserbeam = Line(
            start=laserbox.get_edge_center(UP), end=gitter.get_center(), stroke_color=RED
        )
        splitbeams = VGroup(
            Line(start=gitter.get_center(), end=wall[-1].get_corner(UL), stroke_color=RED),
            Line(start=gitter.get_center(), end=wall[-1].get_edge_center(UP), stroke_color=RED),
            Line(start=gitter.get_center(), end=wall[-1].get_corner(UR), stroke_color=RED),
        )
        self.add(laserbox, gitter, wall, laserbeam, splitbeams)
        self.wait()
        self.play(
            wall.animate.shift(3*UP),
            run_time=4,
            # rate_func=rate_functions.linear
        )
        self.wait()

        trekant = VGroup(
            Polygon(
                splitbeams[1].get_start(), splitbeams[1].get_end(), splitbeams[2].get_end(), color=BLACK
            ).set_z_index(0),
            Line(start=splitbeams[1].get_start(), end=splitbeams[1].get_end(), stroke_color=RED).set_z_index(2),
            Line(start=splitbeams[1].get_end(), end=splitbeams[2].get_end(), stroke_color=BLUE).set_z_index(2),
            Line(start=splitbeams[1].get_start(), end=splitbeams[2].get_end(), stroke_color=BLACK).set_z_index(2),
        )
        trekant.add(Angle(trekant[3], trekant[1], color=GREEN_E, radius=1))
        self.play(
            FadeOut(laserbox, gitter, wall, laserbeam, splitbeams),
            FadeIn(trekant[0])
        )
        self.wait()
        self.play(
            LaggedStart(
                *[Create(m) for m in trekant[1:]],
                lag_ratio=0.75
            ),
            run_time=2
        )
        self.wait()
        self.play(
            trekant.animate.move_to(ORIGIN)
        )
        ligninger = VGroup(
            MathTex(r"\tan(", "v", ") = ", color=BLACK),
            MathTex(r"\over", color=BLACK)
        ).arrange(RIGHT).next_to(trekant, RIGHT)
        ligninger[0][1].set_color(GREEN_E)
        ligninger.add(trekant[2].copy().scale(0.5).next_to(ligninger[1], UP))
        ligninger.add(trekant[1].copy().scale(0.25).next_to(ligninger[1], DOWN))
        self.play(
            LaggedStart(
                Write(ligninger[:2]),
                ReplacementTransform(trekant[2].copy(), ligninger[2]),
                ReplacementTransform(trekant[1].copy(), ligninger[3]),
                lag_ratio=0.75
            ),
            run_time=2
        )
        # self.add(ligninger)
        self.wait()

        ligning2 = VGroup(
            MathTex("v", color=GREEN_E),
            MathTex(r" = \tan^{-1}(", color=BLACK),
            MathTex(r"\frac{\quad}{\quad}", color=BLACK),
            MathTex(r")", color=BLACK)
        ).arrange(RIGHT).next_to(trekant, RIGHT)
        ligning2.add(ligninger[2].copy().next_to(ligning2[2], UP))
        ligning2.add(ligninger[3].copy().next_to(ligning2[2], DOWN))
        self.play(
            TransformMatchingShapes(ligninger, ligning2, transform_mismatches=True)
        )
        self.wait()

        meassures = VGroup(
            MathTex(r"1.50\text{cm}", color=BLUE).next_to(ligning2[2], UP),
            MathTex(r"620\text{cm}", color=RED).next_to(ligning2[2], DOWN),
        )
        self.play(
            *[
                Transform(line, val) for line, val in zip(ligning2[-2:], meassures)
            ]
        )
        self.wait()


if __name__ == "__main__":
    cls = GitterLigning
    class_name = cls.__name__
    transparent = cls.btransparent
    command = rf"manim {sys.argv[0]} {class_name} -p --resolution={_RESOLUTION[q]} --frame_rate={_FRAMERATE[q]}"
    # if transparent:
        # command += " --transparent --format=webm"
    scene_marker(rf"RUNNNING:    {command}")
    subprocess.run(command)
