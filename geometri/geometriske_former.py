from manim import *
import sys
sys.path.append("../")
from helpers import *
import subprocess
import random

slides = False
if slides:
    from manim_slides import Slide


q = "ul"
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


class GeometriskUdvikling(ThreeDScene, Slide if slides else Scene):
    btransparent = False

    def construct(self):
        self.dimensionel_udvikling()
        self.wait(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t=t, slides_bool=slides_bool)

    def dimensionel_udvikling(self):
        points = VGroup(*[
            Dot3D(color=c).set_z_index(2-i) for i, c in enumerate([GREEN, RED])
        ])
        # trace = TracedPath(points[1].get_center).set(color=color_gradient([RED, GREEN], 5)).set_z_index(0)
        trace = always_redraw(
            lambda: Line(start=points[0], end=points[1], stroke_color=color_gradient([RED, GREEN], 5)).set_z_index(0)
        )
        self.add(points[0], trace)
        self.slide_pause()
        self.play(
            points[0].animate.shift(LEFT),
            points[1].animate.shift(RIGHT)
        )
        pointline = VGroup(
            *[point.copy() for point in points],
            Line(start=points[0], end=points[1], stroke_color=color_gradient([RED, GREEN], 5)).set_z_index(0)
        )
        self.remove(*[m for m in self.mobjects])
        self.add(pointline)

        _pointline = pointline.copy()
        sqlines = always_redraw(
            lambda: VGroup(*[
                Line(
                    start=pointline[i], end=_pointline[i], stroke_color=pointline[i].get_color()
                ).set_z_index(0) for i in range(2)
            ])
        )
        self.add(sqlines)
        self.play(
            pointline.animate.shift(DOWN),
            _pointline.animate.shift(UP)
        )

        square = VGroup(
            *[side.copy() for side in [*pointline, *_pointline, *sqlines]]
        )
        self.remove(*[m for m in self.mobjects])
        self.add(square)
        self.slide_pause()

        _square = square.copy()
        cubelines = always_redraw(
            lambda: VGroup(*[
                Line(
                    start=square[i], end=_square[i], stroke_color=square[i].get_color()
                ).set_z_index(0) for i in range(len(square)) if isinstance(square[i], Dot3D)
            ])
        )
        self.add(cubelines)
        self.begin_ambient_camera_rotation(rate=0.5, about="phi")
        self.begin_ambient_camera_rotation(rate=0.2)
        self.play(
            square.animate.shift(OUT),
            _square.animate.shift(IN)
        )
        vertices = VGroup(*[
            v for v in [*square, *_square] if isinstance(v, Dot3D)
        ])
        # print(*vertices)
        # for v in vertices:
        #     print(v.get_center())
        # vcoords = []
        # for i in range(3):
        #     for j in [-1, 1]:
        #         vcoords.append([p.get_center() for p in vertices if p.get_center()[i] == j])
        vcoords = [
            [vertices[i].get_center() for i in [3, 2, 0, 1]],
            [vertices[i].get_center() for i in [3, 2, 6, 7]],
            [vertices[i].get_center() for i in [3, 1, 5, 7]],
            [vertices[i].get_center() for i in [4, 5, 7, 6]],
            [vertices[i].get_center() for i in [4, 5, 1, 0]],
            [vertices[i].get_center() for i in [4, 6, 2, 0]],
        ]
        vcolors = [
            [vertices[i].get_color() for i in [3, 2, 0, 1]],
            [vertices[i].get_color() for i in [3, 2, 6, 7]],
            [vertices[i].get_color() for i in [3, 1, 5, 7]],
            [vertices[i].get_color() for i in [4, 5, 7, 6]],
            [vertices[i].get_color() for i in [4, 5, 1, 0]],
            [vertices[i].get_color() for i in [4, 6, 2, 0]],
        ]
        faces = VGroup(*[
            Polygon(
                *coords, fill_opacity=0.5, fill_color=color_gradient(colors, 3)
            ) for coords, colors in zip(vcoords, vcolors)
        ])
        for face in faces:
            # self.add(face)
            self.play(FadeIn(face), run_time=0.25)
            self.slide_pause()
            # self.remove(face)
            self.play(FadeOut(face), run_time=0.25)


if __name__ == "__main__":
    cls = GeometriskUdvikling
    class_name = cls.__name__
    transparent = cls.btransparent
    command = rf"manim {sys.argv[0]} {class_name} -p --resolution={_RESOLUTION[q]} --frame_rate={_FRAMERATE[q]}"
    # if transparent:
    #     command += " --transparent --format=webm"
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

