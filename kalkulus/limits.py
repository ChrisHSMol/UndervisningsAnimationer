from manim import *
import sys
sys.path.append("../")
from helpers import *

slides = False
if slides:
    from manim_slides import Slide


class LimitBase(MovingCameraScene, Slide if slides else Scene):
    def construct(self):
        lim = self.basis_limits()
        self.eksempler(lim)
        self.slide_pause(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def basis_limits(self):
        cmap = {
            "lim": YELLOW,
            "f": BLUE,
            "x": RED
        }
        limit_text = VGroup(
            MathTex(
                r"\lim", "(", "f(x)", ")"
            ),
            MathTex(r"x \rightarrow a").scale(0.5)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.05).scale(3)
        self.add(limit_text)
        self.slide_pause()

        self.play(
            limit_text[0][0].animate.set_color(cmap["lim"])
        )
        self.slide_pause()

        self.play(
            limit_text[0][2].animate.set_color(cmap["f"])
        )
        self.slide_pause()

        self.play(
            limit_text[1].animate.set_color(cmap["x"])
        )
        self.slide_pause()
        self.play(
            limit_text.animate.shift(UP),
            run_time=1
        )
        self.slide_pause()

        lim_forklaring = VGroup(
            Tex(r"''", "Grænseværdien", " for en ", "funktion, f(x)"),
            Tex("når ", "x nærmer sig a", r"''")
        ).arrange(DOWN, aligned_edge=LEFT).next_to(limit_text, DOWN)
        lim_forklaring[0][1].set_color(cmap["lim"])
        lim_forklaring[0][3].set_color(cmap["f"])
        lim_forklaring[1][1].set_color(cmap["x"])
        self.play(
            Write(lim_forklaring),
            run_time=2
        )
        self.slide_pause()

        lim = VGroup(limit_text, lim_forklaring)
        self.play(
            lim.animate.scale(0.33).to_edge(UL)
        )
        return lim

    def eksempler(self, lim):
        def write_limit(f, x="x", a="0"):
            t = MathTex(
                rf"\lim_{{", fr"{x} \rightarrow {a}", rf"}} \left( ", rf"{f}", r"\right)"
            )
            t[0].set_color(YELLOW)
            t[1].set_color(RED)
            t[-2].set_color(BLUE)
            return t
        eksempler = VGroup(
            VGroup(
                write_limit(r"a \cdot x + b"),
                write_limit(r"a \cdot x^2 + b \cdot x + c"),
                write_limit(r"\frac{1}{x}"),
                write_limit(r"\sqrt(x)")
            ),
            VGroup(
                MathTex("=b"),
                MathTex("=c"),
                MathTex(r"=\infty"),
                MathTex("=0")
            )
        )
        animated_limits = VGroup(
            MathTex(r"a \cdot x", "+", "b"),
            MathTex(r"a \cdot x^2", r"+ b \cdot x", "+", "c"),
            MathTex(r"\frac{1}{x}"),
            MathTex(r"\sqrt(x)")
        )
        # self.add(eksempler, animated_limits)

        for i, eks in enumerate(eksempler):
            self.play(
                Write(eks),
                run_time=0.25
            )
            animated_limits[i].to_edge(RIGHT)
            self.play(
                Write(animated_limits[i]),
                run_time=0.25
            )
            self.slide_pause()

            if i in [0, 1, 3]:
                self.play(
                    animated_limits[:-1].animate.scale(
                        0.001
                    ),
                    run_time=4
                )
            elif i == 2:
                self.play(
                    animated_limits[i].animate.scale(
                        1000
                    ),
                    run_time=4
                )
            self.slide_pause()
