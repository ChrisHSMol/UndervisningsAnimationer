import math

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


class RedoxAfstemning(MovingCameraScene, Slide if slides else Scene):
    def construct(self):
        self.camera.background_color = DARKER_GRAY
        # title = Tex("Fældningsreaktioner").scale(2)
        # self.add(title)
        # self.slide_pause()
        # self.play(
        #     FadeOut(title),
        #     run_time=0.25
        # )
        self.afstemning()
        self.wait(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def forklaringstekst_i_boks(self, tekst, trin, color):
        output = VGroup()
        overskrift = Tex(trin, color=color).scale(1.125)
        tekst.next_to(overskrift, DOWN, aligned_edge=LEFT, buff=0.5)
        output.add(overskrift)
        output.add(tekst)
        boks = get_background_rect(output, stroke_colour=color)
        output.add(boks)
        output.move_to(ORIGIN)
        return output

    def afstemning(self):
        step1 = Tex(
            " ", " ", " ", " ", "MnO$_4^-$ (aq)", " + ", " ", "HSO$_3^-$ (aq)", r"$\longrightarrow$",
            " ", "Mn$^{2+}$ (aq)", " + ", " ", "SO$_4^{2-}$ (aq)", " ", " ", " "
        ).scale(0.9).to_edge(UP, buff=0.75)
        forklaring_trin1 = self.forklaringstekst_i_boks(
            Tex(r"Opskriv reaktionsskema uden koefficienter\\med de stoffer, som indeholder\\grundstoffer, der skifter oxidationstal"),
            "Trin 1:",
            color=YELLOW
        )
        self.add(step1, forklaring_trin1)

        step2 = step1.copy()
        step2[4][:2].set_color(BLUE)
        step2[7][1].set_color(RED)
        step2[10][:2].set_color(BLUE)
        step2[13][0].set_color(RED)
        ox_tal = VGroup(
            Tex("+VII", color=BLUE).next_to(step1[4], UP, aligned_edge=LEFT, buff=0.2),
            Tex("+IV", color=RED).next_to(step1[7], UP, aligned_edge=LEFT, buff=0.2),
            Tex("+II", color=BLUE).next_to(step1[10], UP, aligned_edge=LEFT, buff=0.2),
            Tex("+VI", color=RED).next_to(step1[13], UP, aligned_edge=LEFT, buff=0.2),
        )
        forklaring_trin2 = self.forklaringstekst_i_boks(
            Tex(r"Angiv oxidationstal på de grundstoffer,\\der ændrer oxidationstal"),
            "Trin 2:",
            color=interpolate_color(RED, BLUE, 2/3)
        )
        self.remove(step1, forklaring_trin1)
        self.add(step2, ox_tal, forklaring_trin2)

        step3 = step2.copy()
        forklaring_trin3 = self.forklaringstekst_i_boks(
            Tex(r"Beregn ændringerne\\i oxidationstal"),
            "Trin 3:",
            color=interpolate_color(RED, BLUE, 1/3)
        )
        forklaring_trin3.to_edge(DOWN)
        tabel_struktur = VGroup(
            *[
                VGroup(
                    *[
                        Rectangle(
                            width=2, height=1, stroke_color=scol, stroke_width=1
                        ) for scol in (WHITE, BLUE, RED)
                    ]
                ).arrange(DOWN, buff=0.0375) for _ in range(6)
            ]
        ).arrange(RIGHT, buff=0.025).next_to(forklaring_trin3, UP)
        tabel_indhold = VGroup(
            VGroup(*[
                Tex(t).scale(0.75).move_to(tabel_struktur[i][0]) for i, t in enumerate(
                    ("Process", "Grundstof", "Reaktant", "Produkt", "Ændring", "Koefficient")
                )
            ]),
            VGroup(*[
                Tex(t, color=ox_tal[0].get_color()).move_to(tabel_struktur[i][1]) for i, t in enumerate(
                    ("Red", "Mn", "+VII", "+II", r"5$\downarrow$", "2")
                )
            ]),
            VGroup(*[
                Tex(t, color=ox_tal[1].get_color()).move_to(tabel_struktur[i][2]) for i, t in enumerate(
                    ("Ox", "S", "+IV", "+VI", r"2$\uparrow$", "5")
                )
            ])
        )
        tabel_indhold[1][-1].set_color(ox_tal[1].get_color())
        tabel_indhold[2][-1].set_color(ox_tal[0].get_color())
        self.remove(step2, forklaring_trin2)
        self.add(step3, forklaring_trin3, tabel_struktur, tabel_indhold)

        step4 = Tex(
            " ", " ", " ", "2 ", "MnO$_4^-$ (aq)", " + ", "5 ", "HSO$_3^-$ (aq)", r"$\longrightarrow$",
            "2 ", "Mn$^{2+}$ (aq)", " + ", "5 ", "SO$_4^{2-}$ (aq)", " ", " ", " "
        ).scale(0.9).move_to(step3)
        step4[3].set_color(RED)
        step4[4][:2].set_color(BLUE)
        step4[6].set_color(BLUE)
        step4[7][1].set_color(RED)
        step4[9].set_color(RED)
        step4[10][:2].set_color(BLUE)
        step4[12].set_color(BLUE)
        step4[13][0].set_color(RED)

        # forklaring_trin3 = self.forklaringstekst_i_boks(
        #     Tex(r"Beregn ændringerne\\i oxidationstal"),
        #     "Trin 3:",
        #     color=interpolate_color(RED, BLUE, 1/3)
        # )
        self.remove(step3, forklaring_trin3, tabel_struktur, tabel_indhold, ox_tal)
        self.add(step4)

if __name__ == "__main__":
    classes = [
        RedoxAfstemning,
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