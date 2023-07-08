from manim import *
import sys
sys.path.append("../")
from helpers import *
import numpy as np
import math

slides = False
if slides:
    from manim_slides import Slide


class ToPunkt(Slide if slides else Scene):
    def construct(self):
        self.to_punkt()
        self.slide_pause(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def to_punkt(self):
        scene_marker("To-punkt-formel")
        plane = NumberPlane(
            x_range=[-1, 16, 1],
            y_range=[-1, 9, 1],
            x_length=17,
            y_length=10,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.4
            }
        ).scale(0.35).to_edge(UL, buff=0.1)
        plane_box = get_background_rect(plane, buff=0, stroke_colour=TEAL)
        plane_group = VGroup(plane, plane_box)
        self.play(
            # DrawBorderThenFill(plane),
            # Create(plane_box)
            DrawBorderThenFill(plane_group)
        )
        self.slide_pause(0.5)

        p1col, p2col = RED, BLUE
        acol, bcol = PURPLE, GREEN

        x1, x2 = ValueTracker(2), ValueTracker(13)
        y1, y2 = ValueTracker(1), ValueTracker(7)
        points = always_redraw(lambda: VGroup(
            *[
                Dot(
                    plane.c2p(x, y),
                    color=col
                ) for x, y, col in zip(
                    (x1.get_value(), x2.get_value()),
                    (y1.get_value(), y2.get_value()),
                    (p1col, p2col)
                )
            ]
        ))
        point_coords = VGroup(
            MathTex(r"(x_1; y_1)").next_to(points[0], DR, buff=0.1),
            MathTex(r"(x_2; y_2)").next_to(points[1], UL, buff=0.1),
        )
        self.add(point_coords)
        point_eqs = VGroup(
            MathTex(r"y_1", "=", "b", r"\cdot", r"x_1", r"{^a}"),
            MathTex(r"y_2", "=", "b", r"\cdot", r"x_2", r"{^a}"),
        ).arrange(DOWN).to_edge(UR).scale(0.75)
        for eq, pcol in zip(point_eqs, (p1col, p2col)):
            eq[0].set_color(pcol)
            eq[2].set_color(bcol)
            eq[4].set_color(pcol)
            eq[5].set_color(acol)

        for point, peq in zip(points, point_eqs):
            self.play(
                Create(point),
                Write(peq),
                run_time=0.75
            )
            self.slide_pause(0.1)

        # self.play(
        #     plane_group.animate.scale(0.5).to_edge(UL),
        #     point_eqs[0].animate.scale(0.75).to_edge(UR),
        #     point_eqs[1].animate.scale(0.75).to_edge(UR).shift(0.5*DOWN),
        #     run_time=1
        # )
        # self.slide_pause()
