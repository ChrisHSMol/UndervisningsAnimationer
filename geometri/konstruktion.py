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


class KonstruktionSSS(MovingCameraScene, Slide if slides else Scene):
    def construct(self):
        self.konstruktionSSS()
        self.slide_pause(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def get_cmap(self):
        return {"a": GREEN, "b": BLUE, "c": RED}

    def Range(self, in_val, end_val, step=1):
        return list(np.arange(in_val, end_val + step, step))

    def get_coord_from_proportion(self, vmob,proportion):
        return vmob.point_from_proportion(proportion)

    def get_points_from_curve(self, vmob, dx=0.005):
        coords = []
        for point in self.Range(0, 1, dx):
            dot = Dot(self.get_coord_from_proportion(vmob,point))
            coords.append(dot.get_center())
        return coords

    def get_norm(self, coord1, coord2):
        dim = min((len(coord1), len(coord2)))
        s = 0
        for c1, c2 in zip(coord1, coord2):
            s += (c2 - c1)**2
        s = s**(1/dim)
        return s

    def get_intersections_between_two_vmobs(
            self, vmob1, vmob2,
            tolerance=0.15,
            radius_error=0.2,
            use_average=True,
            use_first_vmob_reference=False
    ):
        coords_1 = self.get_points_from_curve(vmob1)
        coords_2 = self.get_points_from_curve(vmob2)
        intersections = []
        for coord_1 in coords_1:
            for coord_2 in coords_2:
                distance_between_points = self.get_norm(coord_1, coord_2)
                if use_average:
                    coord_3 = (coord_2 - coord_1) / 2
                    average_point = coord_1 + coord_3
                else:
                    if use_first_vmob_reference:
                        average_point = coord_1
                    else:
                        average_point = coord_2
                if len(intersections) > 0 and distance_between_points < tolerance:
                    last_intersection=intersections[-1]
                    distance_between_previous_point = self.get_norm(average_point, last_intersection)
                    if distance_between_previous_point > radius_error:
                        intersections.append(average_point)
                if len(intersections) == 0 and distance_between_points < tolerance:
                    intersections.append(average_point)
        return intersections

    def get_top_intersect(self, intersections):
        return intersections[0] if intersections[0][1] > intersections[1][1] else intersections[1]

    def konstruktionSSS(self):
        cmap = self.get_cmap()
        a, b, c = 4, 2, 5
        points = VGroup(
            Dot(stroke_width=0),
            Dot(stroke_width=0).move_to((c, 0, 0)),
            # Dot(fill_color=cmap["c"], stroke_width=0).move_to((np.cos)),
        )
        point_labels = VGroup(
            Tex("A").next_to(points[0], LEFT),
            Tex("B").next_to(points[1], RIGHT)
        )
        lines = VGroup(
            Line(start=points[0], end=points[1], stroke_color=cmap["c"])
        )
        line_labels = VGroup(
            Tex("c", color=cmap["c"]).next_to(lines[0], DOWN)
        )
        circles = VGroup(
            Circle(radius=a, stroke_color=cmap["a"]).move_to(points[1]),
            Circle(radius=b, stroke_color=cmap["b"]).move_to(points[0])
        )
        self.camera.frame.save_state()
        self.camera.frame.move_to(circles)
        # self.add(points, point_labels)
        self.play(
            DrawBorderThenFill(points[0]),
            Write(point_labels[0])
        )
        self.slide_pause(_ONEFRAME)
        self.play(
            Create(lines[0]),
            Write(line_labels[0])
        )
        # self.add(lines, line_labels)
        self.slide_pause(_ONEFRAME)
        self.play(
            DrawBorderThenFill(points[1]),
            Write(point_labels[1])
        )
        self.slide_pause(_ONEFRAME)

        self.play(
            LaggedStart(
                *[GrowFromCenter(circle) for circle in circles],
                lag_ratio=0.9
            )
        )
        # self.add(circles)
        self.slide_pause(_ONEFRAME)

        points.add(
            # line_intersection(circles[0], circles[1])
            points[0].copy().move_to(
                self.get_top_intersect(self.get_intersections_between_two_vmobs(circles[0], circles[1]))
            )
        )
        point_labels.add(
            Tex("C").next_to(points[-1], UP)
        )
        # self.add(points[-1], point_labels[-1])
        self.play(
            DrawBorderThenFill(points[2]),
            Write(point_labels[2])
        )
        self.slide_pause(_ONEFRAME)

        lines.add(
            Line(start=points[0], end=points[-1], stroke_color=cmap["b"])
        )
        lines.add(
            Line(start=points[1], end=points[-1], stroke_color=cmap["a"])
        )
        # self.add(lines[-2:])
        self.play(
            LaggedStart(
                *[Create(line) for line in lines[-2:]],
                lag_ratio=0.9
            )
        )
        self.slide_pause(_ONEFRAME)

        line_labels.add(
            Tex("b", color=cmap["b"]).move_to(lines[-2]).rotate(
                lines[-2].get_angle()
                # np.arctan(
                #     (lines[-2].get_end()[1] - lines[-2].get_start()[1]) / (lines[-2].get_end()[0] - lines[-2].get_start()[0])
                # )
            ).shift(0.3*UL)
        )
        line_labels.add(
            Tex("a", color=cmap["a"]).move_to(lines[-1]).rotate(
                lines[-1].get_angle() + PI
                # np.arctan(
                #     (lines[-1].get_end()[1] - lines[-1].get_start()[1]) / (lines[-1].get_end()[0] - lines[-1].get_start()[0])
                # )
            ).shift(0.3*UP)
        )
        # self.add(line_labels[-2:])
        self.play(
            LaggedStart(
                *[Write(line_label) for line_label in line_labels[-2:]],
                lag_ratio=0.9
            )
        )
        self.slide_pause(_ONEFRAME)


if __name__ == "__main__":
    classes = [
        KonstruktionSSS
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

