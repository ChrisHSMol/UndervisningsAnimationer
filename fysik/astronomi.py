import sys

import numpy as np

sys.path.append("../")
from manim import *
# from manim_chemistry import *
from helpers import *
import random
import subprocess

slides = False
# if slides:
#     from manim_slides import Slide

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


class JordSolMaane(MovingCameraScene, Scene if not slides else Slide):
    def construct(self):
        self.slide_pause()
        self.moon_orbit()

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def get_celestial_info(self):
        return {
            "earth": {
                "navn": "Jorden", "radius": 6_371.0, "masse": 5.97E24, "orbit_radius": 1.496E8, "color": PURE_BLUE
            },
            "moon": {
                "navn": "Månen", "radius": 1_737.4, "masse": 7.342E22, "orbit_radius": 385_000, "color": LIGHT_GRAY
            },
            "sun": {
                "navn": "Solen", "radius": 696_300, "masse": 1.989E30, "orbit_radius": 0, "color": YELLOW
            },
        }

    def moon_orbit(self):
        _CI = self.get_celestial_info()
        scale_factor = 1/_CI["earth"]["radius"]
        earth = Circle(
            radius=_CI["earth"]["radius"] * scale_factor, fill_color=_CI["earth"]["color"],
            fill_opacity=1, stroke_width=0
        )
        # moon = always_redraw(lambda:
        #     Circle(
        #         radius=_CI["moon"]["radius"] * scale_factor, fill_color=LIGHT_GRAY, fill_opacity=1, stroke_width=0
        #     ).shift(_CI["moon"]["orbit_radius"]*scale_factor*RIGHT)
        # )
        moon = Circle(
            radius=_CI["moon"]["radius"] * scale_factor, fill_color=_CI["moon"]["color"],
            fill_opacity=1, stroke_width=0
        ).shift(_CI["moon"]["orbit_radius"]*scale_factor*RIGHT)
        moon.add_updater(lambda m: m.rotate(1 / _FRAMERATE[q], about_point=ORIGIN))

        target_widths = [
            16 / 9 * _CI["moon"]["orbit_radius"] * scale_factor * 2.5,
            16 / 9 * _CI["earth"]["orbit_radius"] * scale_factor * 2.5
        ]

        trace = TracedPath(
            moon.get_center, stroke_color=moon.get_fill_color(),
            # stroke_width=moon.radius, stroke_opacity=[0.5, 1]
            stroke_width=0.1 * target_widths[0],
            # stroke_opacity=[0.0, 1.0], dissipating_time=2
        )
        self.add(earth, moon, trace)
        self.camera.frame.save_state()
        # self.camera.frame.set(width=target_widths[0])
        # self.slide_pause()
        self.play(
            self.camera.frame.animate.set(
                # height=_CI["moon"]["orbit_radius"]*scale_factor * 2.5
                width=target_widths[0]
            ),
            run_time=0.25
        )
        # self.slide_pause()

        # self.play(
        #     moon_orbit_tracker.animate.set_value(5*TAU),
        #     run_time=10,
        #     rate_func=rate_functions.linear
        # )
        self.slide_pause(TAU)
        # self.play(
        #     MoveAlongPath(self.camera.frame, trace),
        #     run_time=TAU
        # )

        # # moon.remove_updater(lambda m: m.rotate(1 / _FRAMERATE[q], about_point=ORIGIN))
        moon.clear_updaters()
        sun = Circle(
            radius=_CI["sun"]["radius"] * scale_factor, fill_color=_CI["sun"]["color"],
            fill_opacity=1, stroke_width=0
        )
        earth.move_to(sun).shift(_CI["earth"]["orbit_radius"] * scale_factor * RIGHT)
        moon.move_to(earth).shift(_CI["moon"]["orbit_radius"] * scale_factor * RIGHT)
        print(sun.get_center(), earth.get_center(), moon.get_center())

        # earth.scale(sun.radius/earth.radius)
        # moon.scale(sun.radius/moon.radius)
        # moon.scale(earth.radius/moon.radius)
        # earth.add_updater(lambda m: m.rotate((TAU/10) / (1.0 * _FRAMERATE[q]), about_point=sun.get_center()))
        # moon.add_updater(lambda m: m.rotate((TAU/120) / (1.0 * _FRAMERATE[q]), about_point=earth.get_center()))
        earth.add_updater(lambda m: m.rotate(TAU / (10.0 * _FRAMERATE[q]), about_point=sun.get_center()))
        moon.add_updater(lambda m: m.rotate(TAU / (120.0 * _FRAMERATE[q]), about_point=earth.get_center()))

        earth_orbit = TracedPath(
            earth.get_center, stroke_color=earth.get_fill_color(),
            stroke_width=0.1 * target_widths[1], dissipating_time=30,
            # stroke_opacity=[0, 1]
        )
        moon_orbit = TracedPath(
            moon.get_center, stroke_color=moon.get_fill_color(),
            stroke_width=0.1 * target_widths[1], dissipating_time=30,
            # stroke_opacity=[0, 1]
        )
        # self.camera.frame.move_to(VGroup(moon))
        self.remove(trace)
        self.add(sun, earth, moon, earth_orbit, moon_orbit)
        # self.add(moon_orbit)
        self.camera.frame.set(width=target_widths[1]).move_to(sun)
        self.slide_pause(40)



if __name__ == "__main__":
    cls = JordSolMaane
    class_name = cls.__name__
    # transparent = cls.btransparent
    command = rf"manim {sys.argv[0]} {class_name} -p --resolution={_RESOLUTION[q]} --frame_rate={_FRAMERATE[q]}"
    # if transparent:
    #     command += " --transparent --format=webm"
    scene_marker(rf"RUNNNING:    {command}")
    subprocess.run(command)
