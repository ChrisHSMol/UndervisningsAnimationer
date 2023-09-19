from manim import *
import sys
sys.path.append("../")
from helpers import *
import subprocess

slides = False
if slides:
    from manim_slides import Slide


class Transformation(MovingCameraScene, Slide if slides else Scene):
    name = "Transformation"

    def construct(self):
        # self.slide_pause()
        # self.linear_transformation()
        # self.square_transformation()
        self.sine_transformation()
        self.slide_pause(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def prepare_board(self, n_segments=3):
        colors = [
            interpolate_color(YELLOW_A, GREEN_E, i/(n_segments - 2)) for i in range(n_segments - 1)
        ]
        background_rects = VGroup(*[
            Rectangle(
                height=self.camera.frame.get_height()/n_segments,
                width=self.camera.frame.get_width(),
                stroke_width=0.001,
                fill_color=color,
                fill_opacity=0.25
            ).set_z_index(0) for color in colors
        ]).arrange(DOWN, buff=0).to_edge(DL, buff=0)
        return colors, background_rects

    def trace_transformations(self, ndots, xline, yline, func, **kwargs):
        xmin, xmax = xline.get_tick_range()[0], xline.get_tick_range()[-1]
        indots = VGroup(*[
            Dot(
                xline.n2p(i),
                color=interpolate_color(BLUE, RED, (i - xmin)/(xmax - xmin)) if i != 0 else PINK
            ).set_z_index(2) for i in np.linspace(xmin, xmax, ndots)
        ])
        outdots = VGroup(*[
            Dot(
                yline.n2p(func(i, **kwargs)),
                color=interpolate_color(BLUE, RED, (i - xmin)/(xmax - xmin)) if i != 0 else PINK
            ).set_z_index(2) for i in np.linspace(xmin, xmax, ndots)
        ])
        # indots = self.get_dots(xline, ndots, xmin, xmax)
        # outline = self.get_dots(yline, ndots, func(xmin, xmax)
        traces = VGroup(*[
            TracedPath(
                indot.get_center, stroke_color=indot.get_color(), dissipating_time=None, stroke_opacity=[1, 0.5]
            ).set_z_index(2) for indot in indots
        ])
        self.add(traces)
        # self.add(indots, outdots)
        self.play(
            FadeIn(indots, lag_ratio=0.1)
        )
        self.slide_pause()

        self.play(
            *[
                ReplacementTransform(indot, outdot) for indot, outdot in zip(indots, outdots)
            ],
            run_time=3
        )
        self.slide_pause()
        self.play(
            FadeOut(outdots, lag_ratio=0.05),
            FadeOut(traces, lag_ratio=0.05),
            run_time=0.5
        )

    def linear_transformation(self):
        def func(x, a=2, b=0):
            return a * x + b

        colors, background_rects = self.prepare_board()
        xmin, xmax = 0, 10
        inline = NumberLine(
            x_range=[xmin, xmax, 1],
            length=0.45 * self.camera.frame.get_width(),
            color=colors[0],
            include_numbers=True,
            include_tip=False,
        ).set_z_index(1).next_to(background_rects[0], RIGHT).shift(self.camera.frame.get_width() * LEFT)
        outline = NumberLine(
            x_range=[func(xmin), func(xmax), 1],
            length=0.90 * self.camera.frame.get_width(),
            color=colors[1],
            include_numbers=True,
            include_tip=False
        ).set_z_index(1).next_to(background_rects[1], RIGHT).shift(self.camera.frame.get_width() * LEFT)
        self.add(inline, outline, background_rects)

        for ndots in [11, 21, 101]:
            self.trace_transformations(ndots, inline, outline, func=func)
        self.slide_pause()

        new_colors, new_background_rects = self.prepare_board(n_segments=4)
        xmin, xmax = -5, 5
        new_inline = NumberLine(
            x_range=[xmin, xmax, 1],
            length=0.40 * self.camera.frame.get_width(),
            color=new_colors[0],
            include_numbers=True,
            include_tip=False,
        ).set_z_index(1).move_to(new_background_rects[0])
        new_intermediate_line = NumberLine(
            x_range=[func(xmin), func(xmax), 1],
            length=0.80 * self.camera.frame.get_width(),
            color=new_colors[1],
            include_numbers=True,
            include_tip=False,
        ).set_z_index(1).move_to(new_background_rects[1])
        new_outline = NumberLine(
            x_range=[func(xmin), func(xmax, b=2), 1],
            length=0.88 * self.camera.frame.get_width(),
            color=new_colors[2],
            include_numbers=True,
            include_tip=False
        ).set_z_index(1).move_to(new_background_rects[2])
        new_outline.shift(
            0.5 * len(new_outline.get_tick_range()) / len(new_intermediate_line.get_tick_range()) * RIGHT
        )
        self.play(
            inline.animate.become(new_inline),
            outline.animate.become(new_outline),
            FadeIn(new_intermediate_line),
            FadeIn(new_background_rects),
            FadeOut(background_rects)
        )

        for ndots in [11, 21, 101]:
            indots = VGroup(*[
                Dot(
                    new_inline.n2p(i),
                    color=interpolate_color(BLUE, RED, (i - xmin)/(xmax - xmin)) if i != 0 else PINK
                ).set_z_index(2) for i in np.linspace(xmin, xmax, ndots)
            ])
            meddots = VGroup(*[
                Dot(
                    new_intermediate_line.n2p(func(i)),
                    color=interpolate_color(BLUE, RED, (i - xmin)/(xmax - xmin)) if i != 0 else PINK
                ).set_z_index(2) for i in np.linspace(xmin, xmax, ndots)
            ])
            outdots = VGroup(*[
                Dot(
                    new_outline.n2p(func(i, b=2)),
                    color=interpolate_color(BLUE, RED, (i - xmin)/(xmax - xmin)) if i != 0 else PINK
                ).set_z_index(2) for i in np.linspace(xmin, xmax, ndots)
            ])
            traces = VGroup(*[
                TracedPath(
                    indot.get_center, stroke_color=indot.get_color(), dissipating_time=None, stroke_opacity=[1, 0.5]
                ).set_z_index(2) for indot in indots
            ])
            self.add(traces)
            self.play(
                FadeIn(indots, lag_ratio=0.1)
            )
            self.slide_pause()
            self.play(
                *[
                    # ReplacementTransform(indot, meddot) for indot, meddot in zip(indots, meddots)
                    indot.animate.move_to(meddot) for indot, meddot in zip(indots, meddots)
                ],
                run_time=3
            )
            self.slide_pause()
            self.play(
                *[
                    # ReplacementTransform(meddot, outdot) for meddot, outdot in zip(meddots, outdots)
                    indot.animate.move_to(outdot) for indot, outdot in zip(indots, outdots)
                ],
                run_time=3
            )
            self.slide_pause()
            self.play(
                FadeOut(indots, lag_ratio=0.05),
                FadeOut(traces, lag_ratio=0.05),
                run_time=0.5
            )

    def square_transformation(self):
        def func(x, a=1):
            return a * x**2

        colors, background_rects = self.prepare_board()
        xmin, xmax = -5, 5
        # inlength = 0.9/(xmax - xmin) * self.camera.frame.get_width()
        inlength = 0.9/3 * self.camera.frame.get_width()
        outlength = 0.9 * self.camera.frame.get_width()
        inline = NumberLine(
            x_range=[xmin, xmax, 1],
            length=inlength,
            color=colors[0],
            include_numbers=True,
            include_tip=False,
        ).set_z_index(1).next_to(background_rects[0], RIGHT).shift(self.camera.frame.get_width() * LEFT)
        outline = NumberLine(
            x_range=[-5, func(xmax), 1],
            length=outlength,
            color=colors[1],
            include_numbers=True,
            include_tip=False
        ).set_z_index(1).next_to(background_rects[1], RIGHT).shift(self.camera.frame.get_width() * LEFT)
        self.add(inline, outline, background_rects)

        for ndots in [11, 21, 101]:
            # self.trace_transformations(ndots, inline, outline, func=func)
            indots = VGroup(*[
                Dot(
                    inline.n2p(i),
                    color=interpolate_color(BLUE, RED, (i - xmin)/(xmax - xmin)) if i != 0 else PINK
                ).set_z_index(2) for i in np.linspace(xmin, xmax, ndots)
            ])
            outdots = VGroup(*[
                Dot(
                    outline.n2p(func(i)),
                    color=interpolate_color(BLUE, RED, (i - xmin)/(xmax - xmin)) if i != 0 else PINK
                ).set_z_index(2) for i in np.linspace(xmin, xmax, ndots)
            ])
            traces = VGroup(*[
                TracedPath(
                    indot.get_center, stroke_color=indot.get_color(), dissipating_time=None, stroke_opacity=[1, 0.5]
                ).set_z_index(2) for indot in indots
            ])
            self.add(traces)
            self.play(
                FadeIn(indots, lag_ratio=0.05)
            )
            self.slide_pause()
            self.play(
                *[
                    indot.animate.move_to(outdot) for indot, outdot in zip(indots, outdots)
                ],
                run_time=3
            )
            self.slide_pause()
            self.play(
                FadeOut(indots, lag_ratio=0.05),
                FadeOut(traces, lag_ratio=0.05),
                run_time=0.5
            )
        self.slide_pause()

    def sine_transformation(self):
        def func(x):
            return np.sin(x*DEGREES)

        colors, background_rects = self.prepare_board()
        xmin, xmax = -720, 720
        inlength = 0.9/1 * self.camera.frame.get_width()
        outlength = 0.9/2 * self.camera.frame.get_width()
        inline = NumberLine(
            x_range=[xmin, xmax, 180],
            length=inlength,
            color=colors[0],
            include_numbers=True,
            include_tip=False,
        ).set_z_index(1).move_to(background_rects[0])
        outline = NumberLine(
            x_range=[-1, 1, 0.2],
            length=outlength,
            color=colors[1],
            include_numbers=True,
            include_tip=False
        ).set_z_index(1).move_to(background_rects[1])
        self.add(inline, outline, background_rects)

        for ndots in [9, 17, 33, 161, 321, 0]:
            if ndots == 0:
                indots = VGroup(*[
                    Dot(
                        inline.n2p(i),
                        color=interpolate_color(BLUE, RED, i/360) if i != 0 else PINK
                    ).set_z_index(2) for i in np.linspace(0, 360, 321)
                ])
                outdots = VGroup(*[
                    Dot(
                        outline.n2p(func(i)),
                        color=interpolate_color(BLUE, RED, i/360) if i != 0 else PINK
                    ).set_z_index(2) for i in np.linspace(0, 360, 321)
                ])
            else:
                indots = VGroup(*[
                    Dot(
                        inline.n2p(i),
                        color=interpolate_color(BLUE, RED, (i - xmin)/(xmax - xmin)) if i != 0 else PINK
                    ).set_z_index(2) for i in np.linspace(xmin, xmax, ndots)
                ])
                outdots = VGroup(*[
                    Dot(
                        outline.n2p(func(i)),
                        color=interpolate_color(BLUE, RED, (i - xmin)/(xmax - xmin)) if i != 0 else PINK
                    ).set_z_index(2) for i in np.linspace(xmin, xmax, ndots)
                ])
            traces = VGroup(*[
                TracedPath(
                    indot.get_center, stroke_color=indot.get_color(), dissipating_time=None, stroke_opacity=[1, 0.5]
                ).set_z_index(2) for indot in indots
            ])
            self.add(traces)
            self.play(
                FadeIn(indots, lag_ratio=0.05)
            )
            self.slide_pause()
            self.play(
                *[
                    indot.animate.move_to(outdot) for indot, outdot in zip(indots, outdots)
                ],
                run_time=3
            )
            self.slide_pause()
            self.play(
                FadeOut(indots, lag_ratio=0.05),
                FadeOut(traces, lag_ratio=0.05),
                run_time=0.5
            )
        self.slide_pause()


if __name__ == "__main__":
    class_name = Transformation.name
    scene_marker(rf"RUNNNING:    manim {sys.argv[0]} {class_name} -pqh")
    subprocess.run(rf"manim {sys.argv[0]} {class_name} -pqh")
    # if slides:
    #     scene_marker(rf"RUNNING:    manim-slides convert {class_name} {class_name}.html")
    #     # subprocess.run(rf"manim-slides convert {class_name} {class_name}.html")
    #     subprocess.run(rf"manim-slides {class_name}")
