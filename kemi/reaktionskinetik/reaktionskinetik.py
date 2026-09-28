# Maxwell-Boltzmann formel:
# PDF: P(x)=np.sqrt(2/np.pi) * x**2 / a**3 * np.exp(-x**2 / (2*a**2))
import math
import random
from turtledemo.clock import setup

from manim import *
import sys

from manim_chemistry import ChemicalFormula
from pyglet.resource import animation

sys.path.append("../../")
sys.path.append("../../../")
import numpy as np
import pandas as pd
import scipy
import subprocess
from helpers import *
from custom_classes import *
# from manim_chemistry import *

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


class HastighedsFordeling(MovingCameraScene, Slide if slides else Scene):
    def construct(self):
        self.camera.background_color = DARKER_GRAY
        title = Tex(r"Maxwell-Boltzmanns \\hastighedsfordeling").scale(2)
        self.add(title)
        self.slide_pause()
        self.play(
            FadeOut(title),
            run_time=0.25
        )
        self.maxwell_boltzmann()
        self.wait(5)

    def slide_pause(self, t=0.5, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def _cmap(self):
        cmap = {"tid": BLUE_C, "sted": GREEN, "hast": YELLOW, "acc": RED}
        return cmap

    def maxwell_boltzmann(self):
        # P(x) = np.sqrt(2 / np.pi) * x ** 2 / a ** 3 * np.exp(-x ** 2 / (2 * a ** 2))
        # f(v) = (m/(2pikBT))^3/2 * 4piv^2^* exp(-mv^2/(2kBT))
        T_min, T_max = 10, 5000
        m_brom, m_chlor = 79.9, 35.45
        eps = 1e-6
        _unit = 1.6605E-27 # kg
        kB = 1.380649E-23 # m^2 kg s^-2 K^-1
        T = ValueTracker(30) # K
        m = ValueTracker(m_brom) * _unit # starter på Brom
        plane = NumberPlane(
            x_range=(0, 3000+eps, 500),
            y_range=(0, 0.005+eps, 0.001),
            x_length=11,
            y_length=6,
            background_line_style={
                "stroke_color": LIGHTER_GRAY,
                "stroke_width": 1,
                "stroke_opacity": 0.3,
            },
            axis_config={
                "include_tip": True,
                "tip_shape": StealthTip,
                "tip_width": 0.2,
                "tip_height": 0.2
            },
        ) # .to_edge(RIGHT, buff=0.1)
        # axis_labels = VGroup(*[
        #     MathTex(
        #         lab, color=c, font_size=36
        #     ).move_to(plane.c2p(coord)).set_z_index(plane.get_z_index()+5)
        #     for lab, c, coord in zip(
        #         ["v~[m/s]", "p"], [(3, 0.25), (0.25, 6.25)]
        #     )
        # ])
        axis_labels = VGroup(
            MathTex("v~[m/s]", font_size=36).next_to(plane[2], RIGHT, aligned_edge=DOWN),
            MathTex("p", font_size=36).next_to(plane[3], UP, aligned_edge=LEFT)
        )
        tickmarks = {
            "x": VGroup(*[Line(
                start=plane.c2p(x, 0.0001), end=plane.c2p(x, -0.0001),
                color=WHITE, stroke_width=0.75
            ) for x in np.arange(0, 3000, 500)]).set_z_index(4),
            "y": VGroup(*[Line(
                start=plane.c2p(100, y), end=plane.c2p(100, y),
                color=WHITE, stroke_width=0.75
            ) for y in np.arange(0, 0.005, 0.001)]).set_z_index(4),
        }
        ticks = {
            "x": VGroup(*[DecimalNumber(
                number=x, num_decimal_places=0, include_sign=x < 0,
                color=WHITE, font_size=24 if x != 0 else 0.01
            ).set_z_index(4).next_to(
                tm, DOWN, buff=0.2
            ) for x, tm in zip(np.arange(0, 3000, 500), tickmarks["x"])]),
            "y": VGroup(*[DecimalNumber(
                number=y, num_decimal_places=3, include_sign=y < 0,
                color=WHITE, font_size=24 if y != 0 else 0.01
            ).set_z_index(4).next_to(
                tm, LEFT, buff=0.5
            ) for y, tm in zip(np.arange(0, 0.005+eps, 0.001), tickmarks["y"])]),
        }
        tick_bgs = VGroup(
            *[
                SurroundingRectangle(
                m, stroke_width=0, fill_opacity=1, fill_color=DARKER_GRAY, buff=0.025
                ) for m in ticks["x"]
            ],
            *[
                SurroundingRectangle(
                m, stroke_width=0, fill_opacity=1, fill_color=DARKER_GRAY, buff=0.025
                ) for m in ticks["y"]
            ],
            *[
                SurroundingRectangle(
                m, stroke_width=0, fill_opacity=1, fill_color=DARKER_GRAY, buff=0.025
                ) for m in axis_labels
            ]
        )
        self.play(
            LaggedStart(
                DrawBorderThenFill(plane),
                LaggedStart(
                    *[Write(l) for l in axis_labels],
                    *[Create(l) for l in tickmarks.values()],
                    *[Write(l) for l in ticks.values()],
                    lag_ratio=0.1
                ),
                lag_ratio=0.5
            ),
            run_time=3
        )
        self.slide_pause()
        graph = always_redraw(lambda:
            plane.plot(
                lambda v: (m.get_value()/(2*np.pi*kB*T.get_value()))**(3/2) * 4*np.pi*v**2 * np.exp((-m.get_value()*v**2)/(2*kB*T.get_value())),
                x_range=(0, 3000),
                color=interpolate_color(BLUE, RED, T.get_value()/(T_max-T_min))
            )
        )
        temperatur_tekst = always_redraw(lambda:
            VGroup(
                Tex("T = "),
                DecimalNumber(
                    T.get_value(), num_decimal_places=0,
                    color=interpolate_color(BLUE, RED, T.get_value()/(T_max-T_min)),
                    unit="K"
                ),
            ).arrange(RIGHT).move_to(plane.c2p(1500, 0.00525))
        )
        masse_tekst = always_redraw(lambda:
            VGroup(
                Tex("m = "),
                DecimalNumber(
                    m.get_value()/_unit, num_decimal_places=2,
                    color=YELLOW,
                    unit="amu"
                ),
            ).arrange(RIGHT).next_to(temperatur_tekst, DOWN, aligned_edge=LEFT)
        )
        # self.add(plane, graph)
        # self.add(axis_labels, *ticks.values(), *tickmarks.values())
        # self.add(temperatur_tekst, masse_tekst)
        self.play(
            LaggedStart(
                Create(graph, run_time=2),
                Write(temperatur_tekst),
                Write(masse_tekst),
                lag_ratio=0.25
            )
        )
        # self.play(
        #     T.animate.set_value(3*T_min)
        # )
        # self.slide_pause()
        # self.play(
        #     T.animate.set_value(T_max),
        #     run_time=10
        # )
        self.slide_pause()
        self.play(
            T.animate.set_value(273)
        )
        self.slide_pause()

        hyppigst = always_redraw(lambda:
            VGroup(
                VGroup(
                    Tex(
                        "Mest {{hyppige}} hastighed: "
                    ).set_color_by_tex_to_color_map({"hyppige": ORANGE}),
                    DecimalNumber(
                        np.sqrt(2 * kB * T.get_value() / m.get_value()), num_decimal_places=1, unit="~m/s"
                    )
                ).scale(0.875).arrange(RIGHT).next_to(masse_tekst, DOWN, aligned_edge=LEFT),
                Dot(
                    stroke_width=0, fill_color=ORANGE
                ).move_to(plane.c2p(
                    np.sqrt(2*kB*T.get_value()/m.get_value()),
                    graph.underlying_function(np.sqrt(2*kB*T.get_value()/m.get_value()))
                )),
            )
        )
        middel = always_redraw(lambda:
            VGroup(
                VGroup(
                    Tex(
                        "Mest {{gennemsnitlige}} hastighed: "
                    ).set_color_by_tex_to_color_map({"gennemsnitlige": PINK}),
                    DecimalNumber(
                        np.sqrt(8 * kB * T.get_value() / (m.get_value() * np.pi)), num_decimal_places=1, unit="~m/s"
                    )
                ).scale(0.875).arrange(RIGHT).next_to(hyppigst[0], DOWN, aligned_edge=LEFT),
                Dot(
                    stroke_width=0, fill_color=PINK
                ).move_to(plane.c2p(
                    np.sqrt(8 * kB * T.get_value() / (m.get_value() * np.pi)),
                    graph.underlying_function(np.sqrt(8 * kB * T.get_value() / (m.get_value() * np.pi)))
                )),
            )
        )
        self.play(
            FadeIn(hyppigst),
            FadeIn(middel),
        )
        self.slide_pause()

        self.play(
            T.animate.set_value(1000),
            run_time=2
        )
        self.slide_pause()

        andel_cutoff_tracker = ValueTracker(1000) # m/s
        andel_areal = always_redraw(lambda:
            plane.get_riemann_rectangles(
                graph, x_range=(andel_cutoff_tracker.get_value(), 3000), dx=10, fill_opacity=0.75,
                stroke_width=0, color=GREEN, show_signed_area=True
            )
        )
        andel_tal = always_redraw(lambda:
            DecimalNumber(
                1 - (scipy.special.erf(andel_cutoff_tracker.get_value()*np.sqrt(m.get_value()/(2*kB*T.get_value()))) - andel_cutoff_tracker.get_value()*np.sqrt(2*m.get_value()/(kB*T.get_value())) * np.exp((-m.get_value()*andel_cutoff_tracker.get_value()**2)/(2*kB*T.get_value()))),
                color=GREEN
            ).move_to(plane.c2p(2500, 0.0015))
        ) # bliver ikke tilføjet, da resultatet går udenfor intervallet [0;1]
        # self.add(andel_areal)
        self.play(
            LaggedStart(
                *[
                    FadeIn(m) for m in andel_areal
                ],
                lag_ratio=0.01
            ),
            run_time=1
        )
        self.remove(andel_areal)
        self.add(andel_areal)
        self.slide_pause()
        self.play(
            T.animate.set_value(T_max)
        )
        self.slide_pause()
        self.play(
            T.animate.set_value(1000)
        )
        self.slide_pause()

        self.play(
            m.animate.set_value(m_chlor*_unit)
        )
        self.slide_pause()


class HastighedsFordelingThumbnail(HastighedsFordeling):
    def construct(self):
        eps = 1e-6
        _unit = 1.6605E-27 # kg
        kB = 1.380649E-23 # m^2 kg s^-2 K^-1
        T = 1500 # K
        m = 30 * _unit # starter på Brom
        plane = NumberPlane(
            x_range=(0, 3000+eps, 500),
            y_range=(0, 0.001+eps, 0.00025),
            x_length=11,
            y_length=6,
            background_line_style={
                "stroke_color": LIGHTER_GRAY,
                "stroke_width": 1,
                "stroke_opacity": 0.3,
            },
            axis_config={
                "include_tip": True,
                "tip_shape": StealthTip,
                "tip_width": 0.2,
                "tip_height": 0.2
            },
        )
        axis_labels = VGroup(
            MathTex("v~[m/s]", font_size=36).next_to(plane[2], RIGHT, aligned_edge=DOWN),
            MathTex("p", font_size=36).next_to(plane[3], UP, aligned_edge=LEFT)
        )
        tickmarks = {
            "x": VGroup(*[Line(
                start=plane.c2p(x, 0.000025), end=plane.c2p(x, -0.000025),
                color=WHITE, stroke_width=0.75
            ) for x in np.arange(0, 3000, 500)]).set_z_index(4),
            "y": VGroup(*[Line(
                start=plane.c2p(100, y), end=plane.c2p(100, y),
                color=WHITE, stroke_width=0.75
            ) for y in np.arange(0, 0.001, 0.00025)]).set_z_index(4),
        }
        ticks = {
            "x": VGroup(*[DecimalNumber(
                number=x, num_decimal_places=0, include_sign=x < 0,
                color=WHITE, font_size=24 if x != 0 else 0.01
            ).set_z_index(4).next_to(
                tm, DOWN, buff=0.2
            ) for x, tm in zip(np.arange(0, 3000, 500), tickmarks["x"])]),
            "y": VGroup(*[DecimalNumber(
                number=y, num_decimal_places=5, include_sign=y < 0,
                color=WHITE, font_size=24 if y != 0 else 0.01
            ).set_z_index(4).next_to(
                tm, LEFT, buff=0.5
            ) for y, tm in zip(np.arange(0, 0.001+eps, 0.00025), tickmarks["y"])]),
        }
        graph = always_redraw(lambda:
            plane.plot(
                lambda v: (m/(2*np.pi*kB*T))**(3/2) * 4*np.pi*v**2 * np.exp((-m*v**2)/(2*kB*T)),
                x_range=(0, 3000),
                color=RED
            )
        )
        andel_areal = plane.get_riemann_rectangles(
            graph, x_range=(1000, 3000), dx=10, fill_opacity=0.75,
            stroke_width=0, color=GREEN, show_signed_area=True
        )
        VGroup(
            plane, graph, *tickmarks.values(), *ticks.values(), axis_labels, andel_areal
        ).scale(0.9).to_edge(DR, buff=0.1)
        overskrift = Tex(r"Maxwell-Boltzmanns hastighedsfordeling", font_size=60).to_edge(UL)
        overskrift_boks = get_background_rect(overskrift, stroke_colour=RED, stroke_width=4)
        VGroup(overskrift, overskrift_boks).to_edge(UL, buff=0.05)
        self.add(
            plane, graph, *tickmarks.values(), *ticks.values(), axis_labels, overskrift, overskrift_boks, andel_areal
        )


class Energidiagrammer(MovingCameraScene, Slide if slides else Scene):
    def construct(self):
        # self.camera.background_color = DARKER_GRAY
        self.camera.background_color = WHITE
        # title = Tex(r"Maxwell-Boltzmanns \\hastighedsfordeling").scale(2)
        # self.add(title)
        # self.slide_pause()
        # self.play(
        #     FadeOut(title),
        #     run_time=0.25
        # )
        # self.basis_energidiagram()
        self.flertrin_energidiagram()
        self.wait(5)

    def slide_pause(self, t=0.5, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def get_cmap(self):
        return {"reak": GREEN, "prod": GOLD, "tran": RED}

    def flertrin_energidiagram(self):
        cmap = self.get_cmap()
        plane = Axes(
            x_range=(0, 8, 8),
            y_range=(0, 1, 0.1),
            x_length=11,
            y_length=6,
            # background_line_style={
            #     "stroke_color": LIGHTER_GRAY,
            #     "stroke_width": 1,
            #     "stroke_opacity": 0.3,
            # },
            axis_config={
                "include_tip": True,
                "tip_shape": StealthTip,
                "tip_width": 0.2,
                "tip_height": 0.2
            },
        ).set_color(BLACK)
        axis_labels = VGroup(
            Tex("Reaktionskoordinat", color=BLACK, font_size=36).next_to(plane[0], UP, aligned_edge=RIGHT),
            MathTex("E_{pot}", color=BLACK, font_size=36).next_to(plane[1], RIGHT, aligned_edge=UP),
        )
        _points = [
            (1, 0.5, 0),
            (2, 0.5, 0),
            (3, 0.8, 0),
            (4, 0.35, 0),
            (5, 0.7, 0),
            (6, 0.3, 0),
            (7, 0.3, 0)
        ]
        points = [plane.c2p(p) for p in _points]
        dots = VGroup(
            *[
                Dot().move_to(plane.c2p(_p)) for _p in _points
            ]
        )
        lines = VGroup(
            *[
                CubicBezier(
                    p1, p1+0.5*RIGHT, p2+0.5*LEFT, p2, color=BLACK, stroke_width=8
                ) for p1, p2 in zip(points[:-1], points[1:])
            ]
        )
        self.add(lines, plane, axis_labels)

        dashed_lines = VGroup(
            *[
                DashedLine(
                    start=plane.c2p(0, y), end=plane.c2p(x, y), color=c, stroke_width=2
                ) for x, y, c in zip(
                    (_points[0][0], _points[2][0], _points[3][0], _points[4][0], _points[5][0]),
                    (_points[0][1], _points[2][1], _points[3][1], _points[4][1], _points[5][1]),
                    (cmap["reak"], cmap["tran"], interpolate_color(cmap["reak"], cmap["prod"], 0.5), cmap["tran"], cmap["prod"])
                )
            ]
        )
        self.add(dashed_lines)


class BestemmelseAfHastighedsudtryk(Energidiagrammer):
    def construct(self):
        self.camera.frame.scale(1.2)
        self.camera.background_color = DARKER_GRAY
        title = Tex(r"Kvantitativ bestemmelse af \\reaktionssorden").scale(2)
        self.add(title)
        self.slide_pause()
        self.play(
            FadeOut(title),
            run_time=0.25
        )
        setup_data = self.setup_problem()
        conc_data = self.show_first_graph(setup_data)
        velo_data = self.show_velocity(conc_data)
        self.update_graph_and_conclude(velo_data)
        self.wait(5)

    def get_data_points(self):
        times = [0, 100, 200, 400, 600, 900, 1200, 1500] # s
        concs = [5.0e-3, 4.65e-3, 4.32e-3, 3.74e-3, 3.23e-3, 2.60e-3, 2.09e-3, 1.68e-3] # M
        return [times, concs]

    def get_cmap(self):
        return {"tid": BLUE, "konc": YELLOW, "velo": RED}

    def setup_problem(self):
        cmap = self.get_cmap()
        problem_text = VGroup(
            Tex("Vi betragter denne reaktion:").scale(0.9).to_edge(LEFT).shift(UP),
            Tex("2 N$_2$O$_5$", r" $\rightleftharpoons$ ", "4 NO$_2$", " + ", "O$_2$"),
            Tex("med følgende hastighedsudtryk:").scale(0.9).to_edge(RIGHT).shift(UP),
            MathTex("v", "=", "k", r"\cdot", r"[\text{N}_2\text{O}_5]", "^x")
        )
        problem_text[1].next_to(problem_text[0], DOWN, aligned_edge=LEFT)
        problem_text[3].next_to(problem_text[2], DOWN, aligned_edge=RIGHT)
        for t in problem_text:
            self.play(
                Write(t)
            )
            self.slide_pause()
        self.play(
            problem_text[-1][0].animate.set_color(cmap["velo"]),
            problem_text[-1][-2].animate.set_color(cmap["konc"]),
            run_time=0.5
        )
        self.slide_pause()

        setup_text = Tex(r"For at finde reaktionsordenen, $x$,\\skal vi bruge målinger fra forsøg").to_edge(DOWN)
        self.play(
            Write(setup_text)
        )
        self.slide_pause()
        keeping_text = VGroup(problem_text[1].copy(), problem_text[3].copy()).arrange(DOWN, aligned_edge=LEFT).to_corner(UL, buff=0)
        keeping_box = get_background_rect(
            keeping_text,
            stroke_colour=color_gradient(cmap.values(), 3)
        )
        self.play(
            FadeOut(setup_text),
            FadeOut(problem_text[0], shift=2/3*UP+1/3*LEFT),
            FadeOut(problem_text[2], shift=1/3*UP+2/3*LEFT),
            ReplacementTransform(VGroup(problem_text[1], problem_text[3]), keeping_text),
            FadeIn(keeping_box, shift=0.25*UL)
        )
        overall_problem = VGroup(keeping_text, keeping_box)
        self.remove(keeping_box, keeping_text)
        return overall_problem

    def show_first_graph(self, prev_mobs):
        overall_problem = prev_mobs
        self.add(overall_problem)
        times, concs = self.get_data_points()
        cmap = self.get_cmap()
        t_start, t_slut, dt, eps = 0, 1600, 200, 1e-6
        c_start, c_slut, dc = 0, 6e-3, 1e-3
        plane = NumberPlane(
            x_range=(t_start, t_slut+eps, dt),
            y_range=(c_start, c_slut+eps, dc),
            x_length=8.5,
            y_length=7,
            background_line_style={
                "stroke_color": LIGHTER_GRAY,
                "stroke_width": 1,
                "stroke_opacity": 0.3,
            },
            axis_config={
                # "include_numbers": True,
                "include_tip": True,
                "tip_shape": StealthTip,
                "tip_width": 0.2,
                "tip_height": 0.2
            },
        )
        # ).to_edge(LEFT, buff=0.2)
        axis_labels = VGroup(*[
            MathTex(
                lab, color=c, font_size=36
            ).move_to(plane.c2p(coord)).set_z_index(plane.get_z_index()+5)
            for lab, c, coord in zip(
                ["t~[s]", r"[\text{N}_2\text{O}_5]~[M]"], [cmap["tid"], cmap["konc"]], [(t_slut, dc/4), (dt, c_slut)]
            )
        ])
        tickmarks = {
            "x": VGroup(*[Line(
                start=plane.c2p(x, dc/20), end=plane.c2p(x, -dc/20), color=WHITE, stroke_width=1.5
            ) for x in np.arange(t_start, t_slut+eps, dt)]).set_z_index(4),
            "y": VGroup(*[Line(
                start=plane.c2p(dt/20, y), end=plane.c2p(-dt/20, y), color=WHITE, stroke_width=1.5
            ) for y in np.arange(c_start, c_slut+eps, dc)]).set_z_index(4),
        }
        ticks = {
            "x": VGroup(*[DecimalNumber(
                number=x, num_decimal_places=0, include_sign=x < 0, color=cmap["tid"], font_size=24 if x != 0 else 0.01
            ).set_z_index(4).next_to(
                tm, DOWN, buff=0.2
            ) for x, tm in zip(np.arange(t_start, t_slut+eps, dt), tickmarks["x"])]),
            "y": VGroup(*[DecimalNumber(
                number=y, num_decimal_places=3, include_sign=y < 0, color=cmap["konc"], font_size=24 if y != 0 else 0.01
            ).set_z_index(4).next_to(
                tm, LEFT, buff=0.2
            ) for y, tm in zip(np.arange(c_start, c_slut+eps, dc), tickmarks["y"])]),
        }
        # tick_bgs = VGroup(
        #     *[
        #         SurroundingRectangle(
        #         m, stroke_width=0, fill_opacity=1, fill_color=DARKER_GRAY, buff=0.025
        #         ) for m in ticks["x"]
        #     ],
        #     *[
        #         SurroundingRectangle(
        #         m, stroke_width=0, fill_opacity=1, fill_color=DARKER_GRAY, buff=0.025
        #         ) for m in ticks["y"]
        #     ],
        #     *[
        #         SurroundingRectangle(
        #         m, stroke_width=0, fill_opacity=1, fill_color=DARKER_GRAY, buff=0.025
        #         ) for m in axis_labels
        #     ]
        # )
        [m.scale(0.9) for m in self.mobjects]
        # self.add(plane, axis_labels)
        # self.add(*tickmarks.values(), *ticks.values())
        self.play(
            LaggedStart(
                AnimationGroup(
                    self.camera.frame.animate.shift(3*LEFT),
                    overall_problem.animate.shift(4.25*LEFT),
                ),
                DrawBorderThenFill(plane),
                *[Create(t) for t in tickmarks.values()],
                *[Write(t) for t in ticks.values()],
                Write(axis_labels),
                lag_ratio=0.25
            )
        )
        self.slide_pause(5*_ONEFRAME)

        # reaction_text = Tex(
        #     "2 N$_2$O$_5$", r" $\rightleftharpoons$ ", "4 NO$_2$", " + ", "O$_2$"
        # ).move_to(plane.c2p(1000, 4e-3))
        # self.add(reaction_text)
        # self.play(
        #     Write(reaction_text)
        # )
        # self.slide_pause()

        data_points = VGroup(
            *[
                Dot().move_to(plane.c2p(t, c)) for t, c in zip(times, concs)
            ]
        )
        self.play(
            LaggedStart(
                *[DrawBorderThenFill(dot) for dot in data_points],
                lag_ratio=0.1
            )
        )
        self.remove(data_points)
        self.add(data_points)
        self.slide_pause(5*_ONEFRAME)

        regression = np.exp(np.polyfit(times, np.log(concs), 1))
        graph = plane.plot(
            lambda x: regression[1] * regression[0]**x,
            color=cmap["konc"]
        ).set_z_index(2)
        # self.add(graph)
        self.play(
            Create(graph)
        )
        self.slide_pause(5*_ONEFRAME)
        self.remove(plane, axis_labels, *tickmarks.values(), *ticks.values(), data_points, graph, overall_problem)
        return [plane, axis_labels, tickmarks, ticks, data_points, regression, graph, overall_problem]

    def show_velocity(self, prev_mobs):
        conc_plane, conc_axis_labels, conc_tickmarks, conc_ticks, data_points, regression, conc_graph, overall_problem = prev_mobs
        self.add(
            conc_plane, conc_axis_labels,
            *conc_tickmarks.values(), *conc_ticks.values(),
            data_points, conc_graph, overall_problem
        )

        times, concs = self.get_data_points()
        cmap = self.get_cmap()
        c_start, c_slut, dc, eps = 0, 6e-3, 1e-3, 1e-8
        v_start, v_slut, dv = -5e-6, 5e-6, 1e-6
        velo_plane = NumberPlane(
            x_range=(c_start, c_slut+eps, dc),
            y_range=(v_start, v_slut+eps, dv),
            x_length=8.5,
            y_length=7,
            background_line_style={
                "stroke_color": LIGHTER_GRAY,
                "stroke_width": 1,
                "stroke_opacity": 0.3,
            },
            axis_config={
                # "include_numbers": True,
                "include_tip": True,
                "tip_shape": StealthTip,
                "tip_width": 0.2,
                "tip_height": 0.2
            },
        )
        # ).to_edge(LEFT, buff=0.2)
        velo_plane.next_to(conc_plane, RIGHT, buff=2)
        velo_axis_labels = VGroup(*[
            MathTex(
                lab, color=c, font_size=36
            ).move_to(velo_plane.c2p(coord)).set_z_index(velo_plane.get_z_index()+5)
            for lab, c, coord in zip(
                [r"[\text{N}_2\text{O}_5]~[M]", r"v^* [~\cdot 10^{-6}M/s]"], [cmap["konc"], cmap["velo"]], [(c_slut, dv/2), (dc, v_slut)]
            )
        ])
        velo_tickmarks = {
            "x": VGroup(*[Line(
                start=velo_plane.c2p(x, dv/10), end=velo_plane.c2p(x, -dv/10), color=WHITE, stroke_width=1.5
            ) for x in np.arange(c_start, c_slut+eps, dc)]).set_z_index(4),
            "y": VGroup(*[Line(
                start=velo_plane.c2p(dc/20, y), end=velo_plane.c2p(-dc/20, y), color=WHITE, stroke_width=1.5
            ) for y in np.arange(v_start, v_slut+eps, dv)]).set_z_index(4),
        }
        velo_ticks = {
            "x": VGroup(*[DecimalNumber(
                number=x, num_decimal_places=3, include_sign=x < 0, color=cmap["konc"], font_size=24 if x != 0 else 0.01
            ).set_z_index(4).next_to(
                tm, DOWN, buff=0.2
            ) for x, tm in zip(np.arange(c_start, c_slut+eps, dc), velo_tickmarks["x"])]),
            "y": VGroup(*[DecimalNumber(
                number=y*1e6, num_decimal_places=1, include_sign=y < 0, color=cmap["velo"], font_size=24 if np.abs(y) > eps else 0.01
            ).set_z_index(4).next_to(
                tm, LEFT, buff=0.2
            ) for y, tm in zip(np.arange(v_start, v_slut+eps, dv), velo_tickmarks["y"])]),
        }
        # self.camera.frame.scale(1.75).move_to(VGroup(conc_plane, velo_plane))
        # self.add(velo_plane, velo_axis_labels)
        # self.add(*velo_tickmarks.values(), *velo_ticks.values())
        self.play(
            LaggedStart(
                AnimationGroup(
                    self.camera.frame.animate.scale(1.25).move_to(VGroup(conc_plane, velo_plane)),
                    overall_problem.animate.next_to(conc_plane, UP, buff=0.5)
                ),
                # reaction_text.animate.next_to(conc_plane, UP, buff=0.5),
                DrawBorderThenFill(velo_plane),
                *[Create(t) for t in velo_tickmarks.values()],
                *[Write(t) for t in velo_ticks.values()],
                Write(velo_axis_labels),
                lag_ratio=0.2
            )
        )
        self.slide_pause()

        v_star_text = VGroup(
            MathTex(
                "v^*", "=", " ", r"\frac{", r"\Delta", r"[\text{N}_2\text{O}_5]", "}{", r"\Delta", "t", "}", " "
            ),
            MathTex(
                "v^*", "=", r"\left|", r"\frac{", r"\Delta", r"[\text{N}_2\text{O}_5]", "}{", r"\Delta", "t", "}", r"\right|"
            )
        ).next_to(velo_plane, UP)
        for i in range(2):
            v_star_text[i][0].set_color(cmap["velo"])
            v_star_text[i][5].set_color(cmap["konc"])
            v_star_text[i][8].set_color(cmap["tid"])
        # self.add(v_star_text[0])
        self.play(
            Write(v_star_text[0])
        )
        self.slide_pause()

        time_tracker = ValueTracker(0)
        conc_tracker = always_redraw(lambda: DecimalNumber(conc_graph.underlying_function(time_tracker.get_value())))
        moving_tangent_point = always_redraw(lambda:
            Dot(fill_color=cmap["velo"], stroke_width=0).move_to(
                conc_plane.c2p(time_tracker.get_value(), conc_graph.underlying_function(time_tracker.get_value()))
            )
        )
        moving_tangent_line = always_redraw(lambda:
            conc_plane.get_secant_slope_group(
                x=time_tracker.get_value(),
                graph=conc_graph,
                secant_line_color=cmap["velo"],
                dx=1e-6,
                secant_line_length=4,
                dx_line_color=None,
                dy_line_color=None,
            )
        )
        # self.add(moving_tangent_line, moving_tangent_point)
        self.play(
            DrawBorderThenFill(moving_tangent_point),
            Create(moving_tangent_line)
        )
        self.slide_pause()

        velos = [
            *[conc_plane.slope_of_tangent(x=t, graph=conc_graph) for t in times]
        ]
        velo_points = VGroup(
            *[
                Dot().move_to(velo_plane.c2p(c, v)) for c, v in zip(concs, velos)
            ]
        )
        velo_regression = np.polyfit(concs, velos, 1)
        velo_graph = always_redraw(lambda:
            velo_plane.plot(
                lambda x: velo_regression[0] * x + velo_regression[1],
                x_range=(c_start, c_slut),
                color=cmap["velo"]
            )
        )
        # self.add(velo_points, velo_graph)

        slope_text = Tex("Hældning", " = ").scale(0.9).move_to(conc_plane.c2p(800, -1e-3))
        slope_val = always_redraw(lambda:
            DecimalNumber(
                conc_plane.slope_of_tangent(x=time_tracker.get_value(), graph=conc_graph)*1e6,
                num_decimal_places=3,
                color=cmap["velo"]
            ).scale(0.9).next_to(slope_text, RIGHT)
        )
        slope_unit = MathTex(r"~\cdot 10^{-6}\frac{M}{s}", color=cmap["velo"]).scale(0.9).next_to(slope_val, RIGHT)
        # self.add(slope_text, slope_val, slope_unit)
        self.play(
            LaggedStart(
                *[Write(m) for m in (slope_text, slope_val, slope_unit)],
                lag_ratio=1
            )
        )
        self.slide_pause()
        conc_markers = always_redraw(lambda:
            VGroup(
                DashedLine(
                    start=conc_plane.c2p(
                        0,
                        conc_graph.underlying_function(time_tracker.get_value())
                    ),
                    end=conc_plane.c2p(
                        time_tracker.get_value(),
                        conc_graph.underlying_function(time_tracker.get_value())
                    ),
                    color=cmap["konc"]
                ),
                DashedLine(
                    start=velo_plane.c2p(
                        conc_graph.underlying_function(time_tracker.get_value()),
                        0
                    ),
                    end=velo_plane.c2p(
                        conc_graph.underlying_function(time_tracker.get_value()),
                        conc_plane.slope_of_tangent(x=time_tracker.get_value(), graph=conc_graph)
                    ),
                    color=cmap["konc"]
                )
            )
        )
        velo_marker = always_redraw(lambda:
            VGroup(
                DashedLine(
                    start=velo_plane.c2p(
                        0,
                        conc_plane.slope_of_tangent(x=time_tracker.get_value(), graph=conc_graph)
                    ),
                    end=velo_plane.c2p(
                        conc_graph.underlying_function(time_tracker.get_value()),
                        conc_plane.slope_of_tangent(x=time_tracker.get_value(), graph=conc_graph)
                    ),
                    color=cmap["velo"]
                ),
                Arrow(
                    start=slope_unit.get_corner(UR),
                    end=velo_plane.c2p(
                        0.5*conc_graph.underlying_function(time_tracker.get_value()),
                        conc_plane.slope_of_tangent(x=time_tracker.get_value(), graph=conc_graph)
                    ),
                    tip_shape=StealthTip,
                )
            )
        )
        # self.add(conc_markers, velo_marker)
        self.play(
            *[Create(cm) for cm in conc_markers],
            Create(velo_marker[0]),
            GrowFromPoint(velo_marker[1], point=velo_marker[1].get_start())
        )
        self.remove(conc_markers, velo_marker)
        self.add(conc_markers, velo_marker)
        self.slide_pause()

        self.play(
            DrawBorderThenFill(velo_points[0])
        )
        self.slide_pause()
        for i, t in enumerate(times[1:]):
            self.play(
                time_tracker.animate.set_value(t),
                run_time=(t-times[i])/200,
            )
            self.play(
                DrawBorderThenFill(velo_points[i+1]),
                run_time=0.5
            )
            self.slide_pause()
        self.remove(velo_points)
        self.add(velo_points)

        # self.play(
        #     Create(velo_graph)
        # )
        # self.slide_pause()

        for m in (slope_unit, slope_val, slope_text, velo_marker, conc_markers, moving_tangent_line, moving_tangent_point):
            print(m)
        self.play(
            *[FadeOut(m) for m in (slope_unit, slope_val, slope_text, velo_marker, conc_markers, moving_tangent_line, moving_tangent_point)]
        )
        self.slide_pause()

        self.remove(
            conc_plane, conc_axis_labels, *conc_tickmarks.values(), *conc_ticks.values(), data_points,
            conc_graph, #reaction_text,
            velo_plane, velo_axis_labels, *velo_tickmarks.values(), *velo_ticks.values(), velo_points, velo_graph,
            v_star_text[0], overall_problem
        )
        return (
            conc_plane, conc_axis_labels, conc_tickmarks, conc_ticks, data_points, regression, conc_graph, overall_problem, #reaction_text,
            velo_plane, velo_axis_labels, velo_tickmarks, velo_ticks, velo_points, velo_graph, v_star_text, time_tracker, velos
        )

    def update_graph_and_conclude(self, prev_mobs):
        conc_plane, conc_axis_labels, conc_tickmarks, conc_ticks, data_points, regression, conc_graph, overall_problem, velo_plane, velo_axis_labels, velo_tickmarks, velo_ticks, velo_points, velo_graph, v_star_text, time_tracker, velos = prev_mobs
        self.add(
            conc_plane, conc_axis_labels, *conc_tickmarks.values(), *conc_ticks.values(), data_points,
            conc_graph, overall_problem, #reaction_text,
            velo_plane, velo_axis_labels, *velo_tickmarks.values(), *velo_ticks.values(), velo_points, # velo_graph,
            v_star_text[0]
        )

        times, concs = self.get_data_points()
        cmap = self.get_cmap()
        c_start, c_slut, dc, eps = 0, 6e-3, 1e-3, 1e-8
        v_start, v_slut, dv = 0, 5e-6, 1e-6
        velo_plane_new = NumberPlane(
            x_range=(c_start, c_slut+eps, dc),
            y_range=(v_start, v_slut+eps, dv),
            x_length=8.5,
            y_length=7,
            background_line_style={
                "stroke_color": LIGHTER_GRAY,
                "stroke_width": 1,
                "stroke_opacity": 0.3,
            },
            axis_config={
                # "include_numbers": True,
                "include_tip": True,
                "tip_shape": StealthTip,
                "tip_width": 0.2,
                "tip_height": 0.2
            },
        )
        velo_plane_new.next_to(conc_plane, RIGHT, buff=2)
        velo_axis_labels_new = VGroup(*[
            MathTex(
                lab, color=c, font_size=36
            ).move_to(velo_plane_new.c2p(coord)).set_z_index(velo_plane_new.get_z_index()+5)
            for lab, c, coord in zip(
                [r"[\text{N}_2\text{O}_5]~[M]", r"v^* [~\cdot 10^{-6}M/s]"], [cmap["konc"], cmap["velo"]], [(c_slut, dv/2), (dc, v_slut)]
            )
        ])
        velo_tickmarks_new = {
            "x": VGroup(*[Line(
                start=velo_plane_new.c2p(x, dv/10), end=velo_plane_new.c2p(x, -dv/10), color=WHITE, stroke_width=1.5
            ) for x in np.arange(c_start, c_slut+eps, dc)]).set_z_index(4),
            "y": VGroup(*[Line(
                start=velo_plane_new.c2p(dc/20, y), end=velo_plane_new.c2p(-dc/20, y), color=WHITE, stroke_width=1.5
            ) for y in np.arange(v_start, v_slut+eps, dv)]).set_z_index(4),
        }
        velo_ticks_new = {
            "x": VGroup(*[DecimalNumber(
                number=x, num_decimal_places=3, include_sign=x < 0, color=cmap["konc"], font_size=24 if x != 0 else 0.01
            ).set_z_index(4).next_to(
                tm, DOWN, buff=0.2
            ) for x, tm in zip(np.arange(c_start, c_slut+eps, dc), velo_tickmarks_new["x"])]),
            "y": VGroup(*[DecimalNumber(
                number=y*1e6, num_decimal_places=1, include_sign=y < 0, color=cmap["velo"], font_size=24 if np.abs(y) > eps else 0.01
            ).set_z_index(4).next_to(
                tm, LEFT, buff=0.2
            ) for y, tm in zip(np.arange(v_start, v_slut+eps, dv), velo_tickmarks_new["y"])]),
        }
        velo_regression = np.polyfit(concs, velos, 1)
        velo_graph_new = velo_plane.plot(
            lambda x: -1 * (velo_regression[0] * x + velo_regression[1]),
            x_range=(c_start, c_slut),
            color=cmap["velo"]
        )

        self.play(
            *[
                TransformMatchingShapes(
                    v_star_text[0][i],
                    v_star_text[1][i],
                ) for i in range(len(v_star_text[0]))
            ],
            # FadeOut(v_star_text[0]),
            # FadeIn(v_star_text[1]),
            *[
                dot.animate.move_to(
                    velo_plane.c2p(c, -v)
                ) for dot, c, v in zip(velo_points, concs, velos)
            ],
            # velo_graph.animate.become(velo_graph_new),
            run_time=2
        )
        # self.remove(velo_graph)
        # self.add(velo_graph_new)
        intermediate_dots = VGroup(
            *[
                dot.copy() for dot in velo_points
            ]
        )
        self.remove(velo_points)
        self.add(intermediate_dots)
        self.slide_pause()

        velo_points_new = VGroup(
            *[dot.move_to(velo_plane_new.c2p(c, -v)).set_z_index(5) for dot, c, v in zip(velo_points, concs, velos)]
        )
        animation_group = []
        for tm, tmn in zip(velo_tickmarks["x"], velo_tickmarks_new["x"]):
            animation_group.append(ReplacementTransform(tm, tmn))
        for tm in velo_tickmarks["y"][:5]:
            animation_group.append(FadeOut(tm, shift=DOWN))
        for tm, tmn in zip(velo_tickmarks["y"][5:], velo_tickmarks_new["y"]):
            animation_group.append(ReplacementTransform(tm, tmn))

        for t, tn in zip(velo_ticks["x"], velo_ticks_new["x"]):
            animation_group.append(ReplacementTransform(t, tn))
        for t in velo_ticks["y"][:5]:
            animation_group.append(FadeOut(t, shift=DOWN))
        for t, tn in zip(velo_ticks["y"][5:], velo_ticks_new["y"]):
            animation_group.append(ReplacementTransform(t, tn))

        for vp, vpn in zip(velo_plane, velo_plane_new):
            animation_group.append(TransformMatchingShapes(vp, vpn, transform_mismatches=False))

        for al, aln in zip(velo_axis_labels, velo_axis_labels_new):
            animation_group.append(ReplacementTransform(al, aln))

        for dot, dotn in zip(intermediate_dots, velo_points_new):
            animation_group.append(ReplacementTransform(dot, dotn))

        self.play(
            *animation_group
        )
        self.slide_pause()

        neg_velos = [
            *[-v for v in velos]
        ]
        velo_fit_deg1 = np.polyfit(concs, neg_velos, 1)
        # velo_fit_deg2 = np.polyfit(concs, neg_velos, 2)
        velo_graph_deg1 = velo_plane_new.plot(
            lambda x: velo_fit_deg1[0] * x + velo_fit_deg1[1],
            color=cmap["velo"]
        )
        # velo_graph_deg2 = velo_plane_new.plot(
        #     lambda x: velo_fit_deg2[0] * x**2 + velo_fit_deg2[1] * x + velo_fit_deg2[2],
        #     # lambda x: np.polyval(velo_fit_deg2, x),
        #     color=cmap["velo"]
        # )
        self.play(
            Create(velo_graph_deg1)
        )
        self.slide_pause()
        # self.play(
        #     Uncreate(velo_graph_deg1[::-1]),
        #     Create(velo_graph_deg2)
        # )
        # self.slide_pause()
        # self.play(
        #     Create(velo_graph_deg1),
        #     Uncreate(velo_graph_deg2[::-1])
        # )
        # self.slide_pause()

        forklarende_tekst = Tex(
            "Reaktionsordenen", r"\\", "er den samme som", r"\\", "polynomieordenen"
        ).move_to(conc_plane).set_z_index(8).scale(2)
        forklarende_tekst_bkg = get_background_rect(forklarende_tekst, buff=2, fill_opacity=0.95, stroke_colour=WHITE)
        # self.add(forklarende_tekst, forklarende_tekst_bkg)
        self.play(
            LaggedStart(
                FadeIn(forklarende_tekst_bkg),
                Write(forklarende_tekst),
                lag_ratio=0.5
            ),
            run_time=2
        )
        self.slide_pause()

        mere_forklarende = Tex(r"Lineære funktioner er\\1.-ordenspolynomier").next_to(forklarende_tekst, DOWN)
        self.play(
            *[
                FadeOut(m) for m in (
                    *conc_ticks.values(), *conc_tickmarks.values(), conc_graph, conc_plane, conc_axis_labels
                )
            ],
            FadeOut(forklarende_tekst, shift=0.5*DOWN),
            FadeOut(forklarende_tekst_bkg, shift=0.5*DOWN),
            FadeIn(mere_forklarende, shift=0.5*DOWN),
            overall_problem.animate.next_to(mere_forklarende, UP)
        )
        self.slide_pause()

        self.play(
            FadeOut(overall_problem[1]),
            overall_problem[0][0].animate.shift(UP),
            ReplacementTransform(
                overall_problem[0][1][-1],
                MathTex("^1")
            )
        )
        self.slide_pause()

        self.play(
            *[FadeOut(m) for m in self.mobjects]
        )


if __name__ == "__main__":
    classes = [
        # HastighedsFordeling,
        # Energidiagrammer,
        BestemmelseAfHastighedsudtryk
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
            if class_name + "Thumbnail" in dir():
                command = rf"manim {sys.argv[0]} {class_name}Thumbnail -pq{q} -o {class_name}Thumbnail.png"
                scene_marker(rf"RUNNNING:    {command}")
                subprocess.run(command)