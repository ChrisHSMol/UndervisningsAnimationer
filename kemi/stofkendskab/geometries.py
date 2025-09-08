import math

from manim import *
import sys

sys.path.append("../")
sys.path.append("../../")
import numpy as np
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


class Tetraeder(ThreeDScene, Slide if slides else Scene):
    def construct(self):
        self.camera.background_color = DARK_GRAY
        self.tetraeder_form()
        self.methan()
        self.ammoniak()
        self.vand()

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def tetraeder_form(self):
        axes = ThreeDAxes(
            x_range=[-2, 2],
            y_range=[-2, 2],
            z_range=[-2, 2],
            x_length=4,
            y_length=4,
            z_length=4,
        )
        ax_labs = VGroup(
            axes.get_x_axis_label(Tex("$x$")),
            axes.get_y_axis_label(Tex("$y$")),
            axes.get_z_axis_label(Tex("$z$"))
        )
        self.add(axes, ax_labs)
        vertices = [
            # (1, 1, 1),
            # (-1, -1, 1),
            # (-1, 1, -1),
            # (1, -1, -1)
            (0, 0, 1),
            (2*np.sqrt(2)/3, 0, -1/3),
            (-np.sqrt(2)/3, np.sqrt(2/3), -1/3),
            (-np.sqrt(2)/3, -np.sqrt(2/3), -1/3)
        ]
        vcs = [
            BLUE, GREEN, RED, YELLOW
        ]
        vertex_opacity_trackers = [
            ValueTracker(0.0) for _ in range(len(vertices))
        ]
        vertex_points = always_redraw(lambda: VGroup(
            *[
                Dot3D(
                    color=c, fill_opacity=vt.get_value(), stroke_opacity=0
                ).move_to(v) for c, v, vt in zip(vcs, vertices, vertex_opacity_trackers)
            ]
        ))
        center = Dot3D(fill_color=WHITE, stroke_opacity=0, fill_opacity=1)
        self.add(vertex_points, center)
        face_opacity_trackers = [
            ValueTracker(0.0) for _ in range(len(vertices))
        ]
        faces = always_redraw(lambda: VGroup(
            Polygon(
                vertices[0], vertices[1], vertices[2], fill_opacity=face_opacity_trackers[0].get_value(),
                # stroke_opacity=0.01, fill_color=color_gradient((vcs[0], vcs[1], vcs[2]), 6)
                stroke_opacity=0.01, fill_color=vcs[3]
            ),
            Polygon(
                vertices[1], vertices[2], vertices[3], fill_opacity=face_opacity_trackers[1].get_value(),
                # stroke_opacity=0.01, fill_color=color_gradient((vcs[1], vcs[2], vcs[3]), 6)
                stroke_opacity=0.01, fill_color=vcs[0]
            ),
            Polygon(
                vertices[0], vertices[2], vertices[3], fill_opacity=face_opacity_trackers[2].get_value(),
                # stroke_opacity=0.01, fill_color=color_gradient((vcs[0], vcs[2], vcs[3]), 6)
                stroke_opacity=0.01, fill_color=vcs[1]
            ),
            Polygon(
                vertices[0], vertices[1], vertices[3], fill_opacity=face_opacity_trackers[3].get_value(),
                # stroke_opacity=0.01, fill_color=color_gradient((vcs[0], vcs[1], vcs[3]), 6)
                stroke_opacity=0.01, fill_color=vcs[2]
            )
        ))
        self.add(faces)
        self.set_camera_orientation(phi=PI/3, zoom=2)
        self.begin_ambient_camera_rotation(rate=0.5, about="theta")
        self.play(
            *[v.animate.set_value(0.) for v in vertex_opacity_trackers[1:]],
            vertex_opacity_trackers[0].animate.set_value(1),
            run_time=2
        )
        self.play(
            vertex_opacity_trackers[0].animate.set_value(0.2),
            vertex_opacity_trackers[1].animate.set_value(1),
            run_time=2
        )
        self.play(
            vertex_opacity_trackers[1].animate.set_value(0.2),
            vertex_opacity_trackers[2].animate.set_value(1),
            run_time=2
        )
        self.play(
            vertex_opacity_trackers[2].animate.set_value(0.2),
            vertex_opacity_trackers[3].animate.set_value(1),
            run_time=2
        )
        self.play(
            *[v.animate.set_value(1) for v in vertex_opacity_trackers],
            run_time=2
        )
        self.play(
            face_opacity_trackers[0].animate.set_value(1),
            run_time=2
        )
        self.play(
            face_opacity_trackers[0].animate.set_value(0.2),
            face_opacity_trackers[1].animate.set_value(1),
            run_time=2
        )
        self.play(
            face_opacity_trackers[1].animate.set_value(0.2),
            face_opacity_trackers[2].animate.set_value(1),
            run_time=2
        )
        self.play(
            face_opacity_trackers[2].animate.set_value(0.2),
            face_opacity_trackers[3].animate.set_value(1),
            run_time=2
        )
        self.play(
            face_opacity_trackers[3].animate.set_value(0.2),
            run_time=2
        )
        self.wait(20)
        self.stop_ambient_camera_rotation()
        self.remove(*self.mobjects)

    def methan(self):
        atomradier = {}
        with open("../data_atomradier.txt", "r") as inFile:
            for line in inFile:
                line = line.split()
                atomradier[str(line[0])] = float(line[2])
        # self.set_camera_orientation(phi=PI/3, zoom=2)
        self.begin_ambient_camera_rotation(rate=0.5, about="theta")
        vertices = np.array([
            (0, 0, 1),
            (2*np.sqrt(2)/3, 0, -1/3),
            (-np.sqrt(2)/3, np.sqrt(2/3), -1/3),
            (-np.sqrt(2)/3, -np.sqrt(2/3), -1/3)
        ]) * 0.5
        vcs = [
            WHITE for _ in range(len(vertices))
        ]
        atoms = VGroup(
            *[
                Dot3D(
                    color=c, fill_opacity=0.9, stroke_opacity=0, radius=atomradier[a]
                ).move_to(v) for c, v, a in zip(vcs, vertices, ["H", "H", "H", "H"])
            ]
        )
        center = Dot3D(radius=atomradier["C"], color=BLACK, stroke_opacity=0, fill_opacity=1)
        bonds = VGroup(
            *[
                Line3D(
                    start=center.get_center(), end=a.get_center(), color=LIGHT_GRAY, stroke_width=0.1
                ) for a in atoms
            ]
        )
        name = Tex("Methan, CH$_4$").next_to(atoms, DOWN)
        self.add_fixed_in_frame_mobjects(name)
        self.add(atoms, center, bonds)
        # self.slide_pause()
        self.wait(5)
        self.slide_pause()
        self.stop_ambient_camera_rotation()
        self.remove(atoms, center, bonds, name)

    def ammoniak(self):
        atomradier = {}
        with open("../data_atomradier.txt", "r") as inFile:
            for line in inFile:
                line = line.split()
                atomradier[str(line[0])] = float(line[2])
        # self.set_camera_orientation(phi=PI/3, zoom=2)
        self.begin_ambient_camera_rotation(rate=0.5, about="theta")
        vertices = np.array([
            # (0, 0, 1),
            (2*np.sqrt(2)/3, 0, -1/3),
            (-np.sqrt(2)/3, np.sqrt(2/3), -1/3),
            (-np.sqrt(2)/3, -np.sqrt(2/3), -1/3)
        ]) * 0.5
        vcs = [
            WHITE for _ in range(len(vertices))
        ]
        atoms = VGroup(
            *[
                Dot3D(
                    color=c, fill_opacity=0.9, stroke_opacity=0, radius=atomradier[a]
                ).move_to(v) for c, v, a in zip(vcs, vertices, ["H", "H", "H"])
            ]
        )
        center = Dot3D(radius=atomradier["N"], color=BLUE, stroke_opacity=0, fill_opacity=1)
        bonds = VGroup(
            *[
                Line3D(
                    start=center.get_center(), end=a.get_center(), color=LIGHT_GRAY, stroke_width=0.1
                ) for a in atoms
            ]
        )
        atoms.add(
            VGroup(
                Surface(
                    lambda u, v: np.array([
                        np.cos(u) * np.cos(v) * 0.175,
                        np.cos(u) * np.sin(v) * 0.175,
                        np.sin(u) * 0.375 + 0.5
                    ]),
                    u_range=(-PI/2, PI/2),
                    v_range=(0, 2*PI),
                    resolution=(16, 16),
                    checkerboard_colors=(YELLOW, YELLOW_A),
                    fill_opacity=0.125,
                    stroke_width=0
                ),
                Dot3D(radius=0.0375, color=YELLOW, stroke_width=0).shift(0.5*OUT+0.075*RIGHT),
                Dot3D(radius=0.0375, color=YELLOW, stroke_width=0).shift(0.5*OUT+0.075*LEFT)
            )
        )
        name = Tex("Ammoniak, NH$_3$").next_to(atoms, DOWN)
        self.add_fixed_in_frame_mobjects(name)
        self.add(atoms, center, bonds)
        # self.slide_pause()
        self.wait(5)
        self.slide_pause()
        self.stop_ambient_camera_rotation()
        self.remove(atoms, center, bonds, name)

    def vand(self):
        atomradier = {}
        with open("../data_atomradier.txt", "r") as inFile:
            for line in inFile:
                line = line.split()
                atomradier[str(line[0])] = float(line[2])
        # self.set_camera_orientation(phi=PI/3, zoom=2)
        self.begin_ambient_camera_rotation(rate=0.5, about="theta")
        vertices = np.array([
            # (0, 0, 1),
            # (2*np.sqrt(2)/3, 0, -1/3),
            (-np.sqrt(2)/3, np.sqrt(2/3), -1/3),
            (-np.sqrt(2)/3, -np.sqrt(2/3), -1/3)
        ]) * 0.5
        vcs = [
            WHITE for _ in range(len(vertices))
        ]
        atoms = VGroup(
            *[
                Dot3D(
                    color=c, fill_opacity=0.9, stroke_opacity=0, radius=atomradier[a]
                ).move_to(v) for c, v, a in zip(vcs, vertices, ["H", "H"])
            ]
        )
        center = Dot3D(radius=atomradier["O"], color=RED, stroke_opacity=0, fill_opacity=1)
        bonds = VGroup(
            *[
                Line3D(
                    start=center.get_center(), end=a.get_center(), color=LIGHT_GRAY, stroke_width=0.1
                ) for a in atoms
            ]
        )
        atoms.add(
            VGroup(
                Surface(
                    lambda u, v: np.array([
                        np.cos(u) * np.cos(v) * 0.175,
                        np.cos(u) * np.sin(v) * 0.175,
                        np.sin(u) * 0.375 + 0.5
                    ]),
                    u_range=(-PI/2, PI/2),
                    v_range=(0, 2*PI),
                    resolution=(16, 16),
                    checkerboard_colors=(YELLOW, YELLOW_A),
                    fill_opacity=0.125,
                    stroke_width=0
                ),
                Dot3D(radius=0.0375, color=YELLOW, stroke_width=0).shift(0.5*OUT+0.075*RIGHT),
                Dot3D(radius=0.0375, color=YELLOW, stroke_width=0).shift(0.5*OUT+0.075*LEFT)
            )
        )
        atoms.add(
            atoms[-1].copy().rotate(120*DEGREES, axis=bonds[0].get_direction(), about_point=center.get_center())
        )
        name = Tex("Vand, H$_2$O").next_to(atoms, DOWN)
        self.add_fixed_in_frame_mobjects(name)
        self.add(atoms, center, bonds)
        # self.slide_pause()
        self.wait(5)
        self.slide_pause()
        self.stop_ambient_camera_rotation()
        self.remove(atoms, center, bonds, name)


if __name__ == "__main__":
    classes = [
        Tetraeder
    ]
    for cls in classes:
        class_name = cls.__name__
        command = rf"manim {sys.argv[0]} {class_name} -p --resolution={_RESOLUTION[q]} --frame_rate={_FRAMERATE[q]}"
        # if _bcol is not None:
        #     command += f" -c {_bcol} --background_color {_bcol}"
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

