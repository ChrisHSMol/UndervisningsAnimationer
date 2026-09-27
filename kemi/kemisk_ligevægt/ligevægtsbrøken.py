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


class OpskrivningAfLigevægtsbrøk(MovingCameraScene, Slide if slides else Scene):
    def construct(self):
        self.camera.background_color = DARKER_GRAY
        # title = Tex(r"Opskrivning af\\ligevægtsbrøker").scale(2)
        # self.add(title)
        # self.slide_pause()
        # self.play(
        #     FadeOut(title),
        #     run_time=0.25
        # )
        self.generel_opskrivning()
        self.wait(5)

    def slide_pause(self, t=0.5, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def get_cmap(self):
        cmap = {"a": BLUE, "b": GREEN, "c": YELLOW, "d": RED}
        ks = ["a", "b", "c", "d"]
        for k in ks:
            cmap[f"${k}$"] = cmap[k]
            cmap[f"^{k}"] = cmap[k]
        return cmap

    def generel_opskrivning(self):
        _c = self.get_cmap()
        titel = Tex("Generel reaktionsbrøk").scale(2).to_edge(UP)
        titel_underline = Line(
            start=titel.get_corner(DL) + 0.25*DL + LEFT, end=titel.get_corner(DR) + 0.25*DR + RIGHT,
            stroke_opacity=[0, 1, 0], stroke_width=3
        )
        reaktionsskema = Tex(
            "$a$", "A", " + ", "$b$", "B", " + ", "...", r" $\rightleftharpoons$ ",
            "$c$", "C", " + ", "$d$", "D", " + ", "..."
        ).set_color_by_tex_to_color_map(_c).shift(UP)
        # self.add(reaktionsskema, titel, titel_underline)
        self.play(
            LaggedStart(
                Write(titel),
                Create(titel_underline),
                lag_ratio=0.5
            ),
            run_time=1
        )
        self.slide_pause()

        for r in [(0, 2), (2, 3), (3, 5), (5, 7), (7, 8), (8, 10), (10, 11), (11, 13), (13, 15)]:
            self.play(
                Write(reaktionsskema[r[0]:r[1]]),
                run_time=0.25
            )
            self.slide_pause()
        # self.remove(reaktionsskema)
        # self.add(reaktionsskema)

        reaktionsbrøk = MathTex(
            "Y", "=", r"\frac{", r"[\text{C}]", "^c", r"\cdot", r"[\text{D}]", "^d", r"\cdot", "...", "}{",
            r"[\text{A}]", "^a", r"\cdot", r"[\text{B}]", "^b", r"\cdot", "...", "}"
        ).set_color_by_tex_to_color_map(_c).shift(DOWN)
        dkemaindeks = index_labels(reaktionsskema)
        brøkindeks = index_labels(reaktionsbrøk)
        # self.add(dkemaindeks, brøkindeks)
        # self.add(reaktionsbrøk)
        self.play(
            LaggedStart(
                *[Write(reaktionsbrøk[i]) for i in [0, 1, 10]],
                lag_ratio=0.25
            ),
            run_time=0.25
        )
        self.slide_pause()

        # for i in (
        #         (9, 3), (8, 4), (10, 5), (12, 6), (11, 7), (13, 8), (14, 9),
        #         (1, 11), (0, 12), (2, 13), (4, 14), (3, 15), (5, 16), (6, 17)
        # ):
        #     ifrom, ito = i
        #     self.play(
        #         ReplacementTransform(
        #             reaktionsskema[ifrom].copy(),
        #             reaktionsbrøk[ito],
        #         ),
        #         run_time=0.5
        #     )
        #     self.slide_pause()
        for i in (
            [(9, 3), (8, 4)], [(10, 5)], [(12, 6), (11, 7)], [(13, 8), (14, 9)],
            [(1, 11), (0, 12)], [(2, 13)], [(4, 14), (3, 15)], [(5, 16), (6, 17)]
        ):
            self.play(
                *[
                    ReplacementTransform(
                        reaktionsskema[j[0]].copy(),
                        reaktionsbrøk[j[1]]
                    ) for j in i
                ],
                run_time=0.5
            )
            self.slide_pause()



if __name__ == "__main__":
    classes = [
        OpskrivningAfLigevægtsbrøk
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