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


class LigningsLoesning(Slide if slides else Scene):
# class LigningsLoesning(Scene):
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

        # i += 1
        # self.play(
        #     TransformMatchingTex(ligninger[i], ligninger[i+1], transform_mismatches=True),
        #     TransformMatchingTex(forklaringer[i], forklaringer[1+i], transform_mismatches=True)
        # )
        # self.slide_pause()
        #
        # i += 1
        # self.play(
        #     TransformMatchingTex(ligninger[i], ligninger[i+1], transform_mismatches=True),
        #     TransformMatchingTex(forklaringer[i], forklaringer[1+i], transform_mismatches=True)
        # )
        # self.slide_pause()
        #
        # i += 1
        # self.play(
        #     TransformMatchingTex(ligninger[i], ligninger[i+1], transform_mismatches=True),
        #     TransformMatchingTex(forklaringer[i], forklaringer[1+i], transform_mismatches=True)
        # )
        # self.slide_pause()
        #
        # i += 1
        # self.play(
        #     # TransformMatchingTex(ligninger[i], ligninger[i+1], transform_mismatches=True)
        #     ReplacementTransform(ligninger[i], ligninger[i+1]),
        #     TransformMatchingTex(forklaringer[i], forklaringer[1+i], transform_mismatches=True)
        # )
        # self.slide_pause()
        #
        # i += 1
        # self.play(
        #     # TransformMatchingTex(ligninger[i], ligninger[i+1], transform_mismatches=True)
        #     ReplacementTransform(ligninger[i], ligninger[i+1]),
        #     TransformMatchingTex(forklaringer[i], forklaringer[1+i], transform_mismatches=True)
        # )
        # self.slide_pause()


if __name__ == "__main__":
    cls = LigningsLoesning
    class_name = cls.__name__
    transparent = cls.btransparent
    command = rf"manim {sys.argv[0]} {class_name} -p --resolution={_RESOLUTION[q]} --frame_rate={_FRAMERATE[q]}"
    # if transparent:
        # command += " --transparent --format=webm"
    scene_marker(rf"RUNNNING:    {command}")
    subprocess.run(command)
