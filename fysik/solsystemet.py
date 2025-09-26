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
_ONEFRAME = 1/_FRAMERATE[q]


class PlanetBaner(ThreeDScene, Slide if slides else Scene):
    def construct(self):
        self.camera.background_color = DARK_GRAY
        self.set_camera_orientation(zoom=3)
        self.jordens_bane()
        self.slide_pause()

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def get_orbit_data(self, planet: str):
        # Enheder: Rjord, Mjord, dage, AU, , år
        data = {
            "Merkur": {
                "rad": 0.383, "mass": 0.0553, "P_rot": 58.6, "a": 0.387, "e": 0.2056, "P_orb": 0.241, "tilt": 0.01
            },
            "Venus": {
                "rad": 0.950, "mass": 0.8150, "P_rot": -243.0, "a": 0.723, "e": 0.0068, "P_orb": 0.615, "tilt": 2.64
            },
            "Jorden": {
                "rad": 1.000, "mass": 1.000, "P_rot": 0.997, "a": 1.000, "e": 0.0167, "P_orb": 1.000, "tilt": 23.44
            },
            "Mars": {
                "rad": 0.532, "mass": 0.1074, "P_rot": 1.026, "a": 1.524, "e": 0.0934, "P_orb": 1.881, "tilt": 25.19
            },
            "Jupiter": {
                "rad": 10.97, "mass": 317.8, "P_rot": 0.414, "a": 5.203, "e": 0.0484, "P_orb": 11.86, "tilt": 3.12
            },
            "Saturn": {
                "rad": 9.14, "mass": 95.16, "P_rot": 0.444, "a": 9.537, "e": 0.0539, "P_orb": 29.45, "tilt": 26.73
            },
            "Uranus": {
                "rad": 3.98, "mass": 14.50, "P_rot": -0.718, "a": 19.19, "e": 0.0473, "P_orb": 84.02, "tilt": 82.23
            },
            "Neptun": {
                "rad": 4.18, "mass": 17.20, "P_rot": 0.671, "a": 30.07, "e": 0.0086, "P_orb": 164.8, "tilt": 28.33
            },
        }
        if not planet in data.keys():
            print(f"{planet} er ikke et gyldigt input")
            pass
        return data[planet]
    
    def get_planets(self):
        return "Merkur", "Venus", "Jorden", "Mars", "Jupiter", "Saturn", "Uranus", "Neptun"

    # def get_ellipse(self, a: float, b: float):
    #     return

    def jordens_bane(self):
        rearth_to_au = 4.2635e-5
        period_to_seconds = 10
        data = self.get_orbit_data("Jorden")
        rad, mass, p_rot, a, e, p_orb = data["rad"], data["mass"], data["P_rot"], data["a"], data["e"], data["P_orb"]
        b = np.sqrt(a**2 * (1-e**2))
        focus = np.array((np.sqrt(a**2 - b**2), 0, 0))
        orbit = Ellipse(width=2*a, height=2*b, stroke_width=0.5, color=BLUE)
        tracker_dot = Dot3D(radius=0, resolution=(1, 1)).move_to(focus)
        print(np.array((1, 1, 1)) - np.array((2, 3, 1)))
        print(type(focus), type(tracker_dot.get_center()))
        planet = always_redraw(lambda: Sphere(
            # center=orbit.get_start(),
            center=tracker_dot.get_center(),
            radius=rad * rearth_to_au * 10000,
            resolution=(20, 20),
            checkerboard_colors=(PURE_BLUE, PURE_BLUE),
            # checkerboard_colors=get_shaded_rgb(
            #     rgb=np.array((0, 0, 255)), point=tracker_dot.get_center(),
            #     unit_normal_vect=tracker_dot.get_center() - focus, light_source=focus
            # ),
            # sheen_direction=tracker_dot.get_center() - focus,
            sheen_direction=RIGHT,
            sheen_factor=-1
        ).rotate(
            -data["tilt"]*DEGREES, axis=np.array((0, 1, 0))
        ))
        sun = Sphere(
            center=focus,
            radius=0.2,
            resolution=(20, 20),
            checkerboard_colors=(YELLOW, GOLD),
            sheen_factor=0,
            sheen_direction=ORIGIN
        )
        self.add(orbit, planet, sun, tracker_dot)
        self.play(
            MoveAlongPath(tracker_dot, orbit, run_time=p_orb*period_to_seconds),
            rate_func=rate_functions.linear
        )

    def solsystemet(self):
        for planet in self.get_planets():
            data = self.get_orbit_data(planet)
            b = np.sqrt(data["a"]**2 * (1-data["e"]**2))
            bane = Ellipse(width=2*data["a"], height=2*b)
            self.add(bane)
            self.slide_pause()

        # data_jord = self.get_orbit_data("Merkur")
        # b = np.sqrt(data_jord["a"]**2 * (1-data_jord["e"]**2))
        # print(data_jord["a"], b, data_jord["e"])
        # bane = Ellipse(
        #     width=2*data_jord["a"], height=2*b
        # )
        # self.add(bane)


if __name__ == "__main__":
    classes = [
        PlanetBaner,
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