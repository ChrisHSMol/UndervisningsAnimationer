import math
import random

from manim import *
import sys

from manim_chemistry import ChemicalFormula

sys.path.append("../")
sys.path.append("../../")
import numpy as np
import pandas as pd
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


class LodretKast(MovingCameraScene, Slide if slides else Scene):
    def construct(self):
        self.camera.background_color = DARKER_GRAY
        title = Tex("Det lodrette kast").scale(2)
        self.add(title)
        self.slide_pause()
        self.play(
            FadeOut(title),
            run_time=0.25
        )
        exp_data = self.experimental_setup()
        sted_data = self.stedfunktion(exp_data)
        hast_data = self.hastighedsfunktion(sted_data)
        acc_data = self.accelerationsfunktion(hast_data)
        self.opsamling(sted_data, hast_data, acc_data)
        self.wait(5)

    def slide_pause(self, t=0.5, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def _simulation_data(self):
        t_start = -1
        t = ValueTracker(t_start)  # s
        g = -9.82  # m/s^2
        m = 1.0  # kg
        h_max = 1.0  # m
        sigY = 0  # m
        v0 = 10  # m/s
        s0 = 0.2  # m
        eps = 1e-6
        t_done = -2 * v0/g
        t_slut = np.ceil(t_done)
        return t_start, t, g, m, h_max, sigY, v0, s0, eps, t_done, t_slut


    def _cmap(self):
        cmap = {"tid": BLUE_C, "sted": GREEN, "hast": YELLOW, "acc": RED}
        cmap["Tid"] = cmap["tid"]
        cmap["Sted"] = cmap["sted"]
        cmap["Hastighed"] = cmap["hast"]
        cmap["Acceleration"] = cmap["acc"]
        return cmap

    def experimental_setup(self):
        t_start, t, g, m, h_max, sigY, v0, s0, eps, t_done, t_slut = self._simulation_data()

        def sted_raw(time, a=g, v=v0, s=s0):
            return 0.5 * a * time ** 2 + v * time + s

        def _sted(time, a=g, v=v0, s=s0):
            return np.max([sted_raw(time, a=a, v=v, s=s), s])

        def sted(time, a=g, v=v0, s=s0, _width=0.05):
            # return np.convolve(time, _sted(time, a=a, v=v, s=s), mode="valid")
            return np.mean([_sted(t, a=a, v=v, s=s) for t in np.linspace(time-0.5*_width, time+0.5*_width, 21)])

        def sted_measured(time, a=g, v=v0, s=s0):
            return sted(time, a=a, v=v, s=s) + random.gauss(mu=0.0, sigma=sigY)

        cmap = self._cmap()
        sensor = VGroup(
            Rectangle(
                width=4, height=0.25, stroke_width=0.25, fill_opacity=1, fill_color=LIGHT_GRAY
            ),
        ).to_edge(DL)
        svg_path = r"..\SVGs\basketball.svg"
        ball = SVGMobject(svg_path).scale(0.75).next_to(sensor, UP, buff=s0, aligned_edge=LEFT)
        ball.add_updater(
            lambda mob:
            mob.move_to(ball_ref.get_center() + sted(t.get_value()) * UP)
        )
        ball_ref = ball.copy()
        self.play(
            LaggedStart(
                DrawBorderThenFill(ball),
                DrawBorderThenFill(sensor),
                lag_ratio=0.5
            ),
            run_time=1.5
        )
        # self.add(sensor, ball)
        self.slide_pause()

        h_brace = always_redraw(lambda:
            BraceBetweenPoints(
                point_1=sensor.get_top(),
                point_2=ball.get_bottom(),
                direction=RIGHT,
                color=cmap["sted"]
            )
        )
        h_text = always_redraw(lambda:
            DecimalNumber(
                sted_measured(t.get_value()),
                num_decimal_places=2,
                include_sign=False,
                color=cmap["sted"],
                unit=" m"
            ).next_to(h_brace, RIGHT)
        )
        ball_lowest_point = always_redraw(lambda:
            DashedLine(start=ball.get_bottom()+0.75*LEFT, end=ball.get_bottom()+1.5*RIGHT, color=LIGHT_GRAY)
        )
        self.play(
            LaggedStart(
                Create(ball_lowest_point),
                GrowFromPoint(h_brace, h_brace.get_start()),
                Write(h_text),
                lag_ratio=0.75
            ),
            run_time=1.5
        )
        # self.add(h_brace, h_text, ball_lowest_point)
        self.slide_pause()

        self.play(
            t.animate.set_value(t_slut),
            run_time=t_slut-t_start,
            rate_func=linear,
        )
        self.slide_pause()
        t.set_value(t_start)

        plane = NumberPlane(
            x_range=(t_start-eps, t_slut+eps+0.25, 0.25),
            y_range=(-1-eps, 6+eps+0.5, 0.5),
            x_length=4.5*2,
            y_length=7.5,
            background_line_style={
                "stroke_color": LIGHTER_GRAY,
                "stroke_width": 1,
                "stroke_opacity": 0.3,
            },
            axis_config={
                # "include_ticks": True,
                "include_tip": True,
                "tip_shape": StealthTip,
                "tip_width": 0.2,
                "tip_height": 0.2
            },
            # x_axis_config={
            #     "numbers_to_include": (-1, 0, 1, 2, 3),
            #     "label_direction": DOWN
            # }
        ).to_edge(RIGHT, buff=0.1)
        axis_labels = VGroup(*[
            MathTex(
                lab, color=c, font_size=36
            ).move_to(plane.c2p(coord)).set_z_index(plane.get_z_index()+5)
            for lab, c, coord in zip(
                ["t~[s]", "s~[m]"], [cmap["tid"], cmap["sted"]], [(3, 0.25), (0.25, 6.25)]
            )
        ])
        tickmarks = {
            "x": VGroup(*[Line(
                start=plane.c2p(x, 0.1), end=plane.c2p(x, -0.1), color=WHITE, stroke_width=0.75
            ) for x in np.arange(-1, 3.1, 0.5)]).set_z_index(4),
            "y": VGroup(*[Line(
                start=plane.c2p(0.05, y), end=plane.c2p(-0.05, y), color=WHITE, stroke_width=0.75
            ) for y in np.arange(-1, 6.1, 1)]).set_z_index(4),
        }
        ticks = {
            "x": VGroup(*[DecimalNumber(
                number=x, num_decimal_places=1, include_sign=x < 0, color=cmap["tid"], font_size=24 if x != 0 else 0.01
            ).set_z_index(4).next_to(
                tm, DOWN, buff=0.2
            ) for x, tm in zip(np.arange(-1, 3.1, 0.5), tickmarks["x"])]),
            "y": VGroup(*[DecimalNumber(
                number=y, num_decimal_places=1, include_sign=y < 0, color=cmap["sted"], font_size=24 if y != 0 else 0.01
            ).set_z_index(4).next_to(
                tm, LEFT, buff=0.2
            ) for y, tm in zip(np.arange(-1, 6.1, 1), tickmarks["y"])]),
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
        # stedpunkter = VGroup(
        #     *[
        #         Dot(
        #             radius=0.05, stroke_width=0, fill_opacity=1, fill_color=cmap["sted"]
        #         ).move_to(plane.c2p(_t, sted_measured(_t))) for _t in np.linspace(t_start, t_slut, 50)
        #     ]
        # )
        # stedgraf = always_redraw(lambda: plane.plot(
        #     lambda x: sted_measured(t.get_value()),
        # ))
        stedgraf = always_redraw(lambda:
            plane.plot(
                # lambda x: sted_raw(x),
                lambda x: sted(x),
                color=cmap["sted"],
                x_range=[t_start, t.get_value()]
            )
        )
        self.play(
            LaggedStart(
                DrawBorderThenFill(plane),
                LaggedStart(
                    *[Write(l) for l in axis_labels],
                    *[Create(l) for l in tickmarks.values()],
                    *[Write(l) for l in ticks.values()],
                    *[FadeIn(l) for l in tick_bgs],
                    lag_ratio=0.1
                ),
                lag_ratio=0.5
            ),
            run_time=3
        )
        # self.add(plane, axis_labels)
        # self.slide_pause()
        # self.add(*ticks.values(), *tickmarks.values(), tick_bgs)
        # self.slide_pause()

        self.add(stedgraf)
        self.slide_pause()
        t.set_value(-1)

        self.play(
            t.animate.set_value(t_slut),
            run_time=t_slut-t_start,
            rate_func=linear,
        )
        t.set_value(t_slut)
        self.slide_pause()

        self.play(
            LaggedStart(
                *[FadeOut(m, shift=0.25*LEFT) for m in [ball, sensor, ball_lowest_point, h_brace, h_text]],
                lag_ratio=0.1
            ),
            run_time=0.5
        )
        # self.remove(ball, ball_lowest_point, sensor, h_brace, h_text)
        # self.slide_pause()
        self.remove(plane, stedgraf, axis_labels, tick_bgs, *ticks.values(), *tickmarks.values())
        return plane, stedgraf, axis_labels, ticks, tick_bgs, tickmarks

    def stedfunktion(self, exp_data):
        t_start, t, g, m, h_max, sigY, v0, s0, eps, t_done, t_slut = self._simulation_data()
        cmap = self._cmap()
        plane, stedgraf, axis_labels, ticks, tick_bgs, tickmarks = exp_data
        toppunkt = (-v0/g, stedgraf.underlying_function(-v0/g))
        self.add(plane, stedgraf, axis_labels, tick_bgs, *ticks.values(), *tickmarks.values())

        graph_rect = SurroundingRectangle(
            VGroup(Dot(plane.c2p(-1, 0.2)), Dot(plane.c2p(0, 0.2))), stroke_color=YELLOW,
            corner_radius=0.05
        )
        bundhoejde_tekst = VGroup(
            Tex(r"{Bolden} blev kastet").set_color_by_tex_to_color_map({"Bolden": ORANGE}),
            Tex(r"fra en h{\o}jde af"),
            DecimalNumber(
                stedgraf.underlying_function(-0.5), num_decimal_places=2, unit="~m",
                color=cmap["sted"]
            ).set_z_index(10)
        ).arrange(DOWN, aligned_edge=RIGHT).next_to(graph_rect, LEFT, aligned_edge=DOWN)
        point_tracker = ValueTracker(-0.5)
        tracker_point = always_redraw(lambda: Dot(
            plane.c2p(point_tracker.get_value(), stedgraf.underlying_function(point_tracker.get_value())),
            color=ORANGE, radius=0.1
        ))
        self.play(
            LaggedStart(
                Write(bundhoejde_tekst),
                AnimationGroup(
                    DrawBorderThenFill(graph_rect),
                    DrawBorderThenFill(tracker_point),
                ),
                lag_ratio=0.8
            ),
            run_time=1.5
        )
        self.slide_pause()

        self.play(
            FadeOut(graph_rect),
            run_time=0.25
        )
        # self.add(bundhoejde_tekst, graph_rect, tracker_point)
        # self.slide_pause()

        tophoejde_tekst = VGroup(
            Tex(r"og blev kastet"),
            Tex(r"op til en h{\o}jde af"),
            DecimalNumber(
                stedgraf.underlying_function(toppunkt[0]), num_decimal_places=2, unit="~m",
                color=cmap["sted"]
            ).set_z_index(10)
        ).arrange(DOWN, aligned_edge=RIGHT).next_to(bundhoejde_tekst, UP, aligned_edge=RIGHT, buff=3)
        # self.add(tophoejde_tekst)
        self.play(
            Write(tophoejde_tekst, run_time=1.0),
            point_tracker.animate.set_value(toppunkt[0]),
            run_time=2.0
        )
        self.slide_pause()

        forskel_hoejde = VGroup(
            BraceBetweenPoints(
                Dot(plane.c2p(toppunkt[0], s0)), Dot(plane.c2p(*toppunkt)), RIGHT, color=cmap["sted"]
            ).set_z_index(plane.get_z_index() + 2),
            DecimalNumber(
                stedgraf.underlying_function(toppunkt[0]), num_decimal_places=2, unit="~m", color=cmap["sted"]
            ).set_z_index(plane.get_z_index() + 2),
            MathTex("-").set_z_index(plane.get_z_index() + 2),
            DecimalNumber(
                s0, num_decimal_places=2, unit="~m", color=cmap["sted"]
            ).set_z_index(plane.get_z_index() + 2),
            MathTex("=").set_z_index(plane.get_z_index() + 2),
            DecimalNumber(
                stedgraf.underlying_function(toppunkt[0])-s0, num_decimal_places=2, unit="~m", color=cmap["sted"]
            ).set_z_index(plane.get_z_index() + 2),
        ).arrange(RIGHT).next_to(VGroup(Dot(plane.c2p(toppunkt[0], s0)), Dot(plane.c2p(*toppunkt))), RIGHT, buff=0)
        udregning_srect = SurroundingRectangle(
            forskel_hoejde[1:], stroke_width=0, fill_opacity=1, fill_color=DARKER_GRAY
        )

        self.camera.frame.save_state()
        self.play(
            self.camera.frame.animate.set(width=self.camera.frame.width * 1.1).shift(RIGHT),
            LaggedStart(
                FadeIn(udregning_srect),
                GrowFromPoint(forskel_hoejde[0], forskel_hoejde[0].get_start()),
                ReplacementTransform(tophoejde_tekst[-1].copy(), forskel_hoejde[1]),
                Write(forskel_hoejde[2]),
                ReplacementTransform(bundhoejde_tekst[-1].copy(), forskel_hoejde[3]),
                Write(forskel_hoejde[4:]),
                lag_ratio=0.25
            ),
            run_time=2.0
        )
        # self.add(forskel_hoejde, udregning_srect)
        # self.camera.frame.set(width=self.camera.frame.width * 1.1).shift(RIGHT)
        self.slide_pause()

        graftype_tekst = VGroup(
            Tex("Ved et lodret kast"),
            Tex("er grafen for"),
            Tex("stedfunktionen", color=cmap["sted"]),
            Tex("en {{parabel}}").set_color_by_tex_to_color_map({"parabel": cmap["sted"]}),
        ).scale(0.9).arrange(DOWN, aligned_edge=LEFT).next_to(plane, RIGHT, aligned_edge=UP)

        self.play(
            point_tracker.animate.set_value(t_start),
            self.camera.frame.animate.shift(4.5*RIGHT),
            LaggedStart(
                FadeIn(graftype_tekst, shift=0.25*LEFT),
                *[
                    FadeOut(m, shift=0.25*LEFT) for m in [
                        bundhoejde_tekst, tophoejde_tekst, *forskel_hoejde, udregning_srect,
                    ]
                ],
                lag_ratio=0.25
            ),
            run_time=2.0
        )
        # self.remove(udregning_srect, forskel_hoejde, bundhoejde_tekst, tophoejde_tekst)
        self.slide_pause()
        # self.camera.frame.shift(4.5*RIGHT)
        # self.add(graftype_tekst)

        self.play(
            FadeOut(graftype_tekst),
            run_time=0.25
        )
        # self.slide_pause()
        self.remove(plane, stedgraf, axis_labels, *ticks.values(), tick_bgs, *tickmarks.values(), tracker_point)
        # self.remove(graftype_tekst)
        return plane, stedgraf, axis_labels, ticks, tick_bgs, tickmarks, point_tracker, tracker_point, toppunkt

    def hastighedsfunktion(self, graf_data):
        t_start, t, g, m, h_max, sigY, v0, s0, eps, t_done, t_slut = self._simulation_data()
        cmap = self._cmap()
        sted_plane, sted_graf, sted_axis_labels, sted_ticks, sted_tick_bgs, sted_tickmarks, point_tracker, sted_tracker_point, sted_toppunkt = graf_data
        self.add(
            sted_plane, sted_graf, sted_axis_labels, *sted_ticks.values(), sted_tick_bgs,
            *sted_tickmarks.values(), sted_tracker_point,
        )

        hast_plane = NumberPlane(
            x_range=(t_start - eps, t_slut + eps + 0.25, 0.25),
            y_range=(-10 - eps, 10 + eps + 1, 1),
            x_length=4.5*2,
            y_length=7.5,
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
        ).next_to(sted_plane, RIGHT, buff=1)
        hast_axis_labels = VGroup(*[
            MathTex(
                lab, color=c, font_size=36
            ).move_to(hast_plane.c2p(coord)).set_z_index(hast_plane.get_z_index()+5)
            for lab, c, coord in zip(
                ["t~[s]", "v~[m/s]"], [cmap["tid"], cmap["hast"]], [(3, 1), (0.5, 9.5)]
            )
        ])
        hast_tickmarks = {
            "x": VGroup(*[Line(
                start=hast_plane.c2p(x, 0.2), end=hast_plane.c2p(x, -0.2), color=WHITE, stroke_width=0.75
            ) for x in np.arange(-1, 3.1, 0.5)]).set_z_index(4),
            "y": VGroup(*[Line(
                start=hast_plane.c2p(0.05, y), end=hast_plane.c2p(-0.05, y), color=WHITE, stroke_width=0.75
            ) for y in np.arange(-10, 10.1, 2)]).set_z_index(4),
        }
        hast_ticks = {
            "x": VGroup(*[DecimalNumber(
                number=x, num_decimal_places=1, include_sign=x < 0, color=cmap["tid"], font_size=24 if x != 0 else 0.01
            ).set_z_index(4).next_to(
                tm, DOWN, buff=0.2
            ) for x, tm in zip(np.arange(-1, 3.1, 0.5), hast_tickmarks["x"])]),
            "y": VGroup(*[DecimalNumber(
                number=y, num_decimal_places=1, include_sign=y < 0, color=cmap["hast"], font_size=24 if y != 0 else 0.01
            ).set_z_index(4).next_to(
                tm, LEFT, buff=0.2
            ) for y, tm in zip(np.arange(-10, 10.1, 2), hast_tickmarks["y"])]),
        }
        hast_tick_bgs = VGroup(
            *[
                SurroundingRectangle(
                m, stroke_width=0, fill_opacity=1, fill_color=DARKER_GRAY, buff=0.025
                ) for m in hast_ticks["x"]
            ],
            *[
                SurroundingRectangle(
                m, stroke_width=0, fill_opacity=1, fill_color=DARKER_GRAY, buff=0.025
                ) for m in hast_ticks["y"]
            ],
            *[
                SurroundingRectangle(
                m, stroke_width=0, fill_opacity=1, fill_color=DARKER_GRAY, buff=0.025
                ) for m in hast_axis_labels
            ]
        )
        self.play(
            self.camera.frame.animate.move_to(
                VGroup(sted_plane, hast_plane)
            ).set(
                # width=VGroup(sted_plane, hast_plane).width * 1.1
                width=hast_plane.width*1.2
            ),
            LaggedStart(
                DrawBorderThenFill(hast_plane),
                LaggedStart(
                    *[Write(l) for l in hast_axis_labels],
                    *[Create(l) for l in hast_tickmarks.values()],
                    *[Write(l) for l in hast_ticks.values()],
                    *[FadeIn(l) for l in hast_tick_bgs],
                    lag_ratio=0.1
                ),
                lag_ratio=0.5
            ),
            run_time=3
        )

        # self.camera.frame.move_to(
        #     VGroup(sted_plane, hast_plane)
        # ).set(
        #     width=VGroup(sted_plane, hast_plane).width * 1.1
        # )
        # self.add(hast_plane)
        # self.slide_pause()
        # self.add(hast_axis_labels, hast_tick_bgs, *hast_ticks.values(), *hast_tickmarks.values())
        self.slide_pause()

        # moving_tangent = always_redraw(lambda:
        #     sted_plane.get_secant_slope_group(
        #         x=point_tracker.get_value()-0.01,
        #         graph=sted_graf,
        #         dx=0.2,
        #         dx_line_color=cmap["tid"],
        #         dx_label=MathTex(r"\Delta t", color=cmap["tid"]),
        #         dy_line_color=cmap["sted"],
        #         dy_label=MathTex(r"\Delta s", color=cmap["sted"]),
        #         secant_line_color=cmap["hast"],
        #         secant_line_length=2
        #     )
        # )
        # self.add(moving_tangent)
        _dx = 0.1
        secant_points = always_redraw(lambda:
            VGroup(
                Dot(radius=0).move_to(
                    sted_plane.c2p(
                        point_tracker.get_value() - 0.5 * _dx,
                        sted_graf.underlying_function(point_tracker.get_value() - 0.5 * _dx)
                    )
                ),
                Dot(radius=0).move_to(
                    sted_plane.c2p(
                        point_tracker.get_value() + 0.5*_dx,
                        sted_graf.underlying_function(point_tracker.get_value() + 0.5*_dx)
                    )
                )
            )
        )
        secant_line = always_redraw(lambda:
            Line(
                start=secant_points[0].get_center(), end=secant_points[1].get_center(), color=cmap["hast"]
            ).scale(2)
        )
        comp_lines = always_redraw(lambda:
            VGroup(
                Line(
                    start=secant_points[0].get_center(),
                    end=sted_plane.c2p(point_tracker.get_value() + 0.5*_dx, sted_graf.underlying_function(point_tracker.get_value() - 0.5*_dx)),
                    color=cmap["tid"]
                ),
                Line(
                    start=sted_plane.c2p(point_tracker.get_value() + 0.5*_dx, sted_graf.underlying_function(point_tracker.get_value() - 0.5*_dx)),
                    end=secant_points[1].get_center(),
                    color=cmap["sted"]
                )
            )
        )

        haeldning_tekst = always_redraw(lambda:
            VGroup(
                Tex(r"H{\ae}ldning: "),
                DecimalNumber(
                    (sted_graf.underlying_function(point_tracker.get_value() + 0.5*_dx) - sted_graf.underlying_function(point_tracker.get_value() - 0.5*_dx))/_dx,
                    num_decimal_places=2, color=cmap["hast"], unit="m/s"
                )
            ).arrange(RIGHT, aligned_edge=DOWN).move_to(sted_plane.c2p(2.5, 4))
        )
        self.play(
            LaggedStart(
                DrawBorderThenFill(secant_points),
                *[Create(cl) for cl in comp_lines],
                Create(secant_line),
                Write(haeldning_tekst),
                lag_ratio=0.5
            ),
            run_time=2
        )
        self.remove(secant_points, comp_lines, secant_line)
        self.add(secant_points, secant_line, comp_lines)
        # self.slide_pause()
        # self.add(haeldning_tekst)
        self.slide_pause()

        # self.camera.frame.move_to(sted_plane).set(width=sted_plane.width)
        # self.play(
        #     point_tracker.animate.set_value(t_slut),
        #     run_time=10,
        #     rate_func=linear,
        # )
        # self.slide_pause()
        point_tracker.set_value(-1)

        def hast_raw(time, a=g, v=v0):
            return a * time + v

        def _hast(time, a=g, v=v0, limits=(0, t_done)):
            return hast_raw(time, a=a, v=v) if limits[0] < time < limits[1] else 0

        def hast(time, a=g, v=v0, limits=(0, t_done), _width=0.05):
            # return np.convolve(time, _sted(time, a=a, v=v, s=s), mode="valid")
            # return np.mean([_hast(t, a=a, v=v, limits=limits) for t in np.linspace(time-0.5*_width, time+0.5*_width, 21)])
            return (sted_graf.underlying_function(time + 0.5*_dx) - sted_graf.underlying_function(time - 0.5*_dx))/_dx
            # return ((sted_graf.underlying_function(_x+0.5*_dx) - sted_graf.underlying_function(_x-0.5*_dx))/_dx + 0*time for _x in np.linspace(t_start, t_slut, 500))

        def hast_measured(time, a=g, v=v0):
            return hast(time, a=a, v=v) + random.gauss(mu=0.0, sigma=sigY)

        hast_graf = always_redraw(lambda:
            hast_plane.plot(
                lambda x: hast(x),
                color=cmap["hast"],
                x_range=[t_start, t.get_value()]
            )
        )
        t.set_value(t_start)
        self.add(hast_graf)
        # self.slide_pause()

        self.play(
            point_tracker.animate.set_value(t_slut),
            t.animate.set_value(t_slut),
            run_time=10,
            rate_func=linear,
        )
        self.slide_pause()

        graftype_tekst = VGroup(
            Tex("Ved et lodret kast"),
            Tex("er grafen for"),
            Tex("hastighedsfunktionen", color=cmap["hast"]),
            Tex("en {{lineær}} graf").set_color_by_tex_to_color_map({"lineær": cmap["hast"]}),
        ).scale(0.9).arrange(DOWN, aligned_edge=LEFT).next_to(hast_plane, RIGHT, aligned_edge=UP)

        self.play(
                self.camera.frame.animate.move_to(hast_plane).set(height=1.05 * hast_plane.height).shift(2 * RIGHT),
            LaggedStart(
                *[
                    FadeOut(m, shift=0.25*LEFT) for m in (
                        haeldning_tekst, secant_line, comp_lines, secant_points, sted_tracker_point,
                        *sted_tickmarks.values(), *sted_ticks.values(), sted_tick_bgs, sted_axis_labels, sted_graf,
                        sted_plane
                    )
                ],
                FadeIn(graftype_tekst, shift=0.25*LEFT),
                lag_ratio=0.05
            ),
            run_time=4
        )
        # self.remove(
        #     sted_plane, sted_graf, sted_axis_labels, *sted_ticks.values(), sted_tick_bgs,
        #     *sted_tickmarks.values(), sted_tracker_point, secant_points, secant_line, comp_lines, haeldning_tekst
        # )
        # self.slide_pause()
        # self.camera.frame.move_to(hast_plane).set(height=1.05*hast_plane.height).shift(2*RIGHT)
        # self.slide_pause()
        # self.add(graftype_tekst)
        self.slide_pause()

        self.play(
            FadeOut(graftype_tekst, shift=0.25*LEFT),
            run_time=0.25
        )

        self.remove(
            hast_plane, hast_graf, hast_axis_labels, *hast_ticks.values(),
            *hast_tickmarks.values(), hast_tick_bgs
        )
        # self.slide_pause()
        return hast_plane, hast_graf, hast_axis_labels, hast_ticks, hast_tickmarks, hast_tick_bgs, point_tracker

    def accelerationsfunktion(self, graf_data):
        t_start, t, g, m, h_max, sigY, v0, s0, eps, t_done, t_slut = self._simulation_data()
        cmap = self._cmap()
        hast_plane, hast_graf, hast_axis_labels, hast_ticks, hast_tickmarks, hast_tick_bgs, point_tracker = graf_data
        self.add(
            hast_plane, hast_graf, hast_axis_labels, *hast_ticks.values(), *hast_tickmarks.values(), hast_tick_bgs
        )

        acc_plane = NumberPlane(
            x_range=(t_start - eps, t_slut + eps + 0.25, 0.25),
            y_range=(-10 - eps, 10 + eps + 1, 1),
            x_length=4.5*2,
            y_length=7.5,
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
        ).next_to(hast_plane, RIGHT, buff=1)
        acc_axis_labels = VGroup(*[
            MathTex(
                lab, color=c, font_size=36
            ).move_to(acc_plane.c2p(coord)).set_z_index(acc_plane.get_z_index()+5)
            for lab, c, coord in zip(
                ["t~[s]", "a~[m/s^2]"], [cmap["tid"], cmap["acc"]], [(3, 1), (0.5, 9.5)]
            )
        ])
        acc_tickmarks = {
            "x": VGroup(*[Line(
                start=acc_plane.c2p(x, 0.2), end=acc_plane.c2p(x, -0.2), color=WHITE, stroke_width=0.75
            ) for x in np.arange(-1, 3.1, 0.5)]).set_z_index(4),
            "y": VGroup(*[Line(
                start=acc_plane.c2p(0.05, y), end=acc_plane.c2p(-0.05, y), color=WHITE, stroke_width=0.75
            ) for y in np.arange(-10, 10.1, 2)]).set_z_index(4),
        }
        acc_ticks = {
            "x": VGroup(*[DecimalNumber(
                number=x, num_decimal_places=1, include_sign=x < 0, color=cmap["tid"], font_size=24 if x != 0 else 0.01
            ).set_z_index(4).next_to(
                tm, DOWN, buff=0.2
            ) for x, tm in zip(np.arange(-1, 3.1, 0.5), acc_tickmarks["x"])]),
            "y": VGroup(*[DecimalNumber(
                number=y, num_decimal_places=1, include_sign=y < 0, color=cmap["acc"], font_size=24 if y != 0 else 0.01
            ).set_z_index(4).next_to(
                tm, LEFT, buff=0.2
            ) for y, tm in zip(np.arange(-10, 10.1, 2), acc_tickmarks["y"])]),
        }
        acc_tick_bgs = VGroup(
            *[
                SurroundingRectangle(
                m, stroke_width=0, fill_opacity=1, fill_color=DARKER_GRAY, buff=0.025
                ) for m in acc_ticks["x"]
            ],
            *[
                SurroundingRectangle(
                m, stroke_width=0, fill_opacity=1, fill_color=DARKER_GRAY, buff=0.025
                ) for m in acc_ticks["y"]
            ],
            *[
                SurroundingRectangle(
                m, stroke_width=0, fill_opacity=1, fill_color=DARKER_GRAY, buff=0.025
                ) for m in acc_axis_labels
            ]
        )
        self.play(
            self.camera.frame.animate.move_to(
                VGroup(hast_plane, acc_plane)
            ).set(
                # width=VGroup(hast_plane, acc_plane).width * 1.1
                width=hast_plane.width*1.2
            ),
            LaggedStart(
                DrawBorderThenFill(acc_plane),
                LaggedStart(
                    *[Write(l) for l in acc_axis_labels],
                    *[Create(l) for l in acc_tickmarks.values()],
                    *[Write(l) for l in acc_ticks.values()],
                    *[FadeIn(l) for l in acc_tick_bgs],
                    lag_ratio=0.1
                ),
                lag_ratio=0.5
            ),
            run_time=3
        )
        # self.camera.frame.move_to(
        #     VGroup(hast_plane, acc_plane)
        # ).set(
        #     width=VGroup(hast_plane, acc_plane).width * 1.0
        # )
        # self.add(acc_plane)
        # self.slide_pause()
        # self.add(acc_axis_labels, acc_tick_bgs, *acc_ticks.values(), *acc_tickmarks.values())
        self.slide_pause()

        _dx = 0.1
        point_tracker.set_value(-1)
        secant_points = always_redraw(lambda:
            VGroup(
                Dot(radius=0).move_to(
                    hast_plane.c2p(
                        point_tracker.get_value() - 0.5 * _dx,
                        hast_graf.underlying_function(point_tracker.get_value() - 0.5 * _dx)
                    )
                ),
                Dot(radius=0).move_to(
                    hast_plane.c2p(
                        point_tracker.get_value() + 0.5*_dx,
                        hast_graf.underlying_function(point_tracker.get_value() + 0.5*_dx)
                    )
                )
            )
        )
        secant_line = always_redraw(lambda:
            Line(
                start=secant_points[0].get_center(), end=secant_points[1].get_center(), color=cmap["acc"]
            ).scale(2)
        )
        comp_lines = always_redraw(lambda:
            VGroup(
                Line(
                    start=secant_points[0].get_center(),
                    end=hast_plane.c2p(point_tracker.get_value() + 0.5*_dx, hast_graf.underlying_function(point_tracker.get_value() - 0.5*_dx)),
                    color=cmap["tid"]
                ),
                Line(
                    start=hast_plane.c2p(point_tracker.get_value() + 0.5*_dx, hast_graf.underlying_function(point_tracker.get_value() - 0.5*_dx)),
                    end=secant_points[1].get_center(),
                    color=cmap["hast"]
                )
            )
        )

        haeldning_tekst = always_redraw(lambda:
            VGroup(
                Tex(r"H{\ae}ldning: "),
                DecimalNumber(
                    (hast_graf.underlying_function(point_tracker.get_value() + 0.5*_dx) - hast_graf.underlying_function(point_tracker.get_value() - 0.5*_dx))/_dx,
                    num_decimal_places=2, color=cmap["acc"], unit="m/s^2"
                )
            ).arrange(RIGHT, aligned_edge=DOWN).move_to(hast_plane.c2p(2.5, 4))
        )
        self.play(
            LaggedStart(
                DrawBorderThenFill(secant_points),
                *[Create(cl) for cl in comp_lines],
                Create(secant_line),
                Write(haeldning_tekst),
                lag_ratio=0.5
            ),
            run_time=2
        )
        self.remove(secant_points, secant_line, comp_lines)
        self.add(secant_points, secant_line, comp_lines)
        # self.slide_pause()
        # self.add(haeldning_tekst)
        self.slide_pause()

        # self.camera.frame.move_to(hast_plane).set(width=hast_plane.width)
        # self.play(
        #     point_tracker.animate.set_value(t_slut),
        #     run_time=10,
        #     rate_func=linear,
        # )
        # self.slide_pause()
        # point_tracker.set_value(-1)

        def acc_raw(time, a=g):
            return a + 0*time

        def _acc(time, a=g, limits=(0, t_done)):
            return acc_raw(time, a=a) if limits[0] < time < limits[1] else 0

        def acc(time, a=g, limits=(0, t_done), _width=0.05):
            # return np.mean([_acc(t, a=a, limits=limits) for t in np.linspace(time-0.5*_width, time+0.5*_width, 21)])
            return np.min([(hast_graf.underlying_function(time + 0.5*_dx) - hast_graf.underlying_function(time - 0.5*_dx))/_dx, 10])

        acc_graf = always_redraw(lambda:
            acc_plane.plot(
                lambda x: acc(x),
                color=cmap["acc"],
                x_range=[t_start, t.get_value()]
            )
        )
        t.set_value(t_start)
        self.add(acc_graf)
        # self.slide_pause()

        self.play(
            point_tracker.animate.set_value(t_slut),
            t.animate.set_value(t_slut),
            run_time=10,
            rate_func=linear,
        )
        self.slide_pause()

        graftype_tekst = VGroup(
            Tex("Ved et lodret kast"),
            Tex("er grafen for"),
            Tex("accelerationsfunktionen", color=cmap["acc"]),
            Tex("en {{konstant}} graf").set_color_by_tex_to_color_map({"konstant": cmap["acc"]}),
        ).scale(0.85).arrange(DOWN, aligned_edge=LEFT).next_to(acc_plane, RIGHT, aligned_edge=UP)

        self.play(
            self.camera.frame.animate.move_to(acc_plane).set(height=1.05 * acc_plane.height).shift(2 * RIGHT),
            LaggedStart(
                *[
                    FadeOut(m, shift=0.25*LEFT) for m in (
                        haeldning_tekst, secant_line, comp_lines, secant_points, hast_tick_bgs, *hast_tickmarks.values(),
                        *hast_ticks.values(), hast_axis_labels, hast_graf, hast_plane
                    )
                ],
                FadeIn(graftype_tekst, shift=0.25*LEFT),
                lag_ratio=0.05
            ),
            run_time=4
        )
        # self.remove(
        #     hast_plane, hast_graf, hast_axis_labels, *hast_ticks.values(), *hast_tickmarks.values(),
        #     hast_tick_bgs, secant_points, secant_line, comp_lines, haeldning_tekst
        # )
        # self.slide_pause()
        # self.camera.frame.move_to(acc_plane).set(height=1.05*acc_plane.height).shift(2*RIGHT)
        # self.slide_pause()
        # self.add(graftype_tekst)
        self.slide_pause()

        opgave = Tex(
            r"Hvordan kan den kaldes\\", "konstant", r"\\når den svinger så meget?"
        ).scale(0.75).arrange(DOWN, aligned_edge=LEFT).next_to(
            graftype_tekst, DOWN, aligned_edge=LEFT, buff=3
        )
        opgave[1].set_color(cmap["acc"])
        opgave_srec = get_background_rect(opgave, stroke_colour=cmap["acc"], fill_color=cmap["acc"], fill_opacity=0.1)
        self.play(
            FadeIn(opgave, shift=0.5*DOWN),
            FadeIn(opgave_srec, shift=0.5*DOWN)
        )
        self.slide_pause()

        # self.play(
        #     LaggedStart(
        #         *[
        #             FadeOut(m, shift=0.25*LEFT) for m in (
        #
        #             )
        #         ]
        #     )
        # )
        self.play(
            *[FadeOut(m, shift=0.25*LEFT) for m in (graftype_tekst, opgave, opgave_srec)],
            run_time=0.5
        )

        self.remove(
            hast_plane, hast_graf, hast_axis_labels, *hast_ticks.values(),
            *hast_tickmarks.values(), hast_tick_bgs
        )
        # self.slide_pause()
        return acc_plane, acc_graf, acc_axis_labels, acc_ticks, acc_tickmarks, acc_tick_bgs

    def opsamling(self, sted_data, hast_data, acc_data):
        t_start, t, g, m, h_max, sigY, v0, s0, eps, t_done, t_slut = self._simulation_data()
        sted_plane, sted_graf, sted_axis_labels, sted_ticks, sted_tick_bgs, sted_tickmarks, _, _, _ = sted_data
        hast_plane, hast_graf, hast_axis_labels, hast_ticks, hast_tickmarks, hast_tick_bgs, _ = hast_data
        acc_plane, acc_graf, acc_axis_labels, acc_ticks, acc_tickmarks, acc_tick_bgs = acc_data
        cmap = self._cmap()

        opsamlings_tekst = Tex("Opsamling", font_size=75).set_z_index(10).move_to(self.camera.frame.get_center())
        opsamlings_rect = get_background_rect(
            opsamlings_tekst, buff=14, fill_color=DARKER_GRAY, fill_opacity=1, stroke_width=0
        )
        self.play(
            LaggedStart(
                FadeIn(opsamlings_rect),
                Write(opsamlings_tekst),
                lag_ratio=0.8
            ),
            run_time=1
        )
        self.remove(acc_graf, acc_axis_labels, *acc_ticks.values(), *acc_tickmarks.values(), acc_tick_bgs, acc_plane)
        self.slide_pause()

        sted_gruppe = VGroup(
            sted_plane, sted_graf, sted_axis_labels, *sted_ticks.values(), sted_tick_bgs, *sted_tickmarks.values()
        ).move_to(sted_plane)
        hast_gruppe = VGroup(
            hast_plane, hast_graf, hast_axis_labels, *hast_ticks.values(), hast_tick_bgs, *hast_tickmarks.values()
        ).move_to(hast_plane)
        acc_gruppe = VGroup(
            acc_plane, acc_graf, acc_axis_labels, *acc_ticks.values(), acc_tick_bgs, *acc_tickmarks.values()
        ).move_to(acc_plane)

        alle_grupper = VGroup(
            sted_gruppe, hast_gruppe, acc_gruppe
        ).arrange(RIGHT, buff=1).next_to(acc_plane, LEFT, buff=-acc_plane.width)

        x_top = -v0/g
        highlight_areas = VGroup(
            *[
                VGroup(
                    DashedLine(start=plane.c2p(x_top-0.9, y1), end=plane.c2p(x_top-0.9, y2)).set_z_index(15),
                    DashedLine(start=plane.c2p(x_top+0.9, y1), end=plane.c2p(x_top+0.9, y2)).set_z_index(15),
                ) for plane, y1, y2 in zip(
                    (sted_plane, hast_plane, acc_plane), (-2, -12, -12), (7, 12, 12)
                )
            ]
        )
        dimmed_zones = VGroup(
            *[
                Rectangle(
                    width=VGroup(highlight_areas[0][1], highlight_areas[1][0]).width,
                    height=VGroup(highlight_areas[0][1], highlight_areas[1][0]).height,
                    fill_color=DARKER_GRAY, fill_opacity=0.75, stroke_width=0
                ).set_z_index(15) for _ in range(4)
            ]
        )
        dimmed_zones[0].next_to(highlight_areas[0][0], LEFT, buff=0)
        dimmed_zones[1].move_to(between_mobjects(highlight_areas[0][1], highlight_areas[1][0]))
        dimmed_zones[2].move_to(between_mobjects(highlight_areas[1][1], highlight_areas[2][0]))
        dimmed_zones[3].next_to(highlight_areas[2][1], RIGHT, buff=0)

        self.remove(*[m for m in self.mobjects if m not in (opsamlings_tekst, opsamlings_rect)])

        self.play(
            *[FadeOut(m, shift=2*RIGHT) for m in (opsamlings_tekst, opsamlings_rect)]
        )
        self.camera.frame.set(width=alle_grupper.width * 1.05).move_to(alle_grupper).shift(4*DOWN)

        # VGroup(sted_gruppe, hast_gruppe).arrange(RIGHT, buff=1).next_to(acc_gruppe, LEFT, buff=1)

        # self.add(sted_gruppe, hast_gruppe)
        # self.play(
        #     # *[
        #     #     ReplacementTransform(m1, m2) for m1, m2 in zip(
        #     #         (acc_plane, acc_graf, acc_axis_labels, *acc_ticks.values(), acc_tick_bgs, *acc_tickmarks.values()),
        #     #         acc_gruppe
        #     #     )
        #     # ],
        #     # VGroup(
        #     #     sted_gruppe, hast_gruppe, acc_gruppe
        #     # ).animate.arrange(RIGHT, aligned_edge=DOWN, buff=1),
        #     self.camera.frame.animate.set(width=hast_gruppe.width*3).move_to(alle_grupper).shift(4*DOWN),
        #     run_time=5
        # )
        self.play(
            *[FadeIn(m, shift=1*d) for m, d in zip((sted_gruppe, hast_gruppe, acc_gruppe), (RIGHT, DOWN, LEFT))],
            run_time=1
        )
        self.slide_pause()

        self.play(
            LaggedStart(
                AnimationGroup(*[Create(l) for l in highlight_areas]),
                AnimationGroup(*[FadeIn(r) for r in dimmed_zones]),
                lag_ratio=0.75
            ),
            run_time=2
        )
        self.slide_pause()

        sammenh_tekst = VGroup(
            Tex("{{Sted}} vs. {{tid}}", font_size=60).set_color_by_tex_to_color_map(cmap).next_to(sted_gruppe, DOWN, buff=2),
            Tex("{{Hastighed}} vs. {{tid}}", font_size=60).set_color_by_tex_to_color_map(cmap).next_to(hast_gruppe, DOWN, buff=2),
            Tex("{{Acceleration}} vs. {{tid}}", font_size=60).set_color_by_tex_to_color_map(cmap).next_to(acc_gruppe, DOWN, buff=2),
        )
        graftype_tekst = VGroup(
            Tex("Parabel", color=cmap["sted"], font_size=60).next_to(sammenh_tekst[0], DOWN, buff=2),
            Tex("Lineær", color=cmap["hast"], font_size=60).next_to(sammenh_tekst[1], DOWN, buff=2),
            Tex("Konstant", color=cmap["acc"], font_size=60).next_to(sammenh_tekst[2], DOWN, buff=2),
        )
        samlet = Tex(r"Lodret kast er et forsøg med ", "konstant acceleration", font_size=60).next_to(graftype_tekst, DOWN, buff=2)
        samlet[-1].set_color(cmap["acc"])
        self.play(
            LaggedStart(
                *[
                    FadeIn(t, shift=0.5*DOWN) for t in sammenh_tekst
                ],
                lag_ratio=0.8
            ),
            run_time=1
        )
        self.slide_pause()

        self.play(
            LaggedStart(
                *[
                    FadeIn(t, shift=0.5 * DOWN) for t in graftype_tekst
                ],
                lag_ratio=0.8
            ),
            run_time=1
        )
        self.slide_pause()
        self.play(
            FadeIn(samlet),
            run_time=1
        )
        self.slide_pause()

        self.play(
            LaggedStart(
                *[
                    FadeOut(m, shift=np.random.uniform()*UP+np.random.uniform()*RIGHT) for m in self.mobjects
                ],
                lag_ratio=0.1
            ),
            run_time=1
        )

class LodretKastThumbnail(LodretKast):
    def construct(self):
        cmap = self._cmap()
        t_start, t, g, m, h_max, sigY, v0, s0, eps, t_done, t_slut = self._simulation_data()
        t.set_value(0.5)
        sensor = VGroup(
            Rectangle(
                width=4, height=0.25, stroke_width=0.25, fill_opacity=1, fill_color=LIGHT_GRAY
            ),
        ).to_edge(DL)
        svg_path = r"..\SVGs\basketball.svg"
        ball = SVGMobject(svg_path).scale(0.75).next_to(sensor, UP, buff=s0, aligned_edge=LEFT)
        ball.move_to(ball.get_center() + (0.5*g*t.get_value()**2 + v0*t.get_value() + s0) * UP)
        ball_lowest_point = DashedLine(start=ball.get_bottom()+0.75*LEFT, end=ball.get_bottom()+1.5*RIGHT, color=LIGHT_GRAY)
        h_brace = BraceBetweenPoints(
            point_1=sensor.get_top(),
            point_2=ball.get_bottom(),
            direction=RIGHT,
            color=cmap["sted"]
        )
        h_text = DecimalNumber(
            0.5*g*t.get_value()**2 + v0*t.get_value() + s0,
            num_decimal_places=2,
            include_sign=False,
            color=cmap["sted"],
            unit=" m"
        ).next_to(h_brace, RIGHT)
        self.add(sensor, ball, ball_lowest_point, h_brace, h_text)

        plane = NumberPlane(
            x_range=(t_start-eps, t_slut+eps+0.25, 0.25),
            y_range=(-1-eps, 6+eps+0.5, 0.5),
            x_length=4.5*2,
            y_length=7.5,
            background_line_style={
                "stroke_color": LIGHTER_GRAY,
                "stroke_width": 1,
                "stroke_opacity": 0.3,
            },
            axis_config={
                # "include_ticks": True,
                "include_tip": True,
                "tip_shape": StealthTip,
                "tip_width": 0.2,
                "tip_height": 0.2
            },
        ).to_edge(RIGHT, buff=0.1)
        axis_labels = VGroup(*[
            MathTex(
                lab, color=c, font_size=36
            ).move_to(plane.c2p(coord)).set_z_index(plane.get_z_index()+5)
            for lab, c, coord in zip(
                ["t~[s]", "s~[m]"], [cmap["tid"], cmap["sted"]], [(3, 0.25), (0.25, 6.25)]
            )
        ])
        tickmarks = {
            "x": VGroup(*[Line(
                start=plane.c2p(x, 0.1), end=plane.c2p(x, -0.1), color=WHITE, stroke_width=0.75
            ) for x in np.arange(-1, 3.1, 0.5)]).set_z_index(4),
            "y": VGroup(*[Line(
                start=plane.c2p(0.05, y), end=plane.c2p(-0.05, y), color=WHITE, stroke_width=0.75
            ) for y in np.arange(-1, 6.1, 1)]).set_z_index(4),
        }
        ticks = {
            "x": VGroup(*[DecimalNumber(
                number=x, num_decimal_places=1, include_sign=x < 0, color=cmap["tid"], font_size=24 if x != 0 else 0.01
            ).set_z_index(4).next_to(
                tm, DOWN, buff=0.2
            ) for x, tm in zip(np.arange(-1, 3.1, 0.5), tickmarks["x"])]),
            "y": VGroup(*[DecimalNumber(
                number=y, num_decimal_places=1, include_sign=y < 0, color=cmap["sted"], font_size=24 if y != 0 else 0.01
            ).set_z_index(4).next_to(
                tm, LEFT, buff=0.2
            ) for y, tm in zip(np.arange(-1, 6.1, 1), tickmarks["y"])]),
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
        stedgraf = plane.plot(
            lambda x: np.max([0, 0.5*g*x**2 + v0*x + s0]),
            color=cmap["sted"],
            x_range=[t_start, t_slut]
        )
        ball_dot = Dot(fill_color=ORANGE).move_to(plane.c2p(t.get_value(), stedgraf.underlying_function(t.get_value())))
        self.add(plane, stedgraf, *tickmarks.values(), *ticks.values(), ball_dot)

        overskrift = Tex("Det lodrette kast", font_size=60).to_edge(UL)
        overskrift_boks = get_background_rect(overskrift, stroke_colour=GREEN)
        VGroup(overskrift, overskrift_boks).to_edge(UL, buff=0.05)
        self.add(overskrift, overskrift_boks)


if __name__ == "__main__":
    classes = [
        LodretKast,
        # LodretKastThumbnail
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