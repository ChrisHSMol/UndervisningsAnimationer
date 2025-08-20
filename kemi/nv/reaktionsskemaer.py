import math

from manim import *
from manim_chemistry import *
import sys

sys.path.append("../")
sys.path.append("../../")
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


class IntroTilReaktioner(MovingCameraScene, Slide if slides else Scene):
    def construct(self):
        play_title2(self, "Intro til reaktioner")
        self.grundprincipper()
        self.eksempel_no2()

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def get_cmap(self):
        return {"reak": GREEN, "prod": GOLD}

    def grundprincipper(self):
        _c = self.get_cmap()
        reaktant_og_produkt = Tex(
            "Reaktanter", r"$\longrightarrow$", "Produkter"
        ).scale(2)
        reaktant_og_produkt[0].set_color(_c["reak"])
        reaktant_og_produkt[2].set_color(_c["prod"])

        forklaring = VGroup(
            Tex("Reaktanter", " er de stoffer, der reagerer med hinanden"),
            Tex(r"$\longrightarrow$", " viser, at der sker en kemisk reaktion"),
            Tex("Produkter", " er stofferne, der bliver dannet af reaktionen")
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(DOWN)
        forklaring[0][0].set_color(_c["reak"])
        forklaring[2][0].set_color(_c["prod"])

        for i in range(len(forklaring)):
            # self.add(forklaring[i], reaktant_og_produkt[i])
            self.play(
                LaggedStart(
                    Write(reaktant_og_produkt[i]),
                    Write(forklaring[i]),
                    lag_ratio=0.1
                )
            )
            self.slide_pause()

        # for i in range(len(forklaring)):
        #     self.remove(forklaring[i], reaktant_og_produkt[i])
        # self.remove(forklaring, reaktant_og_produkt)
        self.play(
            LaggedStart(
                *[FadeOut(m) for m in self.mobjects],
                lag_ratio=0.05
            )
        )
        # self.slide_pause()

    def eksempel_no2(self):
        _c = self.get_cmap()
        reaktionsskema = VGroup(
            Tex("1", "N$_2$", " + ", "1", "O$_2$", r" $\longrightarrow$ ", "1", "NO$_2$", r"\quad (ikke afstemt)"),
            Tex("1", "N$_2$", " + ", "1", "O$_2$", r" $\longrightarrow$ ", "2", "NO$_2$", r"\quad (delvist afstemt)"),
            Tex("1", "N$_2$", " + ", "2", "O$_2$", r" $\longrightarrow$ ", "2", "NO$_2$", r"\quad (afstemt)"),
        ).arrange(ORIGIN, aligned_edge=LEFT, buff=1)
        for rs in reaktionsskema:
            rs[0].set_color(BLACK if int(rs[0].get_tex_string()) == 1 else YELLOW)
            rs[1].set_color(_c["reak"])
            rs[3].set_color(BLACK if int(rs[3].get_tex_string()) == 1 else YELLOW)
            rs[4].set_color(_c["reak"])
            rs[6].set_color(BLACK if int(rs[6].get_tex_string()) == 1 else YELLOW)
            rs[7].set_color(_c["prod"])

        n2_structure = {"N1": [0, 0, 0], "N2": [0.5, 0, 0]}
        o2_structure = {"O1": [0, 0, 0], "O2": [0.5, 0, 0]}
        no2_structure = {"N1": [0, 0, 0], "O1": [0.5, 0, 0], "O2": [-0.155, -0.476, 0]}
        molecules = VGroup(
            *[
                Molecule2D(s) for s in [n2_structure, o2_structure, o2_structure, no2_structure, no2_structure]
            ]
        )
        molecules[0].next_to(reaktionsskema[0][1], DOWN)
        molecules[1].next_to(reaktionsskema[0][4], DOWN)
        molecules[2].next_to(molecules[1], DOWN)
        molecules[3].next_to(reaktionsskema[0][7], DOWN)
        molecules[4].next_to(molecules[3], DOWN)

        self.play(
            Write(reaktionsskema[0][:2]),
            Write(molecules[0])
        )
        self.slide_pause()

        self.play(
            Write(reaktionsskema[0][2:5]),
            Write(molecules[1])
        )
        self.slide_pause()

        self.play(
            Write(reaktionsskema[0][5:]),
            Write(molecules[3])
        )
        self.slide_pause()

        table_structure = VGroup(
            *[
                VGroup(*[
                    Rectangle(width=2, height=1) for _ in range(3)
                ]).arrange(RIGHT, buff=0) for _ in range(3)
            ]
        ).arrange(DOWN, buff=0).to_edge(UR)
        stoich_table = VGroup(
            VGroup(
                Tex("Venstre").move_to(table_structure[0][1]), Tex("Højre").move_to(table_structure[0][2])
            ),
            VGroup(
                Molecule2D({"N": [0, 0, 0]}).move_to(table_structure[1][0]),
                Integer(2).move_to(table_structure[1][1]), Integer(1).move_to(table_structure[1][2])
            ),
            VGroup(
                Molecule2D({"O": [0, 0, 0]}).move_to(table_structure[2][0]),
                Integer(2).move_to(table_structure[2][1]), Integer(2).move_to(table_structure[2][2])
            )
        # ).arrange(DOWN, aligned_edge=RIGHT).to_edge(UR)
        )
        stoich_table.add(Line(start=table_structure[1].get_corner(UL), end=table_structure[1].get_corner(UR)))
        stoich_table.add(Line(start=table_structure[0][1].get_corner(UL), end=table_structure[2][1].get_corner(DL)))

        # self.add(stoich_table)
        self.play(
            LaggedStart(
                Write(stoich_table[:3], lag_ratio=0.1),
                Create(stoich_table[3:], lag_ratio=0.1),
                lag_ratio=0.1
            )
        )
        self.slide_pause()

        self.play(
            *[
                ReplacementTransform(
                    reaktionsskema[0][i].copy(), reaktionsskema[1][i]
                ) for i in range(len(reaktionsskema[0]))
            ],
            Write(molecules[4]),
            stoich_table[1][2].animate.set_value(2),
            stoich_table[2][2].animate.set_value(4),
            FadeOut(reaktionsskema[0], run_time=_ONEFRAME)
        )
        self.slide_pause()

        self.play(
            *[
                ReplacementTransform(
                    reaktionsskema[1][i].copy(), reaktionsskema[2][i]
                ) for i in range(len(reaktionsskema[1]))
            ],
            Write(molecules[2]),
            stoich_table[2][1].animate.set_value(4),
            FadeOut(reaktionsskema[1], run_time=_ONEFRAME)
        )
        self.slide_pause()


if __name__ == "__main__":
    classes = [
        IntroTilReaktioner,
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

