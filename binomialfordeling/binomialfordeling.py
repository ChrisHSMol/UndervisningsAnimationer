import math

from manim import *
import sys
sys.path.append("../")
import numpy as np
import subprocess
from helpers import *

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
_ONEFRAME = 1/_FRAMERATE[q]


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

    def get_axhlines(self, plane):
        xmin, xmax = 0, plane[0].get_tick_range()[-1]
        return VGroup(*[
            DashedLine(
                start=plane.c2p(xmin, y), end=plane.c2p(xmax, y), stroke_width=0.5
            ) for y in plane[1].get_tick_range()
        ]).set_z_index(plane.get_z_index() + 1)

    def get_cmap(self):
        return {"n": YELLOW, "p": BLUE, "prob": GREEN, r"\mu": RED, r"\sigma": RED}

    def basis_for_graphing(self):
        cmap = self.get_cmap()
        xmin, xmax, xstep = 0, 50, 5
        ymin, ymax, ystep = 0, 0.25, 0.05
        plane = Axes(
            x_range=(xmin, xmax, xstep),
            y_range=(ymin, ymax, ystep),
            x_length=12,
            y_length=5,
            x_axis_config={"include_numbers": True},
            y_axis_config={"include_numbers": True},
            tips=False
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
                # DashedLine(
                Line(
                    start=plane.c2p(n.get_value() * p.get_value(), 0.23),
                    end=plane.c2p(
                        n.get_value()*p.get_value() + s*np.sqrt(n.get_value()*p.get_value()*(1-p.get_value())),
                        0.23
                    ),
                    stroke_color=cmap[r"\sigma"],
                    stroke_width=1
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
                # DashedLine(
                Line(
                    start=plane.c2p(n.get_value() * p.get_value(), 0.21),
                    end=plane.c2p(
                        n.get_value()*p.get_value() + s*np.sqrt(n.get_value()*p.get_value()*(1-p.get_value())),
                        0.21
                    ),
                    stroke_color=cmap[r"\sigma"],
                    stroke_width=1
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
            run_time=1/_FRAMERATE[q]
        )
        self.slide_pause()
        self.play(
            # n.animate.set_value(50),
            p.animate.set_value(0.95),
            run_time=1/_FRAMERATE[q]
        )


class BinomialTest(BinomialFordeling):
    def construct(self):
        # self.konfidensinterval()
        # self.overgang1()
        # self.to_sidet_test()
        # self.overgang2()
        self.enkel_sidet_test()
        self.slide_pause(5)

    def get_cmap(self):
        return {
            "tilfæl": BLUE, "signif": RED, "udvalg": YELLOW, "antal": PURPLE, "sands": TEAL,
            "toside": GREEN, "enside": MAROON, "enstre": MAROON_B, "øjre": MAROON_D
        }

    def cross_out_mobject(self, mobject):
        cross_lines = VGroup(
            *[
                Line(
                    start=st, end=en, stroke_color=RED, stroke_opacity=[0.125, 1, 0.125]
                ).scale(1.1) for st, en in zip(
                    (mobject.get_corner(UL), mobject.get_corner(UR)),
                    (mobject.get_corner(DR), mobject.get_corner(DL))
                )
            ]
        )
        self.play(
            LaggedStart(
                *[Create(l) for l in cross_lines],
                lag_ratio=0.25
            ),
            run_time=0.5
        )
        return cross_lines

    def konfidensinterval(self):
        n = 100
        p = 0.5
        r = 38
        cmap = self.get_cmap()
        intro_tekst = VGroup(
            Tex("En mønt mistænkes for at være uærlig."),
            Tex(f"Den flippes ", f"{n}", " gange og lander på plat ", f"{r}", " gange."),
            Tex("Er der grund til mistanke?")
        ).arrange(DOWN, aligned_edge=LEFT)
        intro_tekst[1][1].set_color(cmap["antal"])
        intro_tekst[1][3].set_color(cmap["udvalg"])
        # self.add(intro_tekst)
        self.play(
            Write(intro_tekst),
            run_time=5
        )
        self.slide_pause(5*_ONEFRAME)

        # self.remove(intro_tekst)

        parameter_tekst = VGroup(
            Tex("Antalsparameteren er ", f"$n={n}$"),
            Tex("Antal succeser er ", f"$r={r}$"),
            Tex("Sandsynlighedsparameteren er ", f"$p={p:.2f}$")
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(UL)
        parameter_tekst[0][1].set_color(cmap["antal"])
        parameter_tekst[1][1].set_color(cmap["udvalg"])
        parameter_tekst[2][1].set_color(cmap["sands"])
        # self.add(parameter_tekst)
        self.play(
            Write(parameter_tekst),
            Unwrite(intro_tekst, reverse=False, run_time=0.5)
        )
        self.slide_pause(5*_ONEFRAME)

        punktsandsynligheder = [self.binom_point_prob(n, p, x) for x in range(n+1)]
        kumulerede_sandsynligheder = [sum(punktsandsynligheder[:i]) for i in range(n+1)]
        mu, sigma = n*p, np.sqrt(n*p*(1-p))
        a, b = ValueTracker(-10), ValueTracker(10)
        r_picker = ValueTracker(0)

        xmin, xmax, xstep = 0, n, 5
        ymin, ymax, ystep = 0, np.ceil(max(punktsandsynligheder)*10)/10, 0.01
        plane = Axes(
            x_range=(xmin, xmax, xstep),
            y_range=(ymin, ymax, ystep),
            x_length=12,
            y_length=4,
            tips=False,
            axis_config={"include_numbers": True}
        ).to_edge(DOWN, buff=0.25)
        axhlines = self.get_axhlines(plane)
        # self.add(plane, axhlines)
        self.play(
            Create(plane, lag_ratio=0.2),
            Create(axhlines, lag_ratio=0.2)
        )
        self.slide_pause(5*_ONEFRAME)

        binom_bars = always_redraw(lambda: VGroup(
            *[
                Rectangle(
                    width=0.75*(plane.c2p(1, 0)[0] - plane.c2p(0, 0)[0]),
                    height=plane.c2p(0, prob)[1] - plane.c2p(0, 0)[1],
                    stroke_width=0.1,
                    # fill_color=cmap["tilfældig"] if mu + a.get_value()*sigma < i < mu + b.get_value()*sigma else (cmap["udvalg"] if i == r_picker.get_value() else cmap["signifikant"]),
                    fill_color=[
                        cmap["signif"], cmap["tilfæl"],
                        # interpolate_color(cmap["signif"], cmap["udvalg"], 0.5), cmap["udvalg"]
                        cmap["udvalg"], cmap["udvalg"]
                    ][
                        int(mu + a.get_value() * sigma < i < mu + b.get_value() * sigma) + 2*int(i == r_picker.get_value())
                    ],
                    fill_opacity=0.85
                ).set_z_index(plane.get_z_index()+2).move_to(
                    plane.c2p(i, 0.5*prob)
                ) for i, prob in enumerate(punktsandsynligheder)
            ]
        ))
        # self.add(binom_bars)
        self.play(
            LaggedStart(
                *[
                    GrowFromEdge(bar, DOWN) for bar in binom_bars
                ],
                lag_ratio=0.05
            )
        )
        self.remove(binom_bars)
        self.add(binom_bars)
        self.slide_pause(5*_ONEFRAME)

        # self.play(
        #     a.animate.set_value(-1),
        #     b.animate.set_value(1)
        # )
        # self.slide_pause()
        # self.play(
        #     a.animate.set_value(-10),
        #     b.animate.set_value(10)
        # )

        # self.play(
        #     r_picker.animate.set_value(r),
        #     run_time=_ONEFRAME
        # )
        # self.slide_pause(5*_ONEFRAME)

        self.play(
            parameter_tekst.animate.scale(0.75).to_edge(UL),
            run_time=0.5
        )
        # self.slide_pause(5*_ONEFRAME)

        afvigelser_tekst = VGroup(
            Tex("I et binomialeksperiment findes både"),
            Tex("{{tilfældige}} og {{signifikante}} afvigelser.").set_color_by_tex_to_color_map(cmap)
        ).scale(0.75).arrange(DOWN, aligned_edge=LEFT).to_edge(UR)
        # self.add(afvigelser_tekst)
        self.play(
            Write(afvigelser_tekst)
        )
        self.slide_pause(5*_ONEFRAME)

        signifikans_tekst = Tex(
            "Normalt sættes {{signifikans}}niveauet til ", "$95\%$"
        ).set_color_by_tex_to_color_map(cmap).next_to(plane, UP, buff=0.25)
        signifikans_tekst[-1].set_color(cmap["tilfæl"])
        # self.add(signifikans_tekst)
        self.play(
            ReplacementTransform(afvigelser_tekst.copy(), signifikans_tekst)
        )
        self.slide_pause(5*_ONEFRAME)

        procent_linjer = always_redraw(lambda:
            VGroup(
                Line(
                    start=plane.c2p(xmin, 0.085),
                    end=plane.c2p(mu + a.get_value()*sigma, 0.085),
                    stroke_color=cmap["signif"]
                ),
                Line(
                    start=plane.c2p(mu + a.get_value()*sigma, 0.085),
                    end=plane.c2p(mu + b.get_value()*sigma, 0.085),
                    stroke_color=cmap["tilfæl"]
                ),
                Line(
                    start=plane.c2p(mu + b.get_value()*sigma, 0.085),
                    end=plane.c2p(xmax, 0.085),
                    stroke_color=cmap["signif"]
                )
            )
        )
        # procent_labels = always_redraw(lambda:
        #     VGroup(*[
        #         DecimalNumber(
        #             line.get_length() / sum([l.get_length() for l in procent_linjer]),
        #             num_decimal_places=2,
        #             stroke_color=line.get_color(),
        #             unit=r"\%"
        #         ).scale(
        #             min(0.75, np.exp(line.get_length())-1)
        #         ).next_to(line, UP, buff=0.5) for line in procent_linjer
        #     ])
        # )
        idx0025, idx0975 = 0, 0
        idx017, idx083 = 0, 0
        for i, kum in enumerate(kumulerede_sandsynligheder):
            print(i, kum)
            if kum <= 0.025:
                idx0025 = i
            if kum >= 0.975:
                idx0975 = i
                break
        for i, kum in enumerate(kumulerede_sandsynligheder):
            if kum <= 0.17:
                idx017 = i
            if kum >= 0.83:
                idx083 = i
                break

        a_procent, b_procent = ValueTracker(0), ValueTracker(1)

        procent_labels = always_redraw(lambda:
            VGroup(
                DecimalNumber(
                    # kumulerede_sandsynligheder[idx0025]*100,
                    a_procent.get_value()*100,
                    num_decimal_places=2,
                    color=cmap["signif"],
                    unit=r"\%"
                ).scale(
                    min(0.75, np.exp(procent_linjer[0].get_length())-1)
                ).next_to(procent_linjer[0], UP, buff=0.25),
                DecimalNumber(
                    (b_procent.get_value() - a_procent.get_value())*100,
                    num_decimal_places=2,
                    color=cmap["tilfæl"],
                    unit=r"\%"
                ).scale(
                    min(0.75, np.exp(procent_linjer[1].get_length())-1)
                ).next_to(procent_linjer[1], UP, buff=0.25),
                DecimalNumber(
                    (1 - b_procent.get_value())*100,
                    num_decimal_places=2,
                    color=cmap["signif"],
                    unit=r"\%"
                ).scale(
                    min(0.75, np.exp(procent_linjer[2].get_length())-1)
                ).next_to(procent_linjer[2], UP, buff=0.25)
            )
        )
        # self.add(procent_linjer, procent_labels)
        self.play(
            Create(procent_linjer),
            Write(procent_labels)
        )
        self.slide_pause(5*_ONEFRAME)

        self.play(
            a.animate.set_value(-1),
            a_procent.animate.set_value(kumulerede_sandsynligheder[idx017]),
            b.animate.set_value(1),
            b_procent.animate.set_value(kumulerede_sandsynligheder[idx083]),
            run_time=10
        )
        self.slide_pause(5*_ONEFRAME)

        self.play(
            a.animate.set_value(-2),
            a_procent.animate.set_value(kumulerede_sandsynligheder[idx0025]),
            b.animate.set_value(2),
            b_procent.animate.set_value(kumulerede_sandsynligheder[idx0975]),
            run_time=4
        )
        self.slide_pause(5*_ONEFRAME)

        kritisk_tekst = VGroup(
            Tex("De ", "røde", " tal kaldes"),
            Tex("den ", "kritiske mængde")
        ).scale(0.75).arrange(DOWN, aligned_edge=LEFT).next_to(procent_linjer[-1], DOWN, aligned_edge=LEFT)
        kritisk_tekst[0][1].set_color(cmap["signif"])
        kritisk_tekst[1][1].set_color(cmap["signif"])
        # self.add(kritisk_tekst)
        self.play(
            Write(kritisk_tekst)
        )
        self.slide_pause(5*_ONEFRAME)

        self.play(
            r_picker.animate.set_value(r)
        )
        self.slide_pause(5*_ONEFRAME)

        konklusion_tekst = VGroup(
            Tex(f"$r={r}$", " er i den "),
            Tex("kritiske mængde", ","),
            Tex("og nulhypotesen "),
            Tex("kan derfor forkastes.")
        ).scale(0.75).arrange(DOWN, aligned_edge=RIGHT).next_to(procent_linjer[0], DOWN, aligned_edge=RIGHT)
        konklusion_tekst[0][0].set_color(cmap["udvalg"])
        konklusion_tekst[1][0].set_color(cmap["signif"])
        # konklusion_tekst[1][1].set_color(cmap["signif"])
        # self.add(konklusion_tekst)
        self.play(
            Write(konklusion_tekst)
        )
        self.slide_pause(5*_ONEFRAME)

    def overgang1(self):
        cmap = self.get_cmap()
        overgang_tekst = VGroup(
            Tex("Hvordan laver vi egentlig"),
            Tex("den udregning?")
        ).arrange(DOWN, aligned_edge=LEFT)
        if len(self.mobjects) == 0:
            self.add(Circle())
        self.play(
            FadeOut(*self.mobjects),
            FadeIn(overgang_tekst[0], shift=RIGHT),
            FadeIn(overgang_tekst[1], shift=LEFT)
        )
        self.slide_pause()

        to_sidet_tekst = VGroup(
            Tex("I en ", "tosidet", " test, deler vi"),
            Tex("ligeligt på hver side af fordelingen")
        ).arrange(DOWN, aligned_edge=LEFT)
        to_sidet_tekst[0][1].set_color(cmap["toside"])
        self.play(
            FadeOut(overgang_tekst[0], shift=RIGHT),
            FadeOut(overgang_tekst[1], shift=LEFT),
            FadeIn(to_sidet_tekst[0], shift=RIGHT),
            FadeIn(to_sidet_tekst[1], shift=LEFT)
        )
        self.slide_pause()

        self.play(
            FadeOut(to_sidet_tekst[0], shift=RIGHT),
            FadeOut(to_sidet_tekst[1], shift=LEFT)
        )

    def overgang2(self):
        cmap = self.get_cmap()
        overgang_tekst = VGroup(
            Tex("Hvad så med"),
            Tex("en ", "enkeltsidet", " test?")
        ).arrange(DOWN, aligned_edge=LEFT)
        overgang_tekst[1][1].set_color(cmap["enside"])
        if len(self.mobjects) == 0:
            self.add(Circle())
        self.play(
            FadeOut(*self.mobjects),
            FadeIn(overgang_tekst[0], shift=RIGHT),
            FadeIn(overgang_tekst[1], shift=LEFT)
        )
        self.slide_pause()

        enkelt_sidet_tekst = VGroup(
            Tex("I en ", "enkeltsidet", " test, "),
            Tex("ligger alle afvigelser på den ", "ene", " side")
        ).arrange(DOWN, aligned_edge=LEFT)
        enkelt_sidet_tekst[0][1].set_color(cmap["enside"])
        enkelt_sidet_tekst[1][1].set_color(cmap["enside"])
        self.play(
            FadeOut(overgang_tekst[0], shift=RIGHT),
            FadeOut(overgang_tekst[1], shift=LEFT),
            FadeIn(enkelt_sidet_tekst[0], shift=RIGHT),
            FadeIn(enkelt_sidet_tekst[1], shift=LEFT)
        )
        self.slide_pause()

        self.play(
            FadeOut(enkelt_sidet_tekst[0], shift=RIGHT),
            FadeOut(enkelt_sidet_tekst[1], shift=LEFT)
        )

    def to_sidet_test(self):
        n = 100
        p = 0.5
        r = 38
        cmap = self.get_cmap()

        overskrift = Tex("Tosidet", " test").scale(1.5).to_edge(UL, buff=0.5).shift(0.5*UP)
        overskrift[0].set_color(cmap["toside"])
        parametre = VGroup(
            MathTex("n", " = ", f"{n}", color=cmap["antal"]),
            MathTex("p", " = ", f"{p}", color=cmap["sands"]),
            MathTex("r", " = ", f"{r}", color=cmap["udvalg"])
        ).arrange(RIGHT, buff=1, aligned_edge=UP).to_edge(UR, buff=0.5).shift(0.5*UP)
        [line[1].set_color(WHITE) for line in parametre]
        underlines = VGroup(
            # *[
            #     Underline(
            #         mob, stroke_opacity=[0.25, 1, 0.25], stroke_color=mob[0].get_color()
            #     ) for mob in (overskrift, *parametre)
            # ]
            Underline(
                overskrift, stroke_color=cmap["toside"], stroke_opacity=[0.25, 1, 0.25]
            ).scale(1.5),
            Underline(
                parametre, stroke_opacity=[0.25, 1, 0.25], stroke_color=color_gradient(
                    (cmap["udvalg"], cmap["sands"], cmap["antal"]), 3
                )
            ).scale(1.125)
        )
        self.play(
            LaggedStart(
                FadeIn(overskrift),
                *[FadeIn(line) for line in parametre],
                *[Create(line) for line in underlines],
                lag_ratio=0.5
            ),
            run_time=1
        )
        self.slide_pause(5*_ONEFRAME)

        punktsandsynligheder = [self.binom_point_prob(n, p, x) for x in range(n+1)]
        kumulerede_sandsynligheder = [0 if i == 0 else sum(punktsandsynligheder[:i]) for i in range(n+1)]
        mu, sigma = n*p, np.sqrt(n*p*(1-p))

        ligning = MathTex(
            "P", "(", "X", "=", "r", ") =", "K(", "n", ";", "r", r")\cdot", "p", "^r", r"\cdot (1-", "p",
            ")^{", "n", "-", "r", "}"
        ).shift(2*UP)
        [ligning[i].set_color(cmap["udvalg"]) for i in (4, 9, 12, 18)]
        [ligning[i].set_color(cmap["sands"]) for i in (11, 14)]
        [ligning[i].set_color(cmap["antal"]) for i in (7, 16)]
        [ligning[i].set_color(cmap["tilfæl"]) for i in (0, 2)]
        # self.add(ligning)
        self.play(
            Write(ligning),
            run_time=2
        )
        self.slide_pause(5*_ONEFRAME)

        ligning_sum = VGroup(
            MathTex("P", "(", "X", r"\leq", "r", ") ="),
            *[MathTex("P", "(", "X", "=", f"{l}", ") + ") for l in range(3)],
            MathTex(r"\ldots +"),
            *[MathTex(
                "P", "(", "X", "=",
                f"r-{l}" if l > 0 else "r",
                ") + " if l > 0 else ")"
            ) for l in (1, 0)]
        ).scale(0.75).arrange(RIGHT, buff=0.1).next_to(ligning, DOWN)
        for i, l in enumerate(ligning_sum):
            if i == 4:
                continue
            l[0].set_color(cmap["tilfæl"])
            l[2].set_color(cmap["tilfæl"])
            l[4].set_color(cmap["udvalg"])
        # self.add(ligning_sum)
        self.play(
            Write(ligning_sum[0])
        )
        self.slide_pause(5*_ONEFRAME)
        for i, led in enumerate(ligning_sum[1:]):
            self.play(
                TransformMatchingShapes(
                    ligning[:5].copy(),
                    led,
                    fade_transform_mismatches=True
                )
            )
            self.slide_pause(5*_ONEFRAME)

        alle_udregninger = VGroup(
            *[
                MathTex(
                    "P", "(", "X", r"\leq", f"{l}", ") = ",
                    # r"\text{ }"*(2-len(str(l))),
                    f"{kumulerede_sandsynligheder[l]:.10f}"
                ) for l in range(n+1)
            ]
        ).arrange(ORIGIN, aligned_edge=LEFT)
        for l in alle_udregninger:
            [l[i].set_color(cmap["tilfæl"]) for i in (0, 2, -1)]
            l[4].set_color(cmap["udvalg"])
        # self.add(alle_udregninger[0])
        self.play(
            Write(alle_udregninger[0]),
            run_time=0.5
        )
        self.slide_pause(5*_ONEFRAME)
        for i, udr in enumerate(alle_udregninger[1:]):
            self.play(
                # *[
                #     FadeOut(
                #         alle_udregninger[i][j], shift=1*udr[j].get_height()*UP
                #     ) if j in (4, -1) else FadeOut(
                #         alle_udregninger[i][j], run_time=_ONEFRAME
                #     ) for j in range(len(udr))
                #     # FadeOut(alle_udregninger[i][j], shift=1*udr[j].height*UP) for j in (4, -1)
                # ],
                # *[
                #     FadeIn(
                #     udr[j], shift=1*udr[j].get_height()*UP
                #     ) if j in (4, -1) else FadeIn(
                #         udr[j], run_time=_ONEFRAME
                #     ) for j in range(len(udr))
                #     # FadeIn(udr[j], shift=1*udr[j].height*UP) for j in (4, -1)
                # ],
                FadeOut(alle_udregninger[i]),
                FadeIn(udr),
                run_time=1/6
            )
            # self.remove(alle_udregninger[i], udr)
            # self.add(udr)
        self.slide_pause()
        self.play(
            FadeOut(udr),
            run_time=0.5
        )

        forklaring_tekst = VGroup(
            Tex("Til en ", "tosidet", " test med ", "signifikans", "niveau på ", "$95\%$").set_color_by_tex_to_color_map(cmap),
            Tex("skal grænsen findes ved ", "$2.5\%$", " på hver side.")
        ).arrange(DOWN)
        forklaring_tekst[0][-1].set_color(cmap["tilfæl"])
        forklaring_tekst[1][1].set_color(cmap["signif"])
        # self.add(forklaring_tekst)
        self.play(
            FadeIn(forklaring_tekst[0], shift=2*LEFT),
            FadeIn(forklaring_tekst[1], shift=2*RIGHT)
        )
        self.slide_pause(5*_ONEFRAME)

        lowers = (39, 40)
        uppers = (59, 60)
        #
        # udregning_lower = VGroup(
        #     *[MathTex(
        #         "P", "(", "X", "=", f"{l}", ") = K(", f"{n}", ";", f"{l}", r")\cdot",
        #         f"{p}", f"^{{{l}}}", r"\cdot (1-", f"{p}", ")^{", f"{n}", "-", f"{l}", "} = ",
        #         f"{self.binom_point_prob(n, p, l):.4f}"
        #     ) for l in lowers]
        # ).arrange(DOWN, aligned_edge=LEFT).to_edge(DOWN)
        # for l in udregning_lower:
        #     [l[i].set_color(cmap["udvalg"]) for i in (4, 8, 11, 17)]
        #     [l[i].set_color(cmap["sands"]) for i in (10, 13)]
        #     [l[i].set_color(cmap["antal"]) for i in (6, 15)]
        #     [l[i].set_color(cmap["tilfæl"]) for i in (0, 2, -1)]
        # self.add(udregning_lower)
        sections = VGroup(
            *[
                Rectangle(
                    width=8, height=4, stroke_width=0.5, stroke_color=c, fill_color=c, fill_opacity=0.1
                ) for c in (MAROON_B, MAROON_D)
            ]
        ).arrange(RIGHT, buff=0.025).next_to(forklaring_tekst, DOWN)
        section_headers = VGroup(
            *[
                Tex(
                    l, " $2.5\%$", color=c
                ).next_to(sec, dire, aligned_edge=UP).shift(0.25*DOWN) for l, c, sec, dire in zip(
                    ("Nedre", "Øvre"), (sections[0].get_color(), sections[1].get_color()),
                    (sections[1], sections[0]), (LEFT, RIGHT)
                )
            ]
        )
        # self.add(sections, section_headers)
        self.play(
            FadeIn(sections),
            FadeIn(section_headers[0], shift=4*RIGHT),
            FadeIn(section_headers[1], shift=4*LEFT)
        )
        self.slide_pause(5*_ONEFRAME)

        udregning_lower = VGroup(
            *[MathTex(
                "P", "(", "X", r"\leq", f"{l}", ") = ", f"{kumulerede_sandsynligheder[l+1]:.4f}"
            ) for l in lowers]
        ).arrange(DOWN, aligned_edge=LEFT).move_to(sections[0])
        for l in udregning_lower:
            [l[i].set_color(cmap["tilfæl"]) for i in (0, 2, -1)]
            l[4].set_color(cmap["udvalg"])
        # self.add(udregning_lower)
        self.play(
            LaggedStart(
                *[
                    Write(eq) for eq in udregning_lower
                ],
                lag_ratio=0.9
            ),
            run_time=1
        )
        self.slide_pause(5*_ONEFRAME)

        cross_lines_lower = self.cross_out_mobject(udregning_lower[-1])
        self.slide_pause(5*_ONEFRAME)

        udregning_upper = VGroup(
            *[MathTex(
                "P", "(", "X", r"\leq", f"{l}", ") = ", f"{kumulerede_sandsynligheder[l+1]:.4f}"
            ) for l in uppers]
        ).arrange(DOWN, aligned_edge=LEFT).move_to(sections[1])
        for l in udregning_upper:
            [l[i].set_color(cmap["tilfæl"]) for i in (0, 2, -1)]
            l[4].set_color(cmap["udvalg"])
        # self.add(udregning_upper)
        self.play(
            LaggedStart(
                *[
                    Write(eq) for eq in udregning_upper
                ],
                lag_ratio=0.9
            ),
            run_time=1
        )
        self.slide_pause(5*_ONEFRAME)

        cross_lines_upper = self.cross_out_mobject(udregning_upper[0])
        self.slide_pause(5*_ONEFRAME)

        konklusion_tekst = VGroup(
            Tex("Grænsen til de ", "nederste $2.5\%$", " er ", f"{lowers[0]}", "."),
            Tex("Derfor er observationen ", f"$r={r}$", " mere afvigende,"),
            Tex("end hvad vi forventer fra ", "tilfældighed"),
            Tex("og vi kan derfor ", "forkaste", " hypotesen om, at mønten er ærlig.")
        ).arrange(DOWN, aligned_edge=LEFT).set_z_index(5)
        konklusion_tekst[0][1].set_color(section_headers[0].get_color())
        konklusion_tekst[0][3].set_color(cmap["udvalg"])
        konklusion_tekst[1][1].set_color(cmap["udvalg"])
        konklusion_tekst[2][1].set_color(cmap["tilfæl"])
        konklusion_tekst[3][1].set_color(cmap["signif"])
        brect = get_background_rect(konklusion_tekst, stroke_colour=cmap["signif"])
        self.play(
            LaggedStart(
                Write(konklusion_tekst),
                FadeIn(brect),
                lag_ratio=0.1
            ),
            run_time=2
        )
        self.slide_pause(5*_ONEFRAME)

        self.play(
            LaggedStart(
                *[
                    FadeOut(m) for m in self.mobjects if m not in (konklusion_tekst, brect)
                ],
                lag_ratio=0.02
            )
        )
        self.slide_pause(5*_ONEFRAME)

    def enkel_sidet_test(self):
        n = 50
        p = 0.5
        r = 19
        cmap = self.get_cmap()

        punktsandsynligheder = [self.binom_point_prob(n, p, x) for x in range(n+1)]
        kumulerede_sandsynligheder = [sum(punktsandsynligheder[:i+1]) for i in range(n+1)]
        print(len(punktsandsynligheder), len(kumulerede_sandsynligheder))
        mu, sigma = n*p, np.sqrt(n*p*(1-p))
        a, b = ValueTracker(0), ValueTracker(1)

        xmin, xmax, xstep = 0, n, 5
        ymin, ymax, ystep = 0, np.ceil(max(punktsandsynligheder)*10)/10, 0.02
        plane = Axes(
            x_range=(xmin, xmax, xstep),
            y_range=(ymin, ymax, ystep),
            x_length=12,
            y_length=4,
            tips=False,
            axis_config={"include_numbers": True}
        ).to_edge(DOWN, buff=0.25)
        axhlines = self.get_axhlines(plane)
        self.add(plane, axhlines)
        # self.play(
        #     Create(plane, lag_ratio=0.2),
        #     Create(axhlines, lag_ratio=0.2)
        # )
        self.slide_pause(5*_ONEFRAME)

        binom_bars = always_redraw(lambda: VGroup(
            *[
                Rectangle(
                    width=0.75*(plane.c2p(1, 0)[0] - plane.c2p(0, 0)[0]),
                    height=plane.c2p(0, prob)[1] - plane.c2p(0, 0)[1],
                    stroke_width=0.1,
                    # fill_color=cmap["tilfæl"] if a.get_value() < i <= b.get_value() else cmap["signif"],
                    fill_color=cmap["tilfæl"] if a.get_value() < kum_prob < b.get_value() else cmap["signif"],
                    fill_opacity=0.85
                ).set_z_index(plane.get_z_index()+2).move_to(
                    plane.c2p(i, 0.5*prob)
                ) for i, prob, kum_prob in zip(
                    range(len(punktsandsynligheder)), punktsandsynligheder, kumulerede_sandsynligheder
                )
            ]
        ))
        self.add(binom_bars)
        # self.play(
        #     LaggedStart(
        #         *[
        #             GrowFromEdge(bar, DOWN) for bar in binom_bars
        #         ],
        #         lag_ratio=0.05
        #     )
        # )
        self.remove(binom_bars)
        self.add(binom_bars)
        self.slide_pause(5*_ONEFRAME)

        self.play(
            a.animate.set_value(0.1),
            b.animate.set_value(0.9)
        )
        self.slide_pause(5*_ONEFRAME)

        self.play(
            a.animate.set_value(0),
            b.animate.set_value(0.8)
        )
        self.slide_pause(5*_ONEFRAME)

        self.play(
            a.animate.set_value(0.2),
            b.animate.set_value(1)
        )
        self.slide_pause(5*_ONEFRAME)


if __name__ == "__main__":
    classes = [
        BasisSandsynlighed,
        DeskriptorerBinomial,
        BinomialFordeling,
        BinomialTest
    ]
    for cls in classes:
        class_name = cls.__name__
        command = rf"manim {sys.argv[0]} {class_name} -p --resolution={_RESOLUTION[q]} --frame_rate={_FRAMERATE[q]}"
        scene_marker(rf"RUNNNING:    {command}")
        subprocess.run(command)
        if slides and q == "h":
            command = rf"manim-slides convert {class_name} {class_name}.html --one-file --offline"
            scene_marker(rf"RUNNNING:    {command}")
            subprocess.run(command)
            if class_name+"Thumbnail" in dir():
                command = rf"manim {sys.argv[0]} {class_name}Thumbnail -pq{q} -o {class_name}Thumbnail.png"
                scene_marker(rf"RUNNNING:    {command}")
                subprocess.run(command)

