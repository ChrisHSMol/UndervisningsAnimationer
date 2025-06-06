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


class HyppighedsTabel(MovingCameraScene, Slide if slides else Scene):
    def construct(self):
        self.slide_pause()
        title = Tex("Hyppighedstabel")
        play_title2(self, title)
        self.hyppighedstabel()
        self.slide_pause()
        self.play(
            LaggedStart(
                *[FadeOut(m) for m in self.mobjects],
                lag_ratio=0.15
            )
        )

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t=t, slides_bool=slides_bool)

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

            # dict_sorting[strVal + f"_{num_of_each_value[strVal]}"] = [
            #     s for s in sorted_data if s.get_value() == d.get_value()
            # ][num_of_each_value[strVal]]

            dict_sorting[d] = [
                s for s in sorted_data if s.get_value() == d.get_value()
            ][num_of_each_value[strVal]]

            num_of_each_value[strVal] += 1
        # print(dict_sorting)
        return sorted_data, dict_sorting

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
        # tabel_struktur = VGroup(*[
        #     VGroup(*[
        #         Rectangle(
        #             width=1.5, height=0.65, stroke_width=1,
        #             # fill_color=[*[BLACK for _ in range(1+col_offset)], YELLOW, YELLOW, GREEN, GREEN][i],
        #             # fill_opacity=[*[0 for _ in range(1+col_offset)], 0.1, 0.15, 0.1, 0.15][i]
        #         ) for i in range(5 + col_offset)
        #     ]).arrange(RIGHT, buff=0) for _ in range(num_different_numbers + row_offset)
        # ]).arrange(DOWN, buff=0).to_edge(RIGHT)
        # if include_coloured_inlay:
        #     for row in tabel_struktur:
        #         for i, cell in enumerate(row):
        #             tabel_struktur.add(
        #                 Rectangle(
        #                     width=cell.width - 0.05, height=cell.height - 0.05, fill_opacity=0, stroke_width=2,
        #                     stroke_color=[*[BLACK for _ in range(1+col_offset)], YELLOW, YELLOW, GREEN, GREEN][i],
        #                     stroke_opacity=[*[0 for _ in range(1+col_offset)], 0.5, 0.75, 0.5, 0.75][i]
        #                 ).move_to(cell)
        #             )
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

    def hyppighedstabel(self):
        data_raw = [8, 4, 16, 8, 9, 6, 16, 19, 7, 6, 4, 8, 11, 8, 9, 6, 9, 10, 11, 8, 14, 4, 6, 7, 10]
        data = self.data_to_DecNum(data_raw).to_edge(LEFT, buff=2)
        sorted_data, sorting_dict = self.one_to_one_sort(data, desc=False)
        # self.add(data)
        self.play(
            LaggedStart(
                *[Write(d) for d in data],
                lag_ratio=0.05
            )
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

        different_numbers = np.unique(data_raw)
        num_different_numbers = len(different_numbers)
        # tabel_struktur = VGroup(*[
        #     VGroup(*[
        #         Rectangle(
        #             width=1.5, height=0.65, stroke_width=1
        #         ) for _ in range(5)
        #     ]).arrange(RIGHT, buff=0) for _ in range(num_different_numbers + 1)
        # ]).arrange(DOWN, buff=0).to_edge(RIGHT)
        tabel_struktur, tabel_data, tabel_data_raw = self.prepare_table(data_raw, include_header_row=True)
        VGroup(tabel_struktur, tabel_data).to_edge(RIGHT)
        # self.add(tabel_struktur)
        self.play(
            LaggedStart(
                *[DrawBorderThenFill(r, lag_ratio=0.05) for r in tabel_struktur],
                lag_ratio=0.05
            )
        )

        # _tabel = []
        # kumhyp = 0
        # kumfre = 0
        # for i, obs in enumerate(different_numbers):
        #     hyp = len([d for d in data_raw if d == obs])
        #     kumhyp += hyp
        #     fre = hyp/len(data_raw)
        #     kumfre += fre
        #     _tabel.append([str(obs), str(hyp), str(kumhyp), f"{fre*100:.0f}\\%", f"{kumfre*100:.0f}\\%"])
        #
        # tabel_data = VGroup(*[
        #     VGroup(*[
        #         MathTex(d, font_size=22).move_to(tabel_struktur[j+1][i]) for i, d in enumerate(row)
        #     ]) for j, row in enumerate(_tabel)
        # ])

        col_labels = VGroup(*[Tex(d, font_size=22).move_to(tabel_struktur[0][i]) for i, d in enumerate([
            "Observation", "Hyppighed", "Kumuleret\\\\hyppighed", "Frekvens", "Kumuleret\\\\frekvens"
        ])])
        # self.add(col_labels)
        self.play(
            Write(col_labels, lag_ratio=0.1)
        )
        self.slide_pause()

        for i, obs in enumerate(different_numbers):
            nums_in_sorted_list = VGroup(*[
                d for d in sorted_data if d.get_value() == obs
            ])
            brect = get_background_rect(nums_in_sorted_list, buff=0.1, stroke_colour=YELLOW, fill_opacity=0)
            brace = Brace(nums_in_sorted_list, direction=RIGHT)
            hyp = Tex(str(len(nums_in_sorted_list)), font_size=22).next_to(brace)
            if i == 0:
                self.play(
                    DrawBorderThenFill(brect),
                    run_time=0.5
                )
                self.play(
                    # FadeIn(tabel_data[i][0], shift=tabel_data[i][0].get_center() - brect.get_center())
                    ReplacementTransform(nums_in_sorted_list.copy(), tabel_data[i][0]),
                    run_time=0.5
                )
                self.slide_pause()

                self.play(
                    LaggedStart(
                        DrawBorderThenFill(brace),
                        Write(hyp),
                        lag_ratio=0.8
                    ),
                    run_time=0.5
                )
                self.play(
                    ReplacementTransform(hyp.copy(), tabel_data[i][1]),
                    run_time=0.5
                )
            else:
                self.play(
                    ReplacementTransform(prev_brect, brect),
                    ReplacementTransform(prev_brace, brace),
                    ReplacementTransform(prev_hyp, hyp),
                    run_time=0.85**(i-1)
                )
                self.play(
                    LaggedStart(
                        ReplacementTransform(nums_in_sorted_list.copy(), tabel_data[i][0]),
                        ReplacementTransform(hyp.copy(), tabel_data[i][1]),
                        lag_ratio=1
                    ),
                    run_time=0.85**(i-1)
                )
            self.slide_pause()

            prev_brect, prev_brace, prev_hyp = brect, brace, hyp
            if obs == different_numbers[-1]:
                self.play(
                    FadeOut(brect),
                    FadeOut(brace),
                    FadeOut(hyp),
                    run_time=0.25
                )

        self.camera.frame.save_state()
        self.play(
            *[FadeOut(m) for m in [data, sorted_data]],
            self.camera.frame.animate.move_to(tabel_struktur),
            run_time=1
        )
        self.slide_pause()

        for i, obs in enumerate(different_numbers):
            movement_arrows = VGroup(
                Arrow(
                    start=tabel_data[i][1].get_center(), end=tabel_data[i][2].get_center(), stroke_width=1,
                    max_tip_length_to_length_ratio=0.1
                ),
            )
            if i > 0:
                movement_arrows.add(
                    Arrow(
                        start=tabel_data[i-1][2].get_center(), end=tabel_data[i][2].get_center(), stroke_width=1,
                        max_tip_length_to_length_ratio=0.1
                    ),
                )
            self.play(
                *[GrowArrow(a) for a in movement_arrows]
            )
            self.play(
                ReplacementTransform(
                    tabel_data[i][1].copy() if i == 0 else VGroup(tabel_data[i][1].copy(), tabel_data[i-1][2].copy()),
                    tabel_data[i][2]
                ),
                run_time=1
            )
            self.slide_pause()
            self.play(
                *[FadeOut(a) for a in movement_arrows],
                run_time=0.25
            )

        samlet_rect = tabel_struktur[-1][2].copy().set_fill(
            color=BLUE, opacity=0.25
        ).set_stroke(width=0).set_z_index(tabel_data[-1][2].get_z_index()-1)
        self.play(
            # Circumscribe(tabel_data[-1][2], time_width=2, stroke_opacity=[0, 1, 0]),
            FadeIn(samlet_rect),
            run_time=1
        )
        self.slide_pause()

        moving_rect = tabel_struktur[1][1].copy().set_fill(
            color=BLUE_A, opacity=0.25
        ).set_stroke(width=0).set_z_index(tabel_data[0][1].get_z_index()-1)

        for i, obs in enumerate(different_numbers):
            udregning = VGroup(
                tabel_data[i][1].copy(),
                tabel_data[-1][2].copy()
            ).scale(2).arrange(DOWN, buff=0.2).next_to(tabel_struktur, LEFT, buff=2)
            udregning.add(
                Line(
                    start=udregning[1].get_left(), end=udregning[1].get_right(), stroke_width=2
                ).scale(2).next_to(udregning[1], UP, buff=0.1)
            )
            udr_samlet_rect = samlet_rect.copy().scale(0.75).move_to(udregning[1])
            udr_obs_rect = moving_rect.copy().scale(0.75).move_to(udregning[0])
            udregning.add(
                MathTex("=").next_to(udregning[2], RIGHT)
            )
            udregning.add(
                tabel_data[i][3].copy().scale(2).next_to(udregning[3])
            )
            if i == 0:
                self.play(
                    FadeIn(moving_rect)
                )
                self.play(
                    LaggedStart(
                        ReplacementTransform(moving_rect.copy(), udr_obs_rect),
                        Create(udregning[2]),
                        ReplacementTransform(samlet_rect.copy(), udr_samlet_rect),
                        FadeIn(udregning[0]),
                        FadeIn(udregning[1]),
                        lag_ratio=0.75
                    )
                )
                self.play(
                    LaggedStart(
                        *[FadeIn(m, shift=0.25*RIGHT) for m in udregning[3:]],
                        lag_ratio=0.75
                    )
                )
                self.slide_pause()

                self.play(
                    ReplacementTransform(udregning[4].copy(), tabel_data[i][3])
                )
            else:
                self.play(
                    moving_rect.animate.move_to(tabel_struktur[i+1][1]),
                    FadeOut(prev_udregning[0], shift=0.5*UP),
                    FadeOut(prev_udregning[4], shift=0.25*RIGHT),
                    FadeIn(udregning[0], shift=0.5*UP),
                    FadeIn(udregning[4], shift=0.25*RIGHT),
                    run_time=0.5
                )
                self.play(
                    ReplacementTransform(udregning[4].copy(), tabel_data[i][3])
                )
                self.slide_pause()
                # self.remove(*prev_udregning)
            # self.remove(*udregning, udr_samlet_rect, udr_obs_rect)
            # self.add(*udregning, udr_samlet_rect, udr_obs_rect)
            prev_udregning = udregning

            if obs == different_numbers[-1]:
                cover_box = get_background_rect(udregning, stroke_width=0, fill_opacity=1).set_z_index(10)
                self.play(
                    *[FadeOut(m) for m in (
                        moving_rect, samlet_rect, udr_samlet_rect, udr_obs_rect, *udregning, *prev_udregning
                    )],
                    # *[FadeOut(m) for m in self.mobjects if m not in (*tabel_data, *tabel_struktur)],
                    FadeIn(cover_box),
                    run_time=0.5
                )
                self.slide_pause()

        for i, obs in enumerate(different_numbers):
            movement_arrows = VGroup(
                Arrow(
                    start=tabel_data[i][3].get_center(), end=tabel_data[i][4].get_center(), stroke_width=1,
                    max_tip_length_to_length_ratio=0.1
                ),
            )
            if i > 0:
                movement_arrows.add(
                    Arrow(
                        start=tabel_data[i-1][4].get_center(), end=tabel_data[i][4].get_center(), stroke_width=1,
                        max_tip_length_to_length_ratio=0.1
                    ),
                )
            self.play(
                *[GrowArrow(a) for a in movement_arrows]
            )
            self.play(
                ReplacementTransform(
                    tabel_data[i][3].copy() if i == 0 else VGroup(tabel_data[i][3].copy(), tabel_data[i-1][4].copy()),
                    tabel_data[i][4]
                ),
                run_time=0.75
            )
            self.slide_pause()
            self.play(
                *[FadeOut(a) for a in movement_arrows],
                run_time=0.25
            )

        self.remove(*[m for m in self.mobjects])
        self.add(tabel_data, tabel_struktur, col_labels)


class Deskriptorer(HyppighedsTabel):
    def construct(self):
        self.centrale_deskriptorer()
        # self._tester()
        # self.wait(5)
        self.play(
            LaggedStart(
                *[FadeOut(m) for m in self.mobjects],
                lag_ratio=0.025
            )
        )

    def _tester(self):
        data_raw = [8, 4, 16, 8, 9, 6, 16, 19, 7, 6, 4, 8, 11, 8, 9, 6, 9, 10, 11, 8, 14, 5, 6, 7, 10]
        data = self.data_to_DecNum(data_raw).to_edge(LEFT, buff=2)
        data_sorted, sorting_dict = self.one_to_one_sort(data)
        data_sorted.next_to(data, RIGHT, buff=2)
        self.add(data_sorted, data)
        # self.animer_median(data_sorted)
        self.animer_typetal(data_sorted)

    def animer_median(self, data, colors=(GREEN_A, GREEN_E)):
        moving_arrows = VGroup(
            Arrow(
                start=0.5*LEFT, end=0.5*RIGHT, stroke_color=colors[0],
                max_tip_length_to_length_ratio=1, max_stroke_width_to_length_ratio=1
            ).next_to(data[0], LEFT, buff=0.1),
            Arrow(
                start=0.5*RIGHT, end=0.5*LEFT, stroke_color=colors[1],
                max_tip_length_to_length_ratio=1, max_stroke_width_to_length_ratio=1
            ).next_to(data[-1], RIGHT, buff=0.1),
        )
        self.add(moving_arrows)
        self.play(
            DrawBorderThenFill(moving_arrows, lag_ratio=0.5),
            run_time=0.5
        )
        self.slide_pause()
        i = 0
        while moving_arrows[0].get_y() > moving_arrows[1].get_y():
            # print(moving_arrows[0].get_y(), moving_arrows[1].get_y())
            i += 1
            self.play(
                moving_arrows[0].animate.next_to(data[i], LEFT, buff=0.1),
                moving_arrows[1].animate.next_to(data[-(1+i)], RIGHT, buff=0.1),
            )
        i_median = i
        # print(i_median, len(data)//2)
        self.slide_pause()
        self.play(
            data[i_median].animate.set_color(GREEN_C),
            FadeOut(moving_arrows)
        )

    def animer_kvartil(self, data, indices: tuple[int, int], colors=(GREEN_A, GREEN_E)):
        i_start, i_end = indices
        moving_arrows = VGroup(
            # Arrow(
            #     start=0.5*LEFT, end=0.5*RIGHT, stroke_color=colors[0],
            #     max_tip_length_to_length_ratio=1, max_stroke_width_to_length_ratio=1
            # ).next_to(data[i_start], LEFT, buff=0.1),
            Arrow(
                start=0.5*LEFT, end=0.5*RIGHT, stroke_color=colors[0]
            ).next_to(data[i_start], LEFT, buff=0.1),
            # Arrow(
            #     start=0.5*RIGHT, end=0.5*LEFT, stroke_color=colors[1],
            #     max_tip_length_to_length_ratio=1, max_stroke_width_to_length_ratio=1
            # ).next_to(data[i_end], RIGHT, buff=0.1),
            Arrow(
                start=0.5*RIGHT, end=0.5*LEFT, stroke_color=colors[1]
            ).next_to(data[i_end], RIGHT, buff=0.1),
        )
        # self.add(moving_arrows)
        self.play(
            DrawBorderThenFill(moving_arrows, lag_ratio=0.5),
            run_time=0.5
        )
        # self.slide_pause()
        i = 0
        while moving_arrows[0].get_y() > moving_arrows[1].get_y():
            # print(moving_arrows[0].get_y(), moving_arrows[1].get_y())
            i += 1
            self.play(
                moving_arrows[0].animate.next_to(data[i_start + i], LEFT, buff=0.1),
                moving_arrows[1].animate.next_to(data[i_end - i], RIGHT, buff=0.1),
            )
        if i == 0:
            i = i_end
        # self.slide_pause()

        if moving_arrows[0].get_y() < moving_arrows[1].get_y():
            self.play(
                data[i_end - i:i_start + i + 1].animate.set_color(color_gradient(colors, 3)),
                FadeOut(moving_arrows)
            )
            self.slide_pause()
            brace = Brace(data[i_end - i:i_start + i + 1], RIGHT, fill_color=color_gradient(colors, 3))
            calc = VGroup(
                MathTex(f"{data[i_end-i].get_value()}", "+", f"{data[i_start + i].get_value()}"),
                MathTex("2")
            ).arrange(DOWN, buff=0.25).next_to(brace, RIGHT)
            calc[0][0].set_color(color_gradient(colors, 3))
            calc[0][2].set_color(color_gradient(colors, 3))
            calc.add(
                Line(start=calc[0].get_left(), end=calc[0].get_right(), stroke_width=2).next_to(calc[0], DOWN, buff=0.125)
            )
            numdec = 2
            if ((data[i_end-i].get_value() + data[i_start + i].get_value())/2).is_integer():
                numdec = 0
            calc.add(
                MathTex(
                    "=", f"{(data[i_end-i].get_value() + data[i_start + i].get_value())/2:.{numdec}f}"
                ).next_to(calc[2], RIGHT)
            )
            calc[3][1].set_color(color_gradient(colors, 3))
            calc.scale(0.5).next_to(brace, RIGHT)
            self.play(
                LaggedStart(
                    DrawBorderThenFill(brace),
                    # FadeIn(calc[:3], shift=0.5*RIGHT),
                    # FadeIn(calc[3], shift=RIGHT),
                    # FadeIn(calc, shift=0.5*RIGHT, lag_ratio=0.25),
                    ReplacementTransform(data[i_end-i].copy(), calc[0][0]),
                    ReplacementTransform(data[i_start+i].copy(), calc[0][2]),
                    FadeIn(calc[:3]),
                    FadeIn(calc[3], shift=RIGHT),
                    lag_ratio=1
                )
            )
            self.slide_pause()

            self.play(
                FadeOut(calc[:3], shift=0.5*LEFT),
                FadeOut(calc[3][0], shift=0.5*LEFT),
                calc[3][1].animate.next_to(brace, RIGHT)
            )
            val = (data[i_end-i].get_value() + data[i_start + i].get_value())/2
            if val.is_integer():
                val = int(val)
            return [brace, calc[3][1], val]
        else:
            self.play(
                data[i].animate.set_color(color_gradient(colors, 3)),
                FadeOut(moving_arrows)
            )
            arrow = Arrow(
                start=0.5*LEFT, end=0.5*RIGHT, stroke_color=color_gradient(colors, 3)
            ).next_to(data[i], RIGHT, buff=0.1)
            tal = data[i].copy().next_to(arrow, RIGHT)
            self.play(
                LaggedStart(
                    DrawBorderThenFill(arrow),
                    ReplacementTransform(data[i].copy(), tal)
                )
            )
            # self.slide_pause()
            val = tal.get_value()
            return [arrow, tal, val]

    def animer_typetal(self, data):
        different_numbers = np.unique([d.get_value() for d in data])
        stoerste_tal = VGroup(
            Tex("Største antal: "), Integer(0), Integer(0)
        ).arrange(RIGHT).next_to(data, RIGHT, aligned_edge=DOWN, buff=0.5)
        for i, obs in enumerate(different_numbers):
            nums_in_sorted_list = VGroup(*[
                d for d in data if d.get_value() == obs
            ])
            brect = get_background_rect(nums_in_sorted_list, buff=0.1, stroke_colour=YELLOW, fill_opacity=0)
            brace = Brace(nums_in_sorted_list, direction=RIGHT)
            hyp = Tex(str(len(nums_in_sorted_list)), font_size=22).next_to(brace)
            if i == 0:
                self.play(
                    DrawBorderThenFill(brect),
                    DrawBorderThenFill(stoerste_tal[:2]),
                    run_time=0.5
                )
                self.slide_pause()

                self.play(
                    LaggedStart(
                        DrawBorderThenFill(brace),
                        Write(hyp),
                        lag_ratio=0.8
                    ),
                    run_time=0.5
                )
            else:
                self.play(
                    ReplacementTransform(prev_brect, brect),
                    ReplacementTransform(prev_brace, brace),
                    ReplacementTransform(prev_hyp, hyp),
                    run_time=0.85**(i-1)
                )
            if len(nums_in_sorted_list) > stoerste_tal[1].get_value():
                stoerste_tal[2].set_value(obs)
                self.play(
                    stoerste_tal[1].animate.set_value(len(nums_in_sorted_list)),
                    run_time=0.5
                )

            prev_brect, prev_brace, prev_hyp = brect, brace, hyp
            if obs == different_numbers[-1]:
                self.play(
                    FadeOut(brect),
                    FadeOut(brace),
                    FadeOut(hyp),
                    run_time=0.25
                )
        typetal = Tex("typetal", " = ", f"{stoerste_tal[2].get_value():.0f}").next_to(
            data, RIGHT, aligned_edge=DOWN, buff=0.5
        )
        self.play(
            FadeIn(typetal, shift=UP),
            stoerste_tal[:2].animate.shift(UP)
        )
        self.play(
            FadeOut(stoerste_tal[:2])
        )
        return typetal

    def centrale_deskriptorer(self):
        cmap = {
            "datasæt": YELLOW,
            "observation": BLUE,
            "deskriptor": RED,
            "sorter": GREEN
        }
        data_raw = [8, 4, 16, 8, 9, 6, 16, 19, 7, 6, 4, 8, 11, 8, 9, 6, 9, 10, 11, 8, 14, 5, 6, 7, 10]
        data = self.data_to_DecNum(data_raw).to_edge(LEFT, buff=2)
        # self.add(data)
        self.play(
            LaggedStart(
                *[Write(d) for d in data],
                lag_ratio=0.05
            )
        )

        dataset_box = get_background_rect(data, stroke_colour=cmap["datasæt"])
        brace = Brace(dataset_box, RIGHT, buff=0.2)
        dataset_text = VGroup(
            Tex("Et ", "datasæt").set_color_by_tex_to_color_map(cmap),
            Tex("består af flere ", "observationer", ".").set_color_by_tex_to_color_map(cmap)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(brace, RIGHT)
        dataset_text.shift((dataset_text[0].get_y() - brace.get_y()) * DOWN)
        # self.add(brace, dataset_text, dataset_box)

        self.play(
            DrawBorderThenFill(dataset_box),
            GrowFromEdge(brace, LEFT),
            Write(dataset_text)
        )
        self.slide_pause()
        self.play(
            LaggedStart(
                *[Indicate(m, scale_factor=1.5, color=cmap["observation"]) for m in data],
                lag_ratio=0.25
            ),
            run_time=3
        )
        self.slide_pause()
        self.play(
            LaggedStart(
                FadeOut(dataset_box, shift=LEFT),
                FadeOut(brace, shift=LEFT),
                FadeOut(dataset_text, shift=LEFT),
                lag_ratio=0.2
            )
        )
        self.slide_pause()
        # self.remove(brace, dataset_text, dataset_box)

        deskriptor_text = VGroup(
            Tex("En ", "deskriptor", " er et tal, ").set_color_by_tex_to_color_map(cmap),
            Tex("som beskriver ", "datasættet", ".").set_color_by_tex_to_color_map(cmap)
        ).arrange(DOWN, aligned_edge=LEFT)
        # self.add(deskriptor_text)
        self.play(
            Write(deskriptor_text), run_time=0.5
        )
        self.slide_pause()
        self.play(
            deskriptor_text.animate.arrange(RIGHT, aligned_edge=UP).to_edge(UR)
        )

        size_text = VGroup(
            Tex("Størrelsen", " af et ", "datasæt").set_color_by_tex_to_color_map(cmap),
            Tex("er antallet af ", "observationer", ".").set_color_by_tex_to_color_map(cmap)
        ).arrange(DOWN, aligned_edge=LEFT)
        size_text[0][0].set_color(cmap["deskriptor"])
        size_counter = VGroup(Tex("N", " = "), Integer(0)).arrange(RIGHT).next_to(size_text, DOWN, aligned_edge=LEFT)
        size_counter[0][0].set_color(cmap["deskriptor"])
        # self.add(size_text, size_counter)
        self.play(
            LaggedStart(
                Write(size_text),
                Write(size_counter),
                lag_ratio=0.5
            )
        )
        self.slide_pause()
        for i, d in enumerate(data):
            self.play(
                Indicate(d, color=cmap["observation"]),
                size_counter[1].animate.set_value(i+1),
                run_time=0.25
            )
        self.slide_pause()

        self.play(
            FadeOut(size_text, shift=UP),
            size_counter.animate.next_to(deskriptor_text, DOWN, buff=0.5, aligned_edge=LEFT)
        )
        self.slide_pause()

        middel = Tex(r"Middelværdien kaldes {{$\overline{x}$}} eller {{$\mu$}}.").next_to(data, RIGHT, buff=0.5)
        middel[1].set_color(cmap["deskriptor"])
        middel[3].set_color(cmap["deskriptor"])
        middel_udregning = VGroup(
            MathTex(r"\overline{x}", " = ")
        ).next_to(middel, DOWN, aligned_edge=LEFT, buff=1)
        middel_udregning[0][0].set_color(cmap["deskriptor"])
        middel_udregning.add(
            VGroup(
                data.copy().arrange(RIGHT).next_to(middel_udregning, RIGHT)
            )
        )
        middel_udregning[1].add(
            VGroup(*[
                MathTex("+").scale(0.5).move_to(
                    between_mobjects(middel_udregning[1][0][i], middel_udregning[1][0][i+1])
                ) for i in range(len(data_raw) - 1)
            ])
        )
        middel_udregning[1].add(
            Line(
                start=middel_udregning[1][0].get_left(), end=middel_udregning[1][0].get_right(), stroke_width=1.5
            ).next_to(middel_udregning[1][0], DOWN, buff=0.125),
            # MathTex(f"{len(data_raw):.0f}").next_to(middel_udregning[1][0], DOWN, buff=0.25)
            size_counter[1].copy().next_to(middel_udregning[1][0], DOWN, buff=0.25)
        )
        # self.add(middel, middel_udregning[0])
        self.play(
            LaggedStart(
                Write(middel),
                Write(middel_udregning[0]),
                lag_ratio=0.9
            )
        )
        self.slide_pause()
        self.play(
            ReplacementTransform(data[0].copy(), middel_udregning[1][0][0]),
            data[0].animate.set_opacity(0.5)
        )
        for i in range(len(data_raw) - 1):
            self.play(
                LaggedStart(
                    ReplacementTransform(data[i+1].copy(), middel_udregning[1][0][i+1]),
                    FadeIn(middel_udregning[1][1][i], shift=0.5*RIGHT),
                    data[i+1].animate.set_opacity(0.33),
                    lag_ratio=0.25
                ),
                run_time=0.5
            )
        self.play(
            Create(middel_udregning[1][2]),
            # Write(middel_udregning[1][3]),
            ReplacementTransform(size_counter[1].copy(), middel_udregning[1][3]),
            middel_udregning[0].animate.shift(
                (middel_udregning[0].get_y() - middel_udregning[1][2].get_y()) * DOWN
            )
        )
        self.slide_pause()
        # self.play(
        #     Write(middel_udregning[1][3]),
        #     Indicate(size_counter, color=cmap["deskriptor"])
        # )
        middel_udregning.add(
            VGroup(
                Integer(sum(data_raw)),
                Line(start=Integer(sum(data_raw)).get_left(), end=Integer(sum(data_raw)).get_right(), stroke_width=1.5),
                size_counter[1].copy()
            ).arrange(DOWN, buff=0.125).next_to(middel_udregning[0], RIGHT)
        )
        self.play(
            # *[ReplacementTransform(middel_udregning[1][i], middel_udregning[2][i]) for i in range(3)]
            ReplacementTransform(VGroup(middel_udregning[1][0], middel_udregning[1][1]), middel_udregning[2][0]),
            ReplacementTransform(middel_udregning[1][2], middel_udregning[2][1]),
            ReplacementTransform(middel_udregning[1][3], middel_udregning[2][2])
        )
        self.slide_pause()

        middel_udregning.add(
            VGroup(
                middel_udregning[0].copy(),
                Integer(sum(data_raw)/len(data_raw)).next_to(middel_udregning[0], RIGHT)
            )
        )
        self.play(
            ReplacementTransform(
                middel_udregning[2], middel_udregning[3][1]
            )
        )
        self.slide_pause()

        self.remove(*[m for m in self.mobjects if m not in (deskriptor_text, data, size_counter, middel)])
        self.add(middel_udregning[3])
        self.play(
            FadeOut(middel, shift=UP),
            middel_udregning[3].animate.next_to(size_counter, RIGHT, buff=0.5),
            data.animate.set_opacity(1)
        )
        self.slide_pause()

        median_text = VGroup(
            Tex("Medianen", " er den midterste ", "observation").set_color_by_tex_to_color_map(cmap),
            Tex("i ", "datasættet", ".").set_color_by_tex_to_color_map(cmap),
            Tex("Vi skal derfor ", "sortere", " datasættet", ".").set_color_by_tex_to_color_map(cmap)
        ).arrange(DOWN, aligned_edge=LEFT)
        self.play(
            Write(median_text),
            run_time=1
        )
        data_sorted, sorting_dict = self.one_to_one_sort(data, desc=False)
        self.play(
            data.animate.to_edge(LEFT)
        )
        self.slide_pause()
        data_sorted.next_to(data, RIGHT, buff=1)

        self.play(
            LaggedStart(
                *[TransformFromCopy(k, v) for k, v in sorting_dict.items()],
                lag_ratio=0.1
            ),
            run_time=2
        )
        self.slide_pause()

        self.animer_median(data_sorted)
        self.slide_pause()

        i_median = len(data_sorted)//2
        median = Tex("median", " = ", f"{data_sorted[i_median].get_value():.0f}").next_to(median_text, DOWN, aligned_edge=LEFT)
        median[0].set_color(cmap["deskriptor"])
        self.play(
            Write(median[:2]),
            ReplacementTransform(data_sorted[i_median].copy(), median[2])
        )
        self.slide_pause()

        self.play(
            median.animate.next_to(middel_udregning[3], RIGHT, buff=0.5),
            FadeOut(median_text, shift=UP)
        )
        self.slide_pause()

        typetal_text = VGroup(
            Tex("Typetal", " er det tal, "),
            Tex("som optræder flest gange i ", "datasættet", ".").set_color_by_tex_to_color_map(cmap)
        ).arrange(DOWN, aligned_edge=LEFT)
        typetal_text[0][0].set_color(cmap["deskriptor"])
        self.play(
            Write(typetal_text)
        )
        self.slide_pause()

        typetal = self.animer_typetal(data_sorted)
        self.slide_pause()

        self.play(
            typetal[0].animate.set_color(cmap["deskriptor"]),
            run_time=0.25
        )
        self.play(
            typetal.animate.next_to(median, RIGHT, buff=0.5),
            FadeOut(typetal_text, shift=UP)
        )
        self.slide_pause()

        brace = Brace(
            VGroup(size_counter, middel_udregning[3], median, typetal), DOWN
        )
        centrale_deskriptorer_text = Tex(
            "De centrale ", "deskriptorer", "."
        ).set_color_by_tex_to_color_map(cmap).next_to(brace, DOWN)
        self.play(
            DrawBorderThenFill(brace),
            Write(centrale_deskriptorer_text)
        )
        self.slide_pause()


class PrikOgPindediagrammer(Deskriptorer):
    def construct(self):
        self.slide_pause()
        title = Tex("Prik- og pindediagrammer fra rå data")
        play_title2(self, title)
        self.data_til_prik_og_pindediagram()
        self.slide_pause()

    def data_til_prik_og_pindediagram(self):
        data_raw = [8, 4, 16, 8, 9, 6, 16, 19, 7, 6, 4, 8, 11, 8, 9, 6, 9, 10, 11, 8, 14, 4, 6, 7, 10]
        data = self.data_to_DecNum(data_raw).to_edge(LEFT, buff=2)
        self.play(
            LaggedStart(
                *[Write(d) for d in data],
                lag_ratio=0.05
            )
        )
        axis = NumberLine(
            x_range=[min(min(data_raw)-1, 0), max(data_raw)+1, 1],
            length=10,
            include_numbers=True,
            label_direction=DOWN,
        ).set_z_index(3).to_edge(DR)
        # self.add(axis)
        self.play(
            DrawBorderThenFill(axis),
            run_time=1
        )
        self.slide_pause()

        num_of_each_value = {}
        _dots = {}
        prikker = VGroup()
        _r = 0.15
        for i, d in enumerate(data_raw):
            if d not in num_of_each_value.keys():
                num_of_each_value[d] = 0
                _dots[d] = VGroup()
            prik = Dot(
                point=axis.n2p(d) + (num_of_each_value[d] + 0.5)*2*_r*UP,
                radius=_r, fill_color=RED, fill_opacity=1, stroke_width=0
            ).set_z_index(2)
            prikker.add(prik)
            _dots[d].add(prik)
            num_of_each_value[d] += 1

        self.play(
            LaggedStart(
                *[ReplacementTransform(d.copy(), p) for d, p in zip(data, prikker)],
                lag_ratio=0.75
            ),
            run_time=10
        )
        self.slide_pause()

        plane = Axes(
            x_range=[min(min(data_raw)-1, 0), max(data_raw)+1, 1],
            y_range=[0, 6, 1],
            x_length=10,
            y_length=12*_r,
            x_axis_config={"include_numbers": True, "label_direction": DOWN},
            y_axis_config={"include_numbers": True, "label_direction": LEFT},
            tips=False
            # include_numbers=True,
            # label_direction=DOWN,
        ).set_z_index(3).to_edge(DR)
        axvlines = always_redraw(lambda: VGroup(*[
            DashedLine(
                start=axis.n2p(tick),
                end=plane.c2p(tick, plane.axes[1].get_tick_range()[-1]),
                stroke_width=0.25
            ).set_z_index(1) for tick in axis.get_tick_range()
        ]))
        axhlines = always_redraw(lambda: VGroup(*[
            DashedLine(
                start=plane.c2p(0, tick),
                end=plane.c2p(plane.axes[0].get_tick_range()[-1], tick),
                stroke_width=0.25
            ).set_z_index(1) for tick in plane.axes[1].get_tick_range()
        ]))
        # self.add(plane, axvlines, axhlines)
        self.play(
            # LaggedStart(
            #     DrawBorderThenFill(plane),
            #     FadeIn(axvlines, lag_ratio=0.2),
            #     FadeIn(axhlines, lag_ratio=0.2),
            #     lag_ratio=0.75
            # ),
            # run_time=3
            DrawBorderThenFill(plane),
            run_time=2
        )
        self.play(
            FadeIn(axvlines, lag_ratio=0.1),
            FadeIn(axhlines, lag_ratio=0.1),
            run_time=1
        )
        self.remove(axvlines, axhlines)
        self.add(axvlines, axhlines)
        self.slide_pause()

        pinde = VGroup()
        for k, v in num_of_each_value.items():
            pinde.add(
                get_background_rect(
                    _dots[k], buff=0, fill_color=BLUE, fill_opacity=0, stroke_width=1, stroke_colour=BLUE
                ).set_z_index(2).move_to(plane.c2p(k, 0.5*v))
            )
        # self.add(pinde)
        self.play(
            DrawBorderThenFill(pinde, lag_ratio=0.2)
        )
        self.slide_pause()

        self.play(
            VGroup(plane, pinde).animate.shift(4*UP)
        )
        self.play(
            LaggedStart(
                *[pind.animate.set_fill(opacity=1).set_stroke(width=0) for pind in pinde],
                lag_ratio=0.1
            ),
            FadeOut(axvlines)
        )
        self.slide_pause()

        diagramnavne = VGroup(
            Tex("Pinde", "diagram"),
            Tex("Prik", "diagram")
        ).arrange(DOWN, aligned_edge=RIGHT).next_to(plane, DOWN, aligned_edge=RIGHT)
        diagramnavne[0][0].set_color(BLUE)
        diagramnavne[1][0].set_color(RED)
        self.play(
            Write(diagramnavne, lag_ratio=0.25)
        )


class SumkurveFraTabel(PrikOgPindediagrammer):
    def construct(self):
        self.hyppighedstabel_til_sumkurve()
        self.wait(5)

    def hyppighedstabel_til_sumkurve(self):
        data_raw = [8, 4, 16, 8, 9, 6, 16, 19, 7, 6, 4, 8, 11, 8, 9, 6, 9, 10, 11, 8, 14, 4, 6, 7, 10]
        data = self.data_to_DecNum(data_raw).to_edge(LEFT, buff=2)
        sorted_data, sorting_dict = self.one_to_one_sort(data, desc=False)
        different_numbers = np.unique(data_raw)
        num_different_numbers = len(different_numbers)
        tabel_struktur, tabel_data, tabel_data_raw = self.prepare_table(data_raw, include_header_row=True)
        VGroup(tabel_struktur, tabel_data).to_edge(RIGHT)
        col_labels = VGroup(*[Tex(d, font_size=22).move_to(tabel_struktur[0][i]) for i, d in enumerate([
            "Observation", "Hyppighed", "Kumuleret\\\\hyppighed", "Frekvens", "Kumuleret\\\\frekvens"
        ])])
        self.play(
            LaggedStart(
                *[DrawBorderThenFill(r, lag_ratio=0.05) for r in tabel_struktur],
                *[Write(r) for r in col_labels],
                *[Write(r, lag_ratio=0.05) for r in tabel_data],
                lag_ratio=0.05
            ),
            run_time=2
        )
        # self.add(tabel_data, tabel_struktur, col_labels)


class TrappediagramFraTabel(SumkurveFraTabel):
    def construct(self):
        title = Tex("Trappediagram", " fra hyppighedstabel")
        title[0].set_color(YELLOW)
        play_title2(self, title)
        self.hyppighedstabel_til_trappediagram()
        self.wait(5)

    def hyppighedstabel_til_trappediagram(self):
        data_raw = [8, 4, 16, 8, 9, 6, 16, 19, 7, 6, 4, 8, 11, 8, 9, 6, 9, 10, 11, 8, 14, 4, 6, 7, 10]
        data = self.data_to_DecNum(data_raw).to_edge(LEFT, buff=2)
        sorted_data, sorting_dict = self.one_to_one_sort(data, desc=False)
        different_numbers = np.unique(data_raw)
        num_different_numbers = len(different_numbers)
        tabel_struktur, tabel_data, tabel_data_raw = self.prepare_table(data_raw, include_header_row=True)
        VGroup(tabel_struktur, tabel_data).to_edge(LEFT)
        col_labels = VGroup(*[Tex(d, font_size=22).move_to(tabel_struktur[0][i]) for i, d in enumerate([
            "Observation", "Hyppighed", "Kumuleret\\\\hyppighed", "Frekvens", "Kumuleret\\\\frekvens"
        ])])
        self.play(
            LaggedStart(
                *[DrawBorderThenFill(r, lag_ratio=0.05) for r in tabel_struktur],
                *[Write(r) for r in col_labels],
                *[Write(r, lag_ratio=0.05) for r in tabel_data],
                lag_ratio=0.05
            ),
            run_time=2
        )
        self.remove(tabel_data, tabel_struktur, col_labels)
        self.add(tabel_data, tabel_struktur, col_labels)

        opaque_box = Rectangle(
            height=tabel_struktur.height, width=tabel_struktur.width * 0.4, fill_color=BLACK, fill_opacity=0.9,
            stroke_width=0
        ).next_to(tabel_struktur, RIGHT, buff=-tabel_struktur.width * 0.39)
        self.play(
            # tabel_struktur[-2:].animate.set_style(fill_opacity=0.1, stroke_opacity=0.1)
            FadeIn(opaque_box)
        )

        # plane = NumberPlane(
        #     x_range=(0, 20, 1),
        #     y_range=(0, 30, 2),
        #     x_length=8,
        #     y_length=5
        # ).to_edge(RIGHT)
        plane = Axes(
            x_range=(0, 20, 1),
            y_range=(0, 30, 2),
            x_length=8,
            y_length=6.5,
            tips=False,
            axis_config={"include_numbers": True, "font_size": 30}
        ).to_edge(RIGHT, buff=0.15)
        axhlines = VGroup(*[
            DashedLine(
                start=plane.c2p(0, y), end=plane.c2p(20, y), stroke_width=1, stroke_opacity=0.5
            ) for y in plane[1].get_tick_range()
        ])
        self.play(
            LaggedStart(
                DrawBorderThenFill(plane),
                *[Create(l, run_time=0.5) for l in axhlines],
                lag_ratio=0.2
            )
        )
        self.slide_pause()

        i = 0
        graph = VGroup()
        for row_data, row_cells in zip(tabel_data_raw, tabel_struktur[1:]):
            obs = row_data[0]
            kumhyp = row_data[2]
            highlight_boxes = VGroup(
                *[row_cells[j].copy().set_style(fill_color=BLUE_A, fill_opacity=0.25).set_z_index(5) for j in [0, 2]]
            )

            # if i == 0:
            #     self.play(
            #         FadeIn(highlight_boxes),
            #         run_time=0.5
            #     )
            # self.play(
            #     FadeIn(highlight_boxes),
            #     run_time=0.5
            # )
            x_min = 0
            y_min = 0
            if i > 0:
                x_min = tabel_data_raw[i-1][0]
                y_min = tabel_data_raw[i-1][2]
                self.play(
                    ReplacementTransform(old_boxes, highlight_boxes),
                    run_time=0.5
                )
            else:
                self.play(
                    FadeIn(highlight_boxes),
                    run_time=0.5
                )
            line_h = Line(
                start=plane.c2p(x_min, y_min), end=plane.c2p(obs, y_min), color=BLUE
            )
            line_v = Line(
                start=plane.c2p(obs, y_min), end=plane.c2p(obs, kumhyp), color=BLUE
            )
            graph.add(line_h, line_v)

            self.play(
                LaggedStart(
                    Create(line_h),
                    Create(line_v),
                    lag_ratio=1
                )
            )
            if obs == tabel_data_raw[-1][0]:
                line_h = Line(
                    start=plane.c2p(obs, kumhyp), end=plane.c2p(20, kumhyp), color=BLUE
                )
                self.play(
                    Create(line_h)
                )
            self.slide_pause()
            old_boxes = highlight_boxes

            i += 1
        self.play(
            FadeOut(highlight_boxes)
        )
        self.slide_pause()


class BoksplotOgKvartiler(PrikOgPindediagrammer):
    def construct(self):
        # title = Tex("Ugrupperet", " data")
        title = Tex("Boksplot", " fra rå data")
        title[0].set_color(YELLOW)
        play_title2(self, title)
        # self.slide_pause(0.5)
        self.kvartiler()
        self.slide_pause(5)

    # def data_to_DecNum(self, data):
    #     return VGroup(
    #         *[DecimalNumber(
    #                 val,
    #                 include_sign=False,
    #                 num_decimal_places=0,
    #             ).scale(0.5) for val in data]
    #     ).arrange(DOWN, aligned_edge=RIGHT, buff=0.1)

    def tegn_boksplot(self, kvartiler, kvartiltekst, box_colour=YELLOW, fade_out_text=True):
        q0, q1, q2, q3, q4 = kvartiler
        plane = NumberLine(
            x_range=(kvartiler[0]-2, kvartiler[-1]+2, 1),
            length=12,
            include_tip=True,
            include_numbers=True
        ).shift(2*DOWN)
        self.play(
            DrawBorderThenFill(plane)
        )
        self.slide_pause(0.5)
        full_plot = VGroup(plane)
        for q, t in zip([q0, q4], [kvartiltekst[1], kvartiltekst[9]]):
            line = Line(start=plane.n2p(q) + 0.5*UP, end=plane.n2p(q) + 1*UP)
            hnum = t.copy().scale(0.75).move_to(plane.n2p(q)+2*UP)
            self.play(
                DrawBorderThenFill(
                    line
                ),
                Circumscribe(t),
                DrawBorderThenFill(hnum),
                run_time=2
            )
            full_plot += line
            self.slide_pause(0.5)
        for q, t in zip([q2, q1, q3], [kvartiltekst[5], kvartiltekst[3], kvartiltekst[7]]):
            line = Line(start=plane.n2p(q), end=plane.n2p(q) + 1.5*UP)
            hnum = t.copy().scale(0.75).move_to(plane.n2p(q)+2*UP)
            self.play(
                DrawBorderThenFill(
                    line
                ),
                Circumscribe(t),
                DrawBorderThenFill(hnum),
                run_time=2
            )
            full_plot += line
            self.slide_pause(0.5)

        box = Rectangle(
            height=1.5,
            width=plane.n2p(q3)[0] - plane.n2p(q1)[0],
            fill_color=box_colour,
            fill_opacity=1,
            z_index=-1,
            stroke_width=0.1
        ).move_to(0.5*(plane.n2p(q3)+plane.n2p(q1))+0.75*UP)
        full_plot += box
        lines = VGroup(
            *[
                Line(
                    start=plane.n2p(ql) + 0.75 * UP,
                    end=plane.n2p(qh) + 0.75 * UP
                ) for ql, qh in zip([q0, q3], [q1, q4])
            ],
            Line(
                start=plane.n2p(q1) + 1.5 * UP,
                end=plane.n2p(q3) + 1.5 * UP
            )
        )
        full_plot += lines
        self.play(
            LaggedStart(
                DrawBorderThenFill(lines),
                lag_ratio=0.1
            ),
            FadeIn(box),
            run_time=2
        )
        self.slide_pause(0.5)
        self.add(full_plot)
        if fade_out_text:
            self.play(
                *[FadeOut(m) for m in self.mobjects if m != full_plot]
            )
        return full_plot

    def kvartiler(self):
        data_raw = [8, 4, 16, 8, 9, 6, 16, 19, 7, 6, 4, 8, 11, 8, 9, 6, 9, 10, 11, 8, 14, 4, 6, 7, 10]
        data = self.data_to_DecNum(data_raw).to_edge(LEFT)
        self.play(
            LaggedStart(
                *[DrawBorderThenFill(d) for d in data],
                lag_ratio=0.1
            ),
            run_time=2
        )
        # self.slide_pause(0.5)

        steps = VGroup(
            Tex("Trin 1: Sortér data"),
            Tex("Trin 2: Find midterste tal"),
            Tex("Trin 3: Find midterste tal i nederste halvdel"),
            Tex("Trin 4: Find midterste tal i øverste halvdel"),
            Tex("Trin 5: Find mindste værdi"),
            Tex("Trin 5: Find største værdi")
        ).scale(0.5).arrange(DOWN, aligned_edge=LEFT).to_edge(UR, buff=1.5)
        self.play(
            Write(steps[0]),
            run_time=2
        )
        self.slide_pause(0.5)

        # data_ordered = self.data_to_DecNum(sorted(data_raw)).next_to(data, RIGHT, buff=2)
        data_ordered, sorting_dict = self.one_to_one_sort(data, desc=False)
        # self.play(
        #     TransformFromCopy(
        #         data,
        #         data_ordered
        #     )
        # )
        self.play(
            LaggedStart(
                *[TransformFromCopy(k, v) for k, v in sorting_dict.items()],
                lag_ratio=0.1
            ),
            run_time=2
        )
        self.slide_pause(0.5)

        self.play(
            Write(steps[1]),
            steps[0].animate.set_opacity(0.25),
            run_time=2
        )
        self.slide_pause(0.5)

        q0_mob = data_ordered[0].copy()
        med_arr, med_mob, med_val = self.animer_kvartil(
            data_ordered, indices=(0, len(data) - 1), colors=(GREEN_A, BLUE_E)
        )
        self.slide_pause(0.5)
        self.play(
            Write(steps[2]),
            steps[1].animate.set_opacity(0.25),
            run_time=2
        )
        self.slide_pause(0.5)

        q1_arr, q1_mob, q1_val = self.animer_kvartil(
            data_ordered, indices=(0, len(data) // 2 - 1), colors=(GREEN_A, GREEN_E)
        )
        self.slide_pause(0.5)
        self.play(
            Write(steps[3]),
            steps[2].animate.set_opacity(0.25),
            run_time=2
        )
        self.slide_pause(0.5)

        q3_arr, q3_mob, q3_val = self.animer_kvartil(
            data_ordered, indices=(len(data) // 2 + 1, len(data) - 1), colors=(BLUE_A, BLUE_E)
        )
        self.slide_pause(0.5)
        self.play(
            Write(steps[4]),
            steps[3].animate.set_opacity(0.25),
            run_time=2
        )
        self.slide_pause(0.5)

        q0_arr, q0_mob, q0_val = self.animer_kvartil(
            data_ordered, indices=(0, 0), colors=(GREEN_A, GREEN_A)
        )
        self.slide_pause(0.5)
        self.play(
            Write(steps[5]),
            steps[4].animate.set_opacity(0.25),
            run_time=2
        )
        self.slide_pause(0.5)

        q4_mob = data_ordered[-1].copy()
        q4_arr, q4_mob, q4_val = self.animer_kvartil(
            data_ordered, indices=(-1, -1), colors=(BLUE_E, BLUE_E)
        )
        self.slide_pause(0.5)

        kvartiler = VGroup(q1_mob, med_mob, q3_mob)
        kvartil_tekst = Tex(
            "Kvartilsættet er derfor"
        )
        kvartilsaet = MathTex(
            r"\{", q1_val, r";\quad", med_val, r";\quad", q3_val, r"\}"
        ).next_to(kvartil_tekst, DOWN)
        # for i, col in enumerate([q1_mob.get_color(), med_mob.get_color(), q3_mob.get_color()]):
        #     kvartilsaet[2*i + 1].set_color(col)
        for i in [1, 3, 5]:
            kvartilsaet[i].set_color(YELLOW)
        self.play(
            *[m.animate.set_opacity(0.25) for m in self.mobjects],  # if m not in [median, q1, q3]],
            # *[m.animate.set_opacity(1) for m in [median, q1]],
            TransformFromCopy(kvartiler, kvartilsaet),
            Write(kvartil_tekst),
            run_time=2
        )
        self.slide_pause(0.5)

        kvartilu_tekst = Tex(
            "Det udvidede kvartilsæt er"
        )
        kvartilsaetu = MathTex(
            r"\{", q0_mob.get_value(), r";\quad", q1_val, r";\quad", med_val, r";\quad",
            q3_val, r";\quad", q4_mob.get_value(), r"\}"
        ).next_to(kvartil_tekst, DOWN)
        for i in [1, 3, 5, 7, 9]:
            kvartilsaetu[i].set_color(YELLOW)
        self.play(
            # ReplacementTransform(
            TransformMatchingTex(
                kvartil_tekst,
                kvartilu_tekst
            ),
            # ReplacementTransform(
            TransformMatchingTex(
                kvartilsaet,
                kvartilsaetu
            ),
            run_time=2
        )
        self.slide_pause(0.5)

        # label_arrows = VGroup(*[
        #     Arrow(
        #         start=0.5*DOWN, end=0.5*UP
        #     ).scale(i % 2 + 1).next_to(q, DOWN) for i, q in enumerate(
        #         [kvartilsaetu[1], kvartilsaetu[3], kvartilsaetu[5], kvartilsaetu[7], kvartilsaetu[9]]
        #     )
        # ])
        # labels = VGroup(*[
        #     Tex(t).next_to(ar, DOWN) for t, ar in zip(
        #         ["Minimum", "1. kvartil", "Median", "3. kvartil", "Maksimum"], label_arrows
        #     )
        # ])
        # labels = VGroup(
        #     VGroup(*[Tex(t) for t in ["Minimum", "Median", "Maksimum"]]).arrange(RIGHT, buff=1),
        #     VGroup(*[Tex(t) for t in ["1. kvartil", "3. kvartil"]]).arrange(RIGHT, buff=1)
        # ).arrange(DOWN).next_to(kvartilsaetu, DOWN)
        # srecs = VGroup()
        # for lg in labels:
        #     for label in lg:
        #         srecs.add(get_background_rect(label, buff=0.1, fill_opacity=1, fill_color=BLACK))
        # label_arrows = VGroup(
        #     *[
        #         Arrow(start=label.get_center(), end=q.get_center()) for label, q in zip(
        #             labels[0],
        #             [kvartilsaetu[1], kvartilsaetu[5], kvartilsaetu[9]]
        #         )
        #     ],
        #     *[
        #         Arrow(label.get_center(), end=q.get_center()) for label, q in zip(
        #             labels[1],
        #             [kvartilsaetu[3], kvartilsaetu[7]]
        #         )
        #     ]
        # )
        # self.add(label_arrows, labels, srecs)

        self.play(
            kvartilu_tekst.animate.to_edge(UL),
            kvartilsaetu.animate.to_edge(UP).shift(3*RIGHT),
            *[FadeOut(m) for m in self.mobjects if m not in [kvartilsaetu, kvartilu_tekst]],
            run_time=2
        )
        self.slide_pause(0.5)

        box_kvartiler = [q0_mob.get_value(), q1_val, med_val, q3_val, q4_mob.get_value()]
        boksplot = self.tegn_boksplot(box_kvartiler, kvartilsaetu, box_colour=YELLOW_D)


class OutliersOgBredder(BoksplotOgKvartiler):
    def construct(self):
        title = Tex("Kvartilbredde", " og ", "variationsbredde")
        cmap = self.get_cmap()
        title[0].set_color(cmap["kb"])
        title[2].set_color(cmap["vb"])
        play_title2(self, title)
        self.bredder_og_outliers()
        self.slide_pause(5)

    def get_cmap(self):
        return {"kb": GREEN, "vb": ORANGE, "outlier": RED, "obs": BLUE}

    def bredder_og_outliers(self):
        udvidet_kvartil = (4, 6, 8, 10.5, 19)
        cmap = self.get_cmap()
        q0 = DecimalNumber(udvidet_kvartil[0], num_decimal_places=0).set_color(YELLOW)
        q1 = DecimalNumber(udvidet_kvartil[1], num_decimal_places=0).set_color(YELLOW)
        q2 = DecimalNumber(udvidet_kvartil[2], num_decimal_places=0).set_color(YELLOW)
        q3 = DecimalNumber(udvidet_kvartil[3], num_decimal_places=1).set_color(YELLOW)
        q4 = DecimalNumber(udvidet_kvartil[4], num_decimal_places=0).set_color(YELLOW)
        udv_kvart_text = Tex("Det udvidede kvartilsæt er").to_edge(UL)
        udv_kvart_mobs = MathTex(
            r"\{", q0.get_value(), r";\quad", q1.get_value(), r";\quad", q2.get_value(),
            r";\quad", q3.get_value(), r";\quad", q4.get_value(), r"\}"
        ).to_edge(UR)
        for i in [1, 3, 5, 7, 9]:
            udv_kvart_mobs[i].set_color(YELLOW)
        self.play(
            FadeIn(udv_kvart_mobs),
            FadeIn(udv_kvart_text),
            run_time=0.5
        )
        self.slide_pause()

        boksplot = self.tegn_boksplot(udvidet_kvartil, udv_kvart_mobs, box_colour=YELLOW_D, fade_out_text=True)
        self.play(
            boksplot.animate.to_edge(DOWN)
        )

        kvartilbredde_brace = Brace(boksplot[3:6], direction=UP, color=cmap["kb"], buff=1)
        kvartilbredde_tekst = Tex("Kvartilbredde", font_size=32, color=cmap["kb"]).next_to(kvartilbredde_brace, UP)
        self.play(
            GrowFromCenter(kvartilbredde_brace),
            Write(kvartilbredde_tekst)
        )
        self.slide_pause()

        kvartilbredde_udr = MathTex(
            "kb", " = ", q3.get_value(), " - ", q1.get_value(), " = ", f"{udvidet_kvartil[3] - udvidet_kvartil[1]:.1f}"
        ).next_to(kvartilbredde_tekst, UP)
        for i in [2, 4]:
            kvartilbredde_udr[i].set_color(YELLOW)
        for i in [0, 6]:
            kvartilbredde_udr[i].set_color(cmap["kb"])
        self.play(
            Write(kvartilbredde_udr)
        )
        self.slide_pause()

        self.play(
            FadeOut(kvartilbredde_udr[2:6]),
            VGroup(kvartilbredde_udr[:2], kvartilbredde_udr[-1]).animate.arrange(RIGHT).next_to(kvartilbredde_tekst, UP)
        )
        self.slide_pause()

        kvartilbredde = VGroup(
            kvartilbredde_udr[:2], kvartilbredde_udr[-1]
        ).arrange(RIGHT).next_to(kvartilbredde_tekst, UP)
        self.remove(kvartilbredde_udr)
        self.add(kvartilbredde)
        self.play(
            kvartilbredde.animate.next_to(udv_kvart_text, DOWN, aligned_edge=LEFT),
            FadeOut(kvartilbredde_tekst),
            FadeOut(kvartilbredde_brace)
        )
        self.slide_pause()

        variationsbredde_brace = Brace(boksplot[1:3], direction=UP, color=cmap["vb"], buff=1.25)
        variationsbredde_tekst = Tex("Variationsbredde", font_size=32, color=cmap["vb"]).next_to(variationsbredde_brace, UP)
        self.play(
            GrowFromCenter(variationsbredde_brace),
            Write(variationsbredde_tekst)
        )
        self.slide_pause()

        variationsbredde_udr = MathTex(
            "vb", " = ", q4.get_value(), " - ", q0.get_value(), " = ", f"{udvidet_kvartil[4] - udvidet_kvartil[0]:.0f}"
        ).next_to(variationsbredde_tekst, UP)
        for i in [2, 4]:
            variationsbredde_udr[i].set_color(YELLOW)
        for i in [0, 6]:
            variationsbredde_udr[i].set_color(cmap["vb"])
        self.play(
            Write(variationsbredde_udr)
        )
        self.slide_pause()

        self.play(
            FadeOut(variationsbredde_udr[2:6]),
            VGroup(
                variationsbredde_udr[:2], variationsbredde_udr[-1]
            ).animate.arrange(RIGHT).next_to(variationsbredde_tekst, UP)
        )
        self.slide_pause()

        variationsbredde = VGroup(
            variationsbredde_udr[:2], variationsbredde_udr[-1]
        ).arrange(RIGHT).next_to(variationsbredde_tekst, UP)
        self.remove(variationsbredde_udr)
        self.add(variationsbredde)
        self.play(
            variationsbredde.animate.next_to(kvartilbredde, DOWN, aligned_edge=LEFT),
            FadeOut(variationsbredde_tekst),
            FadeOut(variationsbredde_brace)
        )
        self.slide_pause()

        outlier_forklaring = VGroup(
            Tex("En ", "outlier", " er en ", "observation", ","),
            Tex("som er 1.5 ", "kvartilbredder", " under ", "1. kvartil", ","),
            Tex("eller 1.5 ", "kvartilbredder", " over ", "3. kvartil", ".")
        ).arrange(DOWN, aligned_edge=LEFT).set_z_index(5)
        outlier_forklaring[0][1].set_color(cmap["outlier"])
        outlier_forklaring[0][3].set_color(cmap["obs"])
        outlier_forklaring[1][1].set_color(cmap["kb"])
        outlier_forklaring[1][3].set_color(YELLOW)
        outlier_forklaring[2][1].set_color(cmap["kb"])
        outlier_forklaring[2][3].set_color(YELLOW)
        outlier_box = get_background_rect(
            outlier_forklaring, buff=1, stroke_colour=RED, stroke_width=2, fill_opacity=1.95
        )
        self.play(
            LaggedStart(
                FadeIn(outlier_box, run_time=0.5),
                Write(outlier_forklaring),
                lag_ratio=0.5
            )
        )
        self.slide_pause()

        _outlier_border = 1.5*(udvidet_kvartil[3] - udvidet_kvartil[1])
        outlier_border = VGroup(
            MathTex(r"1.5 \cdot "), kvartilbredde[-1].copy(), Tex(" = "),
            DecimalNumber(_outlier_border, num_decimal_places=2, color=cmap["outlier"])
        ).arrange(RIGHT).next_to(kvartilbredde, RIGHT, buff=1)
        self.play(
            Write(outlier_border),
            FadeOut(outlier_box, run_time=0.5),
            Unwrite(outlier_forklaring, run_time=0.5)
        )
        self.slide_pause()

        print(*boksplot)

        outlier_line_high = DashedLine(
            start=boksplot[0].n2p(q3.get_value()),
            end=boksplot[0].n2p(q3.get_value()) + 3*UP,
            stroke_color=cmap["outlier"],
            stroke_width=6
        )
        outlier_line_dist = always_redraw(lambda:
            DashedLine(
                start=boksplot[0].n2p(q3.get_value()) + 1.5*UP,
                end=outlier_line_high.get_center(),
                stroke_color=cmap["outlier"],
                stroke_width=3
            )
        )
        outlier_line_tracker = always_redraw(lambda:
            DecimalNumber(
                # number=boksplot[0].n2p(outlier_line_dist.get_end()[0])[0] - boksplot[0].n2p(outlier_line_dist.get_start()[0])[0],
                number=boksplot[0].p2n(outlier_line_dist.get_end()) - boksplot[0].p2n(outlier_line_dist.get_start()),
                num_decimal_places=2,
                color=cmap["outlier"]
            ).scale(0.75).next_to(outlier_line_dist, UP)
        )
        outlier_line_place = always_redraw(lambda:
            DecimalNumber(
                number=boksplot[0].p2n(outlier_line_high.get_start()),
                num_decimal_places=2,
                color=cmap["outlier"]
            ).next_to(outlier_line_high, UP)
        )
        self.play(
            Create(outlier_line_high),
            Create(outlier_line_dist),
            Write(outlier_line_tracker),
            Write(outlier_line_place),
            run_time=0.5
        )
        self.slide_pause()

        self.play(
            outlier_line_high.animate.shift(
                (boksplot[0].n2p(q3.get_value() + _outlier_border)[0] - boksplot[0].n2p(q3.get_value())[0]) * RIGHT
            ),
            run_time=_outlier_border/2
        )
        self.slide_pause()

        outliers = Tex("Alle {{observationer}} over {{17.25}} er {{outliers}}.").set_z_index(5)
        outliers[1].set_color(cmap["obs"])
        outliers[3].set_color(cmap["outlier"])
        outliers[5].set_color(cmap["outlier"])
        outliers_box = get_background_rect(
            outliers, buff=1, stroke_colour=RED, stroke_width=2, fill_opacity=1.95
        )
        self.play(
            LaggedStart(
                FadeIn(outliers_box),
                Write(outliers),
                lag_ratio=0.5
            )
        )
        self.slide_pause()


class SampleSize(Slide if slides else Scene):
    def construct(self):
        np.random.seed(42)
        self.slide_pause(0.1)
        pop_size = 3
        sam_size = ValueTracker(0.0)
        # responds = Dot(radius=0.04, color=YELLOW)
        num_res = 500

        scene_marker("Genererer locations")
        locs = [[0.1, 0, 0]]
        for i in range(num_res - 1):
            x, y = 10, 10
            while x**2 + y**2 >= pop_size**2:
                x, y = np.random.uniform(-pop_size, pop_size, 2)
            locs.append([x, y, 0])
        scene_marker(f"{len(locs)} locations genereret")

        population = Circle(radius=pop_size, color=GREEN)
        xt, yt = ValueTracker(0), ValueTracker(0)
        sample = always_redraw(lambda:
            Circle(radius=sam_size.get_value(), color=BLUE).move_to([xt.get_value(), yt.get_value(), 0])
        )
        # respondents = VGroup(*[
        #     responds.copy().move_to(loc) for loc in locs
        # ])
        respondents = always_redraw(lambda: VGroup(*[
            Dot(
                radius=0.04,
                # color=YELLOW if l[0]**2+l[1]**2 >= sam_size.get_value()**2 else BLUE
                color=YELLOW if (l[0]-xt.get_value())**2 + (l[1]-yt.get_value())** 2 >= sam_size.get_value()**2 else BLUE
            ).move_to(l) for l in locs
        ]))
        scene_marker("Respondenter genereret")

        # num_sam = always_redraw(lambda: DecimalNumber(
        #     len([l for l in locs if l[0] ** 2 + l[1] ** 2 < sam_size.get_value() ** 2])
        # ))
        disp_res = VGroup(Tex("Population: "), MathTex(f"{num_res}", color=GREEN)).arrange(RIGHT).to_edge(UL)
        disp_sam = always_redraw(lambda: VGroup(
            Tex("Respondenter: "),
            # MathTex(f"{len([l for l in locs if l[0] ** 2 + l[1] ** 2 < sam_size.get_value() ** 2])}", color=BLUE)
            # MathTex(f"{len([self.is_in_circle(l, sample) for l in locs])}", color=BLUE)
            # MathTex(
            #     f"{len([l for l in locs if (l[0]-xt.get_value())**2 + (l[1]-yt.get_value())** 2 < sam_size.get_value()**2])}",
            #     color=BLUE
            # )
            DecimalNumber(
                len(
                    [l for l in locs if (l[0] - xt.get_value()) ** 2 + (l[1] - yt.get_value()) ** 2 < sam_size.get_value() ** 2]
                ),
                num_decimal_places=0,
                color=BLUE
            )
        ).arrange(RIGHT).next_to(disp_res, DOWN, aligned_edge=LEFT))
        disp_pct = always_redraw(lambda: VGroup(
            Tex("Pct.:"),
            # MathTex(f"{len([l for l in locs if l[0] ** 2 + l[1] ** 2 < sam_size.get_value() ** 2])/num_res*100:.2f} \%", color=BLUE)
            # MathTex(f"{len([self.is_in_circle(l, sample) for l in locs])/num_res*100:.2f} \%", color=BLUE)
            # MathTex(
            #     rf"{len([l for l in locs if (l[0]-xt.get_value())**2 + (l[1]-yt.get_value())** 2 < sam_size.get_value() ** 2])/num_res*100:.2f} \%",
            #     color=BLUE
            # )
            DecimalNumber(
                len(
                    [l for l in locs if (l[0] - xt.get_value()) ** 2 + (l[1] - yt.get_value()) ** 2 < sam_size.get_value() ** 2]
                ) / num_res * 100,
                num_decimal_places=2,
                color=BLUE,
                unit=r"\%"
            )
        ).arrange(RIGHT).next_to(disp_sam, DOWN, aligned_edge=LEFT))

        self.play(
            Create(respondents),
            run_time=2
        )
        self.slide_pause(0.5)
        self.play(
            DrawBorderThenFill(population),
            run_time=0.5
        )
        self.slide_pause(0.5)
        self.play(
            DrawBorderThenFill(sample),
            run_time=0.5
        )
        self.play(
            Write(disp_res),
            Write(disp_sam),
            Write(disp_pct),
            run_time=0.5
        )
        self.slide_pause()

        for d in [4, 2, 1.1, 1]:
            self.play(
                sam_size.animate.set_value(pop_size/d),
                run_time=5
            )
            self.slide_pause()
            if d == 4:
                for x, y in np.append(np.random.uniform(low=-2, high=2, size=(4, 2)), [[0, 0]], axis=0):
                    self.play(
                        xt.animate.set_value(x),
                        yt.animate.set_value(y),
                        run_time=3
                    )
                self.slide_pause()

        self.slide_pause(5)

    def slide_pause(self, t=1.0, slides_bool=slides):
        return slides_pause(self, t, slides)

    def is_in_circle(self, point, circle):
        print((point[0]-circle.get_center()[0])**2, circle.radius**2)
        if (point[0]-circle.get_center()[0])**2 + (point[1]-circle.get_center()[1])**2 < circle.get_radius()**2:
            return point


class PrikVsPind(OutliersOgBredder):
    def construct(self):
        np.random.seed(42)
        self.wait(1)
        lille_data = self.lille_dataset()
        stor_data = self.stort_dataset()
        self.wait(5)

    def lille_dataset(self):
        data = [np.random.randint(1, 11) for _ in range(30)]
        prikline = NumberLine(
            x_range=(0, 11, 1),
            include_numbers=True
        ).scale(0.5).to_edge(DL).shift(2*UP)
        pindline = Axes(
            x_range=(0, 11, 1),
            y_range=(0, 10, 1),
            axis_config={"include_numbers": True}
        ).scale(0.5).to_edge(DR).shift(2*UP)
        axhlines = VGroup(*[
            DashedLine(
                start=pindline.c2p(0, y), end=pindline.c2p(11, y), stroke_width=0.5
            ) for y in pindline[1].get_tick_range()
        ])
        # self.add(prikline, pindline, axhlines)
        self.play(
            LaggedStart(
                DrawBorderThenFill(prikline),
                DrawBorderThenFill(pindline),
                Create(axhlines),
                lag_ratio=0.5
            ),
            run_time=2
        )
        self.slide_pause()

        unikke_tal = np.unique(data)
        _r = 0.15
        dataprikke = VGroup(*[
            VGroup(
                *[
                    Dot(radius=_r, fill_color=RED, stroke_width=0) for x in data if x == num
                ]
            ).arrange(UP, buff=0).move_to(prikline.n2p(num)) for num in unikke_tal
        ])
        [stabel.shift(0.5*stabel.get_height()*UP) for stabel in dataprikke]
        # self.add(dataprikke)
        self.play(
            FadeIn(dataprikke, lag_ratio=0.1),
            run_time=1
        )
        self.slide_pause()

        datapinde = VGroup(*[
            Rectangle(
                width=_r, fill_color=BLUE, stroke_width=0, fill_opacity=1,
                height=pindline.c2p(num, len([n for n in data if n == num]))[1]-pindline.c2p(num, 0)[1]
            ) for num in unikke_tal
        ])
        [pind.move_to(pindline.c2p(n, 0)).shift(0.5*pind.get_height()*UP) for n, pind in zip(unikke_tal, datapinde)]
        # self.add(datapinde)
        self.play(
            FadeIn(datapinde, lag_ratio=0.1),
            run_time=1
        )
        self.slide_pause()
        lille_data = VGroup(
            VGroup(prikline, dataprikke),
            VGroup(pindline, axhlines, datapinde)
        )
        # self.remove(pindline, prikline, dataprikke, axhlines, datapinde)
        self.play(
            *[FadeOut(m) for m in [pindline, prikline, dataprikke, axhlines, datapinde]]
        )
        self.slide_pause()
        return lille_data

    def stort_dataset(self):
        data = [np.random.randint(1, 11) for _ in range(500)]
        prikline = NumberLine(
            x_range=(0, 11, 1),
            include_numbers=True
        ).scale(0.5).to_edge(DL)
        pindline = Axes(
            x_range=(0, 11, 1),
            y_range=(0, 70, 10),
            y_length=10,
            axis_config={"include_numbers": True}
        ).scale(0.5).to_edge(DR)
        axhlines = VGroup(*[
            DashedLine(
                start=pindline.c2p(0, y), end=pindline.c2p(11, y), stroke_width=0.5
            ) for y in pindline[1].get_tick_range()
        ])
        # self.add(prikline, pindline, axhlines)
        self.play(
            # LaggedStart(
            #     DrawBorderThenFill(prikline),
            #     DrawBorderThenFill(pindline),
            #     Create(axhlines),
            #     lag_ratio=0.5
            # ),
            # run_time=2
            *[FadeIn(m) for m in [pindline, prikline, axhlines]]
        )
        self.slide_pause()

        unikke_tal = np.unique(data)
        _r = 0.025
        dataprikke = VGroup(*[
            VGroup(
                *[
                    Dot(radius=_r, fill_color=RED, stroke_width=0) for x in data if x == num
                ]
            ).arrange(UP, buff=0).move_to(prikline.n2p(num)) for num in unikke_tal
        ])
        [stabel.shift(0.5*stabel.get_height()*UP) for stabel in dataprikke]
        # self.add(dataprikke)
        self.play(
            FadeIn(dataprikke, lag_ratio=0.1),
            run_time=1
        )
        self.slide_pause()

        datapinde = VGroup(*[
            Rectangle(
                width=0.15, fill_color=BLUE, stroke_width=0, fill_opacity=1,
                height=pindline.c2p(num, len([n for n in data if n == num]))[1]-pindline.c2p(num, 0)[1]
            ) for num in unikke_tal
        ])
        [pind.move_to(pindline.c2p(n, 0)).shift(0.5*pind.get_height()*UP) for n, pind in zip(unikke_tal, datapinde)]
        # self.add(datapinde)
        self.play(
            FadeIn(datapinde, lag_ratio=0.1),
            run_time=1
        )
        self.slide_pause()

        stor_data = VGroup(
            VGroup(prikline, dataprikke),
            VGroup(pindline, axhlines, datapinde),
        )
        self.remove(prikline, pindline, dataprikke, datapinde, axhlines)
        return stor_data


if __name__ == "__main__":
    classes = [
        HyppighedsTabel,
        Deskriptorer,
        PrikOgPindediagrammer,
        SumkurveFraTabel,
        BoksplotOgKvartiler,
        OutliersOgBredder,
        SampleSize,
        TrappediagramFraTabel,
        PrikVsPind
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
            if class_name+"Thumbnail" in dir():
                command = rf"manim {sys.argv[0]} {class_name}Thumbnail -pq{q} -o {class_name}Thumbnail.png"
                scene_marker(rf"RUNNNING:    {command}")
                subprocess.run(command)
