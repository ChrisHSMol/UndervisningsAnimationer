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


class SolubilityTable(MovingCameraScene, Slide if slides else Scene):
    def construct(self):
        self.camera.background_color = DARKER_GRAY
        title = Tex("Fældningsreaktioner").scale(2)
        self.add(title)
        self.slide_pause()
        self.play(
            FadeOut(title),
            run_time=0.25
        )
        table_info = self.create_solubility_table(show_animations=True)
        self.play_examples(table_info)
        self.wait(1)
        self.play(
            LaggedStart(
                *[FadeOut(m) for m in self.mobjects],
                lag_ratio=0.01
            )
        )

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def _make_cells(self, n_rows, n_cols, cell_width=1.0, cell_height=1.0):
        skeleton = VGroup()
        for irow in range(n_rows):
            row = VGroup()
            for icol in range(n_cols):
                row.add(
                    Rectangle(
                        width=cell_width, height=cell_height, stroke_width=0.75, stroke_color=WHITE
                    )
                )
            row.arrange(RIGHT, buff=0)
            skeleton.add(row)
        skeleton.arrange(DOWN, buff=0)
        return skeleton

    def create_solubility_table(self, show_animations=True):
        data = pd.read_csv("solubility_data.csv", header=0, index_col=0)
        table_skeleton = self._make_cells(
            n_rows=data.shape[0]+1, n_cols=data.shape[1]+1,
            cell_height=0.66
        )
        table_skeleton[0].remove(table_skeleton[0][0])
        table_skeleton[0].set_style(stroke_width=2)
        [cell[0].set_style(stroke_width=2) for cell in table_skeleton[1:]]
        if not show_animations:
            self.add(table_skeleton)
        else:
            self.play(
                LaggedStart(
                    *[DrawBorderThenFill(c) for c in table_skeleton[0]],
                    lag_ratio=0.25
                ),
                LaggedStart(
                    *[DrawBorderThenFill(c[0]) for c in table_skeleton[1:]],
                    lag_ratio=0.25
                ),
                run_time=1
            )

        raw_column_headers = list(data)
        raw_row_headers = list(data.index)
        column_headers = VGroup(
            *[
                MathTex(
                    rf"\text{{{h.split(r'^')[0].split(r'_')[0]}}}_{h.split(r'^')[0].split(r'_')[1]}^{h.split(r'^')[1]}"
                # ).scale(0.5).next_to(s, LEFT, buff=0.1).shift(s.width*RIGHT) for h, s in zip(
                ).scale(0.5).move_to(s) for h, s in zip(
                    raw_column_headers, table_skeleton[0]
                )
            ]
        )
        row_headers = VGroup(
            *[
                MathTex(
                    rf"\text{{{h.split(r'^')[0].split(r'_')[0]}}}_{h.split(r'^')[0].split(r'_')[1]}^{h.split(r'^')[1]}"
                ).scale(0.5).next_to(s, LEFT, buff=0.1).shift(s.width*RIGHT) for h, s in zip(raw_row_headers, [r[0] for r in table_skeleton[1:]])
            ]
        )
        if not show_animations:
            self.add(column_headers, row_headers)
        else:
            self.play(
                LaggedStart(
                    *[Write(c) for c in column_headers],
                    lag_ratio=0.125
                ),
                LaggedStart(
                    *[Write(c) for c in row_headers],
                    lag_ratio=0.125
                ),
                run_time=1
            )
            self.slide_pause()

        # table_values = VGroup(
        #     *[
        #         VGroup(
        #             *[
        #                 MathTex(v).next_to(s, LEFT, buff=0.05).shift(s.width*RIGHT) for v, s in zip(
        #                     row_values, row_cells
        #                 )
        #             ]
        #         ) for row_values, row_cells in zip(
        #
        #         )
        #     ]
        # )
        if show_animations:
            self.play(
                LaggedStart(
                    *[
                        LaggedStart(
                            *[FadeIn(c, shift=DOWN) for c in row[1:]],
                            lag_ratio=0.1
                        ) for row in table_skeleton[1:]
                    ],
                    lag_ratio=0.25
                ),
                run_time=2
            )
            self.slide_pause()
        table_values = VGroup()
        for anion, cell_rows in zip(raw_row_headers, table_skeleton[1:]):
            table_values.add(
                VGroup(*[
                    Tex(
                        data.loc[anion, cation]
                    # ).scale(0.75).next_to(s, LEFT, buff=0.1).shift(s.width*RIGHT) for cation, s in zip(
                    ).set_z_index(3).scale(0.75).move_to(s) for cation, s in zip(
                        raw_column_headers,
                        cell_rows[1:]
                    )
                ])
            )
            if not show_animations:
                [
                    s.set_style(
                        fill_color={"L": GREEN, "T": RED, "-": None, "N": YELLOW}[data.loc[anion, cation]], fill_opacity=0.15
                    ) for cation, s in zip(raw_column_headers, cell_rows[1:])
                ]
        if not show_animations:
            self.add(table_values)
        else:
            self.play(
                LaggedStart(
                    *[
                        LaggedStart(
                            *[
                                ReplacementTransform(VGroup(cat, an).copy(), val) for cat, val in zip(
                                    column_headers, row_values
                                )
                            ],
                            lag_ratio=0.1
                        ) for an, row_values in zip(row_headers, table_values)
                    ],
                    lag_ratio=0.5
                ),
                run_time=5
            )
            self.slide_pause()
            self.play(
                LaggedStart(
                    *[
                        LaggedStart(
                            *[
                                s.animate.set_style(
                                    fill_color={"L": GREEN, "T": RED, "-": None, "N": YELLOW}[data.loc[anion, cation]], fill_opacity=0.15
                                ) for cation, s in zip(raw_column_headers, cell_rows[1:])
                            ],
                            lag_ratio=0.05
                        ) for anion, cell_rows in zip(raw_row_headers, table_skeleton[1:])
                    ],
                    lag_ratio=0.25
                ),
                run_time=2
            )
            self.slide_pause()
        return table_skeleton, column_headers, row_headers, table_values

    def play_examples(self, table_info):
        table_skeleton, column_headers, row_headers, table_values = table_info
        in_mol1 = Sumformel("AgNO3").set_color(GREEN).set_z_index(5)
        in_mol2 = Sumformel("FeBr3").set_color(GREEN).set_z_index(in_mol1.get_z_index())
        in_ions1 = VGroup(
            column_headers[-1].copy(), row_headers[0].copy()
        ).scale(2).arrange(DOWN, buff=0.25, aligned_edge=RIGHT).set_z_index(in_mol1.get_z_index())
        in_ions2 = VGroup(
            column_headers[7].copy(), row_headers[2].copy()
        ).scale(2).arrange(DOWN, buff=0.25, aligned_edge=LEFT).set_z_index(in_mol1.get_z_index())

        out_mol1 = Sumformel("AgBr").set_color(RED).set_z_index(in_mol1.get_z_index())
        out_mol2 = Sumformel("Fe(NO3)3").set_color(GREEN).set_z_index(in_mol1.get_z_index())
        out_ions1 = VGroup(
            column_headers[-1].copy(), row_headers[2].copy()
        ).scale(2).arrange(DOWN, buff=0.25, aligned_edge=RIGHT).set_z_index(in_mol1.get_z_index())
        out_ions2 = VGroup(
            column_headers[7].copy(), row_headers[0].copy()
        ).scale(2).arrange(DOWN, buff=0.25, aligned_edge=LEFT).set_z_index(in_mol1.get_z_index())

        intro_text = VGroup(
            Tex("Eksempel på aflæsning: "), in_mol1, Tex(" + "), in_mol2
        ).arrange(RIGHT, buff=0.1).set_z_index(in_mol1.get_z_index())
        brect = get_background_rect(intro_text, buff=8, fill_opacity=0.825).shift(3.5*DOWN)
        intro_text.to_edge(RIGHT)
        # self.add(intro_text, brect)
        self.play(
            LaggedStart(
                FadeIn(brect, shift=4*UP, rate_func=rate_functions.ease_in_out_back),
                Write(intro_text, run_time=0.75),
                lag_ratio=0.75
            ),
            run_time=3
        )
        self.slide_pause()

        in_ions1.next_to(intro_text[1], DOWN, aligned_edge=RIGHT)
        in_ions2.next_to(intro_text[3], DOWN, aligned_edge=LEFT)
        self.play(
            TransformMatchingShapes(
                intro_text[1].copy(), in_ions1, transform_mismatches=False
            ),
            TransformMatchingShapes(
                intro_text[3].copy(), in_ions2, transform_mismatches=False
            )
        )
        self.slide_pause()

        explanation_texts = VGroup(
            Tex("1. Find de to stoffer i tabellen"),
            Tex("2. Tegn det rektangel, som udspændes af de to celler"),
            Tex("3. Skift diagonal"),
            Tex("4. Fjern rektanglet igen"),
            Tex("5. Aflæs, om et af de nye stoffer er tungtopløselige")
        ).scale(0.75).arrange(DOWN, aligned_edge=LEFT).to_edge(DL).set_z_index(intro_text.get_z_index())
        # self.add(explanation_texts[0])

        starting_rects = VGroup(
            table_skeleton[1][-1].copy().set_style(fill_opacity=0.8),
            table_skeleton[3][8].copy().set_style(fill_opacity=0.8)
        )
        # self.add(starting_rects)
        self.play(
            LaggedStart(
                Write(explanation_texts[0], run_time=0.75),
                FadeIn(starting_rects),
                lag_ratio=0.9
            ),
            run_time=1
        )
        self.slide_pause()

        rect = Rectangle(
            width=table_skeleton[0][0].width * 3,
            height=table_skeleton[0][0].height * 2,
            stroke_color=BLACK, stroke_width=10
        ).set_z_index(5).move_to(between_mobjects(table_skeleton[1][-1], table_skeleton[3][8]))
        starting_diag = Line(
            *starting_rects, stroke_width=10, stroke_color=color_gradient([r.get_color() for r in starting_rects], 2),
        ).set_z_index(rect.get_z_index())
        # self.add(explanation_texts[1])
        # self.add(rect, starting_diag)
        self.play(
            LaggedStart(
                Write(explanation_texts[1], run_time=0.75),
                GrowFromPoint(starting_diag, starting_diag.get_start()),
                FadeIn(rect),
                lag_ratio=0.5
            ),
            run_time=2
        )
        self.slide_pause()

        ending_rects = VGroup(
            table_skeleton[3][-1].copy().set_style(fill_opacity=0.8),
            table_skeleton[1][8].copy().set_style(fill_opacity=0.8)
        )
        ending_diag = Line(
            *ending_rects, stroke_width=10, stroke_color=color_gradient([r.get_color() for r in ending_rects], 2),
        ).set_z_index(rect.get_z_index())
        out_ions1.move_to(in_ions1)
        out_ions2.move_to(in_ions2)
        self.play(
            LaggedStart(
                Write(explanation_texts[2], run_time=0.75),
                AnimationGroup(
                    *[
                        ReplacementTransform(s, e) for s, e in zip(starting_rects, ending_rects)
                    ],
                    ReplacementTransform(starting_diag, ending_diag)
                ),
                AnimationGroup(
                    ReplacementTransform(
                        in_ions1[0], out_ions1[0]
                    ),
                    ReplacementTransform(
                        in_ions2[1], out_ions1[1], path_arc=PI
                    ),
                    ReplacementTransform(
                        in_ions2[0], out_ions2[0]
                    ),
                    ReplacementTransform(
                        in_ions1[1], out_ions2[1], path_arc=PI
                    )
                ),
                lag_ratio=0.9
            )
        )
        self.slide_pause()

        # self.add(explanation_texts[3])
        # self.remove(rect, ending_diag)
        self.play(
            LaggedStart(
                Write(explanation_texts[3], run_time=0.75),
                FadeOut(ending_diag),
                FadeOut(rect),
                lag_ratio=0.5
            ),
            run_time=2
        )
        self.slide_pause()

        # self.add(explanation_texts[4])
        # self.remove(ending_rects[1])
        self.play(
            LaggedStart(
                Write(explanation_texts[4], run_time=0.75),
                FadeOut(ending_rects[1]),
                lag_ratio=0.75
            ),
            run_time=2
        )
        self.slide_pause()

        outro_text = VGroup(
            Tex("Det bundfældende stof er derfor"), out_mol1, Tex(" og ikke "), out_mol2
        ).arrange(RIGHT, buff=0.1).to_edge(DR).set_z_index(in_mol1.get_z_index())
        self.play(
            TransformMatchingShapes(
                out_ions1, outro_text[1], transform_mismatches=False
            ),
            TransformMatchingShapes(
                out_ions2, outro_text[3], transform_mismatches=False
            ),
            FadeOut(explanation_texts),
        )
        self.slide_pause()

        self.play(
            LaggedStart(
                Write(outro_text[0]),
                Write(outro_text[2]),
                lag_ratio=0.5
            )
        )
        self.slide_pause()


class SolubilityTableThumbnail(SolubilityTable):
    def construct(self):
        table_info = VGroup(self.create_solubility_table(show_animations=False))
        table_info.shift(2*DOWN)
        title = Tex("Fældningsreaktioner").scale(2).to_edge(UL).set_color(YELLOW)
        srec = get_background_rect(title, stroke_colour=YELLOW)
        opgave_tekst = Tex("Med eksempel på aflæsning").scale(1.5).to_edge(DOWN).set_z_index(5)
        srec2 = get_background_rect(opgave_tekst, buff=10).shift(4*DOWN)
        self.add(title, srec, opgave_tekst, srec2)


if __name__ == "__main__":
    classes = [
        SolubilityTable,
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