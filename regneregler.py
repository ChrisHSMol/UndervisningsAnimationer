from manim import *
from helpers import *
import numpy as np

slides = False
if slides:
    from manim_slides import Slide


class KvadratSaetning(Slide if slides else Scene):
    def construct(self):
        self.plusplus()
        # self.slide_pause(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t=t, slides_bool=slides_bool)

    def plusplus(self):
        total = 6
        a = ValueTracker(total/2)
        bigrect = Square(
            total,
            color=GREEN,
            fill_color=GREEN,
            fill_opacity=0.075,
            z_index=3
        )
        # self.add(bigrect)
        self.play(
            DrawBorderThenFill(bigrect)
        )

        a_rect = always_redraw(lambda: Square(
            a.get_value(),
            color=BLUE,
            fill_color=BLUE,
            fill_opacity=0.15
        ).next_to(bigrect, UL, buff=0).shift(a.get_value()*DR))
        b_rect = always_redraw(lambda: Square(
            total-a.get_value(),
            color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=0.15
        ).next_to(bigrect, DR, buff=0).shift((total-a.get_value()) * UL))
        rects = always_redraw(lambda: VGroup(
            Rectangle(
                width=a.get_value(),
                height=total-a.get_value(),
                stroke_width=0.01
            ).next_to(a_rect, DOWN, buff=0),
            Rectangle(
                width=total-a.get_value(),
                height=a.get_value(),
                stroke_width=0.01
            ).next_to(a_rect, RIGHT, buff=0)
        ))

        side_labels = always_redraw(lambda:
            VGroup(*[
                MathTex(l, color=rect.get_color()).next_to(rect, d) for l, rect, d in zip(
                    ["a", "a", "b", "b"],
                    [a_rect, a_rect, b_rect, b_rect],
                    [UP, LEFT, DOWN, RIGHT]
                )
            ])
        )

        areas = always_redraw(lambda:
            VGroup(*[
                MathTex(
                    l, color=r.get_color(), font_size=np.sqrt(r.width*r.height) * 10
                ).move_to(between_mobjects(r, r)) for l, r in zip(
                    ["a^2", "b^2", r"a \cdot b", r"b \cdot a"],
                    [a_rect, b_rect, *rects]
                )
           ])
        )

        # self.add(a_rect, b_rect, side_labels, areas)
        self.play(
            DrawBorderThenFill(a_rect),
            DrawBorderThenFill(b_rect),
            DrawBorderThenFill(rects),
            run_time=2
        )
        self.slide_pause()
        self.play(
            Write(side_labels),
            Write(areas),
            run_time=0.5
        )
        self.slide_pause()
        # for i in [5, 1, 2, 4.5]:
        #     self.play(
        #         a.animate.set_value(i),
        #         run_time=4
        #     )

        separator = Rectangle(
            width=16, height=9, fill_color=BLACK, fill_opacity=0.85, stroke_width=0.01, z_index=2
        )
        self.play(
            LaggedStart(
                # FadeIn(separator, run_time=2),
                Circumscribe(bigrect, buff=0.02, color=RED, time_width=1, run_time=2, z_index=3),
                lag_ratio=1
            )
        )
