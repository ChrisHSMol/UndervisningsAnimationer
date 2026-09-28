import math
import random

from manim import *
import sys

sys.path.append("../../")
sys.path.append("../../../")
import subprocess
from helpers import *
from custom_classes import *

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


class WritingEquilibriumFraction(MovingCameraScene, Slide if slides else Scene):
    def _bkg_col(self):
        return DARKER_GRAY

    def construct(self):
        self.camera.background_color = self._bkg_col()
        # title = Tex(r"Opskrivning af\\ligevægtsbrøker").scale(2)
        # self.add(title)
        # self.slide_pause()
        # self.play(
        #     FadeOut(title),
        #     run_time=0.25
        # )
        self.generel_opskrivning()
        self.example_ammonia()
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
            if r[-1]-r[0] > 1:
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
                LaggedStart(
                    *[
                        ReplacementTransform(
                            reaktionsskema[j[0]].copy(),
                            reaktionsbrøk[j[1]]
                        ) for j in i
                    ],
                    lag_ratio=0.75
                ),
                run_time=1.5
            )
            if len(i) > 1:
                self.slide_pause()

        self.play(
            LaggedStart(
                *[FadeOut(m) for m in self.mobjects],
                lag_ratio=0.05
            )
        )

    def example_ammonia(self):
        _c = self.get_cmap()
        titel = Tex("Eksempel: Ammoniak").scale(2).to_edge(UP)
        titel_underline = Line(
            start=titel.get_corner(DL) + 0.25*DL + LEFT, end=titel.get_corner(DR) + 0.25*DR + RIGHT,
            stroke_opacity=[0, 1, 0], stroke_width=3
        )
        reaktionsskema = Tex(
            "3", "H$_2$", " + ", "1", "N$_2$", r" $\rightleftharpoons$ ", "2", "NH$_3$"
        ).shift(UP)
        reaktionsskema[0].set_color(_c["a"])
        reaktionsskema[3].set_color(self._bkg_col())
        reaktionsskema[6].set_color(_c["c"])
        self.play(
            LaggedStart(
                Write(titel),
                Create(titel_underline),
                lag_ratio=0.5
            ),
            run_time=1
        )
        self.slide_pause()

        self.play(
            Write(reaktionsskema)
        )

        reaktionsbrøk = MathTex(
            "Y", "=", r"\frac{", r"[\text{NH}_3]", "^2", "}{",
            r"[\text{H}_2]", "^3", r"\cdot", r"[\text{N}_2]", "^1", "}"
        ).shift(DOWN)
        reaktionsbrøk[4].set_color(_c["c"])
        reaktionsbrøk[7].set_color(_c["a"])
        reaktionsbrøk[10].set_color(self._bkg_col())
        # dkemaindeks = index_labels(reaktionsskema)
        # brøkindeks = index_labels(reaktionsbrøk)
        # self.add(dkemaindeks, brøkindeks)
        # self.add(reaktionsbrøk)
        self.play(
            LaggedStart(
                *[Write(reaktionsbrøk[i]) for i in [0, 1, 5]],
                lag_ratio=0.25
            ),
            run_time=0.25
        )
        self.slide_pause()

        for i in (
            [(7, 3), (6, 4)],
            [(1, 6), (0, 7)], [(2, 8)], [(4, 9)]#, (3, 10)]
        ):
            self.play(
                LaggedStart(
                    *[
                        ReplacementTransform(
                            reaktionsskema[j[0]].copy(),
                            reaktionsbrøk[j[1]]
                        ) for j in i
                    ],
                    lag_ratio=0.75
                ),
                run_time=1.5
            )
            if len(i) > 1:
                self.slide_pause()

        for _ in range(5):
            self.play(
                Indicate(reaktionsskema[3], color=_c["b"]),
                Indicate(reaktionsbrøk[10], color=_c["b"]),
            )
        self.slide_pause()



if __name__ == "__main__":
    classes = [
        WritingEquilibriumFraction
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