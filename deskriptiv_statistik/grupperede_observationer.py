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


class Histogrammer(GrupperingAfData):
    def construct(self):
        # title = Tex("Histogram", " fra tabel")
        # title[0].set_color(YELLOW)
        # play_title2(self, title)
        # self.histogram_fra_hyppighedstabel()
        self.varierende_intervalbredde()
        self.wait(5)

    def get_cmap(self):
        return None

    def histogram_fra_hyppighedstabel(self):
        cmap = self.get_cmap()
        data_raw = [8, 4, 16, 8, 9, 6, 16, 19, 7, 6, 4, 8, 11, 8, 9, 6, 9, 10, 11, 8, 14, 4, 6, 7, 10]
        data = self.data_to_DecNum(data_raw).to_edge(LEFT, buff=0.5)
        sorted_data, sorting_dict = self.one_to_one_sort(data, desc=False)
        grupperinger, interval_starts, interval_ends = self.inddel_i_grupper(data, start=0, end=20, size=2)
        tabel_struktur, tabel_data, tabel_data_raw = self.prepare_table(data_raw, include_header_row=True)
        col_labels = VGroup(*[Tex(d, font_size=22).move_to(tabel_struktur[0][i]) for i, d in enumerate([
            "Interval", "Hyppighed", "Kumuleret\\\\hyppighed", "Frekvens", "Kumuleret\\\\frekvens"
        ])])

        self.play(
            LaggedStart(
                *[DrawBorderThenFill(r, lag_ratio=0.05) for r in tabel_struktur],
                Write(col_labels, lag_ratio=0.1),
                lag_ratio=0.05
            )
        )
        # self.slide_pause()

        intervaller = VGroup(
            *[MathTex(l).scale(0.8).move_to(tabel_struktur[i+1][0]) for i, l in enumerate(grupperinger.keys())]
        )
        hyppigheder = VGroup(
            *[Integer(v).move_to(tabel_struktur[i+1][1]) for i, v in enumerate(grupperinger.values())]
        )
        self.play(
            LaggedStart(
                *[
                    Write(i) for i in intervaller
                ],
                *[
                    Write(i) for i in hyppigheder
                ],
                lag_ratio=0.25
            ),
            run_time=1
        )
        self.slide_pause()

        kumhyppigheder = VGroup()
        kumhyp = 0
        for i, start in enumerate(interval_starts):
            kumhyp += list(grupperinger.values())[i]
            khtex = Integer(kumhyp).move_to(tabel_struktur[i+1][2])
            kumhyppigheder.add(khtex)
            if i == 0:
                self.play(
                    LaggedStart(
                        Indicate(
                            tabel_struktur[i+1][1], scale_factor=1.2, color=tabel_struktur[i+1][1][1].get_color()
                        ),
                        Write(khtex),
                        lag_ratio=0.5
                    )
                )
            else:
                self.play(
                    Indicate(tabel_struktur[i][2], scale_factor=1.2, color=tabel_struktur[i][2][1].get_color()),
                    Indicate(tabel_struktur[i + 1][1], scale_factor=1.2, color=tabel_struktur[i + 1][1][1].get_color()),
                    Write(khtex)
                )
        self.slide_pause()

        frekvenser = VGroup()
        for i, start in enumerate(interval_starts):
            hyp = list(grupperinger.values())[i]
            fretex = Integer(100 * hyp / kumhyppigheder[-1].get_value(), unit=r" \%").move_to(tabel_struktur[i+1][3])
            frekvenser.add(fretex)
            self.play(
                Indicate(
                    tabel_struktur[-1][2], scale_factor=1.2, color=tabel_struktur[-1][2][1].get_color()
                ),
                Indicate(
                    tabel_struktur[i+1][1], scale_factor=1.2, color=tabel_struktur[i+1][1][1].get_color()
                ),
                Write(fretex)
            )
        self.slide_pause()

        kumfrekvenser = VGroup()
        kumfre = 0
        for i, start in enumerate(interval_starts):
            kumfre += frekvenser[i].get_value()
            kftex = Integer(kumfre, unit=r" \%").move_to(tabel_struktur[i+1][4])
            kumfrekvenser.add(kftex)
            if i == 0:
                self.play(
                    Indicate(tabel_struktur[i+1][3], scale_factor=1.2, color=tabel_struktur[i+1][3][1].get_color()),
                    Write(kftex)
                )
            else:
                self.play(
                    Indicate(tabel_struktur[i][4], scale_factor=1.2, color=tabel_struktur[i][4][1].get_color()),
                    Indicate(tabel_struktur[i + 1][3], scale_factor=1.2, color=tabel_struktur[i + 1][3][1].get_color()),
                    Write(kftex)
                )
        self.slide_pause()

        self.play(
            *[FadeOut(m) for m in [
                *[row[1:3] for row in tabel_struktur],
                *[row[-1] for row in tabel_struktur],
                col_labels[1:3], col_labels[-1], hyppigheder, kumhyppigheder, kumfrekvenser
            ]]
        )
        self.slide_pause()

        self.play(
            *[VGroup(row[0], interval).animate.to_edge(
                LEFT, buff=0.5
            ) for row, interval in zip(tabel_struktur, col_labels[0].add(*intervaller))],
            *[VGroup(row[3], frek).animate.to_edge(
                LEFT, buff=0.5+row[0].get_width()
            ) for row, frek in zip(tabel_struktur, col_labels[3].add(*frekvenser))],
        )

        xmin, xmax, xstep = 0, 20, 1
        ymin, ymax, ystep = 0, 40, 5
        plane = Axes(
            x_range=(xmin, xmax+xstep, xstep),
            y_range=(ymin, ymax+ystep, ystep),
            x_length=9,
            y_length=6,
            axis_config={
                'tip_shape': StealthTip
            },
            x_axis_config={
                "numbers_to_include": np.arange(xmin, xmax+xstep, xstep),
            },
            y_axis_config={
                # "numbers_to_include": np.arange(ymin, ymax+ystep, ystep),
            }
        ).set_z_index(5).to_edge(RIGHT)
        plane[1].add_labels({v: Integer(v, unit=r" \%") for v in plane[1].get_tick_range()})
        self.play(
            DrawBorderThenFill(plane)
        )
        self.slide_pause()

        axvlines = VGroup(
            *[
                DashedLine(
                    start=plane.c2p(x, 0), end=plane.c2p(x, ymax+ystep), stroke_width=0.375
                ).set_z_index(plane.get_z_index() - 1) for x in plane[0].get_tick_range()
            ]
        )
        axhlines = VGroup(
            *[
                DashedLine(
                    start=plane.c2p(0, y), end=plane.c2p(xmax+xstep, y), stroke_width=0.375
                ).set_z_index(plane.get_z_index() - 1) for y in plane[1].get_tick_range()
            ]
        )
        self.play(
            LaggedStart(
                *[
                    LaggedStart(
                        *[Create(line) for line in lines],
                        lag_ratio=0.05
                    ) for lines in [axhlines, axvlines]
                ],
                lag_ratio=0.1
            ),
            run_time=1
        )

        _dots = VGroup(
            *[
                VGroup(
                    Dot(plane.c2p(start, 0)),
                    Dot(plane.c2p(start, frek.get_value())),
                    Dot(plane.c2p(end, 0)),
                    Dot(plane.c2p(end, frek.get_value())),
                ) for start, end, frek in zip(interval_starts, interval_ends, frekvenser)
            ]
        )

        hist_bars = VGroup(
            *[
                Rectangle(
                    # width=plane.c2p(end, 0)[0] - plane.c2p(start, 0)[0],
                    # height=plane.c2p(0, hyp.get_value())[1] - plane.c2p(0, 0)[1],
                    width=dots[2].get_x() - dots[0].get_x(),
                    height=dots[3].get_y() - dots[2].get_y(),
                    stroke_color=row[3][1].get_color(),
                    fill_color=row[3][1].get_color(),
                    fill_opacity=0.5
                ).set_z_index(plane.get_z_index() - 3).move_to(
                    # plane.c2p(np.mean((start, end)), 0.5*(plane.c2p(0, hyp.get_value())[1] - plane.c2p(0, 0)[1]))
                # ) for start, end, hyp, row in zip(interval_starts, interval_ends, hyppigheder, tabel_struktur[1:])
                    dots
                ) for dots, row in zip(_dots, tabel_struktur[1:])
            ]
        )
        brect = get_background_rect(plane, fill_opacity=1, buff=0).next_to(plane[0][0], DOWN, buff=-0.5)
        self.add(brect)
        bar_labels = VGroup(
            *[frek.copy().scale(0.75).set_style(fill_color=bar.get_color()).next_to(bar, UP) for frek, bar in zip(frekvenser, hist_bars)]
        )
        for dots, bar, frek, label in zip(_dots, hist_bars, frekvenser, bar_labels):
            _line = Line(
                start=dots[0].get_center(), end=dots[2].get_center(), stroke_color=bar.get_color()
            ).set_z_index(plane.get_z_index() + 1)
            self.play(
                Create(_line),
                run_time=0.5
            )
            bar.shift(bar.get_height() * DOWN)
            self.play(
                LaggedStart(
                    # GrowFromEdge(bar, DOWN),
                    bar.animate.shift(bar.get_height() * UP),
                    ReplacementTransform(frek.copy(), label),
                    FadeOut(_line),
                    lag_ratio=0.25
                ),
                run_time=1
            )
        self.remove(brect)
        self.slide_pause()

        self.play(
            *[VGroup(row[0], row[3], interval, frek).animate.shift(
                4 * LEFT
            ) for row, interval, frek in zip(
                tabel_struktur, col_labels[0].add(*intervaller), col_labels[3].add(frekvenser)
            )],
            VGroup(plane, hist_bars, bar_labels, axvlines, axhlines).animate.to_edge(DOWN)
        )
        overskrift = Tex("Histogram").set_color(YELLOW).next_to(plane, UP, buff=0)
        self.play(
            Write(overskrift),
            run_time=0.5
        )
        self.slide_pause()
        self.play(
            LaggedStart(
                *[
                    FadeOut(m) for m in [*bar_labels, *hist_bars, *axvlines, *axhlines, plane]
                ],
                lag_ratio=0.05
            ),
            run_time=1
        )
        # self.remove(self.mobjects)

    def varierende_intervalbredde(self):
        data_raw = [8, 4, 16, 8, 9, 6, 16, 19, 7, 6, 4, 8, 11, 8, 9, 6, 9, 10, 11, 8, 14, 4, 6, 7, 10]
        data = self.data_to_DecNum(data_raw).to_edge(LEFT, buff=0.5)

        first_start = 0
        last_end = 20
        bredde_tracker = ValueTracker(2)

        interval_starts = always_redraw(lambda:
            VGroup(
                *[
                    DecimalNumber(x, num_decimal_places=2) for x in np.arange(
                        first_start, last_end, bredde_tracker.get_value()
                    )
                ]
            )
        )
        interval_ends = always_redraw(lambda:
            VGroup(
                *[
                    DecimalNumber(x, num_decimal_places=2) for x in np.arange(
                        first_start + bredde_tracker.get_value(), last_end + bredde_tracker.get_value(), bredde_tracker.get_value()
                    )
                ]
            )
        )
        frekvenser = always_redraw(lambda:
            VGroup(
                *[
                    Integer(
                        100 * len([x for x in data if start.get_value() <= x.get_value() < end.get_value()]) / len(data),
                        unit=r" \%"
                    ) for start, end in zip(interval_starts, interval_ends)
                ]
            )
        )

        xmin, xmax, xstep = 0, 20, 1
        ymin, ymax, ystep = 0, 40, 5
        plane = Axes(
            x_range=(xmin, xmax+xstep, xstep),
            y_range=(ymin, ymax+ystep, ystep),
            x_length=9,
            y_length=6,
            axis_config={
                'tip_shape': StealthTip
            },
            x_axis_config={
                "numbers_to_include": np.arange(xmin, xmax+xstep, xstep),
            },
            y_axis_config={
                # "numbers_to_include": np.arange(ymin, ymax+ystep, ystep),
            }
        ).set_z_index(5).to_edge(DOWN)
        plane[1].add_labels({v: Integer(v, unit=r" \%") for v in plane[1].get_tick_range()})

        axvlines = VGroup(
            *[
                DashedLine(
                    start=plane.c2p(x, 0), end=plane.c2p(x, ymax+ystep), stroke_width=0.375
                ).set_z_index(plane.get_z_index() - 1) for x in plane[0].get_tick_range()
            ]
        )
        axhlines = VGroup(
            *[
                DashedLine(
                    start=plane.c2p(0, y), end=plane.c2p(xmax+xstep, y), stroke_width=0.375
                ).set_z_index(plane.get_z_index() - 1) for y in plane[1].get_tick_range()
            ]
        )

        _dots = always_redraw(lambda: VGroup(
            *[
                VGroup(
                    Dot(plane.c2p(start.get_value(), 0)),
                    Dot(plane.c2p(start.get_value(), frek.get_value())),
                    Dot(plane.c2p(end.get_value(), 0)),
                    Dot(plane.c2p(end.get_value(), frek.get_value())),
                ) for start, end, frek in zip(interval_starts, interval_ends, frekvenser)
            ]
        ))

        hist_bars = always_redraw(lambda: VGroup(
            *[
                Rectangle(
                    width=dots[2].get_x() - dots[0].get_x(),
                    height=dots[3].get_y() - dots[2].get_y(),
                    stroke_color=YELLOW,
                    fill_color=YELLOW,
                    fill_opacity=0.5
                ).set_z_index(plane.get_z_index() - 3).move_to(
                    dots
                ) for dots in _dots
            ]
        ))
        bar_labels = always_redraw(lambda: VGroup(
            *[frek.copy().scale(0.75).set_style(fill_color=bar.get_color()).next_to(bar, UP) for frek, bar in zip(frekvenser, hist_bars)]
        ))

        self.add(plane, hist_bars, bar_labels, axvlines, axhlines)
        print(*[s.get_value() for s in interval_starts])
        self.play(
            bredde_tracker.animate.set_value(5),
            run_time=5
        )
        print(*[s.get_value() for s in interval_starts])


if __name__ == "__main__":
    classes = [
        # GrupperingAfData,
        Histogrammer
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
