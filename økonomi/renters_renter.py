from manim import *
import sys
sys.path.append("../")
import numpy as np
import subprocess
from helpers import *

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


class RentersRegning(MovingCameraScene, Slide if slides else Scene):
    b = 100
    r = 0.10
    def construct(self):
        # self.tabeludregning()
        self.udledning()
        self.slide_pause(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides_bool)

    def prepare_table(
            self,
            b: float,
            r: float,
            n: int,
            edge: list[float] = None,
            cell_width: float = 1.6,
            cell_height: float = 0.65,
            include_header_row: bool = False,
            include_label_column: bool = False,
            include_coloured_inlay: bool = True,
            numdecs: list[int] = None,
    ):
        if numdecs is None:
            numdecs = [0, 0]
        row_offset = int(include_header_row)
        col_offset = int(include_label_column)

        tabel_struktur = VGroup()
        for j in range(n + row_offset):
            row = VGroup()
            for i in range(5 + col_offset):
                row.add(
                    VGroup(
                        Rectangle(width=cell_width, height=cell_height, stroke_width=1),
                        Rectangle(
                            width=cell_width - 0.05, height=cell_height - 0.05, fill_opacity=0,
                            stroke_width=3 if include_coloured_inlay else 0,
                            stroke_color=[*[BLACK for _ in range(col_offset)], RED, BLUE, YELLOW, YELLOW, BLUE][i],
                            stroke_opacity=[*[0 for _ in range(col_offset)], 0.75, 0.75, 0.75, 0.5, 0.5][i]
                        )
                    )
                )
            row.arrange(RIGHT, buff=0)
            tabel_struktur.add(row)
        tabel_struktur.arrange(DOWN, buff=0)
        if edge is not None:
            tabel_struktur.to_edge(edge)

        _tabel_raw = []
        _tabel = []
        terms = np.arange(1, n+1)
        for i, term in enumerate(terms):
            old = b * (1 + r) ** i
            new = b * (1 + r) ** term
            diff = new - old
            _tabel_raw.append(
                [term, old, r, diff, new]
            )
            _tabel.append(
                [
                    Integer(term),
                    DecimalNumber(old, num_decimal_places=2),
                    Integer(r*100, unit=r" \%"),
                    DecimalNumber(diff, num_decimal_places=2),
                    DecimalNumber(new, num_decimal_places=2)
                ]
            )

        tabel_data_raw = np.array(_tabel_raw)
        tabel_data = VGroup(*[
            VGroup(*[
                d.scale(0.5).move_to(tabel_struktur[j+row_offset][i+col_offset]) for i, d in enumerate(row)
            ]) for j, row in enumerate(_tabel)
        ])
        return tabel_struktur, tabel_data, tabel_data_raw

    def tabeludregning(self):
        tabel_struktur, tabel_data, tabel_data_raw = self.prepare_table(
            b=self.b,
            r=self.r,
            n=10,
            include_header_row=True,
            edge=LEFT
        )
        col_labels = VGroup(*[Tex(d, font_size=22).move_to(tabel_struktur[0][i]) for i, d in enumerate([
            "Termin", "Gammel saldo", r"Rente (\%)", "Rente (kr.)", "Ny saldo"
        ])])
        self.play(
            LaggedStart(
                *[DrawBorderThenFill(r, lag_ratio=0.05) for r in tabel_struktur],
                Write(col_labels, lag_ratio=0.1),
                lag_ratio=0.05
            )
        )
        self.play(
            Write(tabel_data[0][:3], lag_ratio=0.1)
        )
        # self.add(tabel_struktur, tabel_data[0][:3], col_labels)

        eq_kr = VGroup(
            tabel_data[0][1].copy().scale(2),
            MathTex(r"\cdot"),
            tabel_data[0][2].copy().scale(2),
            MathTex(f" = ", f"{tabel_data_raw[0][1] * tabel_data_raw[0][2]:.2f}")
        ).scale(0.95).arrange(RIGHT).to_edge(UR)
        eq_saldo = VGroup(
            eq_kr[0].copy(),
            MathTex(r"+"),
            eq_kr[3][1].copy(),
            MathTex(f" = ", f"{tabel_data_raw[0][1] * (1+tabel_data_raw[0][2]):.2f}")
        ).scale(0.95).arrange(RIGHT).next_to(eq_kr, DOWN, aligned_edge=RIGHT)
        # self.add(eq_kr, eq_saldo)
        self.play(
            ReplacementTransform(tabel_data[0][1].copy(), eq_kr[0]),
            ReplacementTransform(tabel_data[0][2].copy(), eq_kr[2]),
            ReplacementTransform(tabel_struktur[1][1].copy(), eq_kr[1]),
            ReplacementTransform(tabel_struktur[1][2].copy(), eq_kr[3][0]),
        )
        self.play(
            FadeIn(eq_kr[3][1], shift=RIGHT)
        )
        self.slide_pause()

        self.play(
            ReplacementTransform(eq_kr[3][1].copy(), tabel_data[0][3]),
            ReplacementTransform(eq_kr[3][1].copy(), eq_saldo[2]),
            ReplacementTransform(eq_kr[2].copy(), eq_saldo[0]),
            ReplacementTransform(eq_kr[1].copy(), eq_saldo[1]),
            ReplacementTransform(eq_kr[3][0].copy(), eq_saldo[3][0]),
        )
        self.play(
            FadeIn(eq_saldo[3][1], shift=RIGHT)
        )
        self.slide_pause()

        self.play(
            ReplacementTransform(eq_saldo[3][1].copy(), tabel_data[0][4])
        )

        # for i, row in enumerate(tabel_struktur[2:]):
        #     self.play(
        #         FadeIn(tabel_data[i+1][0], shift=DOWN),
        #         FadeIn(tabel_data[i+1][2], shift=DOWN),
        #         ReplacementTransform(tabel_struktur[i+1][-1].copy(), tabel_struktur[i+2][1]),
        #         ReplacementTransform(tabel_data[i][-1].copy(), tabel_data[i+1][1])
        #     )
        #     self.slide_pause(0.1)
        #
        #     self.play(
        #         ReplacementTransform(
        #             VGroup(*tabel_data[i+1][1:3]).copy(),
        #             tabel_data[i + 1][3]
        #         )
        #     )
        #     self.slide_pause(0.1)
        #
        #     self.play(
        #         ReplacementTransform(
        #             VGroup(tabel_data[i+1][1], tabel_data[i+1][3]).copy(),
        #             tabel_data[i + 1][4]
        #         )
        #     )
        for i, row in enumerate(tabel_struktur[2:]):
            eq_kr_ny = VGroup(
                tabel_data[i+1][1].copy().scale(2),
                MathTex(r"\cdot"),
                tabel_data[i+1][2].copy().scale(2),
                MathTex(f" = ", f"{tabel_data_raw[i+1][1] * tabel_data_raw[i+1][2]:.2f}")
            ).scale(0.95).arrange(RIGHT).to_edge(UR)
            eq_saldo_ny = VGroup(
                eq_kr_ny[0].copy(),
                MathTex(r"+"),
                eq_kr_ny[3][1].copy(),
                MathTex(f" = ", f"{tabel_data_raw[i+1][1] * (1+tabel_data_raw[i+1][2]):.2f}")
            ).scale(0.95).arrange(RIGHT).next_to(eq_kr, DOWN, aligned_edge=RIGHT)
            self.play(
                FadeIn(tabel_data[i+1][0], shift=DOWN),
                FadeIn(tabel_data[i+1][2], shift=DOWN),
                ReplacementTransform(tabel_struktur[i+1][-1].copy(), tabel_struktur[i+2][1]),
                ReplacementTransform(tabel_data[i][-1].copy(), tabel_data[i+1][1]),
                LaggedStart(
                    AnimationGroup(*[
                        ReplacementTransform(ob1, ob2) for ob1, ob2 in zip(eq_kr, eq_kr_ny)
                    ]),
                    AnimationGroup(*[
                        ReplacementTransform(ob1, ob2) for ob1, ob2 in zip(eq_saldo, eq_saldo_ny)
                    ]),
                    lag_ratio=1
                ),
                run_time=2
            )
            self.slide_pause(0.1)
            self.play(
                ReplacementTransform(
                    VGroup(*tabel_data[i+1][1:3]).copy(),
                    tabel_data[i + 1][3]
                )
            )
            self.slide_pause(0.1)

            self.play(
                ReplacementTransform(
                    VGroup(tabel_data[i+1][1], tabel_data[i+1][3]).copy(),
                    tabel_data[i + 1][4]
                )
            )
            self.slide_pause(0.1)
            eq_kr = eq_kr_ny
            eq_saldo = eq_saldo_ny

        self.slide_pause()

    def get_cmap(self):
        cmap = {
            "K_0": RED,
            "n": YELLOW,
            "K_n": GREEN,
            "r": BLUE,
            "a": BLUE_B
        }
        return cmap

    def udledning(self):
        black_box = FullScreenRectangle(fill_color=BLACK, fill_opacity=1).scale(1.1)
        self.add(black_box)
        cmap = self.get_cmap()

        equation1 = VGroup(
            MathTex(f"{self.b:.2f}", "+", f"{self.b:.2f}", r"\cdot", rf"{self.r*100:.2f} \%", "=", r"\text{Ny saldo}"),
            MathTex(f"{self.b:.2f}", "+", f"{self.b:.2f}", r"\cdot", rf"{self.r:.2f}", "=", r"\text{Ny saldo}"),
            MathTex(f"{self.b:.2f}", r"\cdot", r"\left(", "1", "+", rf"{self.r:.2f}", r"\right)", "=", r"\text{Ny saldo}"),
            MathTex(f"{self.b:.2f}", r"\cdot", rf"{1+self.r:.2f}", "=", r"\text{Ny saldo}"),
            MathTex(f"{self.b:.2f}", r"\cdot", rf"{1+self.r:.2f}^1", "=", f"{self.b * (self.r+1):.2f}"),
        ).arrange(ORIGIN, aligned_edge=RIGHT)
        self.add(equation1[0])
        for i, eq in enumerate(equation1[1:]):
            self.play(
                TransformMatchingTex(equation1[i], eq, transform_mismatches=True)
            )
            self.slide_pause(0.1)

        equations = VGroup(
            equation1[-1]
        )
        # self.play(
        #     equations.animate.shift(UP)
        # )
        # self.slide_pause(0.1)
        for i in range(1):
            self.play(
                equations.animate.to_edge(RIGHT)
            )
            self.slide_pause(0.1)
            equation = VGroup(
                MathTex(f"{self.b * (1+self.r)**(i+1):.2f}", r"\cdot", f"{1+self.r:.2f}", "=", r"\text{Ny saldo}"),
            )
            for j in range(i+1):
                eq_string = [f"{self.b * (1+self.r)**(i-j):.2f}"]
                for _ in range(j+1):
                    eq_string.append(r"\cdot")
                    eq_string.append(f"{1+self.r:.2f}")
                eq_string.append(r"\cdot")
                eq_string.append(f"{1+self.r:.2f}")
                eq_string.append("=")
                eq_string.append(r"\text{Ny saldo}")
                equation.add(
                    MathTex(
                        *eq_string
                    ),
                )
            equation.add(
                MathTex(f"{self.b:.2f}", r"\cdot", f"{1+self.r:.2f}^{i+2}", "=", r"\text{Ny saldo}"),
                MathTex(f"{self.b:.2f}", r"\cdot", f"{1+self.r:.2f}^{i+2}", "=", f"{self.b * (1+self.r)**(i+2):.2f}")
            )
            equation.arrange(ORIGIN, aligned_edge=RIGHT).next_to(equations[-1], DOWN, aligned_edge=RIGHT)
            self.play(
                *[
                    ReplacementTransform(ob1.copy(), ob2) for ob1, ob2 in zip(equations[-1][-1], equation[0])
                ]
            )
            self.slide_pause(0.1)
            for j, eq in enumerate(equation[1:]):
                self.play(
                    TransformMatchingTex(equation[j], eq, transform_mismatches=True)
                )
                self.slide_pause(0.1)
            equations.add(equation[-1])

        self.play(
            equations.animate.move_to(ORIGIN)
        )
        self.slide_pause(0.1)

        k0_text = MathTex(r"K_0", color=cmap["K_0"]).next_to(equations[-1][0], DOWN)
        self.play(
            LaggedStart(
                *[eq[0].animate.set_color(cmap["K_0"]) for eq in equations],
                FadeIn(k0_text, shift=DOWN),
                lag_ratio=0.25
            ),
            run_time=1
        )
        self.slide_pause(0.1)

        kn_text = MathTex(r"K_n", color=cmap["K_n"]).next_to(equations[-1][-1], DOWN)
        self.play(
            LaggedStart(
                *[eq[-1].animate.set_color(cmap["K_n"]) for eq in equations],
                FadeIn(kn_text, shift=DOWN),
                lag_ratio=0.25
            ),
            run_time=1
        )
        self.slide_pause(0.1)

        n_text = MathTex(r"n", color=cmap["n"]).next_to(equations[-1][2][-1], DOWN, aligned_edge=RIGHT)
        self.play(
            LaggedStart(
                *[eq[2][-1].animate.set_color(cmap["n"]) for eq in equations],
                FadeIn(n_text, shift=DOWN),
                lag_ratio=0.25
            ),
            run_time=1
        )
        self.slide_pause(0.1)

        a_text = MathTex(r"a", color=cmap["r"]).next_to(equations[-1][2][:-1], DOWN)
        self.play(
            LaggedStart(
                *[eq[2][:-1].animate.set_color(cmap["r"]) for eq in equations],
                FadeIn(a_text, shift=DOWN),
                lag_ratio=0.25
            ),
            run_time=1
        )
        self.slide_pause(0.1)

        # base_equation = VGroup(
        #     *[o.copy() for o in (k0_text, signs[0], a_text, n_text, signs[1], kn_text)]
        # ).arrange(RIGHT)
        base_equation = MathTex(
            r"K_0", r"\cdot", "", "a", "", r"^n", "=", r"K_n"
        ).set_color_by_tex_to_color_map(cmap)
        self.play(
            *[LaggedStart(
                *[
                    FadeOut(b, shift=b.get_center()) for b in line
                ],
                lag_ratio=0.1
            ) for line in equations],
            # *[
            #     ReplacementTransform(o1, o2) for o1, o2 in zip(
            #         (k0_text, a_text, n_text, kn_text), base_equation
            #     )
            # ]
            TransformMatchingTex(
                VGroup(k0_text, a_text, n_text, kn_text), base_equation, transform_mismatches=True
            )
        )
        self.slide_pause(0.1)

        ligning = MathTex(
            r"K_0", r"\cdot", r"\left(1+", "r", r"\right)", r"^n", "=", r"K_n"
        ).set_color_by_tex_to_color_map(cmap)
        ligning[4].set_color(WHITE)
        self.play(
            TransformMatchingTex(base_equation, ligning, transform_mismatches=True)
        )


if __name__ == "__main__":
    classes = [
        RentersRegning
    ]
    for cls in classes:
        class_name = cls.__name__
        command = rf"manim {sys.argv[0]} {class_name} -p --resolution={_RESOLUTION[q]} --frame_rate={_FRAMERATE[q]}"
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
