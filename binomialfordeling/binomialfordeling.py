import math

from manim import *
import sys
sys.path.append("../")
import numpy as np
import subprocess
from helpers import *

slides = False
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


class BasisSandsynlighed(MovingCameraScene, Slide if slides else Scene):
    def construct(self):
        self.stokastisk_variabel()
        self.slide_pause(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def stokastisk_variabel(self):
        np.random.seed(42)
        cmap = {
            "A": BLUE,
            "B": RED,
            "C": YELLOW
        }
        pA = ValueTracker(0.2)
        pB = ValueTracker(0.5)
        # pC = always_redraw(lambda: DecimalNumber(1 - (pA.get_value() + pB.get_value())).move_to(12*RIGHT))
        # self.add(pC)

        radius = 1
        circle_diagram = Circle(
            radius=radius, stroke_width=0.1, stroke_color=WHITE
        )
        slices = always_redraw(lambda:
            VGroup(
                Sector(
                    radius=2*radius, start_angle=PI/2, arc_center=circle_diagram.get_center(),
                    angle=pA.get_value() * TAU, fill_color=cmap["A"], fill_opacity=0.75, stroke_color=cmap["A"],
                    stroke_width=0.75
                ),
                Sector(
                    radius=radius, start_angle=PI/2 + pA.get_value() * TAU, arc_center=circle_diagram.get_center(),
                    angle=pB.get_value() * TAU, fill_color=cmap["B"], fill_opacity=0.75, stroke_color=cmap["B"],
                    stroke_width=0.75
                ),
                Sector(
                    radius=radius, start_angle=PI/2 + (pA.get_value() + pB.get_value()) * TAU,
                    arc_center=circle_diagram.get_center(), angle=(1 - (pA.get_value() + pB.get_value())) * TAU,
                    fill_color=cmap["C"], fill_opacity=0.75, stroke_color=cmap["C"], stroke_width=0.75
                )
            )
        )
        slice_labels = always_redraw(lambda:
            VGroup(
                DecimalNumber((pA.get_value()*100), num_decimal_places=2, unit=r"\%", color=cmap["A"]).move_to(
                    circle_diagram.point_at_angle(PI/2 + 0.5*pA.get_value() * TAU)
                ).scale(0.33).set_z_index(slices[0].get_z_index() + 3),
                DecimalNumber((pB.get_value()*100), num_decimal_places=2, unit=r"\%", color=cmap["B"]).move_to(
                    circle_diagram.point_at_angle(PI/2 + (pA.get_value() + 0.5*pB.get_value()) * TAU)
                ).scale(0.33).set_z_index(slices[1].get_z_index() + 3),
                DecimalNumber((1-pA.get_value()-pB.get_value())*100, num_decimal_places=2, unit=r"\%", color=cmap["C"]).move_to(
                    circle_diagram.point_at_angle(PI/2 - 0.5*(1-(pA.get_value()+pB.get_value())) * TAU)
                ).scale(0.33).set_z_index(slices[2].get_z_index() + 3)
            )
        )
        slice_label_boxes = always_redraw(lambda:
            VGroup(*[
                get_background_rect(
                    lab, fill_opacity=0.8, fill_color=BLACK, stroke_width=0, buff=0.01
                ).move_to(lab) for lab in slice_labels
            ])
        )
        self.camera.frame.save_state()
        self.camera.frame.set(height=2.25*radius)
        # self.add(circle_diagram)
        self.play(
            LaggedStart(
                DrawBorderThenFill(circle_diagram),
                *[
                    DrawBorderThenFill(sl) for sl in slices
                ],
                *[
                    FadeIn(t) for t in slice_labels
                ],
                lag_ratio=0.1
            )
        )
        self.play(
            FadeIn(slice_label_boxes),
            run_time=0.1
        )
        self.remove(slices, slice_labels, slice_label_boxes)
        self.add(slices, slice_labels, slice_label_boxes)
        self.play(
            pA.animate.set_value(0.3)
        )
        # self.play(
        #     pB.animate.set_value(0.35)
        # )
        self.slide_pause()

        self.play(
            self.camera.frame.animate.set(
                height=3.5*radius
            ).shift(1.75*radius*RIGHT)
        )
        self.slide_pause()

        plane = Axes(
            x_range=(0, 4.1, 1),
            y_range=(0, 1.1, 0.1),
            x_length=6*radius,
            y_length=4*radius,
            x_axis_config={"include_numbers": False},
            y_axis_config={"include_numbers": True, "font_size": 30}
            # axis_config={"include_numbers": True}
        ).scale(0.5).next_to(circle_diagram, RIGHT)
        axhlines = VGroup(*[
            DashedLine(
                start=plane.c2p(0, y), end=plane.c2p(4.1, y), stroke_width=0.5
            ) for y in plane[1].get_tick_range()
        ])
        vline = Line(start=plane.c2p(3, 0), end=plane.c2p(3, 1.1))
        self.play(
            *[FadeIn(m) for m in [plane, axhlines]]
        )
        # self.add(plane, axhlines, vline)
        self.slide_pause()

        bars = always_redraw(lambda:
            VGroup(*[
                Rectangle(
                    width=0.25, fill_color=cmap[lp], fill_opacity=0.75, stroke_color=cmap[lp],
                    height=(plane.c2p(0, p)[1] - plane.c2p(0, 0)[1]),
                    stroke_width=0.75
                ).set_z_index(0).move_to(plane.c2p(x-0.5, 0.5*p)) for p, lp, x in zip(
                    (pA.get_value(), pB.get_value(), 1-(pA.get_value()+pB.get_value())),
                    ("A", "B", "C"),
                    plane[0].get_tick_range()
                )
            ])
        )
        bar_labels = always_redraw(lambda:
            VGroup(*[
                slice_label.copy().next_to(bar, 0.5*UP) for slice_label, bar in zip(slice_labels, bars)
            ])
        )
        bar_label_boxes = always_redraw(lambda:
            VGroup(*[
                get_background_rect(
                    lab, fill_opacity=0.8, fill_color=BLACK, stroke_width=0, buff=0.01
                ) for lab in bar_labels
            ])
        )
        stacked_bar = always_redraw(lambda:
            VGroup(*[
                bar.copy() for bar in bars
            ]).arrange(UP, buff=0).move_to(plane.c2p(3.5, 0.5))
        )
        self.play(
            LaggedStart(
                *[
                    FadeIn(bar, shift=0.1*UP) for bar in bars
                ],
                *[
                    FadeIn(lab, shift=0.1*UP) for lab in bar_labels
                ],
                lag_ratio=0.1
            )
        )
        self.play(
            FadeIn(bar_label_boxes),
            run_time=0.1
        )
        self.remove(bars, bar_labels, bar_label_boxes)
        self.add(bars, bar_labels, bar_label_boxes)
        self.slide_pause()

        self.play(
            LaggedStart(
                Create(vline),
                *[
                    ReplacementTransform(bar.copy(), sbar) for bar, sbar in zip(bars, stacked_bar)
                ],
                lag_ratio=0.25
            )
        )
        self.remove(vline, stacked_bar)
        self.add(vline, stacked_bar)
        # self.add(bars, bar_labels, bar_label_boxes, stacked_bar)
        self.slide_pause()

        self.play(
            pA.animate.set_value(0.9),
            pB.animate.set_value(0.05)
        )
        self.slide_pause()

        for i in range(3):
            self.play(
                pA.animate.set_value(np.random.random() * 0.66),
                pB.animate.set_value(np.random.random() * 0.33)
            )
            self.slide_pause()
        self.play(
            pA.animate.set_value(0.2),
            pB.animate.set_value(0.5)
        )
        self.slide_pause()

        self.play(
            self.camera.frame.animate.set(
                height=4*radius
            ).shift(0.75*radius*DOWN)
        )
        self.slide_pause()

        tekst = always_redraw(lambda:
            VGroup(
                *[
                    VGroup(
                        MathTex("P(X=", l, ") = ").set_color_by_tex_to_color_map(cmap),
                        DecimalNumber(p, num_decimal_places=4, color=cmap[l]),
                        MathTex(" = "),
                        DecimalNumber(p*100, num_decimal_places=2, unit=r"\%", color=cmap[l])
                    ).arrange(RIGHT) for p, l in zip(
                        (pA.get_value(), pB.get_value(), 1-(pA.get_value()+pB.get_value())),
                        ("A", "B", "C")
                    )
                ]
            ).scale(0.33).arrange(DOWN, aligned_edge=LEFT).next_to(VGroup(circle_diagram, plane), 0.5*DOWN, aligned_edge=LEFT)
        )
        # self.add(tekst)
        self.play(
            Write(tekst, lag_ratio=0.2),
            run_time=2
        )
        self.slide_pause()
        for i in range(3):
            self.play(
                pA.animate.set_value(np.random.random() * 0.66),
                pB.animate.set_value(np.random.random() * 0.33)
            )
            self.slide_pause()
        self.play(
            pA.animate.set_value(0.2),
            pB.animate.set_value(0.5)
        )
        self.slide_pause()

        complementA = always_redraw(lambda:
            VGroup(
                MathTex("P(X=", r"\overline{A}", ") = 1 - ", "P(X=", "A", ")").set_color_by_tex_to_color_map(cmap),
                MathTex("P(X=", r"\overline{A}", ") = ", "P(X=", "B", ") + P(X=", "C", ")").set_color_by_tex_to_color_map(cmap),
            ).scale(0.33).arrange(DOWN, aligned_edge=LEFT).next_to(tekst, RIGHT)
        )
        # self.add(complementA)
        self.play(
            Write(complementA)
        )


class DeskriptorerBinomial(BasisSandsynlighed):
    def construct(self):
        self.forventning()
        self.slide_pause(5)

    def forventning(self):
        np.random.seed(42)
        n_kast = 50
        alle_kast = np.random.randint(low=1, high=7, size=n_kast)
        kast = ValueTracker(0)
        n_seks = sum([1 if i==6 else 0 for i in alle_kast])
        running_avg = [np.mean(alle_kast[:i+1]) for i in range(len(alle_kast))]
        print(alle_kast)
        print(n_seks)
        print(running_avg)

        plane = Axes(
            x_range=(0, n_kast+1, 5),
            y_range=(0, 6.01, 0.5),
            x_length=12,
            y_length=6,
            x_axis_config={"include_numbers": True},
            y_axis_config={"include_numbers": True, "font_size": 30}
        )
        points = always_redraw(lambda:
            VGroup(
                *[
                    Dot(
                        plane.c2p(i+1, val), fill_opacity=0 if i+1 >= kast.get_value() else 1
                    ) for i, val in enumerate(running_avg)
                ]
            )
        )
        axhlines = VGroup(*[
            DashedLine(
                start=plane.c2p(0, y), end=plane.c2p(51, y), stroke_width=0.5
            ) for y in plane[1].get_tick_range()
        ])

        self.add(plane, axhlines)
        self.add(points)
        self.play(kast.animate.set_value(n_kast), run_time=5)


class BinomialFordeling(DeskriptorerBinomial):
    def construct(self):
        self.basis_for_graphing()
        self.slide_pause(5)

    def binom_point_prob(self, n, p, r):
        return math.factorial(n)/(math.factorial(n-r)*math.factorial(r)) * p**r * (1-p)**(n-r)

    def get_cmap(self):
        return {"n": YELLOW, "p": BLUE, "prob": GREEN, r"\mu": RED, r"\sigma": RED}

    def basis_for_graphing(self):
        cmap = self.get_cmap()
        xmin, xmax, xstep = -0.5, 51, 5
        ymin, ymax, ystep = 0, 0.26, 0.05
        plane = Axes(
            x_range=(xmin, xmax, xstep),
            y_range=(ymin, ymax, ystep),
            x_length=12,
            y_length=5,
            x_axis_config={"include_numbers": True},
            y_axis_config={"include_numbers": True}
        ).set_z_index(1).to_edge(DL)
        axhlines = VGroup(*[
            DashedLine(
                start=plane.c2p(0, y), end=plane.c2p(xmax, y), stroke_width=0.5
            ) for y in plane[1].get_tick_range()
        ]).set_z_index(plane.get_z_index()+1)
        self.add(plane, axhlines)

        n, p = 50, 0.5
        n, p = ValueTracker(n), ValueTracker(p)
        param_labels = always_redraw(lambda:
            VGroup(
                VGroup(
                    MathTex("{{n}} =").set_color_by_tex_to_color_map(cmap),
                    Integer(int(n.get_value()), color=cmap["n"])
                ).arrange(RIGHT),
                VGroup(
                    MathTex("{{p}} = ").set_color_by_tex_to_color_map(cmap),
                    DecimalNumber(p.get_value(), num_decimal_places=3, color=cmap["p"])
                ).arrange(RIGHT)
            ).arrange(DOWN, aligned_edge=LEFT).to_edge(UL).shift(RIGHT * 2)
        )
        self.add(param_labels)
        bars = always_redraw(lambda: VGroup(
            *[
                Rectangle(
                    width=0.75*(plane.c2p(1, 0)[0] - plane.c2p(0, 0)[0]),
                    height=plane.c2p(x, self.binom_point_prob(int(n.get_value()), p.get_value(), r=x))[1] - plane.c2p(x, 0)[1],
                    stroke_width=1, stroke_color=cmap["prob"], fill_color=cmap["prob"], fill_opacity=0.75
                ).set_z_index(plane.get_z_index()+2).move_to(
                    plane.c2p(x, 0.5*self.binom_point_prob(int(n.get_value()), p.get_value(), r=x))
                ) for x in range(int(n.get_value()) + 1)
            ]
        ))
        bar_labels = always_redraw(lambda: VGroup(
            *[
                DecimalNumber(
                    self.binom_point_prob(int(n.get_value()), p.get_value(), r=x), color=cmap["prob"],
                    num_decimal_places=3
                ).set(
                    width=bar.width if self.binom_point_prob(int(n.get_value()), p.get_value(), r=x) >= 0.001 else 0
                # ).scale(
                #     0.35 if self.binom_point_prob(int(n.get_value()), p.get_value(), r=x) >= 0.001 else 0
                ).next_to(bar, UP, buff=0.1).set_z_index(bar.get_z_index()) for x, bar in zip(range(int(n.get_value()) + 1), bars)
            ]
        ))
        self.add(bars, bar_labels)

        mu_line = always_redraw(lambda:
            Line(
                start=plane.c2p(n.get_value() * p.get_value(), ymin-0.025),
                end=plane.c2p(n.get_value() * p.get_value(), 0.225+0.025),
                stroke_color=cmap[r"\mu"],
                stroke_width=2
            ).set_z_indec(plane.get_z_index() + 4)
        )
        mu_label = always_redraw(lambda:
            # VGroup(
            #     MathTex(r"\mu = ", color=mu_line.get_color()),
            #     DecimalNumber(n.get_value() * p.get_value(), num_decimal_places=2, color=mu_line.get_color())
            # ).arrange(RIGHT).scale(0.5).next_to(mu_line, UP, buff=0.1).set_z_index(mu_line.get_z_index())
                MathTex(r"\mu").scale(0.5).next_to(mu_line, UP, buff=0.1).set_z_index(mu_line.get_z_index())
        )
        self.add(mu_label, mu_line)

        sigma_lines = always_redraw(lambda:
            VGroup(*[
                DashedLine(
                    start=plane.c2p(n.get_value() * p.get_value(), 0.23),
                    end=plane.c2p(
                        n.get_value()*p.get_value() + s*np.sqrt(n.get_value()*p.get_value()*(1-p.get_value())),
                        0.23
                    ),
                    stroke_color=cmap[r"\sigma"]
                ).set_z_index(mu_line.get_z_index()) for s in (1, -1)
            ])
        )
        sigma_labels = always_redraw(lambda:
            VGroup(
                # *[VGroup(
                #     MathTex(r"\sigma = ", color=RED),
                #     DecimalNumber(np.sqrt(n.get_value()*p.get_value()*(1-p.get_value())), num_decimal_places=2, color=RED)
                # ).arrange(RIGHT).scale(0.5).next_to(l, UP, buff=0.1) for l in sigma_lines]
                *[MathTex(r"\sigma").scale(0.5).next_to(l, UP, buff=0.1) for l in sigma_lines]
            )
        )
        self.add(sigma_labels, sigma_lines)

        sigma_lines2 = always_redraw(lambda:
            VGroup(*[
                DashedLine(
                    start=plane.c2p(n.get_value() * p.get_value(), 0.21),
                    end=plane.c2p(
                        n.get_value()*p.get_value() + s*np.sqrt(n.get_value()*p.get_value()*(1-p.get_value())),
                        0.21
                    ),
                    stroke_color=cmap[r"\sigma"]
                ).set_z_index(mu_line.get_z_index()) for s in (2, -2)
            ])
        )
        sigma_labels2 = always_redraw(lambda:
            VGroup(
                # *[VGroup(
                #     MathTex(r"2\sigma = ", color=RED),
                #     DecimalNumber(2*np.sqrt(n.get_value()*p.get_value()*(1-p.get_value())), num_decimal_places=2, color=RED)
                # ).arrange(RIGHT).scale(0.5).next_to(l, UP, buff=0.1) for l in sigma_lines2]
                *[MathTex(r"2\sigma").scale(0.5).next_to(l, UP, buff=0.1) for l in sigma_lines2]
            )
        )
        self.add(sigma_labels2, sigma_lines2)

        musig_vals = always_redraw(lambda:
            VGroup(
                VGroup(
                    MathTex(r"{{\mu}} = ").set_color_by_tex_to_color_map(cmap),
                    DecimalNumber(
                        n.get_value() * p.get_value(), num_decimal_places=2, color=cmap[r"\mu"]
                    )
                ).arrange(RIGHT),
                VGroup(
                    MathTex(r"{{\sigma}} = ").set_color_by_tex_to_color_map(cmap),
                    DecimalNumber(
                        np.sqrt(n.get_value() * p.get_value() * (1 - p.get_value())), num_decimal_places=2,
                        color=cmap[r"\sigma"]
                    )
                ).arrange(RIGHT),
                # VGroup(
                #     MathTex(r"2{{\sigma}} = ").set_color_by_tex_to_color_map(cmap),
                #     DecimalNumber(
                #         2 * np.sqrt(n.get_value() * p.get_value() * (1 - p.get_value())), num_decimal_places=2,
                #         color=cmap[r"\sigma"]
                #     )
                # ).arrange(RIGHT)
            ).arrange(DOWN, aligned_edge=LEFT).to_edge(UL).shift(7*RIGHT)
        )
        self.add(musig_vals)

        self.play(
            p.animate.set_value(0.125),
            run_time=10
        )
        self.slide_pause()
        self.play(
            # n.animate.set_value(50),
            p.animate.set_value(0.95),
            run_time=10
        )


if __name__ == "__main__":
    classes = [
        # BasisSandsynlighed,
        # DeskriptorerBinomial,
        BinomialFordeling
    ]
    for cls in classes:
        class_name = cls.__name__
        command = rf"manim {sys.argv[0]} {class_name} -p --resolution={_RESOLUTION[q]} --frame_rate={_FRAMERATE[q]}"
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



