from manim import *
import sys
sys.path.append("../")
from helpers import *
import subprocess

slides = False
if slides:
    from manim_slides import Slide


class BinomialIntro(MovingCameraScene, Slide if slides else Scene):
    name = "BinomialIntro"

    def construct(self):
        # self.slide_pause()
        self.coin_probability()
        self.slide_pause(5)

    def get_factors(self, n):
        i = int(n ** 0.5 + 0.5)
        while n % i != 0:
            i -= 1
        return i, n // i

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def coin_probability(self):
        np.random.seed(42)
        coin_plat = CoinFace(0)
        coin_krone = CoinFace(1)

        n = 100
        kr = 80
        pl = n - kr
        n_factors = self.get_factors(n)
        coins_100 = VGroup(
            *[CoinFace(0) for _ in range(pl)],
            *[CoinFace(1) for _ in range(kr)],
        )
        coins_100.shuffle_submobjects()
        # coins_100.scale(0.75).arrange_in_grid(rows=10, cols=10, buff=0.1)
        coins_100.scale(0.75).arrange_in_grid(rows=n_factors[0], cols=n_factors[1], buff=0.1)
        opener = VGroup(
            VGroup(
                Tex("Hvis du har set "),
                Integer(kr, color=coin_krone.fill_color),
                CoinFace(1),
                Tex("og "),
                Integer(pl, color=coin_plat.fill_color),
                CoinFace(0),
            ).arrange(RIGHT),
            VGroup(
                Tex("Hvad er så $P$("), coin_krone.copy(), Tex(")?")
            ).arrange(RIGHT, buff=0.1)
        ).arrange(DOWN, aligned_edge=ORIGIN).to_edge(UP)
        coins_100.next_to(opener, DOWN)
        self.add(opener, coins_100)
        # self.add(coins_100)
        # self.play(
        #     DrawBorderThenFill(coins_100, lag_ratio=0.2),
        #     Write(opener, lag_ratio=0.5),
        #     run_time=10
        # )
        # self.play(
        #     LaggedStart(
        #         *[
        #             Circumscribe(
        #                 m, color=coin_plat.fill_color, buff=0.05, time_width=1.5, fade_out=True, stroke_width=1.5
        #             ) for m in coins_100 if m.value == 0
        #         ],
        #         lag_ratio=0.01
        #     ),
        #     run_time=5
        # )
        # self.play(
        #     LaggedStart(
        #         *[
        #             Circumscribe(
        #                 m, color=coin_krone.fill_color, buff=0.05, time_width=1.5, fade_out=True, stroke_width=1.5
        #             ) for m in coins_100 if m.value == 1
        #         ],
        #         lag_ratio=0.01
        #     ),
        #     run_time=5
        # )
        # self.slide_pause()

        self.play(
            opener.animate.shift(3*LEFT),
            coins_100.animate.shift(3*LEFT),
        )

        plane = Axes(
            x_range=[0, 11, 1],
            y_range=[0, 1, 0.1],
            x_length=self.camera.frame.get_width() * 0.375,
            y_length=self.camera.frame.get_height() * 0.5,
            tips=False,
        ).to_edge(RIGHT)
        plane_ticks = VGroup(
            VGroup(*[
                Integer(i, font_size=20).move_to(plane.c2p(i+0.5, -0.05)) for i in range(11)
            ]),
            # VGroup(*[
            #     MathTex(rf"{i*10:.0f}\%", font_size=20).move_to(plane.c2p(-1, i/10)) for i in range(11)
            # ])
        )
        self.add(plane, plane_ticks)

        srecs = VGroup(*[
            get_background_rect(
                coins_100[10*i:10*i+10],
                stroke_colour=interpolate_color(
                    coin_plat.fill_color, coin_krone.fill_color, 0.1*sum([c.value for c in coins_100[10*i:10*i+10]])
                ),
                buff=0,
            ) for i in range(10)
        ])

        offsets = {str(i): 0 for i in range(11)}
        for i in range(10):
            print(offsets)
            n_kr = sum([c.value for c in coins_100[10*i:10*i+10]])
            self.play(
                FadeIn(srecs[i])
            )
            self.play(
                coins_100[10*i:10*i+10].copy().animate.scale(1/10).move_to(
                    plane.c2p(n_kr + 0.5, offsets[str(n_kr)] * 1/10)
                )
            )
            offsets[str(n_kr)] += 1


if __name__ == "__main__":
    class_name = BinomialIntro.name
    scene_marker(rf"RUNNNING:    manim {sys.argv[0]} {class_name} -pqh")
    subprocess.run(rf"manim {sys.argv[0]} {class_name} -pqh")
    if slides:
        scene_marker(rf"RUNNING:    manim-slides convert {class_name} {class_name}.html")
        # subprocess.run(rf"manim-slides convert {class_name} {class_name}.html")
        subprocess.run(rf"manim-slides {class_name}")
