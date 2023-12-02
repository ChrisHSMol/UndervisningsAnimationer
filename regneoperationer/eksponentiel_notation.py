from manim import *
import sys
sys.path.append("../")
from helpers import *
import subprocess

slides = False
if slides:
    from manim_slides import Slide
q = "l"


class EkspNot(MovingCameraScene, Slide if slides else Scene):
    def construct(self):
        def AnimateIntegerChange(n1: Mobject, n2: Mobject, direction=0.5*DOWN):
            return AnimationGroup(
                FadeOut(n1, shift=direction),
                FadeIn(n2, shift=direction)
            )

        tal = VGroup(
            MathTex("123.5"),
            MathTex(r"123.5\cdot1"),
            MathTex(r"123.5\cdot10^0"),
            MathTex(r"12.35\cdot10^1"),
            MathTex(r"1.235\cdot10^2")
        ).arrange(ORIGIN, aligned_edge=LEFT)
        self.add(tal[0])
        for i, t in enumerate(tal[1:]):
            self.play(
                TransformMatchingTex(tal[i], t, transform_mismatches=True)
                # ReplacementTransform(tal[i], t, path_arc=PI)
                # FadeOut(tal[i]),
                # FadeIn(t)
            )
            self.wait()
        self.play(TransformMatchingTex(t, tal[2]))
        self.wait()
        self.play(
            AnimateIntegerChange(tal[2][-1], tal[3][-1])
        )
        self.wait()


if __name__ == "__main__":
    class_name = EkspNot.__name__
    command = rf"manim {sys.argv[0]} {class_name} -pq{q} --disable_caching"
    scene_marker(rf"RUNNNING:    {command}")
    subprocess.run(command)

