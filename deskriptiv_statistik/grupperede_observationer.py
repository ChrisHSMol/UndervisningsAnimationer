from PIL.ImImagePlugin import number
from manim import *
import sys
sys.path.append("../")
import numpy as np
import subprocess
from helpers import *

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


class GrupperingAfData(MovingCameraScene, Slide if slides else Scene):
    def construct(self):
        title = Tex("Gruppering", " af data")
        title[0].set_color(YELLOW)
        play_title2(self, title)
        self.interval_notation()
        self.gruppering_af_data()
        self.wait(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t=t, slides_bool=slides_bool)

    def get_cmap(self):
        cmap = {
            "observation": BLUE
        }
        return cmap

    def data_to_DecNum(self, data, numdec=0, bsign=False):
        return VGroup(
            *[DecimalNumber(
                    val,
                    include_sign=bsign,
                    num_decimal_places=numdec,
                ).scale(0.5) for val in data]
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.1)

    def one_to_one_sort(self, data, desc=True):
        _numbers = [d.get_value() for d in data]
        _numbers.sort(reverse=desc)
        sorted_data = self.data_to_DecNum(_numbers).next_to(data, RIGHT, buff=2)

        num_of_each_value = {}
        dict_sorting = {}
        for i, d in enumerate(data):
            strVal = str(d.get_value())

            if strVal not in num_of_each_value.keys():
                num_of_each_value[strVal] = 0

            dict_sorting[d] = [
                s for s in sorted_data if s.get_value() == d.get_value()
            ][num_of_each_value[strVal]]

            num_of_each_value[strVal] += 1
        return sorted_data, dict_sorting

    def inddel_i_grupper(
            self,
            data: list[float],
            start: float = 0.0,
            end: float = 10.0,
            size: float = 2.0
    ):
        grupperinger = {}
        interval_starts = np.arange(start, end, size)
        interval_ends = interval_starts + size
        index_start, index_end = 0, len(data) - 1
        # print(interval_starts)
        for st, en in zip(interval_starts, interval_ends):
            # if st > max([x.get_value() for x in data]):
            #     index_end += 1
            #     continue
            # if en <= min([x.get_value() for x in data]):
            #     index_start += 1
            #     continue
            label = f"[{st}; {en}["
            hyps = len(
                [x for x in data if st <= x.get_value() < en]
            )
            grupperinger[label] = hyps
        # print(grupperinger)
        return grupperinger, interval_starts[index_start:index_end], interval_ends[index_start:index_end]

    def prepare_table(
            self,
            data: list[float],
            cell_width: float = 1.5,
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
        different_numbers = np.unique(data)
        num_different_numbers = len(different_numbers)

        tabel_struktur = VGroup()
        for j in range(num_different_numbers + row_offset):
            row = VGroup()
            for i in range(5 + col_offset):
                row.add(
                    VGroup(
                        Rectangle(width=cell_width, height=cell_height, stroke_width=1),
                        Rectangle(
                            width=cell_width - 0.05, height=cell_height - 0.05, fill_opacity=0,
                            stroke_width=3 if include_coloured_inlay else 0,
                            stroke_color=[*[BLACK for _ in range(1+col_offset)], BLUE, BLUE, YELLOW, YELLOW][i],
                            stroke_opacity=[*[0 for _ in range(1+col_offset)], 0.5, 0.75, 0.5, 0.75][i]
                        )
                    )
                )
            row.arrange(RIGHT, buff=0)
            tabel_struktur.add(row)
        tabel_struktur.arrange(DOWN, buff=0)
        # TODO: coloured inlay to each rect

        _tabel_raw = []
        _tabel = []
        kumhyp = 0
        kumfre = 0
        for i, obs in enumerate(different_numbers):
            hyp = len([d for d in data if d == obs])
            kumhyp += hyp
            fre = hyp/len(data)
            kumfre += fre
            _tabel_raw.append([obs, hyp, kumhyp, fre, kumfre])
            _tabel.append([
                str(obs), str(hyp), str(kumhyp), f"{fre*100:.{numdecs[0]}f} \\%", f"{kumfre*100:.{numdecs[1]}f} \\%"
            ])

        tabel_data_raw = np.array(_tabel_raw)
        tabel_data = VGroup(*[
            VGroup(*[
                MathTex(d, font_size=22).move_to(tabel_struktur[j+row_offset][i+col_offset]) for i, d in enumerate(row)
            ]) for j, row in enumerate(_tabel)
        ])
        return tabel_struktur, tabel_data, tabel_data_raw

    def interval_notation(self):
        cmap = {
            "x": YELLOW,
            "mindre": BLUE,
            "større": RED,
            "tal": GREEN
        }
        intro_tekst = VGroup(
            Tex("Før vi inddeler data i grupper, "),
            Tex("skal vi se, hvordan man skriver intervaller.")
        ).arrange(DOWN, aligned_edge=LEFT)
        x_lt_4 = VGroup(
            MathTex("x", " < ", "4").scale(1.5),
            VGroup(
                Tex("Her kan {{$x$}} være alle tal, som er {{mindre end}} {{4}},"),
                Tex("og kan ikke være {{4}}.")
            ).scale(0.75).arrange(DOWN, aligned_edge=LEFT)
        ).arrange(DOWN, buff=1).shift(DOWN)
        self.play(
            Write(intro_tekst),
            run_time=2
        )
        self.play(
            intro_tekst.animate.scale(0.75).arrange(RIGHT).to_edge(UP),
            FadeIn(x_lt_4, shift=0.5*DOWN),
            run_time=2
        )
        self.slide_pause()

        self.play(
            Circumscribe(x_lt_4[0][0], color=cmap["x"], fade_out=True),
            Circumscribe(x_lt_4[1][0][1], color=cmap["x"], fade_out=True),
            x_lt_4[0][0].animate.set_color(cmap["x"]),
            x_lt_4[1][0][1].animate.set_color(cmap["x"]),
            run_time=2
        )
        self.play(
            Circumscribe(x_lt_4[0][1], color=cmap["mindre"], fade_out=True),
            Circumscribe(x_lt_4[1][0][3], color=cmap["mindre"], fade_out=True),
            x_lt_4[0][1].animate.set_color(cmap["mindre"]),
            x_lt_4[1][0][3].animate.set_color(cmap["mindre"]),
            run_time=2
        )
        self.play(
            Circumscribe(x_lt_4[0][2], color=cmap["tal"], fade_out=True),
            Circumscribe(x_lt_4[1][0][5], color=cmap["tal"], fade_out=True),
            Circumscribe(x_lt_4[1][1][1], color=cmap["tal"], fade_out=True),
            x_lt_4[0][2].animate.set_color(cmap["tal"]),
            x_lt_4[1][0][5].animate.set_color(cmap["tal"]),
            x_lt_4[1][1][1].animate.set_color(cmap["tal"]),
            run_time=2
        )
        self.slide_pause()

        x_leq_4 = VGroup(
            MathTex("x", r" \leq ", "4").scale(1.5),
            Tex("Her kan {{$x$}} være alle tal, som er {{mindre end eller lig med}} {{4}}").scale(0.75)
        ).arrange(DOWN, buff=1).shift(DOWN)
        x_leq_4[0][0].set_color(cmap["x"])
        x_leq_4[0][1].set_color(cmap["mindre"])
        x_leq_4[0][2].set_color(cmap["tal"])
        x_leq_4[1][1].set_color(cmap["x"])
        x_leq_4[1][3].set_color(cmap["mindre"])
        x_leq_4[1][5].set_color(cmap["tal"])
        self.play(
            TransformMatchingTex(x_lt_4[0], x_leq_4[0], transform_mismatches=True),
            TransformMatchingTex(x_lt_4[1], x_leq_4[1], transform_mismatches=True),
            run_time=1
        )
        self.slide_pause()

        x_gt_2 = VGroup(
            MathTex("x", " > ", "2").scale(1.5),
            VGroup(
                Tex("Her kan {{$x$}} være alle tal, som er {{større end}} {{2}},"),
                Tex("og kan ikke være {{2}}.")
            ).scale(0.75).arrange(DOWN, aligned_edge=LEFT)
        ).arrange(DOWN, buff=1).shift(DOWN)
        x_gt_2[0][0].set_color(cmap["x"])
        x_gt_2[1][0][1].set_color(cmap["x"])
        x_gt_2[0][1].set_color(cmap["større"])
        x_gt_2[1][0][3].set_color(cmap["større"])
        x_gt_2[0][2].set_color(cmap["tal"])
        x_gt_2[1][0][5].set_color(cmap["tal"])
        x_gt_2[1][1][1].set_color(cmap["tal"])
        self.play(
            TransformMatchingTex(x_leq_4[0], x_gt_2[0], transform_mismatches=True),
            TransformMatchingTex(x_leq_4[1], x_gt_2[1], transform_mismatches=True),
            run_time=1
        )
        self.slide_pause()

        x_geq_2 = VGroup(
            MathTex("x", r" \geq ", "2").scale(1.5),
            Tex("Her kan {{$x$}} være alle tal, som er {{større end eller lig med}} {{2}}").scale(0.75)
        ).arrange(DOWN, buff=1).shift(DOWN)
        x_geq_2[0][0].set_color(cmap["x"])
        x_geq_2[0][1].set_color(cmap["større"])
        x_geq_2[0][2].set_color(cmap["tal"])
        x_geq_2[1][1].set_color(cmap["x"])
        x_geq_2[1][3].set_color(cmap["større"])
        x_geq_2[1][5].set_color(cmap["tal"])
        self.play(
            TransformMatchingTex(x_gt_2[0], x_geq_2[0], transform_mismatches=True),
            TransformMatchingTex(x_gt_2[1], x_geq_2[1], transform_mismatches=True),
            run_time=1
        )
        self.slide_pause()

        x_in_2_4_excl_ineq = VGroup(
            MathTex("2", "<", "x", "<", "4").scale(1.5),
            VGroup(
                Tex("Her kan {{$x$}} være alle tal, som er {{større end}} {{2}}, men ikke {{2}},"),
                Tex("og som samtidig er {{mindre end}} {{4}}, men ikke {{4}}.")
            ).scale(0.75).arrange(DOWN, aligned_edge=LEFT)
        ).arrange(DOWN, buff=1).shift(DOWN)
        x_in_2_4_excl_ineq[0][2].set_color(cmap["x"])
        x_in_2_4_excl_ineq[1][0][1].set_color(cmap["x"])
        x_in_2_4_excl_ineq[0][1].set_color(cmap["større"])
        x_in_2_4_excl_ineq[1][0][3].set_color(cmap["større"])
        x_in_2_4_excl_ineq[0][3].set_color(cmap["mindre"])
        x_in_2_4_excl_ineq[1][1][1].set_color(cmap["mindre"])
        x_in_2_4_excl_ineq[0][0].set_color(cmap["tal"])
        x_in_2_4_excl_ineq[0][4].set_color(cmap["tal"])
        x_in_2_4_excl_ineq[1][0][5].set_color(cmap["tal"])
        x_in_2_4_excl_ineq[1][0][7].set_color(cmap["tal"])
        x_in_2_4_excl_ineq[1][1][3].set_color(cmap["tal"])
        x_in_2_4_excl_ineq[1][1][5].set_color(cmap["tal"])
        self.play(
            LaggedStart(
                FadeOut(x_geq_2, shift=UP),
                FadeIn(x_in_2_4_excl_ineq, shift=UP)
            )
        )
        self.slide_pause()

        x_in_2_4_incl_ineq = VGroup(
            MathTex("2", r"\leq", "x", r"\leq", "4").scale(1.5),
            VGroup(
                Tex("Her kan {{$x$}} være alle tal, som er {{større end eller lig med}} {{2}},"),
                Tex("og som samtidig er {{mindre end eller lig med}} {{4}}.")
            ).scale(0.75).arrange(DOWN, aligned_edge=LEFT)
        ).arrange(DOWN, buff=1).shift(DOWN)
        x_in_2_4_incl_ineq[0][2].set_color(cmap["x"])
        x_in_2_4_incl_ineq[1][0][1].set_color(cmap["x"])
        x_in_2_4_incl_ineq[0][1].set_color(cmap["større"])
        x_in_2_4_incl_ineq[1][0][3].set_color(cmap["større"])
        x_in_2_4_incl_ineq[0][3].set_color(cmap["mindre"])
        x_in_2_4_incl_ineq[1][1][1].set_color(cmap["mindre"])
        x_in_2_4_incl_ineq[0][0].set_color(cmap["tal"])
        x_in_2_4_incl_ineq[0][4].set_color(cmap["tal"])
        x_in_2_4_incl_ineq[1][0][5].set_color(cmap["tal"])
        x_in_2_4_incl_ineq[1][1][3].set_color(cmap["tal"])
        self.play(
            x_in_2_4_excl_ineq[0].animate.scale(0.8).next_to(intro_tekst, DOWN, aligned_edge=LEFT),
            FadeOut(x_in_2_4_excl_ineq[1], shift=UP),
            FadeIn(x_in_2_4_incl_ineq, shift=UP)
        )
        self.slide_pause()

        self.play(
            x_in_2_4_incl_ineq[0].animate.scale(0.8).next_to(intro_tekst, DOWN, aligned_edge=RIGHT),
            FadeOut(x_in_2_4_incl_ineq[1], shift=UP)
        )
        self.slide_pause()

        x_in_2_4_inex_ineq = MathTex(
            "2", r"\leq", "x", r"<", "4"
        ).scale(1.5*0.8).next_to(x_in_2_4_excl_ineq[0], RIGHT, buff=0.5)
        x_in_2_4_exin_ineq = MathTex(
            "2", r"<", "x", r"\leq", "4"
        ).scale(1.5*0.8).next_to(x_in_2_4_incl_ineq[0], LEFT, buff=0.5)
        for i, col in enumerate([cmap["tal"], cmap["større"], cmap["x"], cmap["mindre"], cmap["tal"]]):
            x_in_2_4_inex_ineq[i].set_color(col)
            x_in_2_4_exin_ineq[i].set_color(col)
        self.play(
            ReplacementTransform(x_in_2_4_excl_ineq[0].copy(), x_in_2_4_inex_ineq),
            ReplacementTransform(x_in_2_4_incl_ineq[0].copy(), x_in_2_4_exin_ineq)
        )
        self.slide_pause()

        ineqs = VGroup(
            x_in_2_4_excl_ineq[0], x_in_2_4_inex_ineq, x_in_2_4_exin_ineq, x_in_2_4_incl_ineq[0]
        ).next_to(intro_tekst, DOWN)
        self.play(
            ineqs.animate.scale(0.8).arrange(RIGHT, buff=1).next_to(intro_tekst, DOWN),
            run_time=0.5
        )
        dividers = VGroup(
            *[
                DashedLine(
                    start=between_mobjects(ineqs[i], ineqs[i+1]) + 0.5*ineqs.get_height()*UP,
                    end=between_mobjects(ineqs[i], ineqs[i+1]) + 3*DOWN,
                    stroke_width=0.5
                ) for i in range(len(ineqs) - 1)
            ]
        )
        self.play(
            Create(dividers),
            run_time=0.5
        )
        self.slide_pause()

        numberline = NumberLine(
            x_range=(0, 6, 1),
            length=7,
            include_tip=True,
            include_numbers=True,
        ).to_edge(DOWN).shift(UP)
        numberline.numbers[2].set_color(cmap["tal"])
        numberline.numbers[4].set_color(cmap["tal"])
        self.play(
            DrawBorderThenFill(numberline)
        )
        self.slide_pause()

        intervals = VGroup()
        dotlines = VGroup()
        for i, ineq in enumerate(ineqs):
            incs = []
            for c in [ineq[1].get_tex_string(), ineq[3].get_tex_string()]:
                if "\\" in c:
                    incs.append(True)
                else:
                    incs.append(False)
            dots = VGroup(
                Dot(
                    numberline.n2p(int(ineq[0].get_tex_string())), stroke_color=ineq[1].get_color(), stroke_width=2,
                    fill_color=ineq[1].get_color() if incs[0] else BLACK, fill_opacity=1, radius=0.1
                ),
                Dot(
                    numberline.n2p(int(ineq[4].get_tex_string())), stroke_color=ineq[-2].get_color(), stroke_width=2,
                    fill_color=ineq[-2].get_color() if incs[1] else BLACK, fill_opacity=1, radius=0.1
                )
            )
            line = Line(
                start=dots[0], end=dots[1], stroke_color=ineq[2].get_color(), stroke_width=4
            )
            dotline = VGroup(dots[0], line, dots[1])
            dotlines.add(dotline)
            icop = ineq.copy()
            self.play(
                icop.animate.next_to(dots, UP, buff=1)
            )
            self.play(
                LaggedStart(
                    DrawBorderThenFill(dots[0]),
                    Create(line),
                    DrawBorderThenFill(dots[1]),
                    lag_ratio=0.75
                )
            )
            # self.slide_pause()

            interval = MathTex(
                "[" if incs[0] else "]",
                f"{int(ineq[0].get_tex_string()):.0f}",
                "; ",
                f"{int(ineq[4].get_tex_string()):.0f}",
                "]" if incs[1] else "["
            ).next_to(numberline, DOWN)
            interval[0].set_color(ineq[1].get_color())
            interval[1].set_color(ineq[0].get_color())
            interval[3].set_color(ineq[4].get_color())
            interval[4].set_color(ineq[3].get_color())
            intervals.add(interval)
            self.play(
                Write(interval)
            )
            self.slide_pause()

            self.play(
                FadeOut(icop, shift=ineq.get_center() - icop.get_center()),
                dotline.animate.next_to(ineq, DOWN, buff=0.5),
                interval.animate.next_to(ineq, DOWN, buff=1)
            )

        forklaring = Tex(
            "De 3 formuleringer i hver kolonne\\\\"
            "beskriver præcist det samme,\\\\"
            "og er derfor 3 forskellige måder at skrive det samme."
        ).to_edge(DOWN)
        self.play(
            FadeOut(numberline),
            Write(forklaring)
        )
        self.slide_pause()

        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=1
        )

    def gruppering_af_data(self):
        cmap = self.get_cmap()
        data_raw = [8, 4, 16, 8, 9, 6, 16, 19, 7, 6, 4, 8, 11, 8, 9, 6, 9, 10, 11, 8, 14, 4, 6, 7, 10]
        data = self.data_to_DecNum(data_raw).to_edge(LEFT, buff=0.5)
        sorted_data, sorting_dict = self.one_to_one_sort(data, desc=False)
        grupperinger, interval_starts, interval_ends = self.inddel_i_grupper(data, start=0, end=20, size=2)

        self.play(
            LaggedStart(
                *[DrawBorderThenFill(d) for d in data],
                lag_ratio=0.1
            ),
            run_time=1
        )
        self.slide_pause()

        self.play(
            LaggedStart(
                *[TransformFromCopy(k, v) for k, v in sorting_dict.items()],
                lag_ratio=0.1
            ),
            run_time=2
        )
        self.slide_pause()

        tabel_struktur = VGroup()
        for j in range(len(grupperinger) + 1):
            row = VGroup()
            # for i in range(5):
            for i in range(2):
                row.add(
                    VGroup(
                        Rectangle(width=1.5, height=0.65, stroke_width=1),
                        Rectangle(
                            width=1.5 - 0.05, height=0.65 - 0.05, fill_opacity=0,
                            stroke_width=3,
                            stroke_color=[BLACK, BLUE, BLUE, YELLOW, YELLOW][i],
                            stroke_opacity=[0, 0.5, 0.75, 0.5, 0.75][i]
                        )
                    )
                )
            row.arrange(RIGHT, buff=0)
            tabel_struktur.add(row)
        tabel_struktur.arrange(DOWN, buff=0).to_edge(RIGHT)
        self.play(
            LaggedStart(
                *[DrawBorderThenFill(r, lag_ratio=0.05) for r in tabel_struktur],
                lag_ratio=0.05
            )
        )
        col_labels = VGroup(*[Tex(d, font_size=22).move_to(tabel_struktur[0][i]) for i, d in enumerate([
            "Interval", "Hyppighed"#, "Kumuleret\\\\hyppighed", "Frekvens", "Kumuleret\\\\frekvens"
        ])])
        self.play(
            Write(col_labels, lag_ratio=0.1)
        )
        self.slide_pause()

        intervaller = VGroup(
            *[
                VGroup(MathTex(l), Integer(v)).scale(0.8).arrange(RIGHT, buff=1) for l, v in grupperinger.items()
            ]
        )
        for i, interval in enumerate(intervaller):
            interval[0].move_to(tabel_struktur[i+1][0])
            interval[1].move_to(tabel_struktur[i+1][1])

        for interval, low, high in zip(intervaller, interval_starts, interval_ends):
            self.play(
                Write(interval[0])
            )
            self.slide_pause()

            self.play(
                LaggedStart(
                    *[Indicate(m, scale_factor=1.5, color=cmap["observation"]) for m in sorted_data],
                    *[m.animate.set_color(cmap["observation"]) for m in sorted_data if low <= m.get_value() < high],
                    lag_ratio=0.25
                ),
                run_time=2
            )
            self.slide_pause()

            if interval[1].get_value() == 0:
                self.play(
                    FadeIn(interval[1]),
                    *[m.animate.set_color(WHITE) for m in sorted_data]
                )
            else:
                self.play(
                    ReplacementTransform(
                        VGroup(*[m.copy() for m in sorted_data if low <= m.get_value() < high]), interval[1]
                    ),
                    *[m.animate.set_color(WHITE) for m in sorted_data]
                )
            self.slide_pause()


if __name__ == "__main__":
    classes = [
        GrupperingAfData
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
