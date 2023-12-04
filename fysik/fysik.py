from manim import *
import sys
sys.path.append("../")
from helpers import *
import subprocess

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


class Tilstand(Slide, MovingCameraScene if slides else MovingCameraScene):
    def construct(self):
        self.tilstandsgraf()

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def tilstandsgraf(self):
        c_is = 2.1          # kJ kg^-1 C^-1
        smelte = 334        # kJ kg^-1
        c_vand = 4180       # kJ kg^-1 C^-1
        fordamp = 2257      # kJ kg^-1
        c_damp = 1.84       # kJ kg^-1 C^-1

        m = 1
        T = [-18, 0, 0, 100, 100, 150]

        colors = [BLUE, BLUE_C, YELLOW, ORANGE, RED]

        plane = Axes(x_range=[0, 500000, 50000], y_range=[-20, 150, 20])
        cum_E = 0.0
        energies = [cum_E]
        for i, c in enumerate([c_is, smelte, c_vand, fordamp, c_damp]):
            if i in [1, 3]:
                cum_E += c * m
                energies.append(cum_E)
            else:
                cum_E += m * c * (T[i+1] - T[i])
                energies.append(cum_E)

        for x, y in zip(energies, T):
            print(x, y)

        graphs = VGroup(
            *[
                Line(
                    start=plane.c2p(energies[i], T[i]),
                    end=plane.c2p(energies[i+1], T[i+1]),
                    color=colors[i]
                ) for i in range(len(T) - 1)
            ]
        )
        # graphs = VGroup(
        #     Line(
        #         start=plane.c2p(0, T[0]),
        #         end=plane.c2p(m * c_is * (T[1]-T[0]), T[1])
        #     ),
        #     Line(
        #         start=plane.c2p(m * c_is * (T[1]-T[0]), T[1]),
        #         end=plane.c2p(m * smelte, T[1])
        #     ),
        #     Line(
        #         start=plane.c2p(m * smelte, T[1]),
        #         end=plane.c2p(m * c_vand * (T[2]-T[1]), T[2])
        #     ),
        #     Line(
        #         start=plane.c2p(m * c_vand * (T[2]-T[1]), T[2]),
        #         end=plane.c2p(m * fordamp, T[2])
        #     ),
        #     Line(
        #         start=plane.c2p(m * fordamp, T[2]),
        #         end=plane.c2p(m * c_damp * (T[3] - T[2]), T[3])
        #     ),
        # )
        # self.add(plane, graphs)
        self.play(
            LaggedStart(
                Create(plane),
                *[Create(graph) for graph in graphs],
                lag_ratio=0.75
            ),
            run_time=20
        )


if __name__ == "__main__":
    class_name = Tilstand.__name__
    command = rf"manim {sys.argv[0]} {class_name} -p --resolution={_RESOLUTION[q]} --frame_rate={_FRAMERATE[q]}"
    scene_marker(rf"RUNNNING:    {command}")
    subprocess.run(command)
