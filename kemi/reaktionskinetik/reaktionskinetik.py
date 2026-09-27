# Maxwell-Boltzmann formel:
# PDF: P(x)=np.sqrt(2/np.pi) * x**2 / a**3 * np.exp(-x**2 / (2*a**2))
import math
import random

from manim import *
import sys

from manim_chemistry import ChemicalFormula

sys.path.append("../../")
sys.path.append("../../../")
import numpy as np
import pandas as pd
import scipy
import subprocess
from helpers import *
from custom_classes import *
# from manim_chemistry import *

slides = False
if slides:
    from manim_slides import Slide

q = "l"
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
        self.camera.background_color = DARKER_GRAY
        conc_data = self.show_first_graph()
        self.show_velocity(conc_data)
        self.wait(5)

    def get_data_points(self):
        times = [0, 100, 200, 400, 600, 900, 1200, 1500] # s
        concs = [5.0e-3, 4.65e-3, 4.32e-3, 3.74e-3, 3.23e-3, 2.60e-3, 2.09e-3, 1.68e-3] # M
        return [times, concs]

    def get_cmap(self):
        return {"tid": BLUE, "konc": YELLOW, "velo": RED}

    def show_first_graph(self):
        times, concs = self.get_data_points()
        cmap = self.get_cmap()
        t_start, t_slut, eps = 0, 1.05*max(times), 1e-6
        plane = NumberPlane(
            x_range=(t_start-eps, t_slut+eps+0.25, 250),
            y_range=(0, 1.05*max(concs)+eps, 1e-3),
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
                ["t~[s]", "[N_2O_5]~[M]"], [cmap["tid"], cmap["konc"]], [(1500, 2.5e-4), (200, 5.0e-3)]
            )
        ])
        tickmarks = {
            "x": VGroup(*[Line(
                start=plane.c2p(x, 5.0e-5), end=plane.c2p(x, -5.0e-5), color=WHITE, stroke_width=1.5
            ) for x in np.arange(0, 1501, 250)]).set_z_index(4),
            "y": VGroup(*[Line(
                start=plane.c2p(10, y), end=plane.c2p(-10, y), color=WHITE, stroke_width=1.5
            ) for y in np.arange(0, 6.0e-3, 1.0e-3)]).set_z_index(4),
        }
        ticks = {
            "x": VGroup(*[DecimalNumber(
                number=x, num_decimal_places=0, include_sign=x < 0, color=cmap["tid"], font_size=24 if x != 0 else 0.01
            ).set_z_index(4).next_to(
                tm, DOWN, buff=0.2
            ) for x, tm in zip(np.arange(0, 1501, 250), tickmarks["x"])]),
            "y": VGroup(*[DecimalNumber(
                number=y, num_decimal_places=3, include_sign=y < 0, color=cmap["konc"], font_size=24 if y != 0 else 0.01
            ).set_z_index(4).next_to(
                tm, LEFT, buff=0.2
            ) for y, tm in zip(np.arange(0, 6.0e-3, 1.0e-3), tickmarks["y"])]),
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
        self.add(plane, axis_labels, *tickmarks.values(), *ticks.values())
        self.slide_pause(5*_ONEFRAME)

        data_points = VGroup(
            *[
                Dot().move_to(plane.c2p(t, c)) for t, c in zip(times, concs)
            ]
        )
        self.add(data_points)
        self.slide_pause(5*_ONEFRAME)

        regression = np.exp(np.polyfit(times, np.log(concs), 1))
        graph = plane.plot(
            lambda x: regression[1] * regression[0]**x,
            color=cmap["konc"]
        ).set_z_index(2)
        self.add(graph)
        self.slide_pause(5*_ONEFRAME)
        self.remove(plane, axis_labels, *tickmarks.values(), *ticks.values(), data_points, graph)
        return [plane, axis_labels, tickmarks, ticks, data_points, regression, graph]

    def show_velocity(self, prev_mobs):
        conc_plane, conc_axis_labels, conc_tickmarks, conc_ticks, data_points, regression, conc_graph = prev_mobs
        self.add(conc_plane, conc_axis_labels, conc_tickmarks, conc_ticks, data_points, regression, conc_graph)

        times, concs = self.get_data_points()
        cmap = self.get_cmap()
        c_start, c_slut, eps = 0, 1.05*max(concs), 1e-6
        v_start = -0.5
        v_slut = -v_start*1.05
        velo_plane = NumberPlane(
            x_range=(c_start-eps, c_slut+eps+0.25, 1e-3),
            y_range=(v_start-eps, v_slut+eps, 2e-1),
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
        # axis_labels = VGroup(*[
        #     MathTex(
        #         lab, color=c, font_size=36
        #     ).move_to(plane.c2p(coord)).set_z_index(plane.get_z_index()+5)
        #     for lab, c, coord in zip(
        #         ["t~[s]", "[N_2O_5]~[M]"], [cmap["tid"], cmap["konc"]], [(1500, 2.5e-4), (200, 5.0e-3)]
        #     )
        # ])
        # tickmarks = {
        #     "x": VGroup(*[Line(
        #         start=plane.c2p(x, 5.0e-5), end=plane.c2p(x, -5.0e-5), color=WHITE, stroke_width=1.5
        #     ) for x in np.arange(0, 1501, 250)]).set_z_index(4),
        #     "y": VGroup(*[Line(
        #         start=plane.c2p(10, y), end=plane.c2p(-10, y), color=WHITE, stroke_width=1.5
        #     ) for y in np.arange(0, 6.0e-3, 1.0e-3)]).set_z_index(4),
        # }
        # ticks = {
        #     "x": VGroup(*[DecimalNumber(
        #         number=x, num_decimal_places=0, include_sign=x < 0, color=cmap["tid"], font_size=24 if x != 0 else 0.01
        #     ).set_z_index(4).next_to(
        #         tm, DOWN, buff=0.2
        #     ) for x, tm in zip(np.arange(0, 1501, 250), tickmarks["x"])]),
        #     "y": VGroup(*[DecimalNumber(
        #         number=y, num_decimal_places=3, include_sign=y < 0, color=cmap["konc"], font_size=24 if y != 0 else 0.01
        #     ).set_z_index(4).next_to(
        #         tm, LEFT, buff=0.2
        #     ) for y, tm in zip(np.arange(0, 6.0e-3, 1.0e-3), tickmarks["y"])]),
        # }
        velo_plane.next_to(conc_plane, RIGHT)
        self.camera.frame.scale(0.75).move_to(VGroup(conc_plane, velo_plane))
        self.add(velo_plane)


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